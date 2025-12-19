# Embeddings — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Claude (repair agent)
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- Core embedding via sentence-transformers (all-mpnet-base-v2, 768 dims)
- embed(), embed_batch(), embed_node() in EmbeddingService
- Lazy model loading
- Cosine similarity computation
- Code location: `engine/infrastructure/embeddings/`

**What's still being designed:**
- One embedding per node: detail > 20 (fallback to name > 20)
- Embedding stored as node.embedding attribute
- Link embedding (detail > 20 only)
- Vector index per node label

**What's proposed (v2+):**
- Hybrid search (vector + keyword)
- Embedding versioning (track model changes)
- Automatic re-indexing on detail updates

---

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/embeddings/service.py`

The current EmbeddingService provides:
- `embed(text)` — Generate 768-dim vector
- `embed_batch(texts)` — Batch embedding
- `embed_node(node)` — Type-specific text generation from node fields
- `similarity(v1, v2)` — Cosine similarity
- `get_embedding_service()` — Singleton accessor

**What's Missing (per new spec):**

| Feature | Current | Needed |
|---------|---------|--------|
| Node embedding | embed_node() combines fields | detail > 20 (fallback name > 20) → node.embedding |
| Link embedding | Not implemented | detail > 20 → link.embedding |
| Storage | N/A | Embedding as attribute on node/link |
| Vector index | N/A | One index per node label |

---

## IN PROGRESS

No active work on embeddings module.

---

## RECENT CHANGES

### 2025-12-19: SYNC Refresh & Path Update

- **What:** Updated SYNC to reflect code restructuring
- **By:** repair agent
- **Changes:**
  - Updated all paths from `engine/embeddings/` to `engine/infrastructure/embeddings/`
  - Changed STATUS from DESIGNING to CANONICAL (per modules.yaml)
  - Code functionality unchanged — core service works, spec gaps remain

### 2024-12-16: Documentation Created

- **What:** Created docs/infrastructure/embeddings/ with full PATTERN → TEST chain
- **Why:** New embedding spec introduces universal `detail` field approach
- **Files:**
  - docs/infrastructure/embeddings/PATTERNS_Embeddings.md
  - docs/infrastructure/embeddings/BEHAVIORS_Embeddings.md
  - docs/infrastructure/embeddings/ALGORITHM_Embeddings.md
  - docs/infrastructure/embeddings/VALIDATION_Embeddings.md
  - docs/infrastructure/embeddings/TEST_Embeddings.md
  - docs/infrastructure/embeddings/SYNC_Embeddings.md
- **Insights:** Current implementation is good foundation but needs refactoring for new spec

---

## KNOWN ISSUES

### Implementation Doesn't Match New Spec

- **Severity:** Medium (feature gap, not bug)
- **Symptom:** Current embed_node() combines fields; new spec: detail > 20 (fallback name), stored as attribute
- **Suspected cause:** Original design predates attribute-based embedding decision
- **Action needed:** Refactor to new spec

### No Link Embedding

- **Severity:** Medium (missing functionality)
- **Symptom:** Can't search link details
- **Action needed:** Implement index_link()

### No Separate Embedding Storage — RESOLVED

- **Status:** By design
- **Decision:** Embeddings stored as node/link attributes, not separate nodes
- **No action needed**

### Stale Paths in Other Docs

- **Severity:** Low (documentation drift)
- **Symptom:** Other docs in this folder still reference old path `engine/embeddings/`
- **Files affected:** ALGORITHM, BEHAVIORS, PATTERNS, TEST, VALIDATION
- **Action needed:** Update IMPL: references in other docs

---

## IMPLEMENTATION PLAN

### Phase 1: Update Models (Low Effort)

1. Ensure all node/link types have `detail` field
2. Add `detail` to nodes.py and links.py if missing

### Phase 2: Update EmbeddingService (Medium Effort)

1. Add `index_node(node)` — embed detail (fallback name), set node.embedding
2. Add `index_link(link)` — embed detail, set link.embedding
3. Return vector or None from index functions

### Phase 3: Vector Indexes (Low Effort)

1. Create vector index per node label (Narrative, Character, Place, Tension)
2. Create vector index for links if supported

### Phase 4: Integration (Low Effort)

1. Hook into graph_ops to index on node/link create
2. Add `index_world()` for batch indexing

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Documentation refreshed, paths updated. Implementation needs updating.

**What you need to understand:**
- Code is at `engine/infrastructure/embeddings/service.py` (174 lines)
- Current implementation works but doesn't match new spec
- New spec: detail > 20 (fallback name > 20), stored as node.embedding attribute
- Links: detail > 20 only (no fallback)
- No conversation embeddings

**Watch out for:**
- Don't break existing embed() and embed_batch() functions
- Return vector or None from index_node/index_link
- Need vector index per node label in FalkorDB
- Other docs in this folder have stale paths (see Known Issues)

**Open questions I had:**
- Should we keep embed_node() for backwards compatibility?
- How to handle vector index creation on first run?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Embeddings module is canonical and working. Core service provides embed(), embed_batch(), embed_node(), and similarity(). Code location updated during project restructure from `engine/embeddings/` to `engine/infrastructure/embeddings/`. The "embed every detail > 20 chars" spec has not yet been implemented.

**Decisions made:**
- Path references updated to new location
- Module marked CANONICAL per modules.yaml (core functionality works)

**Needs your input:**
- Priority of implementing the detail > 20 spec vs other work
- Backwards compatibility requirements for embed_node()

---

## TODO

### Immediate

- [ ] Implement `index_node()` — detail > 20 (fallback name), set node.embedding
- [ ] Implement `index_link()` — detail > 20, set link.embedding
- [ ] Create vector indexes per node label
- [ ] Update path references in other docs (ALGORITHM, BEHAVIORS, PATTERNS, TEST, VALIDATION)

### Later

- [ ] Implement new `search()` with vector index queries
- [ ] Add `index_world()` batch function
- [ ] Hook into graph_ops for automatic indexing

---

## POINTERS

| What | Where |
|------|-------|
| Implementation | engine/infrastructure/embeddings/service.py |
| Module init | engine/infrastructure/embeddings/__init__.py |
| Pattern philosophy | ./PATTERNS_Embeddings.md |
| Observable behaviors | ./BEHAVIORS_Embeddings.md |
| Indexing/search procedures | ./ALGORITHM_Embeddings.md |
| Test invariants | ./VALIDATION_Embeddings.md |
| Test cases | ./TEST_Embeddings.md |
| Graph queries (has search) | engine/physics/graph/graph_queries.py |
| History conversations | engine/infrastructure/history/conversations.py |
