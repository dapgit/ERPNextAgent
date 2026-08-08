import pytest
from conftest import metric_data_points

from utils.exceptions import (
    ERPNextAuthenticationError,
    ERPNextConnectionError,
    ERPNextResponseError,
    ERPNextTimeoutError,
)
from utils.tool_execution import execute_tool


def test_returns_the_operation_result_on_success():
    assert execute_tool(lambda: "ok") == "ok"


def test_value_error_becomes_its_own_message():
    def _raise():
        raise ValueError("item_code must not be empty")

    assert execute_tool(_raise) == "item_code must not be empty"


@pytest.mark.parametrize(
    "exception, expected_message",
    [
        (ERPNextAuthenticationError("bad creds"), "Unable to retrieve information. ERPNext authentication failed."),
        (ERPNextTimeoutError("too slow"), "ERPNext did not respond in time."),
        (ERPNextConnectionError("unreachable"), "Unable to connect to ERPNext."),
        (ERPNextResponseError("500"), "ERPNext returned an unexpected error."),
    ],
)
def test_erpnext_errors_map_to_safe_messages(exception, expected_message):
    def _raise():
        raise exception

    assert execute_tool(_raise) == expected_message


def test_erpnext_error_message_never_leaks_into_the_response():
    def _raise():
        raise ERPNextAuthenticationError(
            "ERPNext rejected the request to http://localhost:8080/api/resource/Company/A Sports (status 401)"
        )

    result = execute_tool(_raise)

    assert "localhost" not in result
    assert "8080" not in result


def test_unexpected_errors_do_not_leak_implementation_details():
    def _raise():
        raise RuntimeError("connection refused at 10.0.0.5:5432")

    result = execute_tool(_raise)

    assert result == "An unexpected error occurred."
    assert "10.0.0.5" not in result


def get_widget():
    """Named like a real Tool function's inner closure so _derive_tool_name recovers "get_widget"."""
    def _get_widget():
        return "ok"

    return execute_tool(_get_widget)


def get_broken_widget():
    def _get_broken_widget():
        raise ERPNextTimeoutError("too slow")

    return execute_tool(_get_broken_widget)


def test_execute_tool_records_duration_tagged_with_the_recovered_tool_name():
    get_widget()

    points = metric_data_points("erpnextagent.tool.duration")
    matching = [(attrs, value) for attrs, value in points if attrs.get("tool") == "get_widget"]

    assert matching, points
    attrs, value = matching[0]
    assert attrs["outcome"] == "success"
    assert value >= 0


def test_execute_tool_records_errors_by_type_without_recording_on_success():
    get_broken_widget()

    duration_points = metric_data_points("erpnextagent.tool.duration")
    error_points = metric_data_points("erpnextagent.tool.errors")

    duration_matching = [
        (attrs, v) for attrs, v in duration_points if attrs.get("tool") == "get_broken_widget"
    ]
    error_matching = [
        (attrs, v) for attrs, v in error_points if attrs.get("tool") == "get_broken_widget"
    ]

    assert duration_matching, duration_points
    assert duration_matching[0][0]["outcome"] == "error"

    assert error_matching, error_points
    assert error_matching[0][0]["error_type"] == "ERPNextTimeoutError"

    success_points = metric_data_points("erpnextagent.tool.errors")
    assert not any(attrs.get("tool") == "get_widget" for attrs, _ in success_points)
