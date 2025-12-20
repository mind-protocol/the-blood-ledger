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

## CURRENT STATE

Archive snapshot of the embeddings module SYNC as of 2025-12-19, reflecting
canonical status in modules.yaml and a stable service implementation with
remaining spec-alignment work noted in the implementation plan below. This
snapshot is for reference only and does not imply current execution status.

---

## IN PROGRESS

No active in-progress work tracked in this archived snapshot; open items remain
in the implementation plan and TODO sections for future follow-up.

---

## KNOWN ISSUES

Specification alignment is incomplete: node/link embedding rules (detail/name
thresholds, per-label indexes) are documented but not yet enforced in code.

---

## HANDOFF: FOR AGENTS

If revisiting embeddings, start from the current SYNC and IMPLEMENTATION docs
to confirm the service paths and then decide which Phase 1-4 items to execute.

---

## HANDOFF: FOR HUMAN

This archive is informational only; no new decisions were made beyond logging
the 2025-12-19 path update and canonical status shift in modules.yaml.

---

## TODO

- [ ] Align EmbeddingService behavior with the documented detail/name rules.
- [ ] Define and create vector indexes for node labels and link embeddings.
- [ ] Wire embedding indexing into graph operations or batch ingestion.

---

## CONSCIOUSNESS TRACE

Confidence is moderate: the archive reflects a stable implementation with clear
gaps, but the spec-vs-code alignment should be verified before execution.

---

## POINTERS

- docs/infrastructure/embeddings/PATTERNS_Embeddings.md
- docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md
- docs/infrastructure/embeddings/VALIDATION_Embeddings.md
- docs/infrastructure/embeddings/TEST/TEST_Overview.md

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


---

# Archived: SYNC_Embeddings.md

Archived on: 2025-12-20
Original file: SYNC_Embeddings.md

---

## RECENT CHANGES

### 2025-12-19: Restore maturity and consciousness trace

- **What:** Added MATURITY and CONSCIOUSNESS TRACE sections and expanded the
  IN PROGRESS entry for template alignment.
- **Why:** Resolve DOC_TEMPLATE_DRIFT warning for missing/short sections.
- **Files:** `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Re-verify algorithm entry template compliance

- **What:** Re-checked that the embeddings algorithm entry includes the
  required ALGORITHM and HELPER FUNCTIONS sections; no content edits were needed.
- **Why:** Confirm the DOC_TEMPLATE_DRIFT target is satisfied in the current tree.
- **Files:** `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Verify algorithm entry template completeness

- **What:** Confirmed the embeddings algorithm entry already includes the
  required ALGORITHM and HELPER FUNCTIONS sections.
- **Why:** Close the DOC_TEMPLATE_DRIFT repair after verifying the entry-point
  doc is template-compliant.
- **Files:** `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- **Struggles/Insights:** None.


### 2025-12-19: Fill archive SYNC template sections

- **What:** Added the missing CURRENT STATE, IN PROGRESS, KNOWN ISSUES, handoffs,
  TODO, consciousness trace, and pointers in the 2025-12 embeddings archive.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the archived snapshot while keeping
  the live SYNC focused on active state.
- **Files:** `docs/infrastructure/embeddings/SYNC_Embeddings_archive_2025-12.md`
- **Struggles/Insights:** None.

### 2025-12-19: Expand algorithm entry template sections

- **What:** Added the missing ALGORITHM and HELPER FUNCTIONS sections plus
  expanded overview/data flow content in the embeddings algorithm entry file.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for missing template headings and short
  sections while keeping the sub-docs canonical.
- **Files:** `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Add maturity and consciousness trace

- **What:** Added MATURITY and CONSCIOUSNESS TRACE sections and expanded the
  IN PROGRESS entry for template alignment.
- **Why:** Resolve DOC_TEMPLATE_DRIFT warning for missing/short sections.
- **Files:** `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Expand archive SYNC template sections

- **What:** Filled missing CURRENT STATE, IN PROGRESS, KNOWN ISSUES, handoffs,
  TODO, consciousness trace, and pointers in the embeddings archive SYNC.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the archive snapshot while keeping
  the main SYNC focused on active state.
- **Files:** `docs/infrastructure/embeddings/SYNC_Embeddings_archive_2025-12.md`
- **Struggles/Insights:** None.

### 2025-12-19: Restore missing template sections in archive

- **What:** Added CURRENT STATE, IN PROGRESS, KNOWN ISSUES, handoffs, TODO,
  consciousness trace, and pointers to the 2025-12 archive SYNC.
- **Why:** Resolve DOC_TEMPLATE_DRIFT warning for the embeddings archive.
- **Files:** `docs/infrastructure/embeddings/SYNC_Embeddings_archive_2025-12.md`
- **Struggles/Insights:** None.

### 2025-12-19: Document implementation schema/logic/concurrency

- **What:** Added SCHEMA, LOGIC CHAINS, and CONCURRENCY MODEL sections to the
  embeddings implementation doc; expanded short template entries.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for missing sections in the implementation
  template and keep structure aligned with other infrastructure modules.
- **Files:** `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Fill missing SCOPE in patterns

- **What:** Added the SCOPE section and updated the timestamp in the embeddings
  patterns doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT warning for missing section and short
  template content.
- **Files:** `docs/infrastructure/embeddings/PATTERNS_Embeddings.md`
- **Struggles/Insights:** None.

### 2025-12-19: Split large algorithm/test docs

- **What:** Split ALGORITHM and TEST docs into focused subfiles with concise overviews; moved detailed examples to archive.
- **Why:** Reduce module doc size below threshold and keep entry points readable.
- **Files:** `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`, `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Overview.md`, `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Indexing.md`, `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Search.md`, `docs/infrastructure/embeddings/TEST_Embeddings.md`, `docs/infrastructure/embeddings/TEST/TEST_Overview.md`, `docs/infrastructure/embeddings/TEST/TEST_Cases.md`, `docs/infrastructure/embeddings/archive/SYNC_archive_2024-12.md`
- **Struggles/Insights:** Moved vector index details plus fixture/performance examples into the archive to keep the entry docs concise.

### 2025-12-19: Verify doc size threshold

- **What:** Recounted module docs after the split; total size is now under 50K characters.
- **Why:** Close the LARGE_DOC_MODULE repair requirement for embeddings.
- **Files:** `docs/infrastructure/embeddings/`
- **Struggles/Insights:** None.

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

