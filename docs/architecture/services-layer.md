---
title: Service Layer
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Service Layer

## Introduction

The Service Layer is responsible for implementing the business logic of ERPNextAgent.

It acts as the bridge between the AI-facing Tool Layer and the data-facing Repository Layer.

Rather than allowing Tools to directly access data, every request passes through the Service Layer, ensuring that business rules remain centralized and reusable.

This separation is one of the key architectural decisions made during Sprint 4.

---

# Purpose

The Service Layer exists to answer one question:

> "How should the application perform this business operation?"

It should not concern itself with:

- AI interactions
- User interfaces
- Database implementation
- ERPNext API details

Instead, it focuses entirely on business behaviour.

---

# Responsibilities

The Service Layer is responsible for:

- Business validation
- Workflow coordination
- Calling repositories
- Combining information from multiple repositories
- Business calculations
- Error interpretation
- Returning domain models

The Service Layer should **not**:

- Read environment variables
- Communicate directly with users
- Register AI tools
- Know how repositories retrieve data

---

# Position in the Architecture

```text
User
 │
 ▼
Agent
 │
 ▼
Tool
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
ERPNext
```

The Service Layer sits between AI and data.

---

# Why Do We Need a Service Layer?

Without a Service Layer:

```text
Tool

↓

```

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](../index.md).
