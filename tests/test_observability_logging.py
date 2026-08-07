import json
import logging
import sys

from observability.logging import JsonFormatter, TextFormatter


def _make_record(msg="hello", exc_info=None, extra=None):
    record = logging.LogRecord(
        name="repositories.customer_repository",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=msg,
        args=(),
        exc_info=exc_info,
        func="get_customer",
    )
    record.correlation_id = "abc123"
    record.layer = "repository"
    for key, value in (extra or {}).items():
        setattr(record, key, value)
    return record


def test_text_formatter_includes_timestamp_level_logger_correlation_and_message():
    line = TextFormatter().format(_make_record())

    assert "INFO" in line
    assert "repositories.customer_repository" in line
    assert "[abc123]" in line
    assert "hello" in line


def test_text_formatter_appends_optional_fields_when_present():
    line = TextFormatter().format(_make_record(extra={"entity": "Customer", "duration_ms": 12.3}))

    assert "entity=Customer" in line
    assert "duration_ms=12.3" in line


def test_text_formatter_omits_optional_fields_when_absent():
    line = TextFormatter().format(_make_record())

    assert "entity=" not in line
    assert "duration_ms=" not in line


def test_json_formatter_produces_the_documented_schema():
    payload = json.loads(JsonFormatter().format(_make_record()))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "repositories.customer_repository"
    assert payload["layer"] == "repository"
    assert payload["operation"] == "get_customer"
    assert payload["correlation_id"] == "abc123"
    assert payload["message"] == "hello"
    assert "timestamp" in payload
    assert "entity" not in payload
    assert "duration_ms" not in payload


def test_json_formatter_includes_optional_fields_when_present():
    payload = json.loads(
        JsonFormatter().format(_make_record(extra={"entity": "Item", "duration_ms": 42.0}))
    )

    assert payload["entity"] == "Item"
    assert payload["duration_ms"] == 42.0


def test_json_formatter_includes_exception_details_on_failure():
    try:
        raise ValueError("boom")
    except ValueError:
        record = _make_record(exc_info=sys.exc_info())

    payload = json.loads(JsonFormatter().format(record))

    assert "ValueError" in payload["exception"]
    assert "boom" in payload["exception"]
