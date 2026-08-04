---
title: ERPNext Handbook — Overview
status: planned
audience: contributors
last_reviewed: 2026-08-04
---

# ERPNext Integration Overview

ERPNext is the future system of record for ERPNextAgent. Sprint 4 deliberately leaves it outside the running application: current repositories use mock data so application behavior and integration behavior can be developed separately.

## Boundary

ERPNext-specific endpoints, authentication, payloads, and permissions belong only in a planned client and repository adapter. Tools and services speak in capabilities and domain models, not DocType payloads.

## First integration scope

Start with read-only customer and company lookup using a controlled ERPNext environment. This gives the project a small, observable path to validate connectivity, mapping, and safe failures before write operations are considered.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added ERPNext handbook overview. |

---

Back to the [ERPNext handbook](handbook.md) · Next: [Integration roadmap](roadmap.md)
