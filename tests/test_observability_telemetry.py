from conftest import metric_data_points, span_exporter

from observability.telemetry import get_meter, get_tracer, traced


def _spans_by_name():
    return {span.name: span for span in span_exporter.get_finished_spans()}


# Defined at module level, like real @traced usage (services/*.py functions,
# repository methods) — a function nested inside a test would pick up the
# test's own name in __qualname__ and defeat these assertions.
@traced()
def _get_customer(name):
    return f"hello {name}"


@traced("custom-op")
def _do_something():
    return 42


class _Repository:
    @traced()
    def get_item(self, code):
        return code


@traced("inner")
def _inner():
    return "done"


@traced("outer")
def _outer():
    return _inner()


@traced("flaky-op")
def _flaky():
    raise ValueError("boom")


def test_traced_creates_a_span_named_after_the_module_qualified_function():
    span_exporter.clear()

    assert _get_customer("ABC") == "hello ABC"

    assert f"{__name__}._get_customer" in _spans_by_name()


def test_traced_accepts_an_explicit_operation_name():
    span_exporter.clear()

    assert _do_something() == 42
    assert "custom-op" in _spans_by_name()


def test_traced_preserves_the_wrapped_functions_metadata():
    @traced()
    def get_item(item_code: str) -> str:
        """Docstring."""
        return item_code

    assert get_item.__name__ == "get_item"
    assert get_item.__doc__ == "Docstring."


def test_traced_on_a_method_includes_the_class_name():
    span_exporter.clear()

    _Repository().get_item("Desk")

    assert f"{__name__}._Repository.get_item" in _spans_by_name()


def test_nested_traced_calls_share_one_trace_and_correct_parentage():
    span_exporter.clear()

    _outer()

    spans = _spans_by_name()
    outer_span = spans["outer"]
    inner_span = spans["inner"]
    assert inner_span.context.trace_id == outer_span.context.trace_id
    assert inner_span.parent.span_id == outer_span.context.span_id


def test_get_tracer_returns_a_usable_tracer():
    tracer = get_tracer("some.module")
    assert tracer is not None


def test_get_meter_returns_a_usable_meter():
    meter = get_meter("some.module")
    assert meter is not None


def test_traced_records_call_duration_with_operation_layer_and_success_outcome():
    _do_something()

    points = metric_data_points("erpnextagent.call.duration")
    matching = [
        (attrs, value) for attrs, value in points if attrs.get("operation") == "custom-op"
    ]

    assert matching, points
    attrs, value = matching[0]
    assert attrs["outcome"] == "success"
    assert attrs["layer"] == "other"  # this test module isn't under a known layer prefix
    assert value >= 0


def test_traced_records_error_outcome_when_the_wrapped_function_raises():
    try:
        _flaky()
    except ValueError:
        pass

    points = metric_data_points("erpnextagent.call.duration")
    matching = [
        (attrs, value) for attrs, value in points if attrs.get("operation") == "flaky-op"
    ]

    assert matching, points
    attrs, _ = matching[0]
    assert attrs["outcome"] == "error"


def test_traced_metric_layer_matches_correlation_filters_layer_derivation():
    _Repository().get_item("Desk")

    points = metric_data_points("erpnextagent.call.duration")
    matching = [
        (attrs, value)
        for attrs, value in points
        if attrs.get("operation") == f"{__name__}._Repository.get_item"
    ]

    assert matching, points
    attrs, _ = matching[0]
    # This test module's __name__ doesn't start with "repositories.", so
    # derive_layer falls back to "other" here too — the point is that
    # traced() and CorrelationFilter agree, not that this module is a
    # real repository. See ADR-0014 and tests/test_observability_correlation.py
    # for the prefix-matching cases (repositories./clients./services./tools.).
    assert attrs["layer"] == "other"
