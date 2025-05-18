from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID, uuid4
from pathlib import Path
import os
import shutil

app = FastAPI(title="LiveKit Agent Manager")


class AgentCreate(BaseModel):
    """Schema used when creating or updating an agent."""

    name: str
    imports: List[str] = []
    env_vars: Dict[str, str] = {}


class Agent(AgentCreate):
    """Schema returned from the API."""

    id: UUID


# In-memory store for demo purposes. Replace with persistent DB in production.
agents: Dict[UUID, Agent] = {}

# Directory where individual agent folders will be created.
BASE_DIR = Path(__file__).resolve().parent.parent
AGENTS_DIR = BASE_DIR / "agents"
AGENTS_DIR.mkdir(exist_ok=True)


def _write_agent_files(agent: Agent):
    """Generate boilerplate agent.py and .env files for a newly created/updated agent."""

    agent_dir = AGENTS_DIR / str(agent.id)
    agent_dir.mkdir(exist_ok=True)

    # agent.py
    agent_py = agent_dir / "agent.py"
    if not agent_py.exists():
        agent_py.write_text(
            """
from dotenv import load_dotenv
import os

load_dotenv()

def run():
    print(f"Hello from {agent.name}!")
    # TODO: customize agent logic here.


if __name__ == "__main__":
    run()
""".lstrip()
        )

    # .env
    env_file = agent_dir / ".env"
    env_lines = [f"{k}={v}\n" for k, v in agent.env_vars.items()]
    if env_lines:
        env_file.write_text("".join(env_lines))

    # environment.yml with agent specific imports
    if agent.imports:
        env_yml = agent_dir / "environment.yml"
        env_yml.write_text(
            "\n".join(
                [
                    f"name: {agent.name}_env",
                    "channels:",
                    "  - defaults",
                    "  - conda-forge",
                    "dependencies:",
                    "  - python=3.11",
                    "  - pip",
                    "  - pip:",
                ]
                + [f"      - {pkg}" for pkg in agent.imports]
            )
            + "\n"
        )


@app.post("/agents", response_model=Agent, status_code=201)
async def create_agent(agent_in: AgentCreate):
    """Create a new LiveKit agent."""

    agent_id = uuid4()
    agent = Agent(id=agent_id, **agent_in.dict())
    agents[agent_id] = agent
    _write_agent_files(agent)
    return agent


@app.get("/agents", response_model=List[Agent])
async def list_agents():
    """List all registered agents."""

    return list(agents.values())


@app.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: UUID):
    """Fetch a single agent by ID."""

    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@app.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(agent_id: UUID, agent_in: AgentCreate):
    """Update an existing agent."""

    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    updated_agent = Agent(id=agent_id, **agent_in.dict())
    agents[agent_id] = updated_agent
    _write_agent_files(updated_agent)
    return updated_agent


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: UUID):
    """Delete an agent and its files from disk."""

    agent = agents.pop(agent_id, None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_dir = AGENTS_DIR / str(agent_id)
    if agent_dir.exists():
        shutil.rmtree(agent_dir)
    return {"detail": "Agent deleted"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 
