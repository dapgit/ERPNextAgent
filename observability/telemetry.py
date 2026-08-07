import functools
from typing import Callable, Optional

from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from settings import get_telemetry_enabled

_configured = False


def configure_telemetry() -> None:
    """
    Initialize the OpenTelemetry SDK when OTEL_ENABLED is set. Idempotent
    and safe to call any number of times. When disabled (the default),
    this is a no-op: every tracer obtained afterwards resolves to the
    OpenTelemetry API's built-in no-op provider, so no instrumented code
    needs to branch on whether telemetry is on. See ADR-0012.
    """
    global _configured
    if _configured:
        return
    _configured = True

    if not get_telemetry_enabled():
        return

    provider = TracerProvider(resource=Resource.create({"service.name": "erpnextagent"}))
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    RequestsInstrumentor().instrument()


def get_tracer(name: str) -> trace.Tracer:
    """Return a tracer for `name`, configuring telemetry on first use."""
    configure_telemetry()
    return trace.get_tracer(name)


def traced(operation_name: Optional[str] = None) -> Callable:
    """
    Decorator that wraps a function body in a span. When operation_name is
    omitted, the span name is derived from the function's module-qualified
    __qualname__ (e.g. "services.item_service.get_item") — mirroring how
    `operation` is derived from record.funcName in the logging layer
    (ADR-0011) rather than passed manually at every call site. The module
    qualifier matters: a bare __qualname__ collides between, e.g., the
    Tool and Service layers' same-named get_item functions. See ADR-0012.

    Not applied to the Tool layer's public functions: the Antigravity SDK
    inspects their signatures to build the tool schema sent to the model,
    and ADR-0011 already established keeping that surface undecorated.
    """

    def decorator(func: Callable) -> Callable:
        span_name = operation_name or f"{func.__module__}.{func.__qualname__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer(func.__module__)
            with tracer.start_as_current_span(span_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator
