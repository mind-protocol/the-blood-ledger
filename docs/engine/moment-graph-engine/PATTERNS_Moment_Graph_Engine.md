# Patterns: Moment Graph Engine

<!-- CHAIN: OBJECTIFS_Engine_Moment_Graph.md → PATTERNS_Moment_Graph_Engine.md → SYNC_Moment_Graph_Engine.md -->

## Purpose

The moment graph engine handles traversal, querying, and navigation of the moment graph structure that underlies the narrative.

## Design Philosophy

### Moments as Nodes
Each moment is a graph node representing a point in the narrative. Moments connect through typed edges representing causation, sequence, and association.

### Query-First
The engine prioritizes efficient querying over mutation. Most operations are reads for moment retrieval and path finding.

### Integration with Physics
Moment operations are implemented in `engine/physics/graph/graph_ops_moments.py` and `graph_queries_moments.py`. This module documents the patterns; implementation lives in physics.

## What's In Scope

- Moment node structure
- Moment traversal algorithms
- Moment queries and search
- Path finding between moments

## What's Out of Scope

- Graph storage (physics layer)
- Narrative generation (agents)
- Moment rendering (frontend)

## Key Operations

| Operation | Purpose |
|-----------|---------|
| Traverse | Walk moment connections |
| Query | Find moments by criteria |
| Path | Find routes between moments |
| Surface | Retrieve narrative-relevant moments |
