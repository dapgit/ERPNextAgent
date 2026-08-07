    Project: ERPNextAgent

    Checkpoint Date: 07-Aug-2026

    Current Sprint: Sprint 6 (Milestone 6.1 Complete)

    Project Status: Active Development

Purpose

This document is the authoritative checkpoint for the ERPNextAgent project.

Its purpose is to allow any future ChatGPT session (or another engineer) to resume development with minimal context loss.

It summarizes:

    Project goals

    Architectural decisions

    Current implementation status

    Documentation status

    Outstanding work

    Lessons learned

    Code review observations

    Next recommended steps

This document should be updated after every major sprint.
Executive Summary

ERPNextAgent is an enterprise AI application built using Google Antigravity SDK and ERPNext.

The project is intentionally designed as a learning and reference implementation rather than a quick prototype.

The primary objectives are:

    Learn Antigravity SDK through implementation.

    Demonstrate enterprise software architecture.

    Integrate with ERPNext using REST APIs.

    Later introduce MCP as an alternative integration layer.

    Produce documentation of comparable quality to production engineering projects.

Current Status

Current Sprint:

Sprint 6

Completed:

    Sprint 1

    Sprint 2

    Sprint 3

    Sprint 4

    Sprint 5.1

    Sprint 5.2
    Sprint 5.3
    Sprint 5.4
    Sprint 5.5
    Sprint 5.6
    Sprint 5.7
    Sprint 6.1

Active Milestone:

Sprint 6.3 – OpenTelemetry (next), then Metrics (6.4) and Documentation (6.5). Sprint 6.2 (Correlation IDs) was folded into 6.1's design and implementation — see ADR-0011.
Technology Stack

Python 3.12

Google Antigravity SDK

Gemini

ERPNext v16

Docker

requests

python-dotenv

Git

Ubuntu 24.04
Architecture Evolution

Sprint 1

Agent

Sprint 2

Agent

↓

Tool

Sprint 3

Agent

↓

Tool

↓

Configuration

Sprint 4

Agent

↓

Tool

↓

Service

↓

Repository

↓

Mock Data

Sprint 5

Agent

↓

Tool

↓

Service

↓

Repository Interface

↓

REST Repository

↓

ERPNextRESTClient

↓

ERPNext REST API

↓

ERPNext

Future

Repository Interface

↓

REST Repository

or

MCP Repository

Major Architectural Decisions
Repository Pattern

Repositories isolate data access from business logic.
Service Layer

Business rules belong exclusively in Services.
Thin Tools

AI Tools perform only orchestration and formatting.
Client Layer

HTTP concerns belong inside the Client layer.

Repositories should never know how HTTP is implemented.
REST First

Decision:

Integrate with ERPNext REST APIs first.

Reason:

Understanding ERPNext's native API provides stronger architectural foundations.
MCP Later

Decision:

Introduce MCP as an additional repository implementation after the REST implementation is complete.

Reason:

The Repository abstraction allows both implementations to coexist.
OpenTelemetry Deferred

Decision:

Do not introduce OpenTelemetry during Sprint 5.

Reason:

Sprint 5 should remain focused on ERP integration.

OpenTelemetry will be introduced in Sprint 6 under an observability/ package.
Current Repository Structure

ERPNextAgent/

app.py

clients/
    erpnext_rest_client.py

repositories/
    company_repository.py
    customer_repository.py
    item_repository.py
    factory.py

services/

tools/

models/

tests/

docs/

Documentation Status
Completed

Repository Documentation

Architecture Documentation

README

CONTRIBUTING

SECURITY

SUPPORT

CHANGELOG

Architecture Decision Records
In Progress

Sprint Journals

Antigravity SDK Handbook

ERPNext Handbook

Development Handbook
Repository Review (06-Aug-2026)
Overall

Repository Health

9.5 / 10

The architecture is clean and consistent.

The project is transitioning from a learning exercise into a production-quality codebase.
Strengths

Excellent layer separation.

Repository Pattern correctly implemented.

Dependency Injection introduced.

Dedicated REST Client.

Repository Interfaces.

Future MCP support designed into the architecture.

Strong documentation structure.

Good unit test foundation.
Remaining Technical Improvements

Expand structured logging.

Introduce OpenTelemetry during Sprint 6.

Expand helper methods inside the REST Client.
Documentation Review

Documentation Quality

8.5 / 10

The documentation structure is excellent.

The repository is easy to navigate.

Architecture documents are coherent.

However, additional depth is still required.
Remaining Documentation Work

Sprint Journals should become engineering journals rather than summaries.

Each journal should eventually contain:

    Objectives

    Problem Statement

    Architecture Review

    Implementation Walkthrough

    File-by-file changes

    Code walkthroughs

    Mermaid diagrams

    Lessons learned

    Common mistakes

    Review comments

    Future improvements

    Retrospective

Expected length:

10–15 pages per sprint.
SDK Handbook

Current handbook is a structural outline.

Needs significant expansion.

Each chapter should include:

    Theory

    Code examples

    Diagrams

    Best practices

    Troubleshooting

    References to project implementation

Target quality:

Book-quality documentation.
ERPNext Handbook

Needs:

REST API examples.

Authentication walkthroughs.

DocType explanations.

Common API patterns.

Example payloads.
Development Handbook

Needs:

Coding standards.

Testing standards.

Documentation standards.

Review process.

Git workflow.

Architecture conventions.
Documentation Observations

The repository review identified several improvements.
Naming Consistency

Standardize filenames.

Example:

Use:

tool-execution.md

instead of:

tools-execution.md

Likewise:

service-layer.md

instead of:

services-layer.md
ADR Naming

Choose a single naming convention.

Preferred:

0001-title.md

0002-title.md

0003-title.md
Checkpoint Documents

Current summary documents should be moved into:

docs/checkpoints/

or

maintained as:

PROJECT_CHECKPOINT.md

Dependency Diagram

Recommended new document:

docs/architecture/dependency-diagrams.md

containing only Mermaid diagrams.
Lessons Learned

The Repository Pattern has proven valuable.

The Client layer simplifies repositories.

Dependency Injection improves testing.

REST-first was the correct architectural decision.

Documentation should evolve alongside implementation.

Small, reviewable sprints reduce architectural risk.
Current Milestone

Sprint 6.1 (complete) — Structured Logging and Correlation IDs

ADR-0011 defines the design: JSON or text log output (configurable, defaulting to text for the interactive CLI), a schema with fields derived automatically from the standard LogRecord where possible (layer, operation, exception) rather than passed manually at each call site, a contextvars-based correlation ID generated once per user turn in app.py, and a logging.Filter that injects it into every record with no changes to any Tool/Service/Repository/Client signature. Verified against the Antigravity SDK: asyncio.to_thread (which the SDK uses to run sync tool functions) copies the contextvars context, so the correlation ID propagates correctly through real tool calls. Tool and Service logging did not exist before this milestone and was added; Repository and Client logging were updated to carry entity/duration_ms as structured fields.

Next: Sprint 6.3 — OpenTelemetry instrumentation on top of this foundation (Sprint 6.2, Correlation IDs, was folded into 6.1).

Completed Sprint 5 follow-up work:

    Sprint 5.3 replaced the mock Company repository with a REST-backed implementation.

    Sprint 5.4 added the repository factory, basic request logging, and a REST-backed Customer repository.

    Sprint 5.5 added the Item domain model, REST-backed repository, service, and tool; verified end-to-end against a live ERPNext instance.

    Sprint 5.6 removed MockCompanyRepository, MockCustomerRepository, and MockItemRepository along with the ERPNEXT_COMPANY environment variable and several ad-hoc, typo-matching workarounds that had accumulated around company-name resolution. The repository factory now always constructs the ERPNext-backed repositories, and ERPNextCompanyRepository always resolves the company by listing it from ERPNext.

    Sprint 5.7 reviewed a proposed 5-phase error-handling plan against the actual codebase. The exception hierarchy (utils/exceptions.py), the REST client's typed exceptions, and the repository layer's not-found handling already matched the intended design, so those were left unchanged. The one real gap — nothing catching exceptions before they reached the agent, letting messages like "ERPNext rejected the request to http://localhost:8080/..." leak internal hostnames and paths — was closed with a single shared helper, utils/tool_execution.execute_tool(), which the Company, Customer, and Item tools now route through. It logs the real exception server-side and returns a short, safe, user-facing message.

Future Roadmap

Sprint 6

    OpenTelemetry

    Observability

    Logging

    Metrics

Sprint 7

    Inventory

    Sales Orders

    Purchase Orders

Sprint 8

    Advanced ERP operations

Sprint 9

    MCP Integration

Sprint 10

    Production Readiness

Instructions for Future ChatGPT Sessions

When resuming this project:

    Read this document first.

    Treat it as the authoritative project checkpoint.

    Preserve the current architecture.

    Continue from Sprint 6.3 (OpenTelemetry), building on the Sprint 6.1 logging/correlation foundation.

    Update documentation alongside implementation.

    Do not bypass the Repository abstraction.

    Keep REST and MCP implementations interchangeable.

    Maintain clean architecture principles.

    Review documentation before considering any sprint complete.

Final Assessment

Current Project Quality

Architecture: 9.5 / 10

Code Quality: 9.5 / 10

Documentation Structure: 9.5 / 10

Documentation Depth: 8.5 / 10

Overall Project Health: 9.3 / 10

Sprint 5 is complete, and Sprint 6.1 (structured logging and correlation IDs) is complete. The project is in a healthy state and is ready to continue with Sprint 6.3 (OpenTelemetry).

The primary focus going forward should be expanding ERPNext functionality while continuing to improve the depth and quality of the documentation without compromising the architectural principles established in Sprints 1–5.