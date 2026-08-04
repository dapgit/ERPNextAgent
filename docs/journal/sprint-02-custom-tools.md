---
title: Sprint 2 Journal — Custom Tools
status: completed
audience: contributors
last_reviewed: 2026-08-04
---

# Sprint 2 Journal — Custom Tools

## Goal

Learn tool registration and expose company and customer information to the agent.

## Delivered scope

- Company and customer information tools.
- Tool registration and model-to-tool interaction.
- A mock customer dataset.

## Decisions and architecture

- [ADR 0002 — Thin Tools](../adr/0002-thin-tools.md)
- [Tools execution](../architecture/tools-execution.md)

## Lessons

Tool metadata is part of the interface contract. A tool should translate agent-facing input into service work, rather than becoming a second business layer.

## Verification evidence

The Sprint 2 changelog records both tools, registration, mock data, and the related learning outcomes.

## Deferred work

The interactive CLI arrived in Sprint 3; service/repository separation arrived in Sprint 4.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created retrospective journal from existing project records. |

---

Previous: [Sprint 1](sprint-01-environment-and-first-agent.md) · Next: [Sprint 3](sprint-03-interactive-application.md) · [Journal index](index.md)
