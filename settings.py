import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    """
    Retrieve the API key from environment variables.

    Returns:
        str: The API key.
    """
    return os.getenv("GEMINI_API_KEY")