---
title: Layered Architecture
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Layered Architecture

## Introduction

ERPNextAgent follows a layered architecture that separates the application into independent logical components.

Each layer has a single responsibility and communicates only with the layer immediately below it.

The purpose of this architecture is to make the application:

- Easier to understand
- Easier to maintain
- Easier to test
- Easier to extend
- Independent of ERPNext implementation details

This architecture evolved over multiple sprints as the project matured from a simple AI demonstration into a production-oriented application.

---

# Why Layered Architecture?

During the early stages of the project, all logic existed inside a single file.

```text
app.py
    │
Everything
```

Although simple, this approach quickly became difficult to maintain.

Problems included:

- Business logic mixed with AI logic.
- Configuration mixed with application startup.
- Tool implementation mixed with data storage.
- Difficult testing.
- Tight coupling between components.

As the application grew, a better architectural approach became necessary.

---

# Architectural Principles

The layered architecture is based on several software engineering principles.

## Single Responsibility Principle (SRP)

Every module should have exactly one responsibility.

Examples:

| Component | Responsibility |
|-----------|----------------|
| app.py | Application startup |
| Agent | AI conversation |
| Tool | AI capability |
| Service | Business rules |
| Repository | Data access |
| Model | Business entity |

---

## Separation of Concerns

Each layer addresses a specific concern.

For example:

The Tool layer understands AI.

The Service layer understands business.

The Repository understands data.

Each layer remains independent of the others.

---

## Low Coupling

Each layer communicates only with adjacent layers.

Example:

```text
Tool

↓

Service

↓

```

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](../index.md).
