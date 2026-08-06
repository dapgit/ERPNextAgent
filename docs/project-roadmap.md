---
title: Project Roadmap
status: active
audience: contributors
last_reviewed: 2026-08-06
---

# Project Roadmap

## Overview

ERPNextAgent is being developed incrementally using a sprint-based approach. Each sprint introduces one major architectural or functional concept while maintaining a production-quality codebase and comprehensive documentation.

---

# Roadmap

| Sprint | Title | Status |
|---------|-------------------------------|----------|
| Sprint 1 | Environment & First Agent | ✅ Complete |
| Sprint 2 | Custom Tools | ✅ Complete |
| Sprint 3 | Interactive Application | ✅ Complete |
| Sprint 4 | Repository Pattern | ✅ Complete |
| Sprint 5 | ERPNext REST Integration | 🚧 In progress — 5.1 and 5.2 complete |
| Sprint 6 | Observability | ⏳ Planned |
| Sprint 7 | ERP Business Operations | ⏳ Planned |
| Sprint 8 | Memory & Context | ⏳ Planned |
| Sprint 9 | Multi-Agent Architecture | ⏳ Planned |
| Sprint 10 | Production Readiness | ⏳ Planned |

---

# Sprint Details

## Sprint 1 – Environment & First Agent

### Objectives

- Install Python environment
- Install Antigravity SDK
- Configure Gemini API
- Create first AI Agent

### Deliverables

- Working Antigravity Agent
- Initial project structure

---

## Sprint 2 – Custom Tools

### Objectives

- Learn Tool registration
- Build Company Tool
- Build Customer Tool

### Deliverables

- Company Information Tool
- Customer Information Tool

---

## Sprint 3 – Interactive Application

### Objectives

- Convert demo into an application
- Separate configuration
- Introduce layered startup

### Deliverables

- app.py orchestration
- assistant.py
- config.py
- settings.py
- prompts.py
- Interactive CLI

---

## Sprint 4 – Repository Pattern

### Objectives

- Separate business logic
- Introduce Repository Layer
- Create Domain Models

### Deliverables

- Customer Repository
- Company Repository
- Customer dataclass
- Thin Tools
- Service Layer

---

## Sprint 5 – ERPNext Integration

### Objectives

- Establish a reusable REST integration boundary
- Connect the Company repository to ERPNext REST API
- Keep upper-layer contracts stable

Completed in 5.1 and 5.2:

- `clients/ERPNextRESTClient` with session reuse, token authentication, URL construction, JSON parsing, and typed integration errors.
- Environment-based ERPNext configuration.
- `CompanyRepository` contract with mock and REST implementations.
- JSON-to-`Company` mapping and unit tests using an injected fake client.

Remaining Sprint 5 scope:

- Extend REST-backed repositories beyond Company.
- Perform controlled live integration verification and document the evidence.
- Add only the resilience features justified by that evidence.

## Sprint 6 – Observability

OpenTelemetry was evaluated during Sprint 5 and deferred so the first REST path can stabilize without cross-cutting instrumentation. Sprint 6 will define the observability package, tracing configuration, span boundaries, safe attributes, and exporter strategy. Python logging remains appropriate for startup and exceptional diagnostics.

---

## Long-Term Vision

By the end of the project, ERPNextAgent will provide:

- Customer Management
- Supplier Management
- Inventory Operations
- Sales Orders
- Purchase Orders
- Financial Information
- Context-aware AI Assistant
- Production-quality Architecture

## Documentation and delivery status

Completed-sprint evidence is maintained in the [sprint journals](journal/index.md) and [ADRs](adr/index.md). Planned sprints must remain planned until implementation and verification evidence are recorded.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata and links to the documentation delivery records. |
| 2026-08-06 | Marked Sprint 5.1–5.2 complete and added the Sprint 6 observability decision. |

---

Back to the [documentation index](index.md) · Next: [Sprint journals](journal/index.md)
