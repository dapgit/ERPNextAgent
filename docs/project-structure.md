---
title: Project Structure
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Project Structure

## Overview

The project follows a layered architecture to promote maintainability, scalability, and separation of concerns.

---

# Directory Structure

```text
ERPNextAgent/
│
├── app.py
├── config.py
├── settings.py
├── prompts.py
│
├── agent/
│
├── tools/
│
├── services/
│
├── repositories/
│
├── models/
│
├── tests/
│
├── examples/
│
└── docs/
```

---

# Responsibilities

## app.py

Application entry point.

Responsibilities:

- Start application
- Initialize Agent
- Start chat loop

---

## tools/

Responsibilities:

- AI Tool definitions
- Parameter handling
- Delegate work to Services

Tools should not contain business logic.

---

## services/

Responsibilities:

- Business Rules
- Validation
- Workflow
- Coordination

---

## repositories/

Responsibilities:

- Data retrieval
- Data persistence
- ERPNext communication

---

## models/

Responsibilities:

- Domain entities
- Dataclasses
- Type-safe objects

---

## docs/

Contains:

- Journals
- ADRs
- Architecture
- Development Guides
- SDK Handbook

---

# Dependency Flow

```text
User

↓

Agent

↓

Tool

↓

Service

↓

Repository

↓

ERPNext
```

Each layer depends only on the layer immediately below it.

## Related documentation

Read the [architecture overview](architecture/overview.md) for the rationale and the [development handbook](development/development-handbook.md) for layer ownership.

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, cross-references, and revision history. |

---

Back to the [documentation index](index.md) · Next: [Architecture overview](architecture/overview.md)
