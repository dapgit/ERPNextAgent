---
title: ERPNext Handbook — Overview
status: in-progress
audience: contributors
last_reviewed: 2026-08-06
---

# ERPNext Integration Overview

ERPNext is the system of record being introduced into ERPNextAgent. Sprint 5.1–5.2 connect the Company capability through the REST API while Customer remains mock-backed.

## Boundary

ERPNext-specific endpoints, authentication, payloads, and permissions belong only in a planned client and repository adapter. Tools and services speak in capabilities and domain models, not DocType payloads.

## First integration scope

The implemented path is read-only Company lookup using `ERPNextRESTClient` and `ERPNextCompanyRepository`. It validates configuration, mapping, and typed failures before write operations or broader entity migration are considered.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added ERPNext handbook overview. |
| 2026-08-06 | Recorded the implemented Company REST path and remaining Customer migration. |

---

Back to the [ERPNext handbook](handbook.md) · Next: [Integration roadmap](roadmap.md)
