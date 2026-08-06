---
title: ADR 0009 — ERPNext REST First, MCP Later
status: accepted
audience: contributors
last_reviewed: 2026-08-06
---

# ADR 0009 — ERPNext REST First, MCP Later

## Status

Accepted in Sprint 5.1.

## Context

ERPNext can be integrated directly through its REST API or through an MCP server. The project needs a controllable first integration path that teaches and validates ERPNext authentication, endpoints, response mapping, and failure semantics without coupling the application to a third-party tool surface.

## Decision

Use direct ERPNext REST as the first transport. Preserve the repository abstraction so a future MCP-backed implementation can satisfy the same application capability. MCP is not installed, configured, or used by the current runtime.

## Rationale

- Direct REST keeps endpoint and error behavior under project control.
- It provides the clearest learning and debugging path for the initial ERPNext integration.
- Repository contracts protect tools and services from later transport changes.
- MCP can be evaluated after a stable REST baseline exists, with a meaningful comparison of operational trade-offs.

## Consequences

- Sprint 5 implements `ERPNextRESTClient` and a REST-backed Company repository.
- Any future MCP client/repository must not force changes to Tool or Service contracts.
- The project must avoid presenting MCP support as delivered until an implementation and verification evidence exist.

## Related records

- [ERPNext REST integration architecture](../architecture/future-erpnext.md)
- [Repository abstraction ADR](0006-repository-abstraction.md)
- [Sprint 5 journal](../journal/sprint-05-erpnext-rest-foundation.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-06 | Recorded the REST-first integration decision and MCP deferral. |

---

Previous: [ADR 0008](0008-client-layer.md) · Back to the [ADR index](index.md) · Next: [ADR 0010](0010-observability-deferred-to-sprint-6.md)
