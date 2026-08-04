# Contributing to ERPNextAgent

Thank you for your interest in contributing to ERPNextAgent.

This repository is more than a software project—it is also a learning resource demonstrating how to build enterprise AI applications using Google's Antigravity SDK and ERPNext.

To maintain consistency and quality, please follow the guidelines below.

---

# Project Philosophy

The project is built around the following principles:

- Learn by Building
- Architecture before Implementation
- Small, Incremental Improvements
- Documentation is a First-Class Deliverable
- Every Architectural Decision should be Documented

---

# Before You Start

Please read the following documents before making changes:

- README.md
- docs/project-roadmap.md
- docs/project-structure.md
- Existing Architecture Decision Records (ADR)

Understanding the existing architecture is important before introducing new functionality.

---

# Repository Structure

```text
ERPNextAgent/
│
├── agent/
├── tools/
├── services/
├── repositories/
├── models/
├── tests/
├── docs/
└── examples/
```

Every directory has a clearly defined responsibility.

---

# Engineering Principles

## 1. Single Responsibility Principle (SRP)

Every module should have exactly one reason to change.

Avoid combining unrelated functionality into a single file.

---

## 2. Thin Tools

Antigravity tools should only:

- Accept parameters from the AI model
- Delegate work to the Service layer
- Return the result

Business logic must never be implemented inside the Tool layer.

Example:

```python
def get_customer(customer_name: str):
    return customer_service.get_customer(customer_name)
```

---

## 3. Business Logic

Business rules belong inside:

```text
services/
```

Examples include:

- Validation
- Authorization
- Workflow
- Calculations
- Business Rules

---

## 4. Repository Layer

Repositories are responsible for retrieving and storing data.

Current Architecture:

```text
Repository
    ↓
Mock Data
```

Future Architecture:

```text
Repository
    ↓
ERPNext REST API
```

Nothing outside the Repository should know how data is retrieved.

---

## 5. Domain Models

Domain entities should be represented using Python dataclasses.

Example:

```python
@dataclass
class Customer:
    name: str
    territory: str
    customer_group: str
```

Avoid returning dictionaries from repositories or services unless there is a specific reason.

---

# Coding Standards

## Python

- Follow PEP 8
- Use Type Hints
- Write Descriptive Function Names
- Keep Functions Small
- Avoid Duplicate Code
- Prefer Composition over Complexity

---

## Imports

Prefer explicit imports.

Good:

```python
from services.customer_service import get_customer
```

Avoid wildcard imports.

---

## Docstrings

Every public function should include a docstring.

Example:

```python
def get_customer(customer_name: str):
    """
    Retrieve customer information.
    """
```

---

# Documentation Standards

Every feature should update documentation.

Documentation changes may include:

- README
- CHANGELOG
- Sprint Journal
- ADR
- Architecture Guide

Documentation is considered part of the implementation.

---

# Architecture Decision Records (ADR)

Whenever an architectural decision changes the project, create or update an ADR.

Each ADR should include:

- Status
- Context
- Problem
- Decision
- Rationale
- Consequences

---

# Definition of Done

A feature is complete only when all of the following are satisfied:

- Feature implemented
- Code reviewed
- Refactored
- Documentation updated
- Tests added (where applicable)
- Architecture updated (if required)

---

# Pull Request Checklist

Before submitting changes:

- [ ] Code follows project structure
- [ ] Tools contain no business logic
- [ ] Services contain business rules
- [ ] Repository abstraction maintained
- [ ] Documentation updated
- [ ] ADR updated (if required)
- [ ] CHANGELOG updated

---

# Branch Naming

Recommended format:

```text
feature/customer-service
feature/erpnext-client
refactor/repository-layer
docs/sprint-04
```

---

# Commit Message Convention

Use Conventional Commits.

Examples:

```text
feat(customer): add customer repository

refactor(service): move validation into service layer

docs(journal): add Sprint 4 journal

fix(tool): correct customer lookup
```

---

# Questions

If you're unsure where new functionality belongs, follow this rule:

> Business logic belongs in the Service layer.

If you're still unsure, document the decision in an ADR before implementation.

---

Thank you for helping maintain the quality of ERPNextAgent.