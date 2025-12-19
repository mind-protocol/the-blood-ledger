# Archived: SYNC_Physics.md

Archived on: 2025-12-19
Original file: SYNC_Physics.md

---

## MATURITY

STATUS: ARCHIVED. This file is a frozen snapshot from 2025-12-19 and should
not be treated as the live source of truth for the physics module.

## CURRENT STATE

This archive preserves a past physics SYNC state for traceability; it is not
updated and exists only for historical context.

## IN PROGRESS

No active work is tracked in this archive; any new or ongoing physics tasks
belong in the live SYNC file, not here.

## RECENT CHANGES

**2025-12-19: Repair 12 re-verified physics tick energy helpers**
- Confirmed `_flow_energy_to_narratives`, `_propagate_energy`, `_decay_energy`, and `_update_narrative_weights` in `engine/physics/tick.py` already have implementations
- Repair task marked as stale; no runtime changes

**2025-12-19: Reconfirmed moment graph query helpers already implemented**
- Rechecked `get_dormant_moments`, `get_wait_triggers`, and `get_moments_attached_to_tension` in `engine/moment_graph/queries.py`
- Repair task marked as stale; no runtime changes

**2025-12-19: Repair 13 verified physics tick energy helpers already implemented**
- Confirmed `_flow_energy_to_narratives`, `_propagate_energy`, `_decay_energy`, and `_update_narrative_weights` in `engine/physics/tick.py` contain concrete logic
- Repair task marked as stale; no runtime changes

**2025-12-19: Verified moment graph traversal helpers already implemented**
- Confirmed `make_dormant` and `process_wait_triggers` in `engine/moment_graph/traversal.py` already have concrete logic
- Repair task marked as stale; no runtime changes

**2025-12-19: Verified moment graph query helpers already implemented**
- Confirmed `get_dormant_moments`, `get_wait_triggers`, and `get_moments_attached_to_tension` in `engine/moment_graph/queries.py` are implemented
- Repair task marked as stale; no runtime changes

**2025-12-19: Normalized moment graph query row handling**
- `engine/moment_graph/queries.py` now normalizes dict/list query rows for dormant moments, wait triggers, and tension-attached moments
- Keeps traversal/reactivation logic stable across FalkorDB result formats

**2025-12-19: Moment API resolves playthrough graph names from configured directory**
- `engine/infrastructure/api/moments.py` now reads `player.yaml` under the router's `playthroughs_dir` when resolving graph names
- Falls back to `get_playthrough_graph_name()` if no playthrough metadata is present

**2025-12-19: Consolidated physics algorithm docs**
- Merged physics algorithm content into `docs/physics/ALGORITHM_Physics.md`
- Removed standalone ALGORITHM_* docs to keep one canonical algorithm file
- Updated doc references to point at the consolidated algorithm

**2025-12-19: Split graph_ops.py monolith (1094 → 792 lines)**
- Extracted image generation helpers to `graph_ops_image.py` (163 lines)
  - `generate_node_image()`, `get_image_path()`, `_generate_node_image_async()`
  - Async image generation for characters, places, things
- Extracted event emitter to `graph_ops_events.py` (66 lines)
  - `add_mutation_listener()`, `remove_mutation_listener()`, `emit_event()`
  - Used by graph_ops_apply.py for mutation events
- Extracted types/exceptions to `graph_ops_types.py` (59 lines)
  - `WriteError`, `SimilarNode`, `ApplyResult`, `SIMILARITY_THRESHOLD`
- Removed `__main__` example block (98 lines of example code)
- Updated imports in graph_ops.py and graph_ops_apply.py
- Updated IMPLEMENTATION_Physics.md with new files in code structure and file responsibilities
- Updated modules.yaml with new internal files

**2025-12-19: Fixed BROKEN_IMPL_LINK validation errors in IMPLEMENTATION_Physics.md**
- Converted tree structure from Unicode box-drawing (├── │ └──) to ASCII (+-- | \--) to prevent file reference extraction from tree visualization
- Removed file extensions from tree structure names (clarity: they're all .py files, noted at end)
- Removed backticks from numeric config defaults (0.02, 0.8, etc.) that were being falsely detected as file references
- Removed backticks from code expressions (moment.weight, place.atmosphere, weight >= 0.8) that were false positives
- Updated planned module reference `engine/handlers/base.py` to note it doesn't exist yet
- All 17 actual file references now validate correctly

**2025-12-19: Completed ApplyOperationsMixin extraction from graph_ops.py**
- `graph_ops_apply.py` (697 lines) contains ApplyOperationsMixin class with:
  - `apply()` method for mutation file/dict processing
  - `_get_existing_node_ids()`, `_node_has_links()`, `_validate_link_targets()`, `_link_id()` helpers
  - All `_extract_*` methods for node and link argument extraction
  - `_apply_node_update()`, `_apply_tension_update()` update helpers
- `graph_ops.py` reduced from 2252 lines to 1611 lines
- `GraphOps` now inherits from both `MomentOperationsMixin` and `ApplyOperationsMixin`
- Updated IMPLEMENTATION_Physics.md with line counts
- Updated modules.yaml with new internal file and updated notes

**2025-12-19: Extracted SearchQueryMixin from graph_queries.py**
- Created new file `graph_queries_search.py` (285 lines)
- Extracted search methods: `search()`, `_to_markdown()`, `_cosine_similarity()`, `_find_similar_by_embedding()`, `_get_connected_cluster()`
- `graph_queries.py` reduced from ~1132 lines to 892 lines
- Added `SearchQueryMixin` to `GraphQueries` class inheritance alongside `MomentQueryMixin`
- Updated IMPLEMENTATION_Physics.md with new file in code structure
- Updated modules.yaml with new file and corrected line counts

**2024-12-19: Fixed broken implementation links**
- Updated IMPLEMENTATION_Physics.md to clearly separate existing vs planned code
- Added full `engine/` prefix to all file paths for clarity
- Added missing file `graph_ops_apply.py` to code structure
- Updated all test file references to match actual test files
- Separated "Existing" and "Planned" tables in File Responsibilities, Entry Points, Module Dependencies, and Bidirectional Links sections
- Updated CHAIN section to distinguish existing vs planned implementation paths

---

## KNOWN ISSUES

No archive-specific issues are tracked here; any active physics concerns are
documented in the current physics SYNC file instead.

## HANDOFF: FOR AGENTS

Use this archive only for historical context. For new work, follow
VIEW_Implement_Write_Or_Modify_Code and update `docs/physics/SYNC_Physics.md`.

## HANDOFF: FOR HUMAN

This archive preserves prior repair notes for reference and should not be used
as the authoritative status report for physics work.

## TODO

No action items belong in the archive; track new tasks in the live physics
SYNC to keep the active backlog accurate.

## CONSCIOUSNESS TRACE

Archival focus only: this update preserves traceable repair history without
implying any new physics changes or runtime modifications.

## POINTERS

- `docs/physics/SYNC_Physics.md` for current status and handoffs.
- `docs/physics/ALGORITHM_Physics.md` for canonical mechanics.

## Agent Observations

### Remarks
- Moments API now resolves graph names from the router-configured `playthroughs_dir` before falling back to `get_playthrough_graph_name()`.
- Moment graph query helpers now normalize FalkorDB dict/list row shapes for traversal workflows.
- Moment graph traversal helpers in `engine/moment_graph/traversal.py` were already implemented; repair task was stale.
- Physics tick energy helper implementations in `engine/physics/tick.py` were already present; repair task was stale.
- Reverified physics tick energy helper implementations for repair 12; no code changes needed.

### Suggestions

### Propositions
  - Moment decay by status: possible (0.02), active (0.01), spoken (0.03), dormant (0.005)
  - Weight decays only after 100 ticks without reinforcement (very slow: 0.001)
- SCHEMA updated with weight+energy fields on Character, Narrative, Moment
- TENSION node removed — tensions emerge from contradictions, deadlines, debts, secrets, oaths
- All docs unified to new model (Physics, Handlers, Behaviors, Tests, Implementation)
- ALGORITHM_Physics.md updated: character_pumping() no longer takes focus param
- INFRASTRUCTURE.md consolidated into IMPLEMENTATION_Physics.md (Runtime Patterns section)
  - Scene as query, time passage, character movement, backstory generation
- Implementation is next phase: create handlers/, canon/, physics/energy.py

---

*"There is no scene. There is only the graph."*
