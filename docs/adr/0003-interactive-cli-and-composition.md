---
title: ADR 0003 — Interactive CLI and Composition
status: accepted
audience: contributors
last_reviewed: 2026-08-04
---

# ADR 0003 — Interactive CLI and Composition

## Status

Accepted.

## Context

Sprint 3 converted a demonstration into an interactive application and separated configuration, prompts, assistant setup, and the application entry point.

## Problem

The project needed a repeatable application lifecycle without a single entry point owning settings, prompt policy, agent construction, and business behavior.

## Options

1. Keep a single-file CLI.
2. Recreate an agent for each message.
3. Use a composition root and a long-lived session agent.

## Decision

Use `app.py` as the composition and conversation-loop boundary. Keep configuration, prompt management, and agent construction in dedicated modules.

## Rationale

Dedicated startup concerns make the lifecycle inspectable and allow future interfaces to reuse the same composition and services.

## Consequences

- Startup is easier to inspect and change.
- The agent is created once per application run, as documented.
- Later interfaces can reuse services and agent composition rather than copying business logic.

## Alternatives considered

A single-file CLI was rejected because it combines settings, runtime setup, and interaction flow. Recreating the agent for each user message was rejected because it complicates lifecycle management.

## Future Work

Define an interface-adapter strategy and session/memory policy before adding a web UI, chat integration, or durable conversation context.

## Related records

- [Sprint 3 journal](../journal/sprint-03-interactive-application.md)
- [Agent lifecycle](../architecture/agent-lifecycle.md)
- [Development handbook](../development/development-handbook.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Created from Sprint 3 changelog and architecture records. |

---

Back to the [ADR index](index.md).
