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


def get_log_level():
    """
    Retrieve the logging level from environment variables.

    Returns:
        str: The logging level name, defaulting to "INFO".
    """
    return os.getenv("LOG_LEVEL", "INFO")


def get_log_format():
    """
    Retrieve the logging output format from environment variables.

    Returns:
        str: "text" (default, human-readable, for local/interactive use)
        or "json" (structured, for aggregated/production use). See ADR-0011.
    """
    return os.getenv("LOG_FORMAT", "text")


def get_telemetry_enabled():
    """
    Whether OpenTelemetry tracing is enabled.

    Returns:
        bool: True if OTEL_ENABLED is set to a truthy value, defaulting to
        False. See ADR-0012.
    """
    return os.getenv("OTEL_ENABLED", "false").strip().lower() in ("1", "true", "yes", "on")