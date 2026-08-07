---
title: Documentation Index
status: active
audience: contributors
last_reviewed: 2026-08-06
---

# Documentation Index

This is the entry point for ERPNextAgent documentation. Sprint 5 is in progress: milestones 5.1–5.6 are complete and recorded; remaining error-handling scope is the active work before Sprint 6.

## Start here

- [Project vision](project-vision.md) and [roadmap](project-roadmap.md)
- [Learning path](learning-path.md)
- [Architecture overview](architecture/overview.md)
- [Development handbook](development/development-handbook.md)

## Architecture

- [Layered architecture](architecture/layered-architecture.md)
- [Agent lifecycle](architecture/agent-lifecycle.md)
- [Tools execution](architecture/tools-execution.md)
- [Service layer](architecture/services-layer.md)
- [Repository layer](architecture/repository-layer.md)
- [ERPNext REST integration architecture](architecture/future-erpnext.md)

## Decision and delivery records

- [ADR index](adr/index.md)
- [Sprint journal index](journal/index.md)
- [Changelog](../CHANGELOG.md)

## Integration handbooks

- [Antigravity SDK handbook](antigravity-sdk/handbook.md)
- [ERPNext handbook](erpnext/handbook.md)
- [Development handbook](development/development-handbook.md)

## Documentation governance

- [Documentation style guide](documentation-style-guide.md)
- [Glossary](glossary.md)
- [Documentation audit](documentation-audit-2026-08-04.md)

## Documentation map

```mermaid
flowchart TD
  I[Documentation index] --> V[Vision and roadmap]
  I --> A[Architecture]
  I --> D[ADRs]
  I --> J[Sprint journals]
  I --> H[Handbooks]
  D --> A
  J --> D
  H --> A
```

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created documentation navigation and governance entry point. |
| 2026-08-06 | Added Sprint 5 implementation navigation and updated integration wording. |

---

Next: [Project vision](project-vision.md) · [Style guide](documentation-style-guide.md)
