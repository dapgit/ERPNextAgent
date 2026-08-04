---
title: Repository Layer
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Repository Layer

## Introduction

The Repository Layer is responsible for all data access within ERPNextAgent.

Its primary purpose is to isolate the rest of the application from the implementation details of the underlying data source.

Today, repositories retrieve data from mock objects used during development.

In future sprints, these repositories will communicate directly with ERPNext through its REST API.

The Service Layer should never need to know which implementation is being used.

---

# Why a Repository Layer?

Without a Repository Layer, Services would communicate directly with ERPNext.

Example:

```text
Service

↓
# Repository Layer

## Introduction

The Repository Layer is responsible for all data access within ERPNextAgent.

Its primary purpose is to isolate the rest of the application from the implementation details of the underlying data source.

Today, repositories retrieve data from mock objects used during development.

In future sprints, these repositories will communicate directly with ERPNext through its REST API.

The Service Layer should never need to know which implementation is being used.

---

# Why a Repository Layer?

Without a Repository Layer, Services would communicate directly with ERPNext.

Example:

```text
Service

↓

ERPNext REST API
```

This creates several problems:

- Business logic becomes tightly coupled to ERPNext.
- Unit testing becomes difficult.
- Changing the data source requires modifications throughout the application.
- Mocking external systems becomes complicated.

Instead, ERPNextAgent uses:

```text
Service

↓

Repository

↓

ERPNext
```

The Service communicates with an abstraction.

The Repository communicates with the implementation.

---

# Responsibilities

Repositories are responsible for:

- Retrieving data
- Persisting data
- Communicating with external APIs
- Translating external responses into domain models
- Hiding implementation details

Repositories are **not responsible** for:

- Business rules
- AI interactions
- Validation
- User interface logic
- Workflow decisions

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

The Repository is the only layer that knows how data is obtained.

---

# Current Implementation

At the end of Sprint 4, repositories use in-memory mock data.

Example:

```python
_CUSTOMERS = {
    "ABC Traders": Customer(
        name="ABC Traders",
        territory="Karnataka",
        customer_group="Retail"
    )
}
```

The repository exposes methods such as:

```python
get_customer(customer_name: str)
```

The rest of the application is unaware that the data comes from a dictionary.

---

# Future Implementation

During Sprint 5, the implementation will change.

Instead of:

```text
Repository

↓

Dictionary
```

It will become:

```text
Repository

↓

ERPNext REST API

↓

ERPNext Server
```

Importantly, the Service Layer will remain unchanged.

This is the primary advantage of the Repository Pattern.

---

# Repository Responsibilities

A repository should perform only data-related operations.

Typical examples include:

- Retrieve customer
- Retrieve company
- Retrieve item
- Create sales order
- Update customer
- Delete supplier

Business validation should not appear here.

---

# Repository Interface

Repositories expose a clean interface to the Service Layer.

Example:

```python
def get_customer(customer_name: str) -> Customer | None:
    ...
```

The Service should not know:

- Whether data comes from a dictionary
- Whether data comes from ERPNext
- Whether data comes from a cache
- Whether multiple API calls were required

Those implementation details belong inside the Repository.

---

# Returning Domain Models

Repositories should return domain models rather than raw dictionaries.

Example:

```python
Customer(
    name="ABC Traders",
    territory="Karnataka",
    customer_group="Retail",
    customer_type="Company"
)
```

Benefits include:

- Strong typing
- Better readability
- Easier testing
- Clear contracts between layers

---

# Mapping External Data

ERPNext will typically return JSON.

Example:

```json
{
    "customer_name": "ABC Traders",
    "territory": "Karnataka",
    "customer_group": "Retail"
}
```

The Repository is responsible for translating this response into a domain model.

Example:

```python
Customer(
    name=response["customer_name"],
    territory=response["territory"],
    customer_group=response["customer_group"]
)
```

The Service Layer never sees raw JSON.

---

# Repository Flow

A typical request follows this sequence.

```text
Customer Service

↓

Customer Repository

↓

ERPNext REST API

↓

ERPNext

↓

JSON Response

↓

Customer Domain Model

↓

Customer Service
```

The Repository isolates all communication details.

---

# Error Handling

Technical failures occur in the Repository Layer.

Examples:

- Network timeout
- Authentication failure
- HTTP 404
- HTTP 500
- Invalid response
- Connection failure

Repositories should raise meaningful exceptions or return well-defined error states.

The Service Layer is responsible for interpreting those errors.

---

# Caching (Future)

Repositories provide a natural location for caching.

Future architecture:

```text
Repository

↓

Cache

↓

ERPNext

↓

Database
```

The Service Layer remains unchanged.

---

# Logging (Future)

Repositories are also an appropriate place for technical logging.

Examples:

- API request duration
- Response codes
- Retry attempts
- Connection failures

Business logging should remain in the Service Layer.

---

# Retry Policies (Future)

Transient failures should be handled inside the Repository.

Examples:

- Retry HTTP timeouts
- Retry temporary network failures
- Exponential backoff

Higher layers should not implement retry logic.

---

# Testing

Repositories should be independently testable.

Example tests:

- Customer exists
- Customer not found
- Invalid response mapping
- Authentication failure
- Timeout handling

Mock implementations can be used to verify Service behaviour without requiring a live ERPNext instance.

---

# Anti-Patterns

## Business Logic in Repository

❌ Incorrect

```python
if customer.credit_limit > ...
```

Business rules belong in the Service Layer.

---

## Repository Returning Raw JSON

❌ Incorrect

```python
return response.json()
```

Repositories should return domain models.

---

## Repository Calling Services

❌ Incorrect

```text
Repository

↓

Service
```

Dependencies should always flow downward.

---

## Repository Performing Presentation Formatting

❌ Incorrect

Repositories should not generate user-facing messages.

Formatting belongs to the Tool Layer or the Agent.

---

# Evolution of the Repository

## Sprint 4

```text
Repository

↓

Dictionary
```

---

## Sprint 5

```text
Repository

↓

ERPNext REST API
```

---

## Future

```text
Repository

↓

Cache

↓

Retry Policy

↓

ERPNext REST API

↓

ERPNext
```

The interface remains stable while the implementation evolves.

---

# Design Principles

The Repository Layer follows several architectural principles.

- Repository Pattern
- Dependency Inversion
- Separation of Concerns
- Single Responsibility Principle
- Domain-Driven Design

These principles ensure that changes to ERPNext integration remain isolated within the Repository Layer.

---

# Summary

The Repository Layer is responsible for all communication with external data sources.

By isolating ERPNext-specific implementation details behind a stable interface, the rest of the application remains independent of the underlying data source.

This approach enables easier testing, cleaner architecture, and seamless migration from mock data to a live ERPNext environment without affecting the Tool or Service layers.

```

## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](../index.md).
