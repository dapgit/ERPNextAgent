---
title: ADR 0006 — Repository Abstraction
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0006 — Repository Abstraction

## Status

Accepted.

## Context

Sprint 4 needed a stable way to use mock data immediately while preparing for a future ERPNext data source.

## Problem

Direct data access from tools or services would couple application behavior to the current mock representation and require a broad rewrite for REST integration.

## Options

1. Let tools read the data source directly.
2. Let services make transport calls directly.
3. Introduce repositories as the exclusive data-access boundary.

## Decision

Use repositories to retrieve and persist data, map external data into domain models, and present domain-level errors to services.

## Rationale

This isolates storage and transport details from business rules and AI-facing tools. Mock and REST-backed implementations can share the same service-facing contract.

## Consequences

- Services do not contain HTTP or mock-data details.
- Sprint 5 can replace repository implementations incrementally.
- Repository mapping and failure behavior require dedicated tests.

## Future Work

Define the concrete ERPNext repository contracts, mapping rules, authentication behavior, and integration-test fixtures before enabling live requests.

## Related records

- [Repository layer](../architecture/repository-layer.md)
- [Future ERPNext architecture](../architecture/future-erpnext.md)
- [Sprint 4 journal](../journal/sprint-04-repository-pattern.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Recorded the repository-abstraction decision evidenced in Sprint 4. |

---

Previous: [ADR 0005](0005-documentation-first-governance.md) · Back to the [ADR index](index.md) · Next: [ADR 0007](0007-domain-models.md)
