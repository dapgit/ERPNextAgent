from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

from agent.prompts import SYSTEM_PROMPT
from tools.company import get_company_information
from tools.customer import get_customer
from settings import get_api_key

def create_local_agent_config():
    # Create a local agent configuration

    config = LocalAgentConfig(
        api_key = get_api_key(),
        system_instructions = SYSTEM_PROMPT, 
        tools=[ 
                get_company_information, get_customer
            ]
    )

    return config
    
