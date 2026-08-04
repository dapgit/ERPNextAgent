---
title: Changelog
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Changelog

All notable changes to this project will be documented in this file.

This project follows a sprint-based development approach. Each sprint represents a logical milestone in the evolution of the ERPNext AI Assistant.

---

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

## Sprint 5 (Planned)

- ERPNext REST Client
- Authentication
- Session Management
- Repository implementation using ERPNext REST API
- Error handling
- Logging
- Unit Tests
- Integration Tests

---

# Version History

| Version | Sprint |
|----------|--------|
| 0.1.0 | Sprint 1 |
| 0.2.0 | Sprint 2 |
| 0.3.0 | Sprint 3 |
| 0.4.0 | Sprint 4 |

Future releases will continue following semantic versioning aligned with sprint milestones.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added documentation-system metadata and navigation. |

---

Documentation: [index](docs/index.md) · [sprint journals](docs/journal/index.md) · [ADRs](docs/adr/index.md)
