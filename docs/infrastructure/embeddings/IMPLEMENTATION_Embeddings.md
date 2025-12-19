# Embeddings - Implementation: Embedding Service Architecture

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Embeddings.md
BEHAVIORS:      ./BEHAVIORS_Embeddings.md
ALGORITHM:      ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:     ./VALIDATION_Embeddings.md
THIS:           IMPLEMENTATION_Embeddings.md
TEST:           ./TEST/TEST_Overview.md
SYNC:           ./SYNC_Embeddings.md

IMPL:           ../../../engine/infrastructure/embeddings/service.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/
└── embeddings/
    ├── __init__.py      # Public exports for EmbeddingService
    └── service.py       # Core embedding service implementation
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| engine/infrastructure/embeddings/__init__.py | Public API exports and usage docs | `EmbeddingService`, `get_embedding_service` | ~20 | OK |
| engine/infrastructure/embeddings/service.py | Embedding generation and similarity helpers | `EmbeddingService`, `get_embedding_service` | ~173 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Service module (utility layer)

**Why this pattern:** The module provides pure embedding operations with minimal state, making it a shared infrastructure service across the engine.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Singleton | `service.py:get_embedding_service` | Avoid repeated model loading |
| Lazy initialization | `engine/infrastructure/embeddings/service.py:EmbeddingService._load_model` | Load large model only when needed |

### Anti-Patterns to Avoid

- **Embedding model re-loads**: Avoid instantiating `SentenceTransformer` per call; use the singleton.
- **Graph coupling**: Do not add graph storage logic here; keep it a pure embedding service.
- **Silent empty vectors**: Avoid masking errors when text is missing; keep explicit empty vector behavior.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Embedding service | Model loading, text embedding, similarity math | Graph indexing, storage, search, and persistence | `EmbeddingService`, `get_embedding_service` |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `engine/infrastructure/embeddings/service.py:EmbeddingService.embed` | `engine/infrastructure/embeddings/service.py:48` | Any call needing a single embedding |
| `engine/infrastructure/embeddings/service.py:EmbeddingService.embed_batch` | `engine/infrastructure/embeddings/service.py:64` | Batch embedding for multiple texts |
| `engine/infrastructure/embeddings/service.py:EmbeddingService.embed_node` | `engine/infrastructure/embeddings/service.py:84` | Node embedding request |
| `engine/infrastructure/embeddings/service.py:EmbeddingService.similarity` | `engine/infrastructure/embeddings/service.py:135` | Similarity scoring |
| `get_embedding_service` | `engine/infrastructure/embeddings/service.py:147` | Shared singleton access |

---

## DATA FLOW

### Embed Text: Single Input

```
Caller
  └─> EmbeddingService.embed(text)
        ├─> _load_model()  # lazy load SentenceTransformer
        └─> model.encode(text) -> vector
              └─> list[float] returned
```

### Embed Node: Node-Specific Text

```
Caller
  └─> EmbeddingService.embed_node(node)
        ├─> _node_to_text(node, node_type)
        └─> embed(text) -> vector
              └─> list[float] returned
```

### Similarity: Cosine Score

```
Caller
  └─> EmbeddingService.similarity(vec1, vec2)
        └─> cosine similarity via numpy
              └─> float score
```

---

## SCHEMA

### Core Fields

| Field | Type | Owner | Notes |
|-------|------|-------|-------|
| `embedding` | `list[float]` | Node/Link attribute | 768-dim vector (all-mpnet-base-v2) stored on graph entities |
| `dimension` | `int` | EmbeddingService | Mirrors model dimension for empty-vector padding |
| `model_name` | `str` | EmbeddingService | HuggingFace model identifier used for encoding |

### Text Inputs

| Source | Fields | Notes |
|--------|--------|-------|
| Node dict | `name`, `content`, `description`, and type-specific fields | `_node_to_text` builds a composite string from known keys |
| Direct text | `text` | `embed()` expects non-empty text or returns a zero vector |

---

## LOGIC CHAINS

### Single Embed Path

```
Caller -> EmbeddingService.embed(text)
       -> _load_model() (lazy)
       -> SentenceTransformer.encode(normalize=True)
       -> list[float] returned to caller
```

### Node Embed Path

```
Caller -> EmbeddingService.embed_node(node)
       -> _node_to_text(node, node_type)
       -> embed(text)
       -> list[float] returned to caller
```

### Similarity Path

```
Caller -> EmbeddingService.similarity(vec1, vec2)
       -> numpy dot/norm
       -> float score returned to caller
```

These chains describe the current implementation only; no graph writes or
indexing are performed in this module.

---

## MODULE DEPENDENCIES

### Internal Dependencies

No internal engine modules are required; the service stays self-contained and
only depends on its own module-level singleton state.

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `sentence-transformers` | Embedding model and encoding | `engine/infrastructure/embeddings/service.py` |
| `numpy` | Cosine similarity math | `engine/infrastructure/embeddings/service.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| `_embedding_service` | `engine/infrastructure/embeddings/service.py` module global | Module | Process lifetime |
| `model` | `engine/infrastructure/embeddings/service.py:EmbeddingService.model` | Instance | Loaded on first call |
| `dimension` | `engine/infrastructure/embeddings/service.py:EmbeddingService.dimension` | Instance | Set on model load |

---

## CONCURRENCY MODEL

The module exposes a process-wide singleton without explicit locking. In
multi-threaded contexts, concurrent calls can race on first-time model load,
but the load is idempotent and subsequent calls reuse the shared model
instance. Callers should treat `EmbeddingService` as read-only once initialized.

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Caller requests EmbeddingService or get_embedding_service()
2. Service constructed with model name
3. Model loads lazily on first embed call
```

### Main Call Flow

```
1. Input text or node supplied
2. _load_model ensures SentenceTransformer is ready
3. model.encode returns normalized vector
4. Vector returned to caller
```

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `model_name` | `engine/infrastructure/embeddings/service.py:EmbeddingService.__init__` | `sentence-transformers/all-mpnet-base-v2` | HuggingFace model selection |

---

## BIDIRECTIONAL LINKS

### Code -> Docs

DOCS references exist in both `engine/infrastructure/embeddings/__init__.py`
and `engine/infrastructure/embeddings/service.py` to make `ngram context`
resolve the module documentation chain.

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| Embedding generation | `engine/infrastructure/embeddings/service.py:41` |
| Batch embedding | `engine/infrastructure/embeddings/service.py:62` |
| Node-to-text mapping | `engine/infrastructure/embeddings/service.py:89` |
| Similarity scoring | `engine/infrastructure/embeddings/service.py:125` |

---

## GAPS / IDEAS / QUESTIONS

### Missing Implementation

- [ ] `index_node()` and `index_link()` per docs (see SYNC)
- [ ] Vector index integration for search

### Questions

- QUESTION: Should `embed_node()` remain once indexing is updated to detail/name rules?
