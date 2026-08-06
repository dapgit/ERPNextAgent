---
title: ADR 0010 — Defer OpenTelemetry to Sprint 6
status: accepted
audience: contributors
last_reviewed: 2026-08-06
---

# ADR 0010 — Defer OpenTelemetry to Sprint 6

## Status

Accepted in Sprint 5.2.

## Context

OpenTelemetry was evaluated as the long-term observability approach for the ERPNext integration. The current code has no telemetry package, tracer provider, spans, exporters, or instrumentation. Sprint 5’s immediate objective is to validate a small REST-backed repository path.

## Decision

Defer OpenTelemetry implementation to Sprint 6. Treat it as observability—not a replacement for all Python logging. The REST client will be the first candidate for outbound ERPNext spans because it centralizes transport behavior.

## Rationale

- Instrumentation introduces cross-cutting configuration and operational choices (resource naming, exporters, sampling, attributes, and secret redaction).
- The first REST path should stabilize before timing and error telemetry are designed around it.
- The client/repository split now provides a clean future instrumentation boundary without changing current application behavior.

## Consequences

- Do not claim OpenTelemetry is implemented in Sprint 5.
- Continue to use ordinary Python logging where startup or exceptional diagnostics require it.
- Sprint 6 must define a dedicated observability package, safe span attributes, context propagation, exporter configuration, and tests before adding instrumentation.

## Related records

- [Sprint 5 journal](../journal/sprint-05-erpnext-rest-foundation.md)
- [Architecture overview](../architecture/overview.md)
- [Project roadmap](../project-roadmap.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-06 | Recorded OpenTelemetry evaluation and deliberate Sprint 6 deferral. |

---

Previous: [ADR 0009](0009-rest-first-mcp-later.md) · Back to the [ADR index](index.md).
