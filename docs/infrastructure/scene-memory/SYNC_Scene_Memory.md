# Scene Memory System — Sync

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: CANONICAL
```

===============================================================================
## DOCUMENT CHAIN
===============================================================================

| Document | Status | Purpose |
|----------|--------|---------|
| PATTERNS_Scene_Memory.md | Superseded | Original design - now Moment Graph |
| BEHAVIORS_Scene_Memory.md | Superseded | Original behaviors - evolved |
| ALGORITHM_Scene_Memory.md | Superseded | Original algorithm - replaced |
| VALIDATION_Scene_Memory.md | Superseded | Original validation - needs update |
| IMPLEMENTATION_Scene_Memory.md | Current | MomentProcessor architecture and data flow |
| TEST_Scene_Memory.md | Draft | Test coverage for moment processing |
| SYNC_Scene_Memory.md | Current | This file — state tracking |

**NOTE:** The original "Scene Memory" design evolved into the **Moment Graph** architecture.
The Scene node type was replaced by individual Moment nodes with graph-based relationships.
See `docs/physics/` for current Moment Graph documentation.

===============================================================================
## ARCHITECTURE EVOLUTION
===============================================================================

**Original Design (2024-12):** Scene-based memory with Scene containers holding Moments

**Current Design (2025):** Moment Graph architecture
- No Scene container nodes
- Moments are first-class nodes with lifecycle states
- Weight-based surfacing instead of scene containers
- Click traversal with <50ms target
- Persistence via dormant/reactivate states

===============================================================================
## IMPLEMENTATION STATUS
===============================================================================

| Component | Status | Location |
|-----------|--------|----------|
| Moment model | **CANONICAL** | `engine/models/nodes.py:189` |
| MomentProcessor | **CANONICAL** | `engine/infrastructure/memory/moment_processor.py` |
| Graph moment ops | **CANONICAL** | `engine/physics/graph/graph_ops.py:792` (add_moment) |
| Moment lifecycle | **CANONICAL** | `engine/physics/graph/graph_ops_moments.py` |
| Moment queries | **CANONICAL** | `engine/physics/graph/graph_queries_moments.py` |
| Moment Graph engine | **CANONICAL** | `engine/moment_graph/` |
| API endpoints | **CANONICAL** | `engine/infrastructure/api/moments.py` |
| Tests | **CANONICAL** | `engine/tests/test_moment*.py` (5 files) |
| Embeddings | **CANONICAL** | Generated for text > 20 chars |

===============================================================================
## LINK TYPES (IMPLEMENTED)
===============================================================================

| Link | Purpose | Status |
|------|---------|--------|
| `Character -[CAN_SPEAK]-> Moment` | Who can say this | CANONICAL |
| `Character -[SAID]-> Moment` | Who said this (after spoken) | CANONICAL |
| `Moment -[ATTACHED_TO]-> *` | Presence gating | CANONICAL |
| `Moment -[CAN_LEAD_TO]-> Moment` | Click traversal | CANONICAL |
| `Moment -[THEN]-> Moment` | Sequence after spoken | CANONICAL |
| `Moment -[AT]-> Place` | Location | CANONICAL |
| `Narrative -[FROM]-> Moment` | Source attribution | CANONICAL |

===============================================================================
## INTEGRATION POINTS
===============================================================================

| System | Integration | Status |
|--------|-------------|--------|
| Narrator orchestration | Uses MomentProcessor for output | CANONICAL |
| Graph ops | add_moment, handle_click, etc. | CANONICAL |
| Embeddings service | Called for text > 20 chars | CANONICAL |
| Moments API | REST endpoints for frontend | CANONICAL |
| Moment Graph engine | Traversal, queries, surfacing | CANONICAL |

===============================================================================
## DECISIONS MADE (HISTORICAL)
===============================================================================

| Decision | Rationale |
|----------|-----------|
| No Scene containers | Moments are independent; graph topology provides context |
| Moment Graph architecture | Enables <50ms click response without LLM |
| Weight-based surfacing | Probabilistic selection based on graph topology |
| Status lifecycle | possible → active → spoken (or dormant/decayed) |
| Transcript.json | Preserves full history for playthrough |
| FROM links for attribution | Graph relationships, not embedded arrays |
| SAID links for dialogue | Query "what did X say?" directly |
| THEN links for sequence | Preserve moment order |

===============================================================================
## OPEN QUESTIONS
===============================================================================

- [ ] Should PATTERNS/BEHAVIORS/ALGORITHM/VALIDATION docs be updated to match Moment Graph?
- [ ] Are original Scene-based docs still needed or should they be deprecated?

===============================================================================
## CONFLICTS
===============================================================================

### DECISION: Moment Processor Incomplete Impl
- Conflict: Repair task flagged `_write_transcript`, `last_moment_id`,
  `transcript_line_count`, and `get_moment_processor` as incomplete, but the file
  already contains functional implementations.
- Resolution: Treat the issue as already resolved; no code changes.
- Reasoning: Each function provides concrete behavior used by the moment
  processing flow and transcript management.
- Updated: `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`

===============================================================================
## Agent Observations
===============================================================================

### Remarks
- Repair task appears stale relative to `engine/infrastructure/memory/moment_processor.py`.
- Added IMPLEMENTATION/TEST docs and DOCS reference for the module.
- Added a DOCS reference in `engine/infrastructure/memory/__init__.py` so package-level context points to scene-memory docs.

===============================================================================
## RECENT CHANGES
===============================================================================

### 2025-12-19: Normalized code structure paths in implementation doc
- **What:** Rewrote the code structure tree to use full file paths.
- **Why:** Prevent bare filename references from being flagged as broken links.
- **Files:** `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md`

### 2025-12-19: Fixed broken implementation doc references
- **What:** Replaced method/attribute-only references with concrete file paths
  and line anchors, and removed non-existent extraction target paths from the
  implementation doc.
- **Why:** Clear broken-link checks for the scene-memory implementation doc.
- **Files:** `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md`

### 2025-12-19: Updated scene-memory test path in modules.yaml
- **What:** Switched the scene-memory `tests` entry from a glob to the concrete
  file `engine/tests/test_moment.py`.
- **Why:** `ngram validate` treats glob strings as literal paths; pointing to an
  existing test file avoids YAML drift.
- **Files:** `modules.yaml`

### 2025-12-19: Rechecked moment processor helpers for current repair run
- **What:** Confirmed `_write_transcript`, `last_moment_id`,
  `transcript_line_count`, and `get_moment_processor` are already implemented in
  `engine/infrastructure/memory/moment_processor.py`.
- **Why:** The INCOMPLETE_IMPL alert remains stale; no code changes required.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Logged moment processor helper verification for repair 02
- **What:** Verified the helper implementations flagged by the repair task remain
  complete (`_write_transcript`, `last_moment_id`, `transcript_line_count`,
  `get_moment_processor`).
- **Why:** This repair run confirms the INCOMPLETE_IMPL alert is stale.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Rechecked moment processor helper implementations for current repair run
- **What:** Confirmed `_write_transcript`, `last_moment_id`, `transcript_line_count`,
  and `get_moment_processor` are already implemented in
  `engine/infrastructure/memory/moment_processor.py`.
- **Why:** The INCOMPLETE_IMPL alert is stale for this repair task.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Revalidated moment processor helpers for current repair run
- **What:** Rechecked `_write_transcript`, `last_moment_id`,
  `transcript_line_count`, and `get_moment_processor`; all implementations
  remain present.
- **Why:** Confirm the INCOMPLETE_IMPL alert is stale for this repair task.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Reconfirmed moment processor implementations
- **What:** Rechecked the helper implementations flagged by the repair task;
  no missing bodies were found.
- **Why:** This repair run validates the INCOMPLETE_IMPL alert is stale.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Reverified moment processor helpers for repair 03
- **What:** Checked `_write_transcript`, `last_moment_id`,
  `transcript_line_count`, and `get_moment_processor` in
  `engine/infrastructure/memory/moment_processor.py`; all implementations are
  present.
- **Why:** Confirm the INCOMPLETE_IMPL report is stale.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Reconfirmed moment processor implementations for repair 02
- **What:** Rechecked the same helper implementations flagged in this repair run;
  no empty bodies were found.
- **Why:** Validate the INCOMPLETE_IMPL alert remains stale.
- **Files:** `engine/infrastructure/memory/moment_processor.py`

### 2025-12-19: Added DOCS references for memory module entry points
- **What:** Added `# DOCS: docs/infrastructure/scene-memory/` to
  `engine/infrastructure/memory/__init__.py` and standardized the comment in
  `engine/infrastructure/memory/moment_processor.py`.
- **Why:** Ensure `ngram` doc mapping resolves both files in the module.
- **Files:** `engine/infrastructure/memory/__init__.py`,
  `engine/infrastructure/memory/moment_processor.py`


---

## ARCHIVE

Older content archived to: `SYNC_Scene_Memory_archive_2025-12.md`
