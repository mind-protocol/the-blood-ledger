# Embeddings — Sync: Current State

```
LAST_UPDATED: 2024-12-16
UPDATED_BY: Claude (documentation session)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Core embedding via sentence-transformers (all-mpnet-base-v2, 768 dims)
- embed(), embed_batch(), embed_node() in EmbeddingService
- Lazy model loading
- Cosine similarity computation

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

**Existing Implementation:** `engine/embeddings/service.py`

The current EmbeddingService provides:
- `embed(text)` — Generate 768-dim vector
- `embed_batch(texts)` — Batch embedding
- `embed_node(node)` — Type-specific text generation from node fields
- `similarity(v1, v2)` — Cosine similarity

**What's Missing (per new spec):**

| Feature | Current | Needed |
|---------|---------|--------|
| Node embedding | embed_node() combines fields | detail > 20 (fallback name > 20) → node.embedding |
| Link embedding | Not implemented | detail > 20 → link.embedding |
| Storage | N/A | Embedding as attribute on node/link |
| Vector index | N/A | One index per node label |

---

## IN PROGRESS

### Documentation Creation

- **Started:** 2024-12-16
- **By:** Claude
- **Status:** Complete
- **Context:** Created full documentation chain based on new embedding spec

---

## RECENT CHANGES

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

**Where I stopped:** Documentation complete. Implementation needs updating.

**What you need to understand:**
- Current `engine/embeddings/service.py` works but doesn't match new spec
- New spec: detail > 20 (fallback name > 20), stored as node.embedding attribute
- Links: detail > 20 only (no fallback)
- No conversation embeddings

**Watch out for:**
- Don't break existing embed() and embed_batch() functions
- Return vector or None from index_node/index_link
- Need vector index per node label in FalkorDB

**Open questions I had:**
- Should we keep embed_node() for backwards compatibility?
- How to handle vector index creation on first run?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created complete documentation for the Embedding System based on the new "embed every detail > 20 chars" spec. Current implementation (engine/embeddings/service.py) provides the core embedding functionality but needs refactoring to match the new universal `detail` field approach.

**Decisions made:**
- New subfolder docs/infrastructure/embeddings/ (distinct module)
- Documented the target architecture per spec
- Noted gaps between current implementation and spec

**Needs your input:**
- Confirm the implementation plan phases are correct
- Confirm backwards compatibility requirements
- Priority of this refactoring vs other work

---

## TODO

### Immediate

- [ ] Implement `index_node()` — detail > 20 (fallback name), set node.embedding
- [ ] Implement `index_link()` — detail > 20, set link.embedding
- [ ] Create vector indexes per node label

### Later

- [ ] Implement new `search()` with vector index queries
- [ ] Add `index_world()` batch function
- [ ] Hook into graph_ops for automatic indexing

---

## POINTERS

| What | Where |
|------|-------|
| Existing implementation | engine/embeddings/service.py |
| Pattern philosophy | ./PATTERNS_Embeddings.md |
| Observable behaviors | ./BEHAVIORS_Embeddings.md |
| Indexing/search procedures | ./ALGORITHM_Embeddings.md |
| Test invariants | ./VALIDATION_Embeddings.md |
| Test cases | ./TEST_Embeddings.md |
| Graph queries (has search) | engine/db/graph_queries.py |
| History conversations | engine/history/conversations.py |
