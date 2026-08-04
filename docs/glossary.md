---
title: Glossary
status: active
audience: contributors
last_reviewed: 2026-08-04
---

# Glossary

## Agent

An Antigravity object responsible for interacting with the language model and coordinating tool execution.

---

## Tool

A callable capability exposed to the AI model.

Example:

- Get Customer
- Get Company Information

---

## Service

Contains business logic.

Services coordinate workflows and validation.

---

## Repository

Responsible for data access.

Repositories isolate the application from the data source.

---

## Domain Model

A Python dataclass representing a business entity.

Example:

- Customer
- Company

---

## ERPNext

An open-source ERP system used as the backend for this project.

---

## Gemini

Google's family of large language models used by the Antigravity Agent.

---

## Antigravity SDK

Google's Python SDK for building AI agents with tools, conversations, hooks, and other capabilities.

---

## ADR

Architecture Decision Record.

A document describing an important architectural decision.

---

## Sprint Journal

A chronological record of the work completed during each sprint, including objectives, implementation details, lessons learned, and future work.

---

## Layered Architecture

A software architecture where responsibilities are divided into distinct layers:

- Presentation
- Tool
- Service
- Repository
- Data Source

Each layer has a single responsibility and communicates only with adjacent layers.

---

## Thin Tool

A design principle where an AI tool performs minimal processing and delegates business logic to the service layer.

---

## Repository Pattern

A design pattern that abstracts data access behind a dedicated repository layer, allowing the data source to change without affecting the rest of the application.


## Revision history

| Date | Change |
| --- | --- |
| 2026-08-04 | Added metadata, documentation navigation, and revision history. |

---

Back to the [documentation index](index.md).
