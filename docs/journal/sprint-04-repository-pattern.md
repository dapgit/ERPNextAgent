---
title: Sprint 4 Journal — Repository Pattern
status: completed
audience: contributors
last_reviewed: 2026-08-04
---

# Sprint 4 Journal — Repository Pattern

## Goal

Separate business logic from data access and prepare the application for an ERPNext data source.

## Delivered scope

- Customer and company repositories backed by mock data.
- Customer domain model and repository abstraction.
- Service-to-repository delegation and thin tools.

## Decisions and architecture

- [ADR 0004 — Layered Service and Repository Design](../adr/0004-layered-service-repository-design.md)
- [Repository layer](../architecture/repository-layer.md)
- [Service layer](../architecture/services-layer.md)

## Lessons

The repository boundary lets an external API adapter evolve without forcing services and tools to learn transport details.

## Verification evidence

The changelog records the repository layer, domain model, service/repository communication, and removal of tool-layer business logic.

## Deferred work

ERPNext REST integration, authentication, error handling, logging, and automated tests are planned for future work; they are not represented as completed scope.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created retrospective journal from existing project records. |

---

Previous: [Sprint 3](sprint-03-interactive-application.md) · Next: [Roadmap](../project-roadmap.md) · [Journal index](index.md)
