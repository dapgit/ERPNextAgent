---
title: Antigravity SDK Handbook — Conversations
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Conversations

The current CLI supports an interactive sequence of requests within one running agent session. That is session continuity, not durable customer memory. Do not claim that context persists across restarts until a storage, privacy, retention, and deletion design exists.

When a future conversation feature is introduced, define what context is kept, who can access it, how it is bounded, and how business-sensitive data is redacted before giving it to the runtime.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added conversation and memory boundary guidance. |

---

Previous: [Tools](04-tools.md) · Next: [Policies](06-policies.md)
