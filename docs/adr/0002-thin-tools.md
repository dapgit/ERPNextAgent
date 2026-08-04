---
title: ADR 0002 — Thin Tools
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0002 — Thin Tools

## Status

Accepted.

## Context

Sprint 2 introduced company and customer tools. Tools must be understandable to the model while the business behaviour remains testable and independent of the agent runtime.

## Problem

Without an explicit boundary, tools could accumulate business workflows and data access simply because they are easy to call from the agent.

## Options

1. Put workflows in tools.
2. Let tools call repositories directly.
3. Make tools adapters that delegate to services.

## Decision

Tools accept and lightly validate model-facing input, delegate work to services, and format a response. They do not own business rules or data access.

## Rationale

This maintains model-facing capability contracts without coupling domain behavior to a particular SDK interface.

## Consequences

- Tool functions remain small and easy to register.
- Services are reusable outside the agent interface.
- New tools require clear input/output descriptions and service-level tests.

## Alternatives considered

Putting workflows in tools was rejected because it couples business rules to the SDK. Calling repositories directly from tools was rejected because it bypasses service-level validation and coordination.

## Future Work

Document input/output contracts for each new tool and add representative tool-integration tests while keeping business-rule tests at the service layer.

## Related records

- [Sprint 2 journal](../journal/sprint-02-custom-tools.md)
- [Tools execution](../architecture/tools-execution.md)
- [ADR 0004](0004-layered-service-repository-design.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created from Sprint 2 and contribution guidance. |

---

Back to the [ADR index](index.md).
