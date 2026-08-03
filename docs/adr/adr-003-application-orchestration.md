# ADR-003: Application Orchestration

Status: Accepted

## Decision
`app.py` is responsible only for orchestration.

## Responsibilities
- Display banner
- Start chat loop
- Create the agent
- Handle application shutdown

All configuration and lifecycle management are delegated to dedicated modules.
