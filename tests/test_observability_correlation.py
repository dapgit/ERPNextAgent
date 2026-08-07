import logging

from observability.correlation import (
    CorrelationFilter,
    begin_correlation,
    get_correlation_id,
    new_correlation_id,
    set_correlation_id,
)


def test_get_correlation_id_defaults_to_a_placeholder():
    assert get_correlation_id() == "-"


def test_set_and_get_correlation_id_round_trip():
    set_correlation_id("turn-1")
    try:
        assert get_correlation_id() == "turn-1"
    finally:
        set_correlation_id("-")


def test_new_correlation_id_generates_distinct_values():
    assert new_correlation_id() != new_correlation_id()


def test_begin_correlation_sets_and_returns_the_same_id():
    correlation_id = begin_correlation()
    try:
        assert get_correlation_id() == correlation_id
    finally:
        set_correlation_id("-")


def _filtered_record(logger_name: str) -> logging.LogRecord:
    record = logging.LogRecord(
        name=logger_name,
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello",
        args=(),
        exc_info=None,
    )
    CorrelationFilter().filter(record)
    return record


def test_filter_attaches_the_active_correlation_id():
    set_correlation_id("turn-42")
    try:
        record = _filtered_record("repositories.customer_repository")
        assert record.correlation_id == "turn-42"
    finally:
        set_correlation_id("-")


def test_filter_derives_layer_from_logger_name():
    assert _filtered_record("repositories.customer_repository").layer == "repository"
    assert _filtered_record("clients.erpnext_rest_client").layer == "client"
    assert _filtered_record("services.customer_service").layer == "service"
    assert _filtered_record("tools.customer").layer == "tool"
    assert _filtered_record("some.other.module").layer == "other"


def test_filter_overrides_tool_execution_helper_to_the_tool_layer():
    assert _filtered_record("utils.tool_execution").layer == "tool"
