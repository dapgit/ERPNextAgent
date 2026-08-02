import asyncio

#from dotenv import load_dotenv
#from google.antigravity import Agent, LocalAgentConfig

from agent.assistant import create_agent


#load_dotenv()

"""
questions = [
    "Tell me about our company,Include the company name, country, currency, fiscal year, and industry.",
    "Tell me about customer ABC Traders,Include the customer name, customer group, territory, and customer type.",
    "Tell me about customer XYZ Stores,Include the customer name, customer group, territory, and customer type."
]
"""

def print_banner():
    print("=====================================================================================\n")
    print("Welcome to the ERP Assistant! You can ask questions about your company and customers.\n")
    print("Type 'exit' or 'quit' to end the session.\n")
    print("=====================================================================================\n")

async def chat_loop(local_agent):
    while True:
        question = input("Ask your question: ").strip()
        if not question:
            continue
        if question.lower() in ["exit", "quit"]:
            break

        response = await local_agent.chat(question)
        print(await response.text())


async def main():
    print_banner()

    async with create_agent() as local_agent:
        await chat_loop(local_agent)

if __name__ == "__main__":
    asyncio.run(main())
        