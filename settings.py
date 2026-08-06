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


def get_erpnext_url():
    """
    Retrieve the ERPNext base URL from environment variables.

    Returns:
        str: The ERPNext base URL.
    """
    return os.getenv("ERPNEXT_URL")


def get_erpnext_api_key():
    """
    Retrieve the ERPNext API key from environment variables.

    Returns:
        str: The ERPNext API key.
    """
    return os.getenv("ERPNEXT_API_KEY")


def get_erpnext_api_secret():
    """
    Retrieve the ERPNext API secret from environment variables.

    Returns:
        str: The ERPNext API secret.
    """
    return os.getenv("ERPNEXT_API_SECRET")


def get_erpnext_company_name():
    """
    Retrieve the name of the ERPNext Company document to use.

    Optional: if unset, the ERPNext repository falls back to the first
    company visible to the configured API user.

    Returns:
        str | None: The ERPNext Company name.
    """
    return os.getenv("ERPNEXT_COMPANY")