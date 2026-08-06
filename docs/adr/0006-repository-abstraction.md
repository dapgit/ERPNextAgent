---
title: ADR 0006 — Repository Abstraction
status: accepted
audience: contributors
last_reviewed: 2026-08-06
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

## Implementation update (Sprint 5.1–5.2)

The Company contract is now explicit: `CompanyRepository` has mock and REST-backed implementations. `ERPNextCompanyRepository` accepts an optional REST client through its constructor, maps ERPNext JSON into `Company`, and leaves transport work to the client layer. The repository choice currently occurs once in `company_repository.py` based on `ERPNEXT_URL`.

This validates the decision for Company: the Company Service and Tool keep their existing contract while the data source changes. Customer has not yet been migrated and remains mock-backed.

## Future Work

Extend concrete contracts and mapping rules to other entities, add controlled integration-test fixtures, and introduce a central factory only when multiple repository selections make it worthwhile.

## Related records

- [Repository layer](../architecture/repository-layer.md)
- [ERPNext REST integration architecture](../architecture/future-erpnext.md)
- [Sprint 4 journal](../journal/sprint-04-repository-pattern.md)
- [Sprint 5 journal](../journal/sprint-05-erpnext-rest-foundation.md)
- [Client layer ADR](0008-client-layer.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Recorded the repository-abstraction decision evidenced in Sprint 4. |
| 2026-08-06 | Recorded the implemented Company contract and REST adapter evidence. |

---

Previous: [ADR 0005](0005-documentation-first-governance.md) · Back to the [ADR index](index.md) · Next: [ADR 0007](0007-domain-models.md)
