import logging

from observability.correlation import CorrelationFilter
from observability.logging import JsonFormatter, TextFormatter
from settings import get_log_format, get_log_level

_configured = False


def _configure_root_logger() -> None:
    global _configured
    if _configured:
        return

    formatter = JsonFormatter() if get_log_format() == "json" else TextFormatter()

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(CorrelationFilter())

    root = logging.getLogger()
    root.setLevel(get_log_level())
    root.addHandler(handler)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Structured INFO/ERROR logging. Output format (text/json) and correlation
    ID propagation are configured centrally here; see ADR-0011. OpenTelemetry
    tracing is planned for Sprint 6.3.
    """
    _configure_root_logger()
    return logging.getLogger(name)
