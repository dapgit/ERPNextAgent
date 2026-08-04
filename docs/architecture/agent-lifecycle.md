---
title: Agent Lifecycle
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Agent Lifecycle

## Introduction

The Antigravity Agent is the heart of ERPNextAgent.

It acts as the bridge between the user and the application, interpreting natural language requests, deciding when to invoke tools, and coordinating the overall conversation.

Unlike traditional applications where user actions directly call business logic, ERPNextAgent introduces an AI-driven decision layer.

Understanding the lifecycle of the Agent is essential before implementing advanced features such as memory, multiple tools, ERPNext integration, or multi-agent collaboration.

---

# Responsibilities

The Antigravity Agent is responsible for:

- Managing conversations
- Understanding user intent
- Selecting the appropriate tool
- Executing tool calls
- Returning responses to the user

The Agent is **not responsible** for:

- Business rules
- ERPNext communication
- Data persistence
- Validation of business entities

Those responsibilities belong to the Service and Repository layers.

---

# High-Level Lifecycle

The lifecycle of an interaction is shown below.

```text
Application Starts
        │
        ▼
Load Configuration
        │
        ▼
Create Agent
        │
        ▼
Wait For User Input
        │
        ▼
Receive Prompt
        │
        ▼
Reason About Request
        │
        ▼
Need Tool?
 ┌───────────────┐
 │               │
Yes             No
 │               │
 ▼               ▼
Execute Tool   Generate Response
 │               │
 └──────┬────────┘
        ▼
Return Response
        │
        ▼
Wait For Next Prompt
```

The Agent remains alive throughout the application lifetime.

---

# Application Startup

The lifecycle begins when the application starts.

Current implementation:

```text
main()

↓

create_agent()

↓

Agent Ready

↓

chat_loop()
```

The Agent is created only once.

Creating an Agent for every prompt would introduce unnecessary overhead and make maintaining conversational context more difficult.

---

# Configuration Phase

Before the Agent is created, the application loads its configuration.

Responsibilities include:

- Loading environment variables
- Reading API keys
- Building the Agent configuration
- Loading system instructions
- Registering tools

Example flow:

```text
settings.py

↓

config.py

↓

Agent Configuration

↓

Agent
```

This separation keeps configuration independent from application logic.

---

# Agent Initialization

During initialization, the Agent receives:

- Model configuration
- API credentials
- System instructions
- Registered tools

Conceptually:

```python
Agent(
    config=LocalAgentConfig(
        ...
    )
)
```

The initialization phase should not perform business operations.

Its only purpose is to prepare the runtime environment.

---

# Conversation Loop

Once initialized, the Agent enters a continuous conversation loop.

```text
while True

↓

Read User Input

↓

Process Prompt

↓

Return Response

↓

Repeat
```

This design allows a single Agent instance to handle multiple user requests during one application session.

---

# Prompt Processing

When the user enters a prompt, the Agent performs several logical steps.

```text
User Prompt

↓

Understand Intent

↓

Determine Required Capability

↓

Select Tool (if necessary)

↓

Execute Tool

↓

Generate Final Response
```

These steps are handled internally by the Antigravity SDK.

Our application provides the tools and business logic that the Agent can invoke.

---

# Tool Selection

The Agent decides whether a Tool is required.

Example:

User:

```text
Show customer ABC Traders.
```

The Agent recognizes that the request requires customer information.

It selects:

```text
get_customer()
```

The Tool receives only the required parameters.

---

# Tool Invocation

The Tool delegates immediately to the Service layer.

```text
Agent

↓

Customer Tool

↓

Customer Service

↓

Customer Repository
```

The Agent does not know how the data is retrieved.

It only knows that the Tool provides the requested capability.

---

# Response Generation

After the Tool completes its work, the response flows back to the Agent.

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

The Agent combines the Tool output with natural language generation before presenting the final response.

---

# Error Handling

Errors can occur at several points in the lifecycle.

Examples:

- Invalid user input
- Tool execution failure
- Repository failure
- ERPNext connection failure
- Authentication error

The Agent should return meaningful, user-friendly responses while avoiding exposure of internal implementation details.

Example:

Instead of:

```text
KeyError: CUSTOMER_NOT_FOUND
```

Return:

```text
I couldn't find a customer named "ABC Traders".
```

---

# Agent Lifetime

One Agent instance exists for the duration of the application.

```text
Application

↓

Create Agent

↓

Many User Requests

↓

Shutdown
```

The Agent is destroyed only when the application exits.

This design improves performance and supports future conversational memory.

---

# Current Lifecycle

Current implementation:

```text
Application

↓

Load Settings

↓

Create Configuration

↓

Create Agent

↓

Interactive Chat

↓

Tool Execution

↓

Service

↓

Repository

↓

Mock Data
```

---

# Future Lifecycle

When ERPNext integration is introduced, the lifecycle remains largely unchanged.

```text
Application

↓

Agent

↓

Tool

↓

Service

↓

ERP Repository

↓

ERPNext REST API

↓

ERPNext
```

Notice that only the Repository implementation changes.

The Agent lifecycle remains identical.

---

# Future Enhancements

The current lifecycle has been intentionally designed to accommodate future capabilities.

Planned enhancements include:

- Conversational memory
- Session management
- Context persistence
- Multi-agent collaboration
- Streaming responses
- Retry policies
- Logging
- Observability
- Tool usage metrics

Each enhancement extends the lifecycle without changing its fundamental structure.

---

# Design Decisions

The following architectural decisions were made during Sprint 3 and Sprint 4.

- The Agent is created once during application startup.
- Configuration is externalized into dedicated modules.
- Business logic is isolated from the Agent.
- The Agent communicates only through registered Tools.
- Tools delegate to Services.
- Services delegate to Repositories.

These decisions improve maintainability and allow the application to scale without significant architectural changes.

---

# Summary

The Antigravity Agent serves as the intelligent coordinator of ERPNextAgent.

It manages conversations, selects tools, and presents responses while remaining independent of business logic and data access.

By keeping the Agent focused on AI orchestration, the application maintains clear separation of concerns and provides a stable foundation for future ERPNext integration, memory, and advanced AI capabilities.


## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](../index.md).
