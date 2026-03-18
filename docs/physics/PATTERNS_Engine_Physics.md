# Patterns: Engine Physics

<!-- CHAIN: OBJECTIFS_Engine_Physics.md → PATTERNS_Engine_Physics.md → SYNC_Physics.md -->

## Purpose

Physics layer handles graph operations, embeddings, and tick orchestration for the narrative simulation.

## Design Philosophy

### Graph as Foundation
All world state lives in the graph. Physics operations read and mutate graph nodes/links through a consistent interface (`engine/physics/graph/`).

### Separation of Concerns
- **graph_ops_*.py** — Write operations (mutations)
- **graph_queries_*.py** — Read operations (queries)
- **graph_interface.py** — Abstraction layer for graph backend

### Embeddings
Semantic similarity via embeddings (`embeddings.py`) enables narrative coherence and search.

## What's In Scope

- Graph read/write operations
- Moment traversal
- Event handling
- Embedding-based similarity
- Image operations on graph nodes

## What's Out of Scope

- Business logic (belongs in infrastructure services)
- UI concerns (belongs in frontend)
- Narrative generation (belongs in agents)

## Dependencies

- Graph backend (external)
- Embedding service

## Key Files

| File | Purpose |
|------|---------|
| `graph_interface.py` | Graph abstraction |
| `graph_ops.py` | Core write operations |
| `graph_queries.py` | Core read operations |
| `embeddings.py` | Semantic similarity |
