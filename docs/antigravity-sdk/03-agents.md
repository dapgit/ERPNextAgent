---
title: Antigravity SDK Handbook — Agents
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Agents

An agent is the application’s AI orchestration boundary. It interprets a user request, selects an available capability when appropriate, and turns results into a response. It is not a service layer and must not be given ERP-specific business rules.

ERPNextAgent creates the agent at startup so a CLI session can handle multiple requests. The agent’s inputs should be limited to configuration, prompt policy, and carefully described tools. See the [agent lifecycle](../architecture/agent-lifecycle.md).

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added agent responsibilities and lifecycle guidance. |

---

Previous: [Runtime](02-runtime.md) · Next: [Tools](04-tools.md)
