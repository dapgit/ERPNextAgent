---
title: Antigravity SDK Handbook — Runtime
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Runtime

## Role in ERPNextAgent

The runtime receives a prompt, applies agent configuration, makes registered tools available, and returns a response. Application startup constructs this runtime once for the interactive session; it is not rebuilt for every prompt.

## Operational boundary

Runtime setup may load model configuration, system instructions, and tool registrations. It must not embed ERP credentials, business policies, or raw ERP request logic. Those concerns remain in settings, services, and repositories.

## Upgrade discipline

Check the installed SDK reference before changing runtime APIs. Exercise a representative prompt and tool invocation, keep secrets out of logs, and record materially changed behavior in architecture documentation.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added runtime guidance. |

---

Previous: [Introduction](01-introduction.md) · Next: [Agents](03-agents.md)
