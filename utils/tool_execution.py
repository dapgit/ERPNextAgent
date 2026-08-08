import time
from typing import Callable

from observability.telemetry import get_meter
from utils.exceptions import (
    ERPNextAuthenticationError,
    ERPNextConnectionError,
    ERPNextError,
    ERPNextTimeoutError,
)
from utils.logger import get_logger

logger = get_logger(__name__)

_meter = get_meter(__name__)
_tool_duration = _meter.create_histogram(
    "erpnextagent.tool.duration",
    unit="ms",
    description="Duration of a Tool-layer call, success or failure.",
)
_tool_errors = _meter.create_counter(
    "erpnextagent.tool.errors",
    description="Count of Tool-layer call failures, by error type.",
)


def _derive_tool_name(operation: Callable) -> str:
    """
    Recover the enclosing Tool function's name from the inner closure
    execute_tool() is actually called with (e.g. tools/customer.py's
    get_customer() passes its local _get_customer closure). Mirrors the
    module-qualification approach in observability.telemetry.traced()
    rather than requiring every tools/*.py call site to pass a name
    manually. See ADR-0014.
    """
    qualname = getattr(operation, "__qualname__", "unknown")
    return qualname.split(".<locals>.")[0]


def execute_tool(operation: Callable[[], str]) -> str:
    """
    Run a Tool's ERPNext-backed logic, converting failures into a safe,
    user-facing message instead of letting exceptions (and the internal
    details they carry, e.g. ERPNext URLs) reach the agent.
    """
    tool_name = _derive_tool_name(operation)
    start = time.perf_counter()
    outcome = "success"
    error_type = None

    try:
        return operation()
    except ValueError as exc:
        outcome, error_type = "error", "ValueError"
        logger.warning("Tool call rejected invalid input: %s", exc)
        return str(exc)
    except ERPNextAuthenticationError as exc:
        outcome, error_type = "error", "ERPNextAuthenticationError"
        logger.error("Tool call failed: authentication error: %s", exc)
        return "Unable to retrieve information. ERPNext authentication failed."
    except ERPNextTimeoutError as exc:
        outcome, error_type = "error", "ERPNextTimeoutError"
        logger.error("Tool call failed: timeout: %s", exc)
        return "ERPNext did not respond in time."
    except ERPNextConnectionError as exc:
        outcome, error_type = "error", "ERPNextConnectionError"
        logger.error("Tool call failed: connection error: %s", exc)
        return "Unable to connect to ERPNext."
    except ERPNextError as exc:
        outcome, error_type = "error", "ERPNextError"
        logger.error("Tool call failed: %s", exc)
        return "ERPNext returned an unexpected error."
    except Exception:
        outcome, error_type = "error", "Exception"
        logger.exception("Tool call failed with an unexpected error")
        return "An unexpected error occurred."
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        _tool_duration.record(duration_ms, {"tool": tool_name, "outcome": outcome})
        if error_type is not None:
            _tool_errors.add(1, {"tool": tool_name, "error_type": error_type})
