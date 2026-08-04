---
title: Antigravity SDK Handbook — Best Practices
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Best Practices

- Keep the agent responsible for intent and response generation, not domain policy.
- Make tools small, accurately described, and deterministic where possible.
- Validate installed SDK APIs before relying on version-sensitive behavior.
- Keep secrets and sensitive ERP data out of prompts and logs.
- Test services independently; use agent-level tests for representative integration paths.
- Label unimplemented extensions as planned and document adoption decisions before building them.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added SDK best-practice checklist. |

---

Previous: [MCP](09-mcp.md) · Back to the [SDK handbook](handbook.md)
