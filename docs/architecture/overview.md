---
title: Architecture Overview
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Architecture Overview

## Introduction

ERPNextAgent is designed as a layered enterprise application that uses Google's Antigravity SDK to provide AI-powered interactions with ERPNext.

The architecture emphasizes:

- Separation of Concerns
- Single Responsibility Principle
- Maintainability
- Testability
- Extensibility

Rather than embedding business logic inside AI tools, the application separates responsibilities into clearly defined layers. This allows the AI layer to remain independent of the underlying ERP implementation.

---

# Architecture Goals

The architecture has the following objectives:

1. Keep AI-specific code isolated.
2. Separate business logic from tool definitions.
3. Allow the backend implementation to change without affecting AI capabilities.
4. Support future ERPNext integration with minimal code changes.
5. Make every layer independently testable.

---

# High-Level Architecture

```text
+----------------------+
|        User          |
+----------+-----------+
           |
           v
+----------------------+
|  Antigravity Agent   |
+----------+-----------+
           |
           v
+----------------------+
|      Tool Layer      |
+----------+-----------+
           |
           v
+----------------------+
|    Service Layer     |
+----------+-----------+
           |
           v
+----------------------+
|   Repository Layer   |
+----------+-----------+
           |
           v
+----------------------+
| Mock Data / ERPNext  |
+----------------------+
```

---

# Layer Responsibilities

## User

The user interacts with the application using the command-line interface.

Responsibilities:

- Ask business questions
- Provide parameters
- Receive formatted responses

---

## Antigravity Agent

The Antigravity Agent is responsible for:

- Receiving user prompts
- Understanding intent
- Selecting tools
- Invoking tools
- Returning responses

The agent never contains ERP business logic.

---

## Tool Layer

The Tool Layer exposes capabilities to the language model.

Examples:

- Get Company Information
- Get Customer Information

Responsibilities:

- Accept parameters
- Validate basic input
- Delegate to the Service Layer
- Format the response

The Tool Layer should remain intentionally thin.

---

## Service Layer

The Service Layer contains business rules.

Examples:

- Validation
- Workflow coordination
- Business calculations
- Authorization (future)

Responsibilities:

- Coordinate repositories
- Apply business rules
- Prepare domain objects

The Service Layer must not contain data access code.

---

## Repository Layer

The Repository Layer abstracts data access.

Current implementation:

```text
Repository
    ↓
Mock Data
```

Future implementation:

```text
Repository
    ↓
ERPNext REST API
```

Only the repository should know how data is retrieved.

---

## Domain Models

Repositories return domain objects rather than dictionaries.

Example:

```python
@dataclass
class Customer:
    name: str
    territory: str
    customer_group: str
```

Benefits:

- Type safety
- Readability
- IDE support
- Easier testing

---

# Request Flow

The following sequence illustrates a typical request.

```text
User
 │
 │ "Get customer ABC Traders"
 ▼
Antigravity Agent
 │
 ▼
Customer Tool
 │
 ▼
Customer Service
 │
 ▼
Customer Repository
 │
 ▼
Mock Data / ERPNext
 │
 ▲
 │ Customer
 │
Customer Service
 │
 ▲
 │
Customer Tool
 │
 ▲
 │
Antigravity Agent
 │
 ▲
 │
User
```

---

# Dependency Direction

Dependencies flow in one direction only.

```text
app.py
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
```

No layer should depend on a higher layer.

Examples of invalid dependencies:

- Repository → Service
- Service → Tool
- Repository → Tool

Maintaining one-way dependencies improves maintainability and reduces coupling.

---

# Architectural Principles

The project follows several architectural principles.

## Single Responsibility Principle

Every module has one reason to change.

---

## Dependency Inversion

Higher layers depend on abstractions rather than implementation details.

---

## Separation of Concerns

Each layer has a clearly defined purpose.

---

## Thin Tools

AI tools should not contain business logic.

---

## Repository Pattern

Repositories abstract data access from business logic.

---

## Documentation First

Architecture changes are documented before a sprint is considered complete.

---

# Evolution of the Architecture

## Sprint 1

```text
User
   │
Agent
```

---

## Sprint 2

```text
User
   │
Agent
   │
Tool
```

---

## Sprint 3

```text
User
   │
Agent
   │
Tool
   │
Configuration
```

---

## Sprint 4

```text
User
   │
Agent
   │
Tool
   │
Service
   │
Repository
```

---

## Sprint 5 (Planned)

```text
User
   │
Agent
   │
Tool
   │
Service
   │
ERP Repository
   │
ERPNext REST API
```

Notice that the Tool and Service layers remain unchanged while only the Repository implementation changes.

This demonstrates the primary architectural goal of isolating data access behind a dedicated abstraction.

---

# Future Enhancements

The architecture is designed to support future additions without major refactoring.

Planned enhancements include:

- Authentication Layer
- Logging
- Caching
- Retry Policies
- Memory
- Multi-Agent Collaboration
- MCP Integration
- Unit and Integration Testing

These additions will extend the existing architecture rather than replace it.

---

# Summary

ERPNextAgent follows a layered architecture that separates AI interaction, business logic, and data access.

By maintaining clear boundaries between layers, the application remains easy to understand, test, maintain, and extend.

This architecture provides a solid foundation for integrating ERPNext while preserving the simplicity of the AI tooling layer.


## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](../index.md).
