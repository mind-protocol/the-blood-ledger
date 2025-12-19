# Map System — Implementation: Semantic Search Code Architecture

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Map.md
BEHAVIORS:      ./BEHAVIORS_Map.md
ALGORITHM:      ./ALGORITHM_Rendering.md
VALIDATION:     ./VALIDATION_Map_Invariants.md
THIS:           IMPLEMENTATION_Map_Code_Architecture.md
TEST:           ./TEST_Map_Test_Coverage.md
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
        ├── __init__.py          # Re-exports SemanticSearch API
        └── semantic.py          # Semantic search implementation
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/world/map/__init__.py` | Public API re-export | `SemanticSearch`, `get_semantic_search` | ~20 | OK |
| `engine/world/map/semantic.py` | Embedding-driven search and fallback logic | `SemanticSearch`, `get_semantic_search` | ~296 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Layered (service wrapper over graph + embeddings)

**Why this pattern:** Keeps semantic search API small while delegating storage and embedding concerns to existing services.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Singleton | `semantic.py:get_semantic_search` | Shared SemanticSearch instance per process |
| Adapter | `SemanticSearch` | Wraps GraphQueries/embeddings behind map-friendly API |

### Anti-Patterns to Avoid

- **God Object**: Avoid adding map rendering or visibility logic here; keep it search-only.
- **Premature Abstraction**: Avoid new helper layers until multiple callers need them.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Semantic search layer | Query embedding + graph search | Graph storage details, embedding implementation | `SemanticSearch` methods |

---

## SCHEMA

### SearchResult

```yaml
SearchResult:
  required:
    - id: string          # Node id
    - name: string        # Node name
    - type: string        # Node type (place, narrative, etc.)
    - similarity: float   # Similarity score
  optional:
    - content: string
    - description: string
    - wound: string
    - why_here: string
    - mood: string
    - tone: string
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `SemanticSearch` | `engine/world/map/semantic.py:20` | Direct instantiation or via helper |
| `get_semantic_search` | `engine/world/map/semantic.py:289` | Callers needing singleton access |

---

## DATA FLOW

### Query Search Flow: Natural Language Query

```
┌─────────────────┐
│  Caller Query   │
└────────┬────────┘
         │ text
         ▼
┌─────────────────┐
│ SemanticSearch  │ ← embeds query
│ semantic.py     │
└────────┬────────┘
         │ embedding
         ▼
┌─────────────────┐
│ GraphQueries    │ ← vector search or fallback
│ physics/graph   │
└────────┬────────┘
         │ rows
         ▼
┌─────────────────┐
│ Filter + Limit  │
│ semantic.py     │
└────────┬────────┘
         │ results
         ▼
┌─────────────────┐
│   Caller        │
└─────────────────┘
```

---

## LOGIC CHAINS

### LC1: find()

**Purpose:** Return nodes similar to a natural language query.

```
query
  → engine/world/map/semantic.py (SemanticSearch.find)
    → embeddings.embed()
      → SemanticSearch._vector_search()
        → GraphQueries.query()
      → filter by similarity + limit
        → results
```

**Data transformation:**
- Input: `str` — raw query
- After embed: `List[float]` — embedding vector
- After query: `List[Dict[str, Any]]` — raw results with scores
- Output: filtered `List[Dict[str, Any]]`

### LC2: find_similar()

**Purpose:** Return nodes similar to a given node id.

```
node_id
  → SemanticSearch._get_node_with_embedding()
    → GraphQueries.query()
      → SemanticSearch._vector_search()
        → filter out node_id
          → results
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/world/map/semantic.py
    ├── imports → engine.infrastructure.embeddings
    └── imports → engine.physics.graph
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `logging` | Module logging | `engine/world/map/semantic.py` |
| `typing` | Type hints | `engine/world/map/semantic.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| `_semantic_search` | `engine/world/map/semantic.py:_semantic_search` | module-global | Process lifetime |

### State Transitions

```
None ──get_semantic_search()──▶ SemanticSearch instance
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. get_semantic_search() checks module singleton
2. engine/world/map/semantic.py (SemanticSearch.__init__) creates GraphQueries + embedding service
3. Instance ready for queries
```

### Request Cycle

```
1. Caller invokes find/find_similar
2. Embedding generated or retrieved
3. Graph query executed
4. Results filtered and returned
```

---

## CONCURRENCY MODEL

Synchronous. No explicit threading or async handling.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `graph_name` | `engine/world/map/semantic.py (SemanticSearch.__init__)` | `blood_ledger` | FalkorDB graph name |
| `host` | `engine/world/map/semantic.py (SemanticSearch.__init__)` | `localhost` | FalkorDB host |
| `port` | `engine/world/map/semantic.py (SemanticSearch.__init__)` | `6379` | FalkorDB port |
| `min_similarity` | `engine/world/map/semantic.py (SemanticSearch.find)` | 0.3 | Similarity filter threshold |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `engine/world/map/semantic.py` | 6 | Docstring references `docs/world/map/PATTERNS_Map.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| BEHAVIORS: visibility update rules | Not implemented in code yet |
| ALGORITHM: rendering layers | Not implemented in code yet |
| Semantic search interface | `engine/world/map/semantic.py (SemanticSearch)` |

---

## GAPS / IDEAS / QUESTIONS

### Missing Implementation

- [ ] Implement visual map rendering (frontend canvas layers).
- [ ] Implement visibility/knowledge system per playthrough.
- [ ] Implement map data loading for places/routes.

### Questions

- QUESTION: Should semantic search include place-specific filters by default?
