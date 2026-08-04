---
title: Development Handbook — Branching Strategy
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Branching Strategy

Use a short-lived branch for one coherent change. Prefer descriptive names such as `feature/erpnext-client`, `refactor/repository-layer`, or `docs/sprint-05`. Keep documentation changes with the implementation they describe.

Before merging, rebase or otherwise reconcile safely with the target branch, review the diff for unrelated edits, and ensure the change’s tests and documentation evidence are included.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added branching guidance. |

---

Previous: [Coding standards](coding-standards.md) · Next: [Review process](review-process.md)
