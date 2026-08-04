---
title: ADR 0001 — Antigravity Agent Runtime
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0001 — Antigravity Agent Runtime

## Status

Accepted.

## Context

The project needs an agent runtime to accept natural-language requests, select registered tools, and produce responses using Gemini. Sprint 1 established this runtime.

## Problem

The project needed a runtime that supports agent-led tool use without mixing model setup into business and data-access code.

## Options

1. Use direct model calls.
2. Distribute agent setup through the application.
3. Use an Antigravity runtime behind the application/agent boundary.

## Decision

Use Google's Antigravity SDK as the agent runtime and keep its lifecycle behind the application/agent boundary.

## Rationale

The chosen boundary teaches the project’s agent-and-tool lifecycle while allowing the ERP implementation to evolve independently.

## Consequences

- Agent-specific concerns remain outside services and repositories.
- Tool schemas and runtime APIs must be checked against the installed SDK version.
- The application can evolve its ERP implementation without making the runtime responsible for business rules.

## Alternatives considered

Direct model calls were not selected because the project explicitly teaches an agent-and-tool lifecycle. Embedding agent setup throughout the application was not selected because it would blur startup responsibilities.

## Future Work

Revalidate runtime APIs against the installed SDK during upgrades and document future memory, streaming, or extension decisions before adoption.

## Related records

- [Sprint 1 journal](../journal/sprint-01-environment-and-first-agent.md)
- [Agent lifecycle](../architecture/agent-lifecycle.md)
- [Antigravity SDK handbook](../antigravity-sdk/handbook.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created from the Sprint 1 changelog and architecture records. |

---

Back to the [ADR index](index.md).
