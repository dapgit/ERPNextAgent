import json
import logging
from datetime import datetime, timezone


def _optional_fields(record: logging.LogRecord) -> dict:
    fields = {}
    entity = getattr(record, "entity", None)
    if entity is not None:
        fields["entity"] = entity
    duration_ms = getattr(record, "duration_ms", None)
    if duration_ms is not None:
        fields["duration_ms"] = duration_ms
    return fields


class TextFormatter(logging.Formatter):
    """Human-readable formatter for local/interactive use. See ADR-0011."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        correlation_id = getattr(record, "correlation_id", "-")
        line = f"{timestamp} {record.levelname} {record.name} [{correlation_id}]: {record.getMessage()}"

        extras = _optional_fields(record)
        if extras:
            line += " (" + " ".join(f"{key}={value}" for key, value in extras.items()) + ")"

        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)

        return line


class JsonFormatter(logging.Formatter):
    """Structured JSON formatter for aggregated/production use. See ADR-0011 for the schema."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "layer": getattr(record, "layer", "other"),
            "operation": record.funcName,
            "correlation_id": getattr(record, "correlation_id", "-"),
            "message": record.getMessage(),
        }
        payload.update(_optional_fields(record))

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload)
