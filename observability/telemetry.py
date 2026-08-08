import functools
import os
import time
from typing import IO, Callable, Optional

from opentelemetry import metrics, trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from observability.correlation import derive_layer
from settings import get_telemetry_enabled

_configured = False

# The console metric reader's default export interval is 60s, which would
# make local verification impractical. See ADR-0014.
_CONSOLE_METRIC_EXPORT_INTERVAL_MILLIS = 5000

# Console exporters default to stdout, which collides with the interactive
# CLI's own output — every span and every 5s metric export would print
# into the same screen the user is chatting in. Route them to files
# instead, so the terminal stays clean and traces/metrics are available
# to tail or open when actually wanted. Not a new environment variable:
# this only changes where the existing console-style exporters write to,
# not what they emit.
_LOG_DIR = "logs"


def _open_console_log(filename: str) -> IO:
    os.makedirs(_LOG_DIR, exist_ok=True)
    return open(os.path.join(_LOG_DIR, filename), "a", encoding="utf-8")


def configure_telemetry() -> None:
    """
    Initialize the OpenTelemetry SDK when OTEL_ENABLED is set. Idempotent
    and safe to call any number of times. When disabled (the default),
    this is a no-op: every tracer/meter obtained afterwards resolves to
    the OpenTelemetry API's built-in no-op provider, so no instrumented
    code needs to branch on whether telemetry is on. See ADR-0012, ADR-0014.
    """
    global _configured
    if _configured:
        return
    _configured = True

    if not get_telemetry_enabled():
        return

    resource = Resource.create({"service.name": "erpnextagent"})

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter(out=_open_console_log("traces.log")))
    )
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(
        ConsoleMetricExporter(out=_open_console_log("metrics.log")),
        export_interval_millis=_CONSOLE_METRIC_EXPORT_INTERVAL_MILLIS,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    RequestsInstrumentor().instrument()


def get_tracer(name: str) -> trace.Tracer:
    """Return a tracer for `name`, configuring telemetry on first use."""
    configure_telemetry()
    return trace.get_tracer(name)


def get_meter(name: str) -> metrics.Meter:
    """Return a meter for `name`, configuring telemetry on first use."""
    configure_telemetry()
    return metrics.get_meter(name)


def traced(operation_name: Optional[str] = None) -> Callable:
    """
    Decorator that wraps a function body in a span and records its
    duration as the erpnextagent.call.duration histogram. When
    operation_name is omitted, the span/metric name is derived from the
    function's module-qualified __qualname__ (e.g.
    "services.item_service.get_item") — mirroring how `operation` is
    derived from record.funcName in the logging layer (ADR-0011) rather
    than passed manually at every call site. The module qualifier
    matters: a bare __qualname__ collides between, e.g., the Tool and
    Service layers' same-named get_item functions. See ADR-0012, ADR-0014.

    Not applied to the Tool layer's public functions: the Antigravity SDK
    inspects their signatures to build the tool schema sent to the model,
    and ADR-0011 already established keeping that surface undecorated.
    """

    def decorator(func: Callable) -> Callable:
        span_name = operation_name or f"{func.__module__}.{func.__qualname__}"
        layer = derive_layer(func.__module__)
        duration_histogram = get_meter(func.__module__).create_histogram(
            "erpnextagent.call.duration",
            unit="ms",
            description="Duration of a traced Service/Repository call.",
        )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer(func.__module__)
            start = time.perf_counter()
            outcome = "error"
            try:
                with tracer.start_as_current_span(span_name):
                    result = func(*args, **kwargs)
                outcome = "success"
                return result
            finally:
                duration_ms = (time.perf_counter() - start) * 1000
                duration_histogram.record(
                    duration_ms,
                    {"operation": span_name, "layer": layer, "outcome": outcome},
                )

        return wrapper

    return decorator
