# Patterns: Engine Models

<!-- CHAIN: OBJECTIFS_Engine_Models.md → PATTERNS_Engine_Models.md → SYNC_Engine_Models.md -->

## Purpose

Engine Models defines the data structures for graph nodes, links, and schema helpers used throughout the engine.

## Design Philosophy

### Type Safety
Models provide typed representations of graph entities, enabling IDE support and compile-time checks.

### Schema Consistency
All graph nodes and links follow consistent schemas defined here, ensuring data integrity across the system.

### Separation from Operations
Models are pure data definitions. Operations on models live in physics layer; business logic lives in infrastructure services.

## What's In Scope

- Node type definitions
- Link type definitions
- Schema validation helpers
- Type guards and utilities

## What's Out of Scope

- Graph operations (physics layer)
- Business logic (infrastructure)
- Persistence (physics/graph)

## Key Concepts

| Concept | Description |
|---------|-------------|
| Node | Graph vertex with typed properties |
| Link | Graph edge connecting nodes |
| Schema | Validation rules for node/link types |
| Type Guard | Runtime type checking utilities |
