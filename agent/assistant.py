import asyncio
import os
from dotenv import load_dotenv

from google.antigravity import Agent, LocalAgentConfig

import agent.prompts 
import config.create_local_agent_config

load_dotenv()

async def create_agent():
    """
    Create a new agent instance.

    Returns:
        Agent: A new instance of the Agent class.
    """

    async with Agent(config) as agent:
        return agent