import os
from dotenv import load_dotenv

load_dotenv()

def run():
    """Entry point for the LiveKit agent."""
    agent_name = os.getenv("AGENT_NAME", "default_agent")
    print(f"Running LiveKit agent: {agent_name}")
    # TODO: Implement interaction with LiveKit here


if __name__ == "__main__":
    run() 