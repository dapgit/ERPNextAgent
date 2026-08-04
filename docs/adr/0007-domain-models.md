---
title: ADR 0007 — Domain Models at Layer Boundaries
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0007 — Domain Models at Layer Boundaries

## Status

Accepted.

## Context

Early mock data was naturally represented as dictionaries. Sprint 4 introduced services and repositories, which need clearer contracts as the application grows.

## Problem

Passing raw dictionaries across layers exposes source-specific field names, permits inconsistent shapes, and makes validation and tests harder to understand.

## Options

1. Continue returning raw dictionaries everywhere.
2. Return ERPNext response objects directly.
3. Map repository results to project-owned domain models.

## Decision

Use project-owned domain models, beginning with `Customer`, at repository and service boundaries.

## Rationale

Domain models provide explicit, typed application contracts without coupling business behavior to the current mock-data shape or a future ERPNext payload.

## Consequences

- Repositories must map source data deliberately.
- Services and tests receive predictable entities.
- New fields require intentional model evolution and compatibility review.

## Future Work

Define models for the next business entities only when their service operations are introduced, and document validation and mapping rules with the relevant integration work.

## Related records

- [Repository layer](../architecture/repository-layer.md)
- [Service layer](../architecture/services-layer.md)
- [Sprint 4 journal](../journal/sprint-04-repository-pattern.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Recorded the domain-model boundary introduced in Sprint 4. |

---

Previous: [ADR 0006](0006-repository-abstraction.md) · Back to the [ADR index](index.md)
