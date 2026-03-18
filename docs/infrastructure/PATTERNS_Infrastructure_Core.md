# Patterns: Infrastructure Core

<!-- CHAIN: OBJECTIFS_Infrastructure_Core.md → PATTERNS_Infrastructure_Core.md → SYNC_Infrastructure_Core.md -->

## Purpose

Infrastructure Core is the parent module for shared services that power the engine. It contains subdirectories for specific infrastructure domains.

## Design Philosophy

### Service-Oriented
Each subdirectory is a self-contained service with its own documentation chain:
- `canon/` — Canonical speaker/narrator
- `history/` — Conversation persistence
- `tempo/` — Time and pacing control
- `world_builder/` — World generation and enrichment
- `orchestration/` — Agent coordination
- `embeddings/` — Embedding service wrapper

### Shared Patterns
All services follow:
- Single responsibility per module
- Clean interfaces for engine consumption
- Explicit state management

## What's In Scope

- Service orchestration
- Cross-cutting infrastructure concerns
- Module coordination

## What's Out of Scope

- Domain-specific logic (belongs in individual subdirectories)
- Physics operations (belongs in physics/)
- Frontend (belongs in frontend/)

## Subdirectory Documentation

Each subdirectory has its own full documentation chain. See:
- `docs/infrastructure/canon/`
- `docs/infrastructure/history/`
- `docs/infrastructure/tempo/`
- `docs/infrastructure/world-builder/`
- `docs/infrastructure/embeddings/`
