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

Future releases will continue following semantic versioning aligned with sprint milestones.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added documentation-system metadata and navigation. |
| 2026-08-06 | Recorded Sprint 5.1–5.2 implementation and observability deferral. |
| 2026-08-07 | Recorded Sprint 5.5 Item lookup completion, Sprint 5.6 mock-repository removal, and Sprint 5.7 tool-layer error handling. Sprint 5 is now complete. |

---

Documentation: [index](docs/index.md) · [sprint journals](docs/journal/index.md) · [ADRs](docs/adr/index.md)
