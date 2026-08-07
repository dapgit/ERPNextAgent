---
title: ADR 0012 — OpenTelemetry Tracing
status: accepted
audience: contributors
last_reviewed: 2026-08-07
---

# ADR 0012 — OpenTelemetry Tracing

## Status

Accepted in Sprint 6.3.

## Context

ADR 0010 deferred OpenTelemetry to Sprint 6 and required that the sprint first define "a dedicated observability package, safe span attributes, context propagation, exporter configuration, and tests before adding instrumentation." ADR 0011 (Sprint 6.1) built that foundation — structured logging and a `contextvars`-based correlation ID — and explicitly flagged that the correlation ID was "designed to become — or sit alongside — the OpenTelemetry trace ID in Sprint 6.3." Sprint 6.2 (Correlation IDs) was folded into 6.1, so Sprint 6.3 is the next milestone, focused purely on distributed tracing.

Checking the environment before designing further: only `opentelemetry-api` is installed, and it arrived as a transitive dependency of `mcp` (pulled in via `google-antigravity`) — this project never declared it. `opentelemetry-sdk` (which provides `TracerProvider`, `ConsoleSpanExporter`, span processors), and `opentelemetry-instrumentation-requests` are not installed. The `-api` package alone defaults to a no-op tracer provider; nothing is exported today even though the package is present.

## Decision

### 1. Dependencies

Add `opentelemetry-sdk` and `opentelemetry-instrumentation-requests` to `requirements.txt`. No exporter/collector packages are added yet (Decision 2).

### 2. Exporter: console first, collector deferred

Use `ConsoleSpanExporter` (part of `opentelemetry-sdk`) for Sprint 6.3. Defer OTLP/collector export — and the `docker`-based local collector setup originally scoped into this sprint — to a later sprint, once there is an actual collector target to point at. The `TracerProvider` → `SpanProcessor` → exporter chain is already OpenTelemetry's designed seam for swapping exporters via configuration, so nothing about the instrumentation itself needs to change when that happens.

### 3. Telemetry is optional, off by default, and configuration-driven

Add `settings.get_telemetry_enabled()`, reading `OTEL_ENABLED` (default `false`). When disabled, `observability/telemetry.py` never calls the SDK's `set_tracer_provider()`, so every span-creation call in the codebase hits the OpenTelemetry API's built-in no-op provider automatically. This means "disabled" requires no conditional logic anywhere instrumentation appears — the same centralize-it-once approach ADR 0011 used for the logging filter.

### 4. Correlation ID and trace ID: attribute, not replacement

`correlation_id` (ADR 0011, `contextvars`-based) remains the sole source of truth for logs, unchanged. When telemetry is enabled, it is additionally attached as a span attribute (`span.set_attribute("correlation_id", get_correlation_id())`) on the root span created per user turn. It does not become, and is not replaced by, the OpenTelemetry trace ID — the two are independently generated (one always, one only when telemetry is enabled) and conflating their formats would recouple something ADR 0011 deliberately kept simple. The attribute is what lets a collector UI cross-reference a trace back to its logs.

### 5. A shared span-creation helper, not hand-written spans per method

Add a `traced(operation_name: Optional[str] = None)` decorator in `observability/telemetry.py`, using `functools.wraps`, that wraps a function body in `tracer.start_as_current_span(...)`. When `operation_name` is omitted, derive the span name from the function's **module-qualified** `__qualname__` (e.g. `services.item_service.get_item`) — mirroring how `operation` is already derived from `record.funcName` in `JsonFormatter` (ADR 0011) rather than passed manually. Apply `@traced` to Service and Repository methods.

A bare `__qualname__` was tried first and rejected during Decision 8's live verification: the Tool layer's manually-created span and the Service layer's `@traced`-derived span for the same operation are both plain module-level functions named `get_item`, so a bare `__qualname__` produced two identically-named spans distinguishable only by tree position. The module qualifier fixes this — `tools.item.get_item` vs. `services.item_service.get_item` — and was applied consistently to the Tool layer's manual span names too.

The Tool layer is **not** decorated externally. ADR 0011 already established why: the Antigravity SDK inspects each Tool function's signature to build the schema it sends to Gemini, and `tools/*.py`'s public functions were deliberately kept undecorated for that reason (logic lives in inner closures instead, e.g. around `execute_tool`). Tool-layer spans are started inside those same inner closures, not via a decorator on `get_customer`, `get_item`, etc.

### 6. REST client: auto-instrumentation, not manual spans

Use `opentelemetry-instrumentation-requests`'s `RequestsInstrumentor().instrument()`, called once during telemetry initialization, to capture outbound HTTP calls made by `ERPNextRESTClient`'s `requests.Session`. This requires no changes inside `clients/erpnext_rest_client.py`, preserving the client-layer boundary ADR 0008 established.

### 7. Root span and correlation ID start together

`app.py`'s `chat_loop` starts one root span per user turn (only when telemetry is enabled) alongside the existing `begin_correlation()` call, and attaches `correlation_id` to it per Decision 4.

### 8. Instrument one flow first

Instrument Item lookup (Tool → Service → Repository → REST Client) first. Verify the span hierarchy and the `correlation_id` attribute in the console exporter's output before extending `@traced` to the Company and Customer Service/Repository methods.

Verified live, twice: once as a direct synchronous call, and again through `asyncio.to_thread` (the exact mechanism the Antigravity SDK uses to run Tool functions — see ADR 0011) to confirm the span hierarchy survives the same thread boundary the correlation ID already had to. Both produced the full `user_turn → tools.* → services.* → repositories.* → GET (×N, auto-instrumented)` hierarchy under one shared `trace_id`, with `correlation_id` present as an attribute on the root span. Company and Customer were then instrumented the same way in the same pass, once the pattern was confirmed correct.

## Rationale

- A no-op default `TracerProvider` means Decision 3 requires zero conditional branches in instrumented code — consistent with how ADR 0011's `CorrelationFilter` centralizes correlation-ID injection instead of scattering it.
- Starting with the console exporter avoids requiring infrastructure (a running collector) before the instrumentation itself is proven correct; the exporter is designed to be swapped later without touching span-creation code.
- Treating `correlation_id` as a span attribute rather than merging identifier schemes keeps ADR 0011 unmodified and avoids coupling a value generated unconditionally every turn (`uuid4().hex`) to one that only exists when telemetry happens to be enabled.
- A shared `traced()` decorator avoids repeating `with tracer.start_as_current_span(...)` at every Service/Repository method — the same repetition concern already raised (and deliberately deferred) for logging's `extra={...}` kwargs, but here the shape of the repetition is obvious up front, so the helper is built alongside the first use rather than after.
- Auto-instrumenting `requests` avoids touching `clients/erpnext_rest_client.py` at all.

## Consequences

- `requirements.txt` gains `opentelemetry-sdk` and `opentelemetry-instrumentation-requests`.
- New `observability/telemetry.py`: SDK initialization (`TracerProvider` + `ConsoleSpanExporter`, gated by `get_telemetry_enabled()`), the `traced()` decorator, and `RequestsInstrumentor` wiring.
- `settings.py` gains `get_telemetry_enabled()` (`OTEL_ENABLED`, default `false`).
- `app.py` starts one root span per turn when telemetry is enabled, alongside `begin_correlation()`.
- Company, Customer, and Item are all instrumented: Service and Repository methods carry `@traced()`; Tool-layer spans are added inside existing inner closures, not via decorators on the public Tool functions.
- No change to any method signature, to `clients/erpnext_rest_client.py`'s business logic, or to ADR 0011's logging/correlation design.
- Existing tests continue to pass with telemetry disabled (the default). New tests for `observability/telemetry.py` use an in-memory span exporter, not the console exporter, so test output stays clean.

## Related records

- [ADR 0010 — Defer OpenTelemetry to Sprint 6](0010-observability-deferred-to-sprint-6.md)
- [ADR 0011 — Structured Logging and Correlation IDs](0011-structured-logging-and-correlation-ids.md)
- [ADR 0008 — Client Layer](0008-client-layer.md)
- [Architecture overview](../architecture/overview.md)
- [Project roadmap](../project-roadmap.md)
- [Project checkpoint](../checkpoints/PROJECT_CHECKPOINT.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-07 | Proposed the OpenTelemetry tracing design for Sprint 6.3. |

---

Previous: [ADR 0011](0011-structured-logging-and-correlation-ids.md) · Back to the [ADR index](index.md).
