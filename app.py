import asyncio
import os

#from dotenv import load_dotenv
#from google.antigravity import Agent, LocalAgentConfig

import config
from tools.company import get_company_information
from tools.customer import get_customer
from agent.assistant import create_agent
import config

#load_dotenv()

"""
questions = [
    "Tell me about our company,Include the company name, country, currency, fiscal year, and industry.",
    "Tell me about customer ABC Traders,Include the customer name, customer group, territory, and customer type.",
    "Tell me about customer XYZ Stores,Include the customer name, customer group, territory, and customer type."
]
"""

async def main():
#    config = LocalAgentConfig(
#        api_key=os.getenv("GEMINI_API_KEY"),
#        system_instructions="""
#You are an ERP assistant.
#Always use available tools whenever appropriate.
#""", 
#    tools=[
#        get_company_information, get_customer
#    ]
#    )
 
    local_config = create_local_agent_config()
    create_agent(local_config)

    print("=====================================================================================\n")
    print("Welcome to the ERP Assistant! You can ask questions about your company and customers.\n")
    print("Type 'exit' or 'quit' to end the session.\n")
    print("=====================================================================================\n")
        
    while True:

        question = input("Ask your question: ")
        if question.lower() in ["exit", "quit"]:
            break

        response = await agent.chat(question)
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
        