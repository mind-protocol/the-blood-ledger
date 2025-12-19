# Archived: SYNC_Embeddings.md

Archived on: 2025-12-19
Original file: SYNC_Embeddings.md

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
  - docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Overview.md
  - docs/infrastructure/embeddings/VALIDATION_Embeddings.md
  - docs/infrastructure/embeddings/TEST/TEST_Overview.md
  - docs/infrastructure/embeddings/SYNC_Embeddings.md
- **Insights:** Current implementation is good foundation but needs refactoring for new spec

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

