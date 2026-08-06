---
title: ADR 0008 — Client Layer
status: accepted
audience: contributors
last_reviewed: 2026-08-06
---

# ADR 0008 — Client Layer

## Status

Accepted in Sprint 5.1.

## Context

The first ERPNext REST integration needed HTTP behavior—session reuse, authentication headers, URL construction, timeouts, JSON parsing, and HTTP failure translation. Putting that behavior into entity repositories would conflate transport with domain mapping and duplicate it as more repositories migrate.

## Decision

Introduce a `clients/` layer. `ERPNextRESTClient` owns generic ERPNext REST transport. Repositories use it to retrieve entity-specific payloads and map them into domain models.

## Consequences

- `ERPNextCompanyRepository` has no direct `requests` dependency and can receive a fake client in unit tests.
- The client has no Company or Customer knowledge, avoiding a growing all-purpose business client.
- Future retry, timeout policy, and OpenTelemetry instrumentation have a centralized outbound-call boundary.
- The current client supports GET, `get_doc`, and `get_list`; write operations require deliberate design later.

## Related records

- [Architecture overview](../architecture/overview.md)
- [Repository layer](../architecture/repository-layer.md)
- [Sprint 5 journal](../journal/sprint-05-erpnext-rest-foundation.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-06 | Recorded introduction of the client layer. |

---

Previous: [ADR 0007](0007-domain-models.md) · Back to the [ADR index](index.md) · Next: [ADR 0009](0009-rest-first-mcp-later.md)
