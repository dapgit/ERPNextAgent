# ERPNextAgent Project Checkpoint
**Date:** 06-Aug-2026

---

# Project Summary

ERPNextAgent is a learning and reference project that demonstrates how to build an enterprise AI application using **Google Antigravity SDK** integrated with **ERPNext**.

The project has two primary goals:

1. Learn Google's Antigravity SDK through practical implementation.
2. Build a production-quality AI assistant using sound software engineering practices.

Rather than building a quick prototype, the project follows an incremental sprint-based approach where architecture, documentation, and implementation evolve together.

---

# Project Vision

Build an AI-powered ERPNext assistant that demonstrates:

- Google Antigravity SDK
- Clean Architecture
- Repository Pattern
- Service Layer
- Domain Models
- Enterprise Documentation
- ERPNext REST Integration
- Future MCP Integration
- Future OpenTelemetry Observability

The project is intended to become a high-quality reference implementation for developers.

---

# Technology Stack

## AI

- Google Antigravity SDK
- Gemini Models

## ERP

- ERPNext v16

## Backend

- Python 3.12
- requests
- python-dotenv

## Development Environment

- Ubuntu 24.04
- Docker-based ERPNext installation

---

# Completed Sprints

## Sprint 1 – Environment Setup

Completed:

- Python environment
- Virtual environment
- Gemini API configuration
- Antigravity SDK installation
- First AI Agent

Outcome:

A working Antigravity Agent capable of responding to user prompts.

---

## Sprint 2 – Custom Tools

Completed:

- Company Tool
- Customer Tool
- Tool registration
- Tool invocation

Outcome:

The AI Agent can invoke custom tools.

---

## Sprint 3 – Application Architecture

Major refactoring performed.

Introduced:

- app.py
- assistant.py
- config.py
- settings.py
- prompts.py

Implemented:

- Interactive chat loop
- Configuration separation
- Cleaner startup sequence

Outcome:

The application became a maintainable interactive application instead of a demo script.

---

## Sprint 4 – Enterprise Architecture

Major architectural redesign.

Introduced:

- Repository Pattern
- Service Layer
- Domain Models
- Thin Tools

Architecture:

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

Mock Data

Outcome:

Business logic is isolated from AI logic.

Data access is abstracted.

The project is now ready for ERPNext integration.

---

# Sprint 5 (Current)

Current Status:

Sprint 5.1 and Sprint 5.2 completed.

---

## Sprint 5.1

Completed:

- ERPNext REST API planning
- Environment configuration
- API authentication strategy

Environment Variables:

- GEMINI_API_KEY
- ERPNEXT_URL
- ERPNEXT_API_KEY
- ERPNEXT_API_SECRET

---

## Sprint 5.2

Major additions:

### Client Layer

Introduced:

clients/

ERPNextRESTClient

Responsibilities:

- HTTP communication
- Authentication
- URL construction
- JSON parsing
- Session management

The client knows HTTP but does not know ERP business entities.

---

### Repository Interfaces

Repository interfaces introduced.

Current design:

CompanyRepository (interface)

↓

MockCompanyRepository

↓

ERPNextCompanyRepository

Future:

↓

MCPCompanyRepository

This validates the Repository Pattern introduced in Sprint 4.

---

### Dependency Injection

Repositories now receive the REST client through dependency injection where appropriate.

Benefits:

- Better testing
- Lower coupling
- Future extensibility

---

### REST Client Improvements

Implemented:

- requests.Session
- URL builder
- GET helpers
- Response parsing
- Exception handling
- Context manager support

---

# Architectural Decisions

## Repository Pattern

Repositories isolate data access.

Services remain independent of ERPNext.

---

## Client Layer

Introduced between Repository and ERPNext.

Architecture:

Tool

↓

Service

↓

Repository

↓

ERPNextRESTClient

↓

ERPNext REST API

Purpose:

Separate HTTP concerns from business concerns.

---

## Thin Tools

Tools contain no business logic.

Responsibilities:

- Receive parameters
- Delegate to Service
- Format response

---

## Service Layer

Services own:

- Business rules
- Validation
- Workflow coordination

They never communicate directly with ERPNext.

---

## Domain Models

Repositories return domain models instead of raw JSON.

Example:

Company

Customer

Item

---

# Future Architecture

Target architecture:

User

↓

Antigravity Agent

↓

Tool

↓

Service

↓

Repository Interface

↓

REST Repository

or

MCP Repository

↓

REST Client

or

MCP Client

↓

ERPNext

This allows REST and MCP implementations to coexist without changing the Tool or Service layers.

---

# OpenTelemetry Decision

Decision:

OpenTelemetry will **not** be introduced during Sprint 5.

Reason:

Sprint 5 focuses on ERPNext integration.

Observability will be introduced in Sprint 6.

Planned observability package:

observability/

- telemetry.py
- tracing.py
- metrics.py

The initial instrumentation target will be ERPNextRESTClient, followed by Repository, Service, Tool, and Agent layers in later sprints.

---

# Documentation Status

Completed:

- Repository Documentation
- Architecture Documentation

In Progress:

- ADRs
- Sprint Journals
- SDK Handbook
- ERPNext Handbook
- Development Handbook

Documentation is maintained alongside the implementation and is considered part of the definition of done.

---

# Current Project Structure

```text
ERPNextAgent/

app.py

settings.py

config.py

clients/
    erpnext_rest_client.py

repositories/
    company_repository.py
    customer_repository.py

services/
    company_service.py
    customer_service.py

tools/

models/

docs/
```

---

# Lessons Learned

- Clean architecture pays off when integrating with external systems.
- Separating HTTP logic into a dedicated client simplifies repositories.
- Repository interfaces make future REST/MCP switching possible.
- Documentation should evolve with the code, not afterwards.
- Small, incremental sprints make architecture changes easier to review and validate.

---

# Next Sprint Objectives

Sprint 5.3

- Replace the mock Company repository with the ERPNext implementation.
- Retrieve Company data from the live ERPNext instance.
- Verify Tool → Service → Repository → REST Client flow.

Sprint 5.4

- Implement Customer repository using the same pattern.

Sprint 5.5

- Add Item repository.

Sprint 5.6

- Improve error handling.
- Introduce structured logging.

Sprint 5.7

- Complete Sprint 5 documentation.
- Update ADRs.
- Update architecture documentation.

---

# Long-Term Roadmap

Sprint 6

- Authentication improvements
- OpenTelemetry observability
- Logging
- Metrics

Sprint 7

- Sales Orders
- Purchase Orders
- Inventory

Sprint 8

- Reports
- Advanced ERPNext operations

Sprint 9

- MCP integration
- REST vs MCP comparison

Sprint 10

- Production readiness
- Testing
- Packaging
- Deployment

---

# Working Principles

The following principles guide the project:

- Documentation is part of the implementation.
- Every sprint updates both code and documentation.
- Architecture changes are documented through ADRs.
- Business logic belongs in Services.
- Data access belongs in Repositories.
- HTTP concerns belong in Clients.
- AI Tools remain intentionally thin.
- Future integrations (such as MCP) should be introduced behind stable abstractions.

---

# Session Resume Prompt

When resuming this project in a future ChatGPT session:

> We are building **ERPNextAgent**, an enterprise AI assistant using Google's Antigravity SDK and ERPNext. Sprints 1–4 are complete. Sprint 5.1 and 5.2 are complete, including the introduction of `ERPNextRESTClient`, repository interfaces, and dependency injection. We intentionally chose ERPNext REST APIs first and deferred MCP integration to a later sprint behind the Repository abstraction. OpenTelemetry has been evaluated and is planned for Sprint 6. Continue from Sprint 5.3 while preserving the current architecture and keeping the documentation synchronized with the implementation.