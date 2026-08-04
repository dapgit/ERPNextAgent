---
title: Antigravity SDK Handbook — Triggers
status: planned
audience: contributors
last_reviewed: 2026-08-04
---

# Triggers

Automated triggers are not implemented. A future trigger must name its event source, input schema, authority, idempotency behavior, audit trail, and operator-visible failure path before it invokes any business operation.

Do not treat a model instruction as authorization to run background ERP actions. Event handling belongs behind the same service and repository boundaries used by interactive tools.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added planned-trigger safety criteria. |

---

Previous: [Hooks](07-hooks.md) · Next: [MCP](09-mcp.md)
