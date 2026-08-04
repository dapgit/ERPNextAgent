---
title: Antigravity SDK Handbook — Tools
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Tools

Tools are the model-facing contracts for application capabilities. A tool should have a precise purpose, a small input shape, and a stable user-safe result. The model may select it; the tool must not become the owner of business logic.

In this project, a tool delegates to a service. Validate interface-level requirements at the tool boundary; put workflows, authorization rules, and domain validation in services; keep data access in repositories. See [tool execution](../architecture/tools-execution.md) and [ADR 0002](../adr/0002-thin-tools.md).

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added tool-design guidance. |

---

Previous: [Agents](03-agents.md) · Next: [Conversations](05-conversations.md)
