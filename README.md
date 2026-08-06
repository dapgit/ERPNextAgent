---
title: ERPNextAgent
status: active
audience: contributors
last_reviewed: 2026-08-06
---

# ERPNextAgent

> **Building a Production-Quality ERPNext AI Assistant using Google's Antigravity SDK**

---

# Project Status

**Current Sprint:** Sprint 5 in progress (milestones 5.1 and 5.2 completed)

| Area | Status |
|------|--------|
| Environment Setup | ✅ Complete |
| Antigravity SDK Setup | ✅ Complete |
| Custom Tools | ✅ Complete |
| Interactive CLI | ✅ Complete |
| Layered Architecture | ✅ Complete |
| Repository Pattern | ✅ Complete |
| Domain Models | ✅ Complete |
| ERPNext REST foundation | 🚧 In progress — milestones 5.1 and 5.2 complete |
| Multi-Agent Support | ⏳ Planned |

---

# Table of Contents

- [Project Vision](#project-vision)
- [Why This Project Exists](#why-this-project-exists)
- [Project Goals](#project-goals)
- [Learning Philosophy](#learning-philosophy)
- [Repository Structure](#repository-structure)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Sprint Progress](#sprint-progress)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Project Documentation](#project-documentation)
- [Engineering Principles](#engineering-principles)
- [Development Workflow](#development-workflow)
- [Current Architecture](#current-architecture)
- [Future Roadmap](#future-roadmap)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

# Project Vision

ERPNextAgent is an educational and production-oriented project that demonstrates how to build an AI-powered ERP assistant using Google's Antigravity SDK.

This repository is designed with two primary objectives:

1. Build a production-quality AI Assistant for ERPNext.
2. Become a comprehensive learning resource for Google's Antigravity SDK.

Unlike most sample repositories, this project documents not only the implementation but also the engineering decisions that shaped it.

---

# Why This Project Exists

The Antigravity SDK is a powerful framework for building AI agents, but practical examples demonstrating enterprise application architecture are limited.

This repository fills that gap by showing how to evolve a simple AI agent into a maintainable enterprise application using software engineering best practices.

Throughout the project we focus on:

- Clean Architecture
- Layered Design
- Repository Pattern
- Service Layer
- Domain Models
- Documentation
- Refactoring
- Maintainability
- Testability

---

# Project Goals

The project aims to:

- Learn Google's Antigravity SDK through practical implementation.
- Integrate Antigravity with ERPNext.
- Demonstrate enterprise software architecture.
- Produce high-quality technical documentation.
- Serve as a reference implementation for future developers.

---

# Learning Philosophy

The project follows several core principles.

## Learn by Building

Every concept is introduced through implementation rather than isolated examples.

---

## Build Like a Production Project

Although this started as a learning exercise, the repository is maintained using professional software engineering practices.

These include:

- Layered Architecture
- Architecture Decision Records (ADR)
- Sprint Journals
- Code Reviews
- Refactoring
- Documentation-First Development

---

## One Concept Per Sprint

Each sprint introduces exactly one major concept.

Examples include:

- Building the first Agent
- Creating Custom Tools
- Interactive Applications
- Repository Pattern
- ERPNext Integration

This incremental approach keeps learning manageable.

---

# Repository Structure

```text
ERPNextAgent/
│
├── app.py
├── config.py
├── settings.py
├── requirements.txt
├── .env.example
│
├── agent/
│
├── tools/
│
├── services/
│
├── repositories/
│
├── clients/
│   └── erpnext_rest_client.py
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

# Architecture

The project follows a layered architecture.

```text
User
 │
 ▼
Antigravity Agent
 │
 ▼
Tool Layer
 │
 ▼
Service Layer
 │
 ▼
Repository Layer
 │
 ▼
Repository implementation
 │
 ▼
ERPNext REST Client
 │
 ▼
ERPNext REST API
```

Each layer has a clearly defined responsibility.

| Layer | Responsibility |
|--------|----------------|
| app.py | Application orchestration |
| agent | Antigravity lifecycle |
| tools | AI interface |
| services | Business logic |
| repositories | Data access |
| clients | HTTP transport, session/authentication setup, and response parsing |
| models | Domain objects |

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.12 |
| AI Runtime | Google Antigravity SDK |
| LLM | Gemini |
| ERP | ERPNext |
| Architecture | Layered Architecture |
| Documentation | Markdown + ADR |

---

# Sprint Progress

| Sprint | Status |
|---------|--------|
| Sprint 1 – Environment Setup | ✅ Complete |
| Sprint 2 – Custom Tools | ✅ Complete |
| Sprint 3 – Interactive Application | ✅ Complete |
| Sprint 4 – Repository Pattern | ✅ Complete |
| Sprint 5 – ERPNext REST Integration | 🚧 In progress — 5.1 and 5.2 complete |
| Sprint 6 – Observability | Planned |
| Sprint 7 – Advanced ERP Operations | Planned |
| Sprint 8 – Multi-Agent Architecture | Planned |

---

# Getting Started

## Prerequisites

- Python 3.12+
- Google Gemini API Key
- Google Antigravity SDK
- Git

---

## Clone the Repository

```bash
git clone https://github.com/<your-username>/ERPNextAgent.git

cd ERPNextAgent
```

---

## Create Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

Example:

```text
GEMINI_API_KEY=your_api_key
ERPNEXT_URL=https://your-erpnext-instance
ERPNEXT_API_KEY=your_erpnext_api_key
ERPNEXT_API_SECRET=your_erpnext_api_secret
# Optional; otherwise the first visible Company is used
ERPNEXT_COMPANY=your-company-name
```

---

# Running the Application

Start the assistant:

```bash
python app.py
```

Example:

```text
========================================
ERPNext AI Assistant
Type 'exit' to quit.
========================================

You >
```

---

# Project Documentation

Documentation is maintained alongside the source code.

```text
docs/
├── journal/
├── adr/
├── architecture/
├── antigravity-sdk/
├── erpnext/
└── development/
```

Every sprint updates the documentation before it is considered complete.

Use the [documentation index](docs/index.md) as the maintained starting point. It links the architecture, ADRs, completed-sprint journals, development workflow, and integration handbooks. The [documentation audit](docs/documentation-audit-2026-08-04.md) records the current baseline and remaining gaps.

---

# Engineering Principles

## Single Responsibility Principle

Every module should have exactly one responsibility.

---

## Thin Tools

Antigravity tools should contain as little business logic as possible.

---

## Business Logic in Services

Business rules belong inside the Service layer.

---

## Repository Pattern

Repositories abstract data access.

For the Company capability today:

```text
Repository
    ↓
MockCompanyRepository (when ERPNEXT_URL is unset)

or

ERPNextCompanyRepository
    ↓
ERPNextRESTClient
    ↓
ERPNext REST API
```

Future:

```text
Repository
    ↓
ERPNext REST API
```

---

## Documentation First

Documentation evolves alongside the code.

A sprint is not complete until:

- Code is complete
- Documentation is complete
- ADRs are updated
- Architecture is documented

---

# Development Workflow

Every sprint follows the same lifecycle.

1. Define the problem.
2. Discuss the architecture.
3. Implement.
4. Review.
5. Refactor.
6. Update documentation.
7. Record lessons learned.

---

# Current Architecture

```text
User
   │
   ▼
Antigravity Agent
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
CompanyRepository contract
   │
   ├── MockCompanyRepository
   └── ERPNextCompanyRepository
          │
          ▼
   ERPNextRESTClient
          │
          ▼
   ERPNext REST API
```

The Company Service and Tool use the same capability regardless of implementation. Customer remains mock-backed in this increment.

---

# Future Roadmap

Planned enhancements include:

- ERPNext REST API Integration
- Authentication
- Customer Management
- Supplier Management
- Sales Orders
- Purchase Orders
- Inventory
- Finance
- OpenTelemetry-based observability (deferred to Sprint 6)
- Unit Testing
- Integration Testing
- Memory
- Multi-Agent Architecture
- MCP Integration

---

# License

The project license will be finalized before the first public release.

---

# Acknowledgements

This project builds upon:

- Google's Antigravity SDK
- Google's Gemini models
- ERPNext

The implementation, architecture, documentation, and sprint methodology have been developed incrementally to demonstrate how to build maintainable enterprise AI applications.

---

# About This Repository

This repository intentionally documents both the implementation and the reasoning behind every architectural decision.

The objective is to help engineers understand how to design, build, document, and maintain enterprise AI applications using Google's Antigravity SDK.

---

Documentation: [index](docs/index.md) · [roadmap](docs/project-roadmap.md) · [style guide](docs/documentation-style-guide.md) · [audit](docs/documentation-audit-2026-08-04.md)

## Revision History

| Date | Change |
| --- | --- |
| 2026-08-04 | Added documentation-system navigation, metadata, and audit link. |
