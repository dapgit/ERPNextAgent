---
title: ADR 0014 — OpenTelemetry Metrics
status: accepted
audience: contributors
last_reviewed: 2026-08-07
---

# ADR 0014 — OpenTelemetry Metrics

## Status

Accepted in Sprint 6.4.

## Context

ADR 0012 (Sprint 6.3) added the second observability signal, tracing. This sprint adds the third, metrics, completing the original Sprint 6 sequence: 6.1 logging/correlation, 6.3 tracing, 6.4 metrics, 6.5 documentation, 6.6 platform hardening (ADR 0013).

ADR 0013's tiered Definition of Done applies. Sprint 6.4 touches the Client, Tool, Service, and Repository layers, so it is a Tier 1 sprint: architecture, implementation, documentation, and validation are all required before it is considered complete — including a sprint journal entry, which Sprint 6.1 and 6.3 did not get. Backfilling those two is explicitly Sprint 6.5 scope, not a Sprint 6.4 blocker.

Checked before designing further: `opentelemetry-instrumentation-requests` (already installed and instrumented in Sprint 6.3 for tracing) emits an HTTP client request-duration histogram automatically once a `MeterProvider` is configured, using semantic-convention attributes (method, host, port, status code) rather than the raw URL — it is already cardinality-safe by default. `opentelemetry.sdk.metrics` and `InMemoryMetricReader` are already available via the `opentelemetry-sdk` dependency added in Sprint 6.3. No new dependency is required for this sprint.

## Decision

### 1. One flag, one init point

`OTEL_ENABLED` (existing) gates both tracing and metrics — no new environment variable. `configure_telemetry()` is extended to also construct a `MeterProvider`, following the same enabled/disabled no-op pattern already established for tracing: when disabled, no provider is set, and every meter obtained afterward resolves to the OpenTelemetry API's built-in no-op implementation.

### 2. Exporter: ConsoleMetricExporter, collector deferred

Matches ADR 0012's exporter decision for traces, for the same reason: local verification now, OTLP/collector export later, once there's a real target. `PeriodicExportingMetricReader` exports on an interval; the console reader uses a short interval (a few seconds) rather than the 60-second default, since a minute-long wait would make local verification impractical.

### 3. Rely on existing HTTP auto-instrumentation for generic request metrics; add one domain-specific counter alongside it

`RequestsInstrumentor` (already instrumented in Sprint 6.3) provides HTTP request count and duration automatically once a `MeterProvider` exists — this requires no code change in `ERPNextRESTClient`. It cannot express which ERPNext doctype was queried, since that's domain knowledge the HTTP layer doesn't have. Add one `Counter`, `erpnextagent.erpnext.requests`, incremented once per request inside `ERPNextRESTClient.get()`, with attributes `{doctype, outcome}`. `get()` gains an optional `doctype` parameter, passed through from `get_doc()` and `get_list()` (which already know it), keeping the counting logic in the one place `get()` already centralizes timing and logging for every request.

### 4. Tool duration and error-count-by-type, centralized in execute_tool()

Every tool call already passes through `utils.tool_execution.execute_tool()`, and its existing exception branches (`ERPNextAuthenticationError`, `ERPNextTimeoutError`, `ERPNextConnectionError`, generic `ERPNextError`, `ValueError`, unexpected `Exception`) already distinguish exactly the categories an `error_type` attribute needs. Add:

- `erpnextagent.tool.duration` (Histogram), attributes `{tool, outcome}`.
- `erpnextagent.tool.errors` (Counter), attributes `{tool, error_type}`.

No changes to `tools/*.py` are required — the same centralize-don't-scatter approach as ADR 0011's logging filter and ADR 0012's `traced()` decorator.

### 5. Repository/Service duration by extending traced(), not a second decorator

`traced()` (ADR 0012) already wraps every `@traced()` Service/Repository method in a span. Extend it to also record `erpnextagent.call.duration` (Histogram) at the same point, with attributes `{operation (the same module-qualified name used for the span), layer (reusing CorrelationFilter's layer-derivation logic rather than duplicating it), outcome}`. One metric name covers both layers, distinguished by the `layer` attribute, rather than a name like `.repository.duration` that would be misleading once applied to Service methods too. One code path produces both the span and the metric.

### 6. Cardinality rule, stated explicitly

No metric attribute is ever a free-form or user-supplied value. Permitted attribute values come only from small, code-controlled sets: `layer` (tool/service/repository/client/other), `operation` (the codebase's own function names — bounded because they're ours), `tool` (the small set of Tool functions), `entity` / `doctype` (Company/Customer/Item), `outcome` (success/error), `error_type` (the bounded exception-class set from Decision 4). Item codes, customer names, correlation IDs, and raw request paths are never used as metric attributes — correlation IDs in particular belong on spans and logs (ADR 0011, ADR 0012), not on metrics, precisely because an attribute with unbounded cardinality defeats the aggregation metrics exist for.

### 7. Naming convention

All custom metrics are prefixed `erpnextagent.`, matching the `service.name` resource attribute already set in ADR 0012 — `erpnextagent.tool.duration`, `erpnextagent.tool.errors`, `erpnextagent.erpnext.requests`, `erpnextagent.call.duration`.

### 8. Write Sprint 6.4's journal entry now, don't defer it again

Under ADR 0013's Tier 1 DoD, this sprint's journal entry is written as part of the sprint, not deferred. Backfilling journal entries for Sprint 6.1 and 6.3 remains Sprint 6.5 scope, not a Sprint 6.4 blocker.

## Rationale

- Reusing existing auto-instrumentation instead of hand-rolling HTTP metrics avoids a redundant, competing histogram for the same underlying calls.
- Extending `execute_tool()` and `traced()` rather than introducing new mechanisms keeps metrics collection at the same chokepoints already established for logging and tracing — one place to reason about per layer, not three.
- Making the cardinality rule an explicit, written decision, rather than an implicit convention, is the point of this ADR existing at all: cardinality mistakes are easy to make silently and expensive to discover later, once a real metrics backend is ingesting them.
- Writing 6.4's journal now, while explicitly not backfilling 6.1/6.3 in the same breath, keeps Tier 1 scope honest without turning this sprint into a documentation-debt cleanup project that belongs to 6.5.

## Consequences

- `observability/telemetry.py` gains a `MeterProvider`, a `get_meter()` helper, and `traced()` is extended to record `erpnextagent.call.duration` alongside the span it already creates.
- `utils/tool_execution.py` gains `erpnextagent.tool.duration` and `erpnextagent.tool.errors` recording in its existing exception branches.
- `clients/erpnext_rest_client.py`'s `get()` gains an optional `doctype` parameter and the `erpnextagent.erpnext.requests` counter; `get_doc()`/`get_list()` pass their doctype through. No other client behavior changes.
- No new dependency, no new environment variable, no method signature changes outside the one noted addition to the client's internal `get()`.
- Tests use `InMemoryMetricReader`, mirroring the `InMemorySpanExporter` pattern from ADR 0012's tests.
- A Sprint 6 journal entry is created covering Sprint 6.4; Sprint 6.1/6.3 remain undocumented in journal form until Sprint 6.5.

## Related records

- [ADR 0010 — Defer OpenTelemetry to Sprint 6](0010-observability-deferred-to-sprint-6.md)
- [ADR 0011 — Structured Logging and Correlation IDs](0011-structured-logging-and-correlation-ids.md)
- [ADR 0012 — OpenTelemetry Tracing](0012-opentelemetry-tracing.md)
- [ADR 0013 — Tiered Definition of Done and Platform Hardening Before Sprint 7](0013-tiered-definition-of-done-and-platform-hardening.md)
- [Project checkpoint](../checkpoints/PROJECT_CHECKPOINT.md)
- [Project roadmap](../project-roadmap.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-07 | Proposed the metrics design for Sprint 6.4. |

---

Previous: [ADR 0013](0013-tiered-definition-of-done-and-platform-hardening.md) · Back to the [ADR index](index.md).
