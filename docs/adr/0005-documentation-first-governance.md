---
title: ADR 0005 — Documentation-First Governance
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0005 — Documentation-First Governance

## Status

Accepted.

## Context

The project is both a reference implementation and a learning resource. The previous structure named journals, ADRs, and handbooks but did not include the corresponding navigation or document set.

## Problem

Without a documented standard and traceable records, readers cannot distinguish delivered behavior from plans or understand why the design evolved.

## Options

1. Maintain unstructured project notes.
2. Produce documentation after implementation when convenient.
3. Govern documentation as part of delivery with canonical indexes and review criteria.

## Decision

Maintain a documentation index, style guide, ADR index, sprint-journal index, focused handbooks, and an auditable revision history. A sprint is documented as complete only when implementation evidence and delivery records agree.

## Rationale

The project’s learning and reference goals require readers to find the canonical explanation, decision, and delivery evidence for each significant change.

## Consequences

- Decisions and delivery evidence become discoverable.
- Planned work remains visibly separate from completed work.
- Documentation changes are part of each future sprint's definition of done.

## Alternatives considered

An unstructured set of project notes was rejected because it makes status, decision history, and learning material hard to find.

## Future Work

Continue expanding records to the agreed depth, perform a closure audit at each sprint end, and reopen documentation approval whenever evidence and claimed scope diverge.

## Related records

- [Style guide](../documentation-style-guide.md)
- [Documentation audit](../documentation-audit-2026-08-04.md)
- [Contributing guide](../../CONTRIBUTING.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Established documentation governance. |

---

Back to the [ADR index](index.md).
