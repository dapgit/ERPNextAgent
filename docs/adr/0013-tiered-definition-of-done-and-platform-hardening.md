---
title: ADR 0013 — Tiered Definition of Done and Platform Hardening Before Sprint 7
status: accepted
audience: contributors
last_reviewed: 2026-08-07
---

# ADR 0013 — Tiered Definition of Done and Platform Hardening Before Sprint 7

## Status

Accepted. Governs Sprint 6.4 onward.

## Context

Sprints 6.1 and 6.3 were each completed under an informal but consistent pattern: architecture decision (recorded as an ADR), implementation with tests, documentation updates (CHANGELOG, checkpoint, roadmap), and live verification before commit. It worked well but was never written down as a rule.

A proposal was raised to formalize this as a project-wide Definition of Done with four parallel deliverables — Architecture, Implementation, Documentation, Validation — mandatory for every future sprint, alongside reframing the project's primary objective from "learning and reference implementation" to "enterprise-class application first." It also proposed restructuring Sprint 6.4/6.5 so each sprint ships its own documentation, rather than 6.5 becoming "write the docs for Sprint 6" after the fact.

Reviewing this against the actual project surfaced two problems worth resolving before adopting it as-is:

1. **"Enterprise-class" describes a direction, not the current state.** Concrete gaps remain: no auth/authz on the assistant itself, secrets held in a plaintext `.env` with no rotation policy, no CI pipeline, no fail-fast startup configuration validation, no retry/backoff for transient failures, no security review performed. The clearest existing evidence for the resilience gap specifically: the Gemini 429 quota-exhaustion crash that opened this project's very first debugging session took the whole process down with an unhandled error — not a hypothetical failure mode, one already observed.
2. **An unconditional full four-part DoD risks recreating the same debt it's meant to prevent, in a different shape.** The checkpoint's own existing target for sprint journals is 10–15 pages, book-quality, per sprint. Mandating that — plus an ADR, diagram updates, and a separate documentation review — for every future sprint regardless of size means small maintenance work (a dependency bump, a doc correction) either gets the same ceremony as an architecture change, or the rule quietly gets skipped under time pressure a few sprints from now. Either outcome undermines the rule.

## Decision

### 1. Adopt a tiered Definition of Done

**Tier 1 — architecture-affecting sprints** (new capability, cross-cutting concern, interface or dependency change): the full four-part DoD applies —

- *Architecture*: design decisions, an ADR when a real decision was made, dependency/interface changes recorded.
- *Implementation*: production-quality code, tests, error handling, security considerations, observability where relevant.
- *Documentation*: affected existing documentation updated, that sprint's journal entry completed, diagrams/handbook updates where relevant, decisions and lessons recorded.
- *Validation*: unit/integration tests, end-to-end verification where applicable, code/architecture review, documentation review.

**Tier 2 — maintenance/fix work** (doc corrections, dependency bumps, small non-architectural fixes): code and tests where applicable, plus one CHANGELOG/checkpoint line. No mandatory ADR, journal entry, or handbook chapter.

Tier assignment is made explicitly at planning time — the same propose → react → implement pattern already used for every sprint in this project — not inferred after the fact or defaulted to whichever tier is more convenient.

### 2. State the enterprise-class objective as a goal, with its gaps enumerated

The checkpoint's Executive Summary now states that ERPNextAgent's primary objective is to become an enterprise-class application, with reference/learning value as a secondary objective — reordered from the previous framing, not replaced by it. The checkpoint explicitly lists the concrete gaps still open (Decision 3) rather than asserting the label is already earned, so a future session reading it cold does not overestimate what's safe to rely on.

### 3. Insert Sprint 6.6 — Platform Hardening — before Sprint 7

Sequencing stays Sprint 6.4 (Metrics) → 6.5 (documentation system quality) as already planned. A new Sprint 6.6 is inserted after 6.5 and before Sprint 7 (ERP Business Operations: Inventory, Sales Orders, Purchase Orders), scoped to:

- Retry/backoff for transient ERPNext failures, and graceful handling of upstream rate-limit errors (the Gemini 429 case already encountered) instead of an unhandled crash.
- Fail-fast configuration validation at startup — missing required environment variables surfaced immediately, not on the first repository call several layers deep.
- A CI pipeline running the test suite on every push.
- A written secrets-handling policy (least-privilege ERPNext API user, rotation expectations). Actual secrets-manager/vault integration is explicitly deferred until a real deployment target exists, to avoid building infrastructure for an application that isn't deployed anywhere yet.
- A security review pass using this environment's `security-review` capability, against the current branch.
- Auth/authz on the assistant itself is explicitly deferred, not silently absent. It is captured here as a deliberate gap to revisit alongside Sprint 9's MCP/multi-agent work, once there is an actual multi-user surface to protect.

Sprint 7 does not begin until Sprint 6.6 is complete. Sprint 6.6 is itself a Tier 1 sprint under Decision 1.

## Rationale

- Tiering the DoD instead of applying it unconditionally keeps the rule sustainable. It concentrates full rigor where it earns its cost (Sprint 6.4 clearly qualifies — metrics touch every layer) without making every small change carry the weight of an architecture decision, which is what would eventually cause the rule to be quietly abandoned.
- Stating the enterprise objective honestly, gaps included, keeps the checkpoint trustworthy as a resumption document. Its stated purpose is to let a future session or engineer resume "with minimal context loss" — that fails if it overstates production-readiness.
- Hardening before feature expansion mirrors a pattern that already worked in this project: Sprint 5.6–5.7 cleaned up mock repositories and error handling before Item lookup shipped further, rather than layering more capability on unresolved debt.
- Scoping Sprint 6.6 now, with a concrete list rather than a vague "harden the platform" intention, makes it something that can actually be planned, reviewed, and closed the same way every other sprint in this project has been — rather than an aspiration that never gets scheduled because it never became a numbered sprint.

## Consequences

- `docs/checkpoints/PROJECT_CHECKPOINT.md` is updated: Executive Summary reframed with the gap list, "Lessons Learned" gains a note on DoD tiering, a Sprint 6.6 entry is added under "Future Roadmap," and "Instructions for Future Sessions" references this ADR and the Sprint 7 gate.
- `docs/project-roadmap.md` is updated: the Sprint 6 section notes 6.6 and the Sprint 7 gate; the roadmap table's Sprint 6 status reflects 6.1/6.3 complete, 6.4–6.6 remaining.
- Every future sprint states its DoD tier at planning time before implementation begins.
- Sprint 6.4 (Metrics) proceeds under the full Tier 1 DoD, as already planned before this ADR.
- No code changes result from this ADR directly — it is a governance decision, not an implementation one.

## Related records

- [ADR 0010 — Defer OpenTelemetry to Sprint 6](0010-observability-deferred-to-sprint-6.md)
- [ADR 0011 — Structured Logging and Correlation IDs](0011-structured-logging-and-correlation-ids.md)
- [ADR 0012 — OpenTelemetry Tracing](0012-opentelemetry-tracing.md)
- [Project checkpoint](../checkpoints/PROJECT_CHECKPOINT.md)
- [Project roadmap](../project-roadmap.md)

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-07 | Accepted the tiered Definition of Done and the Sprint 6.6 platform-hardening milestone. |

---

Previous: [ADR 0012](0012-opentelemetry-tracing.md) · Back to the [ADR index](index.md) · Next: [ADR 0014](0014-opentelemetry-metrics.md)
