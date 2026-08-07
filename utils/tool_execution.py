from typing import Callable

from utils.exceptions import (
    ERPNextAuthenticationError,
    ERPNextConnectionError,
    ERPNextError,
    ERPNextTimeoutError,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def execute_tool(operation: Callable[[], str]) -> str:
    """
    Run a Tool's ERPNext-backed logic, converting failures into a safe,
    user-facing message instead of letting exceptions (and the internal
    details they carry, e.g. ERPNext URLs) reach the agent.
    """
    try:
        return operation()
    except ValueError as exc:
        logger.warning("Tool call rejected invalid input: %s", exc)
        return str(exc)
    except ERPNextAuthenticationError as exc:
        logger.error("Tool call failed: authentication error: %s", exc)
        return "Unable to retrieve information. ERPNext authentication failed."
    except ERPNextTimeoutError as exc:
        logger.error("Tool call failed: timeout: %s", exc)
        return "ERPNext did not respond in time."
    except ERPNextConnectionError as exc:
        logger.error("Tool call failed: connection error: %s", exc)
        return "Unable to connect to ERPNext."
    except ERPNextError as exc:
        logger.error("Tool call failed: %s", exc)
        return "ERPNext returned an unexpected error."
    except Exception:
        logger.exception("Tool call failed with an unexpected error")
        return "An unexpected error occurred."
