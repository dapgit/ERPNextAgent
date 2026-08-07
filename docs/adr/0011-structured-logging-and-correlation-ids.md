---
title: ADR 0011 — Structured Logging and Correlation IDs
status: accepted
audience: contributors
last_reviewed: 2026-08-07
---

# ADR 0011 — Structured Logging and Correlation IDs

## Status

Accepted in Sprint 6.1.

## Context

ADR 0010 deferred OpenTelemetry to Sprint 6 and required that Sprint 6 first define "a dedicated observability package, safe span attributes, context propagation, exporter configuration, and tests before adding instrumentation." Instrumenting traces and metrics on top of today's logging would mean redoing the logging work twice, so Sprint 6 begins with the logging and correlation foundation instead.

Today, logging is inconsistent in coverage even though it is consistent in style:

- `repositories/*.py` and `clients/erpnext_rest_client.py` log through `utils.logger.get_logger(__name__)` with plain, `%s`-interpolated messages (e.g. `"Fetching Company '%s' from ERPNext"`).
- `tools/*.py` and `services/*.py` do not log at all. `utils.tool_execution.execute_tool()` is the only Tool-layer logging that exists, and it was added in Sprint 5.7 specifically for error paths.
- There is no request or correlation identifier anywhere. A single user turn spanning Tool → Service → Repository → Client produces log lines with no shared field to group them by.
- The output is free text, not machine-parseable, which blocks both external log aggregation and eventual correlation with OpenTelemetry trace/span IDs.

## Decision

### 1. Log format: JSON, selectable per environment

Adopt JSON as the structured log format — it is the format OpenTelemetry-adjacent tooling and log aggregators expect natively, and free-text or key-value formats would need a second migration once Sprint 6.3 arrives.

However, `app.py` is an interactive CLI the user watches live in a terminal; raw JSON is worse for that use case than the current plain-text output. Add `get_log_format()` to `settings.py`, mirroring the existing `get_log_level()`:

- `LOG_FORMAT=text` (default) — human-readable, current-style output, for local/interactive use.
- `LOG_FORMAT=json` — structured output, for aggregated/production use.

Both formatters read from the same `LogRecord`, so no log call site depends on which one is active.

### 2. Log schema

| Field | Required | Source |
| --- | --- | --- |
| `timestamp` | Yes | Automatic (`LogRecord.created`) |
| `level` | Yes | Automatic (`LogRecord.levelname`) |
| `logger` | Yes | Automatic (`LogRecord.name`) |
| `layer` | Yes | **Derived** from `logger` (`repositories.*` → `repository`, `clients.*` → `client`, `services.*` → `service`, `tools.*` → `tool`, else `other`) |
| `operation` | Yes | **Derived** from `LogRecord.funcName` |
| `correlation_id` | Yes | Injected by the logging filter (Decision 3) |
| `message` | Yes | Call-site (the log call's own message) |
| `entity` | Optional | Call-site, via `extra={"entity": "Customer"}` when relevant |
| `exception` | Optional | **Derived** from `LogRecord.exc_info` when present |
| `duration_ms` | Optional | Call-site, via `extra={"duration_ms": ...}` when timing an operation |

`layer`, `operation`, `timestamp`, `level`, `logger`, and `exception` are all recovered from data the standard library already attaches to every `LogRecord`. No call site needs to pass them — `logger.info("Fetching customer")` stays exactly that simple. Only `entity` and `duration_ms` require an explicit `extra={...}` when the call site actually has that data (e.g. `erpnext_rest_client.py` already computes `duration_ms` today, just not as a structured field).

This schema applies to logs emitted through `utils.logger.get_logger()`. It does not apply to and cannot cover third-party or SDK-internal logging (e.g. the `google.antigravity` harness's own log output), which is outside this application's control.

### 3. Correlation IDs via `contextvars`

Use a single `contextvars.ContextVar[str]` to carry a correlation ID, generated once per user turn at the application boundary (`app.py`'s `chat_loop`, before calling `local_agent.chat(...)`), not threaded as a parameter through Tool/Service/Repository/Client signatures. This keeps every existing method signature unchanged and works correctly under async execution, since `contextvars` — unlike thread-locals — follows the `asyncio` task that sets it.

### 4. Logging filter

A `logging.Filter` (living in `observability/correlation.py`) does all of the derivation work:

- Reads the correlation ID from the `ContextVar`, defaulting to a fixed placeholder (e.g. `"-"`) when no request context is active (startup/shutdown logging).
- Derives `layer` from `record.name` and `operation` from `record.funcName`.
- Attaches `exception` from `record.exc_info` when present.

The filter is registered once, centrally, when logging is configured — no application code anywhere is aware it exists.

### 5. Logging ownership per layer

| Layer | Responsibility |
| --- | --- |
| Tool | Request start/end, user-facing outcome |
| Service | Business decisions and orchestration |
| Repository | Data access operations (already covers most of today's logging) |
| Client | HTTP requests, retries, response status (already covers the rest) |

Repository and Client logging already roughly follows this — Sprint 6.1 reformats those call sites to use structured `extra` fields where appropriate. Tool and Service logging does not exist yet anywhere in the codebase; Sprint 6.1 adds it, it is not purely a reformatting pass.

## Rationale

- Deriving `layer`, `operation`, and `exception` from the `LogRecord` instead of requiring them as manual `extra` kwargs at every call site avoids the exact failure mode structured logging is meant to prevent: a forgotten or mistyped field silently breaking the schema at one call site while the rest of the codebase stays consistent.
- A configurable formatter avoids forcing a choice between "readable for the person running the CLI today" and "parseable for aggregation later" — both are real, current requirements.
- `contextvars` over explicit parameters preserves every architectural decision made in ADRs 0002–0008 (thin tools, layered services/repositories, an entity-agnostic client) without reopening any of their signatures.
- The correlation ID set up here is designed to become — or sit alongside — the OpenTelemetry trace ID in Sprint 6.3, so Sprint 6.1 is not building an identifier that gets thrown away later.

## Consequences

- `settings.py` gains `get_log_format()`; `utils/logger.py` gains a JSON formatter alongside the existing text formatter and selects between them based on it.
- A new `observability/` package is introduced starting with `observability/logging.py` (formatters) and `observability/correlation.py` (the `ContextVar` and filter) — `observability/telemetry.py`, `observability/metrics.py`, and `observability/config.py` are deferred to Sprints 6.3–6.4 and are not created yet.
- `app.py`'s `chat_loop` generates a correlation ID per turn and sets it on the `ContextVar` before invoking the agent.
- Existing `repositories/*.py` and `clients/erpnext_rest_client.py` log calls are updated to pass `entity`/`duration_ms` via `extra={...}` where relevant; their messages and log levels are otherwise unchanged.
- New log statements are added to `tools/*.py` and `services/*.py` per the Decision 5 ownership table; these did not exist before Sprint 6.1.
- No Service, Repository, or Client method signature changes. No business logic moves into the Tool layer.
- Third-party/SDK log output remains free-text and is explicitly out of scope for the schema.

## Related records

- [ADR 0010 — Defer OpenTelemetry to Sprint 6](0010-observability-deferred-to-sprint-6.md)
- [ADR 0008 — Client Layer](0008-client-layer.md)
- [Architecture overview](../architecture/overview.md)
- [Project roadmap](../project-roadmap.md)
- [Project checkpoint](../checkpoints/PROJECT_CHECKPOINT.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-07 | Proposed the structured logging and correlation ID design for Sprint 6.1. |

---

Previous: [ADR 0010](0010-observability-deferred-to-sprint-6.md) · Back to the [ADR index](index.md) · Next: [ADR 0012](0012-opentelemetry-tracing.md)
