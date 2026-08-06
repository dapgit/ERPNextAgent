---
title: ERPNext Handbook — Integration Roadmap
status: in-progress
audience: contributors
last_reviewed: 2026-08-06
---

# Integration Roadmap

## Sprint 5

Completed: a bounded HTTP client, environment-backed token configuration, typed error handling, and a read-only Company repository mapping. Remaining: controlled live-query evidence and any additional entity migration.

## Subsequent increments

Add more read capabilities only after mapping and authorization rules are clear. Consider write operations only with explicit confirmation behavior, idempotency handling, audit records, and integration tests. Add resilience, monitoring, and performance work once real operational evidence exists.

## Decision gates

Each increment needs an approved endpoint/permission contract, an ADR when the architecture changes, unit tests for mapping and failures, and an updated sprint journal. No planned capability is considered delivered merely because it appears in a roadmap.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added integration sequencing and decision gates. |
| 2026-08-06 | Marked the Company REST foundation complete and retained remaining work as planned. |

---

Previous: [Overview](overview.md) · Next: [Future integration](future-integration.md)
