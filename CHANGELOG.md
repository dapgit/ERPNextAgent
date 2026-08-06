---
title: Changelog
status: active
audience: contributors
last_reviewed: 2026-08-06
---

# Changelog

All notable changes to this project will be documented in this file.

This project follows a sprint-based development approach. Each sprint represents a logical milestone in the evolution of the ERPNext AI Assistant.

---

# Sprint 5 – ERPNext REST Integration (in progress)

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

## Deferred

- Customer remains backed by mock data; its REST repository is not yet implemented.
- Retries, write operations, structured logging, and OpenTelemetry are not implemented. OpenTelemetry was evaluated and deliberately deferred to Sprint 6.

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

## Sprint 5 (in progress)

- 5.1 and 5.2 are recorded above.
- Remaining scope includes additional repositories, controlled end-to-end verification, and follow-on resilience work.

---

# Version History

| Version | Sprint |
|----------|--------|
| 0.1.0 | Sprint 1 |
| 0.2.0 | Sprint 2 |
| 0.3.0 | Sprint 3 |
| 0.4.0 | Sprint 4 |
| 0.5.0 (in progress) | Sprint 5.1–5.2 |

Future releases will continue following semantic versioning aligned with sprint milestones.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added documentation-system metadata and navigation. |
| 2026-08-06 | Recorded Sprint 5.1–5.2 implementation and observability deferral. |

---

Documentation: [index](docs/index.md) · [sprint journals](docs/journal/index.md) · [ADRs](docs/adr/index.md)
