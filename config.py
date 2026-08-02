import os

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

from agent.prompts import SYSTEM_PROMPT
from tools.company import get_company_information
from tools.customer import get_customer


load_dotenv()

def create_local_agent_config():
    # Create a local agent configuration

    config = LocalAgentConfig(
        api_key = os.getenv("GEMINI_API_KEY"),
        system_instructions = SYSTEM_PROMPT[0], 
        tools=[ 
                get_company_information, get_customer
            ]
    )

    return config
    
