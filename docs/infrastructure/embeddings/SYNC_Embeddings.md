# Embeddings — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: CANONICAL
```

---

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/embeddings/service.py`

The current EmbeddingService provides:
- `embed(text)` — Generate 768-dim vector
- `embed_batch(texts)` — Batch embedding
- `embed_node(node)` — Type-specific text generation from node fields
- `similarity(v1, v2)` — Cosine similarity
- `get_embedding_service()` — Singleton accessor

Documentation chain now includes an IMPLEMENTATION doc with file-level responsibilities and
updated IMPL paths.

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

## RECENT CHANGES

### 2025-12-19: Normalize embeddings implementation references

- **What:** Replaced method-only tokens with concrete file paths in the embeddings implementation doc.
- **Why:** Resolve broken implementation links flagged for the embeddings module.
- **Files:** `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Link module init to docs

- **What:** Added a DOCS reference in the embeddings module initializer.
- **Why:** Ensure `ngram context` resolves docs for `engine/infrastructure/embeddings/__init__.py`.
- **Files:** `engine/infrastructure/embeddings/__init__.py`
- **Struggles/Insights:** None.

### 2025-12-19: Documentation mapping and DOCS linkage

- **What:** Added modules.yaml mapping for embeddings and a DOCS reference in the service file.
- **Why:** Connect existing embeddings docs to the code path for `ngram context` and validation coverage.
- **Files:** `modules.yaml`, `engine/infrastructure/embeddings/service.py`
- **Struggles/Insights:** None.

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


---

## ARCHIVE

Older content archived to: `SYNC_Embeddings_archive_2025-12.md`
