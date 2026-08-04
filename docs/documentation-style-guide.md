---
title: Documentation Style Guide
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Documentation Style Guide

This guide is the documentation contract for ERPNextAgent. It applies to new documents and to existing documents whenever they are materially revised.

## Required document shape

Each maintained document begins with YAML metadata containing `title`, `status`, `audience`, and `last_reviewed`. Use one H1, concise H2 sections, relative Markdown links, and a revision-history table. End significant documents with contextual navigation.

## Naming and locations

| Content | Location | Naming |
| --- | --- | --- |
| Architecture decisions | `docs/adr/` | `NNNN-short-title.md` |
| Sprint journals | `docs/journal/` | `sprint-NN-title.md` |
| Architecture | `docs/architecture/` | lowercase kebab case |
| Product/integration guides | `docs/<topic>/` | lowercase kebab case |

## Status vocabulary

Use `active`, `accepted`, `superseded`, `completed`, `planned`, or `draft`. Planned documentation must never describe unimplemented behaviour as current behaviour.

## ADR template

Use: Status, Context, Problem, Options, Decision, Rationale, Consequences, Future Work, Related records, Revision history, and navigation. An ADR records a decision; it does not replace implementation documentation.

## Sprint-journal template

Use: Goal, Delivered scope, Architecture/decision links, Lessons, Verification evidence, Deferred work, Revision history, and navigation. A journal for an incomplete future sprint remains `planned`.

## Diagrams and links

Use Mermaid where a flow, dependency, or lifecycle is clearer than prose. Keep diagrams small and label planned components. Link to the canonical document instead of duplicating material.

## Documentation completion checklist

- Metadata and status are accurate.
- Navigation and relative links resolve.
- ADRs and journals are linked for completed sprints.
- Current, planned, and inferred information are clearly separated.
- Revision history records the change.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Established the project documentation contract. |

---

Back to the [documentation index](index.md).
