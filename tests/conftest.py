from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

# Application code only calls trace.set_tracer_provider() / metrics.set_meter_
# provider() when OTEL_ENABLED is set (default: false), which it isn't
# anywhere in the test suite. That makes these the first and only calls in
# the process, so it's safe to install test-only providers once here,
# before any test module is collected — pytest always imports conftest.py
# first, so this doesn't depend on which test file happens to import
# first alphabetically. See ADR-0012, ADR-0014.

span_exporter = InMemorySpanExporter()
_tracer_provider = TracerProvider()
_tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
trace.set_tracer_provider(_tracer_provider)

metric_reader = InMemoryMetricReader()
_meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(_meter_provider)


def metric_data_points(metric_name):
    """
    Flatten the shared InMemoryMetricReader's export into (attributes,
    value) pairs for a given metric name. The reader is cumulative (it
    never resets), so tests should key assertions off distinct
    operation/tool names rather than expecting a clean slate.
    """
    points = []
    for resource_metrics in metric_reader.get_metrics_data().resource_metrics:
        for scope_metrics in resource_metrics.scope_metrics:
            for metric in scope_metrics.metrics:
                if metric.name != metric_name:
                    continue
                for point in metric.data.data_points:
                    value = point.sum if hasattr(point, "sum") else point.value
                    points.append((dict(point.attributes), value))
    return points
