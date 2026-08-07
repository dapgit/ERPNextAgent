from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from observability.telemetry import get_tracer, traced

# Application code only calls trace.set_tracer_provider() when OTEL_ENABLED
# is set (default: false), which it isn't anywhere in the test suite. That
# makes this the first and only call in the process, so it's safe to set a
# test-only provider once here rather than fighting the OTel API's
# "can only be set once" rule with a real one. See ADR-0012.
_exporter = InMemorySpanExporter()
_provider = TracerProvider()
_provider.add_span_processor(SimpleSpanProcessor(_exporter))
trace.set_tracer_provider(_provider)


def _spans_by_name():
    return {span.name: span for span in _exporter.get_finished_spans()}


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


def test_traced_creates_a_span_named_after_the_module_qualified_function():
    _exporter.clear()

    assert _get_customer("ABC") == "hello ABC"

    assert f"{__name__}._get_customer" in _spans_by_name()


def test_traced_accepts_an_explicit_operation_name():
    _exporter.clear()

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
    _exporter.clear()

    _Repository().get_item("Desk")

    assert f"{__name__}._Repository.get_item" in _spans_by_name()


def test_nested_traced_calls_share_one_trace_and_correct_parentage():
    _exporter.clear()

    _outer()

    spans = _spans_by_name()
    outer_span = spans["outer"]
    inner_span = spans["inner"]
    assert inner_span.context.trace_id == outer_span.context.trace_id
    assert inner_span.parent.span_id == outer_span.context.span_id


def test_get_tracer_returns_a_usable_tracer():
    tracer = get_tracer("some.module")
    assert tracer is not None
