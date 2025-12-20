# Embeddings — Implementation: Embedding Service Architecture

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Embeddings.md
BEHAVIORS:      ./BEHAVIORS_Embeddings.md
ALGORITHM:      ./ALGORITHM_Embeddings.md
VALIDATION:     ./VALIDATION_Embeddings.md
THIS:           IMPLEMENTATION_Embeddings.md
HEALTH:         ./HEALTH_Embeddings.md
SYNC:           ./SYNC_Embeddings.md

IMPL:           engine/infrastructure/embeddings/service.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/
└── embeddings/
    ├── __init__.py      # Exports EmbeddingService facade
    └── service.py       # Sentence-transformers wrapper
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/embeddings/service.py` | Vector generation | `EmbeddingService` | ~173 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Singleton Infrastructure Service.

**Why this pattern:** Prevents expensive redundant loading of the 768-dimension transformer model across different parts of the engine.

---

## SCHEMA

### Embedding (Attribute)

```yaml
Embedding:
  required:
    - vector: List[float]       # 768 dimensions
  constraints:
    - Stored as property on Node or Link
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| embed | `service.py:48` | Graph indexers / Search queries |
| embed_node | `service.py:84` | World seeding / mutations |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Text Vectorization: String → Transformer → Vector

This flow handles the conversion of raw game text into high-dimensional vectors for semantic search.

```yaml
flow:
  name: text_vectorization
  purpose: Generate semantic signatures for world data.
  scope: String -> Embedding Model -> Float List
  steps:
    - id: step_1_load
      description: Lazy load the sentence-transformer model.
      file: engine/infrastructure/embeddings/service.py
      function: _load_model
      input: model_name
      output: model instance
      trigger: first embed call
      side_effects: high memory usage (cached)
    - id: step_2_encode
      description: Compute the normalized vector for the input text.
      file: engine/infrastructure/embeddings/service.py
      function: embed
      input: text (str)
      output: vector (List[float])
      trigger: caller request
      side_effects: none
  docking_points:
    guidance:
      include_when: models are loaded or vectors are computed
    available:
      - id: embedding_input
        type: custom
        direction: input
        file: engine/infrastructure/embeddings/service.py
        function: embed
        trigger: caller
        payload: input_text
        async_hook: optional
        needs: none
        notes: Pure string ingestion
      - id: embedding_output
        type: custom
        direction: output
        file: engine/infrastructure/embeddings/service.py
        function: embed
        trigger: return
        payload: List[float]
        async_hook: not_applicable
        needs: none
        notes: Normalized vector ready for graph storage
    health_recommended:
      - dock_id: embedding_output
        reason: Verification of vector dimensionality and consistency.
```

---

## LOGIC CHAINS

### LC1: Node-to-Text Mapping

**Purpose:** Flatten structured graph data into a searchable string.

```
Node (Character/Place/Thing)
  → service.py:_node_to_text()
    → Joined string of name + backstory + significance
      → service.py:embed()
        → vector
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

None. The service is a leaf-node in the dependency graph.

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| sentence-transformers | Embedding model and encoding | `service.py` |
| numpy | Similarity math | `service.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Transformer Model | `EmbeddingService.model` | process | created once, kept in memory |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Model Load | Sync/Lazy | Idempotent load on first call |
| Inference | Sync | Model.encode is typically CPU/GPU bound |
