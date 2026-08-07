import contextvars
import logging
import uuid

_NO_CORRELATION_ID = "-"

_correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=_NO_CORRELATION_ID
)


def new_correlation_id() -> str:
    """Generate a new correlation ID. Does not set it as the active one."""
    return uuid.uuid4().hex


def set_correlation_id(correlation_id: str) -> None:
    """Set the correlation ID for the current execution context."""
    _correlation_id.set(correlation_id)


def get_correlation_id() -> str:
    """Return the correlation ID for the current execution context, or '-' if none is active."""
    return _correlation_id.get()


def begin_correlation() -> str:
    """Start a new correlation scope (e.g. once per user turn) and return its ID."""
    correlation_id = new_correlation_id()
    set_correlation_id(correlation_id)
    return correlation_id


class CorrelationFilter(logging.Filter):
    """
    Attaches correlation_id and layer to every log record that passes
    through it. Register once on the root handler; no application code
    needs to be aware this exists. See ADR-0011.
    """

    _LAYER_PREFIXES = (
        ("repositories.", "repository"),
        ("clients.", "client"),
        ("services.", "service"),
        ("tools.", "tool"),
    )

    # utils.tool_execution implements Tool-layer error handling (ADR-0011,
    # Sprint 5.7) but lives under utils/, so the prefix table above wouldn't
    # otherwise classify it correctly.
    _LOGGER_OVERRIDES = {
        "utils.tool_execution": "tool",
    }

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = get_correlation_id()
        record.layer = self._derive_layer(record.name)
        return True

    @classmethod
    def _derive_layer(cls, logger_name: str) -> str:
        if logger_name in cls._LOGGER_OVERRIDES:
            return cls._LOGGER_OVERRIDES[logger_name]
        for prefix, layer in cls._LAYER_PREFIXES:
            if logger_name.startswith(prefix):
                return layer
        return "other"
