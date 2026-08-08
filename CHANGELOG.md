---
title: Changelog
status: active
audience: contributors
last_reviewed: 2026-08-07
---

# Changelog

All notable changes to this project will be documented in this file.

This project follows a sprint-based development approach. Each sprint represents a logical milestone in the evolution of the ERPNext AI Assistant.

---

# Sprint 6 – Observability (in progress)

## Completed milestones

### 6.1 — Structured logging and correlation IDs

- Added [ADR-0011](docs/adr/0011-structured-logging-and-correlation-ids.md), covering log format, schema, correlation ID propagation, and per-layer logging ownership.
- Added the `observability/` package: `observability/logging.py` (`TextFormatter` for local/interactive use, `JsonFormatter` for aggregated/production use) and `observability/correlation.py` (a `contextvars`-based correlation ID plus the `CorrelationFilter` that injects `correlation_id` and a derived `layer` into every log record).
- Added `settings.get_log_format()` (`LOG_FORMAT=text|json`, defaulting to `text`); `utils/logger.py` now configures the formatter and filter centrally.
- `app.py`'s `chat_loop` starts a new correlation ID per user turn; it propagates through `asyncio.to_thread` (confirmed against the Antigravity SDK's own tool-execution path) with no changes to any Tool/Service/Repository/Client method signature.
- Added Tool-layer (request start/end) and Service-layer (orchestration) logging, which did not exist before this sprint; Repository and Client logging were updated to carry `entity`/`duration_ms` as structured fields instead of only free text.
- Verified end-to-end: a single tool call now produces one shared `correlation_id` across the Tool, Service, Repository, and Client log lines; separate calls get distinct IDs.

### 6.3 — OpenTelemetry tracing

- Added [ADR-0012](docs/adr/0012-opentelemetry-tracing.md), covering the exporter strategy, the `correlation_id`-as-span-attribute decision, and the shared `traced()` helper.
- Added `opentelemetry-sdk` and `opentelemetry-instrumentation-requests` to `requirements.txt` — only the transitive `opentelemetry-api` (via `mcp`) was present before this milestone.
- Added `observability/telemetry.py`: SDK initialization gated by the new `settings.get_telemetry_enabled()` (`OTEL_ENABLED`, default `false`) using a `ConsoleSpanExporter`; the `traced()` decorator, which derives span names from a function's module-qualified `__qualname__`; and `RequestsInstrumentor` wiring for the REST client's outbound HTTP calls.
- Instrumented Company, Customer, and Item across Service and Repository methods (`@traced()`) and the Tool layer (spans started inside the existing inner closures, not via decorators on the public Tool functions — same signature-safety reasoning as ADR-0011).
- `app.py`'s `chat_loop` starts one root span per user turn, alongside the existing correlation ID, and attaches `correlation_id` to it as a span attribute.
- Verified live, including through `asyncio.to_thread` (the SDK's actual tool-execution path): a single call produces one trace spanning Tool → Service → Repository → auto-instrumented HTTP spans, and the app behaves identically — no console output at all — when telemetry is disabled (the default).
- A naming collision was found and fixed during verification: a bare `__qualname__` produced identically-named Tool-layer and Service-layer spans for the same operation (both just `get_item`); span names are now module-qualified.

### 6.4 — OpenTelemetry metrics

- Added [ADR-0013](docs/adr/0013-tiered-definition-of-done-and-platform-hardening.md) (tiered Definition of Done; Sprint 6.6 platform hardening inserted before Sprint 7) and [ADR-0014](docs/adr/0014-opentelemetry-metrics.md) (metrics design).
- Extended `configure_telemetry()` to also construct a `MeterProvider` (`ConsoleMetricExporter`, 5s export interval), gated by the same `OTEL_ENABLED` flag — no new environment variable, no new dependency (`opentelemetry-sdk`'s metrics support was already installed in 6.3).
- Extended the `traced()` decorator to record `erpnextagent.call.duration` (`{operation, layer, outcome}`) alongside the span it already creates; `layer` derivation was extracted from `CorrelationFilter` into a shared `observability.correlation.derive_layer()` so logging and metrics classify modules identically instead of duplicating the lookup table.
- Extended `utils/tool_execution.execute_tool()` to record `erpnextagent.tool.duration` and `erpnextagent.tool.errors` (`{tool, error_type}`), recovering the Tool name from the wrapped closure's `__qualname__` rather than requiring every `tools/*.py` call site to pass it.
- Extended `ERPNextRESTClient.get()` with an optional `doctype` parameter and a `erpnextagent.erpnext.requests` counter (`{doctype, outcome}`) — confirmed this is additive, not redundant: `opentelemetry-instrumentation-requests` (installed in 6.3) already emits a generic `http.client.duration` histogram automatically once a `MeterProvider` exists, but has no ERPNext-doctype dimension.
- Replaced the per-test-file OpenTelemetry provider setup with a shared `tests/conftest.py`, fixing a latent ordering hazard: `set_tracer_provider()`/`set_meter_provider()` can only succeed once per process, so whichever test file happened to import first was implicitly deciding this for the whole suite.
- Verified live: a real Item lookup and an intentionally invalid Customer lookup produced all four metric families with correctly bounded attributes; the app is silent (no console output at all) with `OTEL_ENABLED=false`. The live run also surfaced a real, unrelated issue — the configured ERPNext credentials are currently returning 401 — flagged separately, not a defect in this sprint.
- Added the Sprint 6 journal ([docs/journal/sprint-06-observability.md](docs/journal/sprint-06-observability.md)), covering 6.4 in full per ADR-0013's Tier 1 Definition of Done; 6.1/6.3 backfill remains Sprint 6.5 scope.

## Deferred

- The full observability documentation pass (Sprint 6.5, including backfilling 6.1/6.3 journal sections) is not yet implemented.
- Sprint 6.6 (Platform Hardening: resilience/retry, startup config validation, CI, secrets policy, security review) gates Sprint 7 — see ADR-0013.
- OTLP/collector export was deliberately deferred out of 6.3's and 6.4's scope — the console exporters are sufficient for local verification, and switching exporters is a configuration change, not a code change, whenever a real collector target exists.

---

# Sprint 5 – ERPNext REST Integration (complete)

## Completed milestones

### 5.1 — Integration boundary and configuration

- Added the `clients/` package and `ERPNextRESTClient` boundary.
- Added environment-backed ERPNext URL, API key, API secret, and optional Company settings.
- Added a distinct ERPNext exception hierarchy.

### 5.2 — Company lookup through REST

- Added `CompanyRepository` as an abstract contract with mock and REST-backed implementations.
- Added dependency injection for `ERPNextCompanyRepository` so its REST client can be replaced in tests.
- Added document and list helpers, a reusable `requests.Session`, authentication headers, URL construction, JSON parsing, timeout handling, and context-manager cleanup.
- Added repository mapping tests and an opt-in connectivity test.

### 5.3–5.4 — Repository scaling

- Completed the REST-backed Company repository, repository factory, basic request logging, and REST-backed Customer repository.
- Preserved Service and Tool contracts while adding constructor-injected, network-free repository tests.

### 5.5 — Item lookup (complete)

- Added `Item` domain model and REST-backed `ItemRepository`.
- Added the Item service and agent tool, with exact-code and partial-name lookup behavior.
- Added factory selection coverage and pytest configuration so `.venv/bin/pytest` resolves project imports reliably.
- Verified end-to-end against a live ERPNext instance.

### 5.6 — Removed mock repositories and ad-hoc company-name workarounds

- Removed `MockCompanyRepository`, `MockCustomerRepository`, and `MockItemRepository`; the app now always talks to a live ERPNext instance, and the repository factory no longer branches on whether `ERPNEXT_URL` is set.
- Removed the `ERPNEXT_COMPANY` environment variable and the ad-hoc, typo-matching patches that had accumulated around resolving the company name: a global monkey-patch of `requests.Session.request`, a bare `except Exception` fallback in the Company tool that bypassed the Repository/Service layers, and hardcoded string matching in the REST client, repository factory, and settings module.
- `ERPNextCompanyRepository` now always resolves the company by listing Companies from ERPNext and using the first one visible to the configured API user — nothing about the company is configured or hardcoded anywhere.

### 5.7 — Tool-layer error handling (Sprint 5 complete)

- Added `utils/tool_execution.execute_tool()`, a shared helper the Company, Customer, and Item tools now route their logic through. It catches `ERPNextError` subclasses (and `ValueError` for input validation) raised anywhere below the Tool layer, logs the real exception server-side, and returns a short, user-facing message with no stack traces, hostnames, or REST paths.
- The existing exception hierarchy (`utils/exceptions.py`) and the repository layer's not-found handling were reviewed and left as-is — both already matched the intended design, so no rework was needed there.
- Closes the last open item from Sprint 5's roadmap (Company, Customer, Item, Error Handling).

## Deferred

- Retries, write operations, and OpenTelemetry are not implemented. OpenTelemetry was evaluated and deliberately deferred to Sprint 6.
- Supplier, Inventory, Sales, and Purchase are placeholder modules with no implementation yet (planned for later sprints).

# Sprint 4 – Repository Pattern

## Added

- Repository layer
- Customer Repository
- Company Repository
- Customer Domain Model
- Repository package
- Repository abstraction
- Service-to-Repository communication

## Changed

- Customer Tool now delegates to Customer Service
- Customer Service now delegates to Repository
- Layered architecture finalized

## Refactored

- Removed business logic from Tool layer
- Moved customer data into Repository
- Simplified Service responsibilities

## Documentation

- Updated project structure
- Added Repository Pattern ADR
- Added Domain Model ADR
- Updated architecture diagrams
- Updated Sprint 4 journal

---

# Sprint 3 – Interactive Application

## Added

- Interactive Command Line Interface
- Agent lifecycle abstraction
- settings.py
- config.py
- assistant.py
- prompts.py

## Changed

- app.py reduced to orchestration
- Agent created once during application startup
- Continuous conversation loop introduced

## Refactored

- Configuration extracted from application entry point
- Prompt management centralized
- Environment management isolated

## Documentation

- Sprint 3 journal
- Architecture documentation
- ADR updates

---

# Sprint 2 – Custom Tools

## Added

- Company Information Tool
- Customer Information Tool
- Tool registration
- Mock Customer dataset

## Learned

- Custom Tool registration
- Tool metadata
- Automatic Tool invocation
- Agent-to-Tool interaction

## Documentation

- Sprint 2 journal
- Initial project notes

---

# Sprint 1 – Project Initialization

## Added

- Python project structure
- Virtual Environment
- Google Antigravity SDK
- Gemini API integration
- First AI Agent
- Initial repository structure

## Learned

- Agent lifecycle
- Async programming model
- LocalAgentConfig
- Gemini integration

## Documentation

- Initial repository documentation

---

# Upcoming

## Sprint 5 (complete)

- 5.1 through 5.7 are recorded above.

---

# Version History

| Version | Sprint |
|----------|--------|
| 0.1.0 | Sprint 1 |
| 0.2.0 | Sprint 2 |
| 0.3.0 | Sprint 3 |
| 0.4.0 | Sprint 4 |
| 0.5.0 | Sprint 5.1–5.4 |
| 0.6.0 | Sprint 5.5–5.7 |
| 0.7.0 (in progress) | Sprint 6.1, 6.3, 6.4 |

Future releases will continue following semantic versioning aligned with sprint milestones.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added documentation-system metadata and navigation. |
| 2026-08-06 | Recorded Sprint 5.1–5.2 implementation and observability deferral. |
| 2026-08-07 | Recorded Sprint 5.5 Item lookup completion, Sprint 5.6 mock-repository removal, and Sprint 5.7 tool-layer error handling. Sprint 5 is now complete. |
| 2026-08-07 | Recorded Sprint 6.4 (OpenTelemetry metrics), ADR-0013 (tiered DoD, Sprint 6.6 platform hardening), and ADR-0014. |

---

Documentation: [index](docs/index.md) · [sprint journals](docs/journal/index.md) · [ADRs](docs/adr/index.md)
