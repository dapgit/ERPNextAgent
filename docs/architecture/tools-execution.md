---
title: Tool Execution Flow
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Tool Execution Flow

## Introduction

One of the fundamental concepts in Google's Antigravity SDK is the **Tool**.

A Tool is the mechanism through which the AI Agent interacts with external functionality.

In ERPNextAgent, a Tool does **not** contain business logic.

Instead, it acts as an interface between the Antigravity Agent and the application's Service Layer.

Understanding the execution flow is essential because every future ERPNext operation—retrieving customers, creating sales orders, checking inventory, or generating reports—will follow this same pattern.

---

# What is a Tool?

A Tool is a callable capability that the Agent can invoke when it determines that external information or functionality is required.

Examples include:

- Get Customer
- Get Company Information
- Get Item
- Create Sales Order
- Get Stock Balance

The Agent decides **when** to call a Tool.

The Tool decides **which Service** should perform the work.

---

# High-Level Execution Flow

```text
User

↓

Agent receives prompt

↓

Agent analyses intent

↓

Agent selects Tool

↓

Tool executes

↓

Service performs business logic

↓

Repository retrieves data

↓

Service returns domain model

↓

Tool formats result

↓

Agent generates response

↓

User
```

---

# Detailed Sequence

## Step 1 – User Request

The user submits a natural language request.

Example:

```text
Show customer ABC Traders.
```

The application receives the request through the interactive CLI.

---

## Step 2 – Agent Interpretation

The Antigravity Agent processes the prompt.

Responsibilities:

- Parse the request
- Understand intent
- Determine whether a Tool is required

At this point, the Agent has **not** accessed ERPNext.

It has only reasoned about the request.

---

## Step 3 – Tool Selection

Based on the prompt, the Agent determines that customer information is required.

The Agent selects:

```text
get_customer()
```

This selection is automatic.

The application does not manually decide which Tool to execute.

---

## Step 4 – Parameter Extraction

The Agent extracts parameters from the user's prompt.

Example:

```text
Customer Name

↓

ABC Traders
```

The extracted parameters are passed to the Tool.

---

## Step 5 – Tool Invocation

The Tool receives the parameters.

Example:

```python
def get_customer(customer_name: str):
```

The Tool should perform minimal work.

Its primary responsibility is delegation.

---

## Step 6 – Service Delegation

The Tool immediately delegates to the Service Layer.

Example:

```python
return customer_service.get_customer(customer_name)
```

This is intentional.

Business rules belong in Services.

---

## Step 7 – Business Logic

The Service Layer performs the required business operations.

Examples:

- Validate input
- Apply business rules
- Coordinate repositories
- Handle errors

The Service should not know anything about the AI Agent.

---

## Step 8 – Repository Access

The Service requests data from the Repository.

Current implementation:

```text
Customer Repository

↓

Dictionary
```

Future implementation:

```text
Customer Repository

↓

ERPNext REST API
```

The Service is unaware of where the data originates.

---

## Step 9 – Domain Model

The Repository returns a domain model.

Example:

```python
Customer(
    name="ABC Traders",
    territory="Karnataka",
    customer_group="Retail"
)
```

Returning structured objects improves readability and type safety.

---

## Step 10 – Response Propagation

The response travels back through each layer.

```text
Repository

↓

Service

↓

Tool

↓

Agent

↓

User
```

Each layer performs only the work appropriate to its responsibility.

---

# Complete Sequence Diagram

```text
User
 │
 │ Request
 ▼
Agent
 │
 │ Select Tool
 ▼
Customer Tool
 │
 │ Delegate
 ▼
Customer Service
 │
 │ Retrieve Customer
 ▼
Customer Repository
 │
 │ Read Data
 ▼
Dictionary / ERPNext

▲
│

Customer

▲
│

Customer Service

▲
│

Customer Tool

▲
│

Agent

▲
│

User
```

---

# Responsibilities

## Agent

Responsible for:

- Intent recognition
- Tool selection
- Natural language generation

Not responsible for:

- Validation
- Business rules
- Data access

---

## Tool

Responsible for:

- Accepting parameters
- Delegating to Services
- Formatting responses

Should never contain:

- Database logic
- ERPNext calls
- Business calculations

---

## Service

Responsible for:

- Validation
- Business rules
- Workflow coordination
- Combining repository results

---

## Repository

Responsible for:

- Data retrieval
- Data persistence
- External API communication

---

# Why Thin Tools?

A common mistake is implementing business logic inside Tools.

Bad example:

```python
def get_customer(customer_name):

    customer = CUSTOMER_DATA.get(customer_name)

    if customer is None:
        ...

    return customer
```

The Tool now knows:

- data source
- validation
- business rules

This creates tight coupling.

---

Correct approach:

```python
def get_customer(customer_name):

    return customer_service.get_customer(customer_name)
```

Now the Tool is simply an interface.

---

# Error Handling

Errors may occur at multiple stages.

Examples:

- Invalid parameters
- Customer not found
- ERPNext unavailable
- Authentication failure

The preferred flow is:

Repository raises an error.

↓

Service interprets the error.

↓

Tool returns a meaningful message.

↓

Agent communicates naturally with the user.

This keeps error handling centralized.

---

# Future Execution Flow

Today:

```text
Repository

↓

Dictionary
```

Sprint 5:

```text
Repository

↓

ERPNext REST API
```

Sprint 8:

```text
Repository

↓

ERPNext

↓

Cache

↓

Retry Policy

↓

Logging
```

Notice that the Tool execution flow remains unchanged.

Only the Repository implementation evolves.

---

# Design Principles

The Tool execution flow follows several important principles:

- Single Responsibility Principle
- Separation of Concerns
- Dependency Inversion
- Repository Pattern
- Thin Tools
- Layered Architecture

These principles ensure that the AI layer remains independent of business logic and data access.

---

# Summary

Tool execution is the central workflow of ERPNextAgent.

The Antigravity Agent interprets user requests and invokes the appropriate Tool.

The Tool delegates to the Service Layer, which applies business rules and retrieves data through the Repository.

By maintaining clear boundaries between layers, the application remains maintainable, testable, and ready for future ERPNext integration without requiring architectural changes.


## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](../index.md).
