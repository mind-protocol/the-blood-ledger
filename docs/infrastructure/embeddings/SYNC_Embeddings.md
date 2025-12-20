# Embeddings — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: CANONICAL
```

---

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- EmbeddingService API surface (embed, embed_batch, similarity, singleton)
  is stable and in active use for semantic search helpers.

What's still being designed:
- The attribute-based indexing flow (detail > 20 fallback) remains a planned
  alignment task and is not yet reflected in the runtime implementation.

What's proposed (v2):
- Optional automated indexing hooks that update embeddings on graph writes.

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

No active work on embeddings module, but the next planned step is aligning
runtime indexing behavior with the documented detail-first embedding spec.

## RECENT CHANGES

- Added `HEALTH_Embeddings.md` to document runtime verification and gaps.

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

### Later

- [ ] Implement new `search()` with vector index queries
- [ ] Add `index_world()` batch function
- [ ] Hook into graph_ops for automatic indexing

---

## CONSCIOUSNESS TRACE

This update focuses only on template alignment (adding maturity/trace and
expanding the in-progress note) without changing the module's behavior.
Revalidated the sync sections for repair #16 after the edit.

---

## POINTERS

| What | Where |
|------|-------|
| Implementation | engine/infrastructure/embeddings/service.py |
| Module init | engine/infrastructure/embeddings/__init__.py |
| Pattern philosophy | ./PATTERNS_Embeddings.md |
| Observable behaviors | ./BEHAVIORS_Embeddings.md |
| Indexing/search procedures | ./ALGORITHM/ALGORITHM_Overview.md |
| Test invariants | ./VALIDATION_Embeddings.md |
| Test cases | ./TEST/TEST_Overview.md |
| Graph queries (has search) | Graph runtime in ngram repo (see `data/ARCHITECTURE — Cybernetic Studio.md`) |
| History conversations | engine/infrastructure/history/conversations.py |


---

## ARCHIVE

Older content archived to: `SYNC_Embeddings_archive_2025-12.md` and `archive/SYNC_archive_2024-12.md`

---

## Agent Observations

### Remarks
- Split documents keep entry points readable while preserving details in the archive.
- Implementation doc now documents schema, logic chains, and concurrency notes.

### Suggestions
- [ ] Add a brief cross-link from VALIDATION to the archive if more test cases are migrated.

### Propositions
- None.


---

## ARCHIVE

Older content archived to: `SYNC_Embeddings_archive_2025-12.md`
