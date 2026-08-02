import asyncio
import os

from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

from tools.company import get_company_information
from tools.customer import get_customer

load_dotenv()

async def main():
    config = LocalAgentConfig(
        api_key=os.getenv("GEMINI_API_KEY"),
        system_instructions="""
You are an ERP assistant.
Always use available tools whenever appropriate.
""", 
    tools=[
        get_company_information, get_customer
    ]
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            """
            Tell me about our company,
            Include the company name, country, currency, fiscal year, and industry.
        """
        )

        print(await response.text())

        response = await agent.chat(
                    """
                    Tell me about customer ABC Traders,
                    Include the customer name, customer group, territory, and customer type.
                """
                )
        
        print(await response.text())


if __name__ == "__main__":
    asyncio.run(main())
        