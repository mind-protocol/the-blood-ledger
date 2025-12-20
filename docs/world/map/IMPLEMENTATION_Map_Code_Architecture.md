# Map System — Implementation: Semantic Search Code Architecture

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Map.md
BEHAVIORS:      ./BEHAVIORS_Map.md
ALGORITHM:      ./ALGORITHM_Map.md
VALIDATION:     ./VALIDATION_Map_Invariants.md
THIS:           IMPLEMENTATION_Map_Code_Architecture.md
HEALTH:         ./HEALTH_Map.md
SYNC:           ./SYNC_Map.md

IMPL:           engine/world/map/semantic.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/
└── world/
    └── map/
        ├── __init__.py          # Exports SemanticSearch facade
        └── semantic.py          # Embedding-driven search implementation
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/world/map/semantic.py` | Embedding-driven search and fallback logic | `SemanticSearch` | ~296 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Adapter.

**Why this pattern:** Wraps GraphQueries (ngram repo graph runtime) and EmbeddingService behind a map-specific API, isolating the search logic from the underlying storage and vector compute implementations.

---

## SCHEMA

### SearchResult (JSON/Dict)

```yaml
SearchResult:
  required:
    - id: string          # Node id
    - name: string        # Node name
    - type: string        # Node type
    - similarity: float   # 0.0-1.0 score
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| find | `semantic.py:65` | Map search UI / CLI |
| find_similar | `semantic.py:120` | Recommendation engine / context builder |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Semantic Search: Query → Embedding → Graph Results

This flow handles natural language queries from the player, transforming them into vector searches against the world graph.

```yaml
flow:
  name: semantic_search
  purpose: Find world entities relevant to player intent.
  scope: String Query -> Vector Embedding -> Vector Search -> Sorted Results
  steps:
    - id: step_1_embed
      description: Convert query text into a high-dimensional vector.
      file: engine/infrastructure/embeddings/service.py
      function: embed
      input: text (str)
      output: vector (List[float])
      trigger: SemanticSearch.find call
      side_effects: none
    - id: step_2_search
      description: Query FalkorDB for nodes near the query vector.
      file: engine/world/map/semantic.py
      function: _vector_search
      input: vector
      output: results (List[Dict])
      trigger: find workflow
      side_effects: none
    - id: step_3_fallback
      description: Fall back to keyword/brute-force search if index fails.
      file: engine/world/map/semantic.py
      function: _fallback_search
      input: query, vector
      output: results (List[Dict])
      trigger: vector_search failure
      side_effects: none
  docking_points:
    guidance:
      include_when: embeddings are generated or search results are ranked
    available:
      - id: search_input
        type: api
        direction: input
        file: engine/world/map/semantic.py
        function: find
        trigger: UI/Caller
        payload: {query, min_similarity}
        async_hook: optional
        needs: none
        notes: Entry for natural language discovery
      - id: search_output
        type: custom
        direction: output
        file: engine/world/map/semantic.py
        function: find
        trigger: return statement
        payload: List[SearchResult]
        async_hook: required
        needs: none
        notes: Ranked results returned to requester
    health_recommended:
      - dock_id: search_output
        reason: Verification of embedding relevance and search sorting.
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/world/map/semantic.py
    ├── imports → engine.infrastructure.embeddings
    └── imports → engine.physics.graph
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Singleton Instance | `semantic.py:_semantic_search` | process | created on first request |
