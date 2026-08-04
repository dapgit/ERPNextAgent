---
title: Development Handbook — Coding Standards
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Coding Standards

Use clear names, type hints for public contracts, small cohesive functions, and project-owned domain models at service and repository boundaries. Keep imports explicit and use docstrings where an API’s behavior needs explanation.

Layer placement is a quality rule: agents orchestrate, tools translate model-facing inputs/outputs, services own business rules, and repositories own source access and mapping. Do not bypass a layer for convenience.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added coding-standard guide. |

---

Back to the [development handbook](development-handbook.md) · Next: [Branching strategy](branching-strategy.md)
