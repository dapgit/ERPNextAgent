---
title: Development Handbook — Review Process
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Review Process

Review changes for correctness, layer ownership, error paths, security impact, and documentation accuracy. A reviewer should be able to trace a feature from its user-facing tool through service and repository behavior without discovering hidden business logic or transport calls.

For architecture changes, require an ADR or explain why the existing record remains sufficient. Reject a completion claim that lacks runnable verification evidence or labels planned behavior as delivered.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added review-process guide. |

---

Previous: [Branching strategy](branching-strategy.md) · Next: [Definition of done](definition-of-done.md)
