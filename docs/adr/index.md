---
title: Architecture Decision Records
status: active
audience: contributors
last_reviewed: 2026-08-06
---

# Architecture Decision Records

ADRs capture architectural decisions evidenced through the current implementation. Sprint 5.1 and 5.2 add the client boundary and establish REST as the first transport while retaining MCP as a later option.

| ADR | Decision | Status | Sprint |
| --- | --- | --- | --- |
| [0001](0001-antigravity-agent-runtime.md) | Use Antigravity as the agent runtime | Accepted | 1 |
| [0002](0002-thin-tools.md) | Keep AI tools thin | Accepted | 2 |
| [0003](0003-interactive-cli-and-composition.md) | Use a CLI with separated startup concerns | Accepted | 3 |
| [0004](0004-layered-service-repository-design.md) | Use services, repositories, and domain models | Accepted | 4 |
| [0005](0005-documentation-first-governance.md) | Govern documentation alongside delivery | Accepted | 1–4 |
| [0006](0006-repository-abstraction.md) | Isolate data access behind repositories | Accepted | 4 |
| [0007](0007-domain-models.md) | Use domain models at layer boundaries | Accepted | 4 |
| [0008](0008-client-layer.md) | Introduce an entity-agnostic client layer | Accepted | 5.1 |
| [0009](0009-rest-first-mcp-later.md) | Use ERPNext REST first; defer MCP | Accepted | 5.1 |
| [0010](0010-observability-deferred-to-sprint-6.md) | Defer OpenTelemetry to Sprint 6 | Accepted | 5.2 |
| [0011](0011-structured-logging-and-correlation-ids.md) | Structured logging and `contextvars`-based correlation IDs | Accepted | 6.1 |
| [0012](0012-opentelemetry-tracing.md) | OpenTelemetry tracing, console exporter first | Accepted | 6.3 |
| [0013](0013-tiered-definition-of-done-and-platform-hardening.md) | Tiered Definition of Done; Sprint 6.6 platform hardening before Sprint 7 | Accepted | 6.4 |
| [0014](0014-opentelemetry-metrics.md) | OpenTelemetry metrics: reuse HTTP auto-instrumentation, extend traced()/execute_tool(), explicit cardinality rule | Accepted | 6.4 |

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created ADR index and normalized the documented decision set. |
| 2026-08-06 | Added Sprint 5 integration and observability decisions. |
| 2026-08-07 | Added the Sprint 6.1 structured logging and correlation ID proposal, later accepted. Added the Sprint 6.3 OpenTelemetry tracing proposal. |
| 2026-08-07 | Accepted the tiered Definition of Done and the Sprint 6.6 platform-hardening milestone. |
| 2026-08-07 | Added the Sprint 6.4 metrics proposal. |

---

Back to the [documentation index](../index.md) · Next: [Sprint journals](../journal/index.md)
