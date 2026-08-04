---
title: ADR 0004 — Layered Service and Repository Design
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0004 — Layered Service and Repository Design

## Status

Accepted.

## Context

Sprint 4 needed a design that separates tools, business rules, mock data, and future ERPNext communication.

## Problem

Data access and business policy would otherwise be coupled to the current mock source and difficult to replace with ERPNext safely.

## Options

1. Let tools or services access data sources directly.
2. Return raw source payloads across layers.
3. Use tools, services, repositories, and domain models with one-way dependencies.

## Decision

Use a layered flow: Tool → Service → Repository → data source. Repositories return domain models rather than raw dictionaries. Current repositories use mock data; a future ERPNext adapter belongs in the repository layer.

## Rationale

The structure isolates transport details while preserving a testable location for business rules and a stable contract for tools.

## Consequences

- ERPNext transport concerns remain isolated.
- Services and tools can be tested with substitute repositories.
- The planned REST integration needs an adapter, authentication design, error model, and tests before it can be considered delivered.

## Alternatives considered

Direct ERP calls from services or tools were rejected because they couple business behaviour to transport. Returning raw API payloads was rejected because external schemas would leak across the application.

## Future Work

Implement the ERPNext adapter incrementally with an approved authentication design, failure model, mapping tests, and controlled integration evidence.

## Related records

- [Sprint 4 journal](../journal/sprint-04-repository-pattern.md)
- [Repository layer](../architecture/repository-layer.md)
- [ERPNext handbook](../erpnext/handbook.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created from Sprint 4 changelog and architecture records. |

---

Back to the [ADR index](index.md).
