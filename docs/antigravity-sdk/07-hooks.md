---
title: Antigravity SDK Handbook — Hooks
status: planned
audience: contributors
last_reviewed: 2026-08-04
---

# Hooks

Hooks are not implemented in ERPNextAgent. If supported by the installed SDK and adopted later, they may provide lifecycle observation or controlled interception points.

Before introducing hooks, document their execution order, failure behavior, performance cost, data exposure, and test strategy. Hooks must not bypass service authorization or repository error handling.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added planned-hook evaluation criteria. |

---

Previous: [Policies](06-policies.md) · Next: [Triggers](08-triggers.md)
