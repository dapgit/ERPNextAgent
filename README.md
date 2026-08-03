# ERPNextAgent

An educational, production-style project for learning Google's Antigravity SDK by building an AI assistant for ERPNext.

## Current Status

- ✅ Sprint 1 – Environment Setup
- ✅ Sprint 2 – First Agent & Custom Tools
- ✅ Sprint 3 – Interactive CLI and Layered Architecture
- ⏳ Sprint 4 – Repository Layer

## Architecture

User → app.py → Agent → Tools → Services → Repository → ERPNext

## Project Structure

- `app.py` – Application entry point
- `agent/` – Agent lifecycle and prompts
- `tools/` – AI callable tools (thin adapters)
- `services/` – Business logic
- `models/` – Domain models
- `docs/` – Journal, ADRs and architecture docs

See `docs/` for detailed documentation.
