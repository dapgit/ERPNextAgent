import logging

from settings import get_log_level

_configured = False


def _configure_root_logger() -> None:
    global _configured
    if _configured:
        return

    logging.basicConfig(
        level=get_log_level(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Simple INFO/ERROR logging for Sprint 5. OpenTelemetry tracing is planned for Sprint 6+."""
    _configure_root_logger()
    return logging.getLogger(name)
