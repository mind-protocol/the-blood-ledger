# Physics — Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-19
```

## Recent Changes

**2025-12-19: Verified physics tick energy helpers already implemented**
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

## CHAIN

```
THIS:            SYNC_Physics.md (you are here)
PATTERNS:        ./PATTERNS_Physics.md
BEHAVIORS:       ./BEHAVIORS_Physics.md
ALGORITHMS:      ./ALGORITHM_Physics.md, ./ALGORITHM_Energy.md (M1-M6, M11-M13),
                 ./ALGORITHM_Handlers.md, ./ALGORITHM_Input.md, ./ALGORITHM_Actions.md,
                 ./ALGORITHM_Questions.md, ./ALGORITHM_Speed.md
SCHEMA:         ../schema/SCHEMA_Moments.md
API:             ./API_Physics.md
VALIDATION:      ./VALIDATION_Physics.md
IMPLEMENTATION:  ./IMPLEMENTATION_Physics.md (+ Runtime Patterns from INFRASTRUCTURE.md)
TEST:            ./TEST_Physics.md, ../../engine/tests/test_moment_graph.py
IMPL (existing): ../../engine/physics/tick.py, ../../engine/physics/graph/
IMPL (planned):  ../../engine/handlers/, ../../engine/canon/, ../../engine/infrastructure/orchestration/speed.py
```

---

## Architecture Summary

**The graph is the only truth.**

| Component | Purpose | Status |
|-----------|---------|--------|
| Energy System | Characters pump, links route, decay drains | ALGORITHM_Energy.md ✓ |
| Physics Tick | Pump, transfer, decay, detect flips | ALGORITHM_Physics.md ✓ |
| Character Handlers | One handler per character, triggered on flip | ALGORITHM_Handlers.md ✓ |
| Flip Detection (M11) | Status progression, salience threshold | ALGORITHM_Energy.md ✓ |
| Canon Holder (M12) | Record what becomes real, THEN links | ALGORITHM_Energy.md ✓ |
| Agent Dispatch (M13) | Runner/Narrator/Citizen/Canon coordination | ALGORITHM_Energy.md ✓ |
| Speed Controller | 1x/2x/3x display modes | ALGORITHM_Speed.md ✓ |

---

## Open Questions

1. **LLM latency at 1x** — If handler takes 3-5s, is that acceptable? Pre-generation helps but may not cover all cases.

2. **Grouped character splitting** — When to split automatically vs. on direct address?

3. **Montage moment generation** — Same handlers or dedicated montage handler?

4. **Energy constants** — What values for PUMP_RATE, transfer factors, etc.? Need playtesting. See ALGORITHM_Energy.md.

5. **Question answerer priority** — When multiple questions queued, which first?

---

## Next Steps

1. ~~**Create ALGORITHM_Speed.md** — Speed controller with The Snap~~ ✓ DONE
2. ~~**Update VALIDATION_Physics.md** — Align with v2 invariants~~ ✓ DONE
3. ~~**Deprecate legacy files**~~ ✓ DONE
4. ~~**Update SCHEMA_Moments.md** — Add energy/weight fields~~ ✓ DONE
5. ~~**Create ALGORITHM_Energy.md** — Energy mechanics, conservation, link transfers~~ ✓ DONE
6. ~~**Remove TENSION node** — Tension is now computed, not stored~~ ✓ DONE
7. **Begin implementation** — Create handlers/, canon/, physics/energy.py

---

## Handoff Notes

For next session:

- v2 architecture is fully documented in ALGORITHM files
- **ALGORITHM_Energy.md** is the master document, containing:
  - **M1-M6**: Strength Mechanics (Activation, Evidence, Association, Source, Commitment, Intensity)
  - **M11**: Flip Detection — status progression, salience threshold, detection queries
  - **M12**: Canon Holder — record, link, time, trigger, strength, notify
  - **M13**: Agent Dispatch — Runner (world), Narrator (scene), Citizen (character), Canon Holder (record)
  - **Weight vs Energy**: All nodes have both weight (importance over time, slow) and energy (current activation, fast)
  - **Salience = weight × energy** — determines surfacing (threshold = 0.3)
  - Characters are batteries, narratives are circuits, moments spend energy on actualization
  - Links route energy (zero-sum), don't create it
  - Tension is computed from structure, not stored
  - **Energy IS proximity** — no separate proximity calculation
  - **Physical gating is link attributes** (presence_required, AT), not functions
  - Transfer types: T1-T6 (narrative links), T7 (CAN_LEAD_TO), T8 (CAN_SPEAK), T9 (ATTACHED_TO)

---

## Agent Observations

### Remarks
- Moments API now resolves graph names from the router-configured `playthroughs_dir` before falling back to `get_playthrough_graph_name()`.
- Moment graph query helpers now normalize FalkorDB dict/list row shapes for traversal workflows.
- Moment graph traversal helpers in `engine/moment_graph/traversal.py` were already implemented; repair task was stale.
- Physics tick energy helper implementations in `engine/physics/tick.py` were already present; repair task was stale.

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
