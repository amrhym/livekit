# LiveKit Agent Manager

This project provides a minimal FastAPI backend for creating and managing **LiveKit** agents.

## Features

* Create, list, update, and delete agents through RESTful APIs.
* Generates an `agent.py` file and corresponding `.env` for every new agent.
* Boilerplate agent script uses **python-dotenv** so your LiveKit credentials stay in environment files.
* Conda `environment.yml` included for reproducible environments.

## Requirements

* [Conda](https://docs.conda.io/) (or **Miniconda** / **Mamba**)

## Setup

```bash
# 1. Create the environment
conda env create -f environment.yml

# 2. Activate it
conda activate livekit_agent_env

# 3. Run the API server
uvicorn app.main:app --reload
```

Once running, open [http://localhost:8000/docs](http://localhost:8000/docs) to explore the interactive Swagger UI.

## API Endpoints

| Method | URL                 | Description                  |
|--------|---------------------|------------------------------|
| POST   | `/agents`           | Create a new agent           |
| GET    | `/agents`           | List all agents              |
| GET    | `/agents/{agent_id}` | Retrieve a specific agent    |
| PUT    | `/agents/{agent_id}` | Update an existing agent     |
| DELETE | `/agents/{agent_id}` | Delete an agent and its files|

### Example: Create an Agent

```jsonc
POST /agents
{
  "name": "my_audio_bot",
  "imports": ["livekit", "numpy"],
  "env_vars": {
    "LIVEKIT_URL": "wss://my-livekit-server",
    "LIVEKIT_API_KEY": "xxx",
    "LIVEKIT_API_SECRET": "yyy"
  }
}
```

The response contains the newly generated `id`. An `agents/<id>/` folder with `agent.py` and `.env` will also be created on disk.

---
Feel free to extend the project—for example by adding persistent storage (SQLModel, PostgreSQL, etc.) or by integrating directly with LiveKit's SDK. 