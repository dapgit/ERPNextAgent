from contextlib import asynccontextmanager
from dotenv import load_dotenv

from google.antigravity import Agent, LocalAgentConfig

from config import create_local_agent_config

@asynccontextmanager
async def create_agent():
    """
    Async context manager that creates and yields a new agent instance.
    """
    local_config = create_local_agent_config()

    async with Agent(local_config) as agent:
        yield agent