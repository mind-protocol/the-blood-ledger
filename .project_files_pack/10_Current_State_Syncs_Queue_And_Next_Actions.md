# 10_Current_State_Syncs_Queue_And_Next_Actions

@pack:generated_at: 2025-12-20T10:41:21
@pack:repo_kind: blood-ledger

SYNC state, current queue, and next actions (resume after rate-limits)

## Notes
This file supports resuming work after rate-limits. Prefer SYNC as authoritative queue.


---

## SOURCE: .ngram/state/SYNC_Project_State.md
# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
```

---

## CURRENT STATE

Opening flow documentation is now aligned to the current playthrough bootstrap
implementation, including seed graph initialization, scenario injection, and
opening moment creation. Local dev startup uses the correct FastAPI entrypoint.
Escalation marker wording in principles and agent guidance now avoids
false-positive escalation detection.

---

## ACTIVE WORK

### Documentation Alignment

- **Area:** `docs/design/opening/`
- **Status:** in progress
- **Owner:** agent
- **Context:** Ensure opening data flow and health checks match current code paths.

---

## RECENT CHANGES

### 2025-12-20: Chronicle implementation doc consolidation

- **What:** Consolidated Chronicle implementation docs into `docs/product/chronicle-system/IMPLEMENTATION_Chronicle_System.md` and converted `docs/product/chronicle-system/IMPLEMENTATION_Chronicle_Technical_Pipeline.md` into a pointer.
- **Why:** Remove duplicate IMPLEMENTATION documentation in the chronicle-system folder.
- **Impact:** Single authoritative implementation reference; technical pipeline now points to the canonical system doc.

### 2025-12-20: Chronicle behaviors doc consolidation

- **What:** Merged Chronicle behavior details into `docs/product/chronicle-system/BEHAVIORS_Chronicle_Types_And_Structure.md` and turned `docs/product/chronicle-system/BEHAVIORS_Chronicle_Types.md` into a pointer.
- **Why:** Remove duplicate BEHAVIORS docs in `docs/product/chronicle-system/`.
- **Impact:** Single canonical behaviors doc with updated chain links.

### 2025-12-20: Map algorithm doc subfolder split

- **What:** Moved map algorithm subdocs into `docs/world/map/ALGORITHM/{places,routes,rendering}/` and updated references.
- **Why:** Remove duplicate ALGORITHM docs within a single folder.
- **Impact:** Map algorithm chain points to subfolder locations.

### 2025-12-20: Map Rendering Algorithm Consolidation

- **What:** Consolidated map rendering algorithm details into the rendering pipeline doc and simplified the map algorithm overview to a pointer.
- **Why:** Resolve duplicate ALGORITHM documentation in the map module for issue #16.
- **Impact:** Single canonical rendering algorithm doc; overview now summarizes and links.

### 2025-12-20: Chronicle validation consolidation

- **What:** Merged the Chronicle metrics/success validation into `docs/product/chronicle-system/VALIDATION_Chronicle_Invariants.md` and replaced the duplicate metrics doc with a reference.
- **Why:** Remove duplicate VALIDATION docs in the chronicle-system folder.
- **Impact:** Single canonical validation doc; metrics doc now points to it.

### 2025-12-20: Scene id deprecation cleanup

- **What:** Scene transforms now use `placeId` as the scene id and fallback uses `place_camp`.
- **Why:** Scene ids are deprecated; moment fetches require place ids.
- **Impact:** Frontend location lookups stay consistent.

### 2025-12-20: Fix moment view query error

- **What:** Reworked `get_current_view` spoken-location filter to avoid FalkorDB alias errors.
- **Why:** Query failures returned empty moments, triggering "needs opening".
- **Impact:** Moments load correctly after player input.

### 2025-12-20: Frontend map PATTERNS duplication check

- **What:** Confirmed the duplicate frontend map PATTERNS document was already removed (repair 19); updated the map view SYNC to reflect the single canonical pattern doc.
- **Why:** Keep the map documentation consolidated and avoid drift across duplicate PATTERNS files.
- **Impact:** Documentation-only update; no behavior changes.

### 2025-12-20: Map algorithm duplication verification

- **What:** Confirmed map algorithm content now lives in `docs/world/map/ALGORITHM_Map.md` with part docs pointing to the canonical overview.
- **Why:** Close the ALGORITHM duplication repair for issue #16.
- **Impact:** Map algorithm documentation has a single authoritative source.


### 2025-12-20: Map rendering algorithm consolidation

- **What:** Removed `docs/world/map/ALGORITHM_Rendering.md`, keeping
  `docs/world/map/ALGORITHM_Map.md` and
  `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md` as the canonical
  map rendering algorithm docs.
- **Why:** Eliminate duplicate ALGORITHM documentation in the map folder.
- **Impact:** Single authoritative rendering algorithm location in map docs.

### 2025-12-20: Consolidated map algorithm docs

- **What:** Merged Places/Routes/Rendering algorithms into `docs/world/map/ALGORITHM_Map.md` and converted part docs into reference stubs.
- **Why:** Remove duplicate ALGORITHM content in the map module.
- **Impact:** Map algorithms now have a single canonical source with stubs pointing to it.

### 2025-12-20: Frontend map patterns consolidation

- **What:** Consolidated the deprecated interactive travel map patterns into the
  parchment map view and removed the duplicate PATTERNS doc in `docs/frontend/map/`.
- **Why:** Eliminate duplicate PATTERNS docs in the frontend map module.
- **Impact:** Single canonical frontend map patterns doc; duplicate removed.

### 2025-12-20: Physics Tick Energy Helpers Verified

- **What:** Recorded verification that `_flow_energy_to_narratives`, `_propagate_energy`, `_decay_energy`, and `_update_narrative_weights` in `engine/physics/tick.py` are already implemented.
- **Why:** Repair issue #16 flagged these helpers as incomplete.
- **Impact:** Documentation-only update; functionality unchanged.

### 2025-12-20: Graph moment query helpers verification

- **What:** Verified `get_narrative_moments`, `get_narratives_from_moment`, `get_available_transitions`, and `get_clickable_words` in `engine/physics/graph/graph_queries_moments.py` already have implementations; no code changes required.
- **Why:** Repair task flagged incomplete implementations for issue #16.
- **Impact:** Documentation-only update in graph SYNC; functionality unchanged.

### 2025-12-20: Models Base Repair 10 Noted

- **What:** Clarified the repair 10 reference in `docs/engine/models/SYNC_Models.md` for the base timestamp comparator verification.
- **Why:** Keep repair tracking explicit for issue #16.
- **Impact:** Documentation-only update; functionality unchanged.

### 2025-12-20: Physics tick helper verification

- **What:** Verified the four energy-flow helpers in `engine/physics/tick.py` are already implemented; updated `docs/physics/SYNC_Physics.md`.
- **Why:** Repair #16 flagged empty implementations; confirmed they are present to close the repair loop.
- **Impact:** Documentation-only update; functionality unchanged.
- **Repair run:** `18-INCOMPLETE_IMPL-physics-tick`.

### 2025-12-20: Moment graph sync conflict recorded

- **What:** Added a conflict note in `docs/engine/moment-graph-engine/SYNC_Moment_Graph_Engine.md` about the missing moment graph module mapping in `modules.yaml`.
- **Why:** Document drift surfaced while verifying traversal helper implementations for repair 14.
- **Impact:** Documentation-only update; module mapping remains unchanged.

### 2025-12-20: Graph Ops Types Verification

- **What:** Verified `SimilarNode.__str__` and `ApplyResult.success` are already implemented in `engine/physics/graph/graph_ops_types.py`.
- **Why:** Repair task for issue #16 flagged these helpers as incomplete.
- **Impact:** No code changes; graph SYNC updated to record verification.

### 2025-12-20: Graph moment query helpers verification

- **What:** Verified `get_narrative_moments`, `get_narratives_from_moment`, `get_available_transitions`, and `get_clickable_words` in `engine/physics/graph/graph_queries_moments.py` are already implemented.
- **Why:** Repair task for issue #16 flagged the helpers as incomplete.
- **Impact:** No code changes; graph SYNC updated to record verification.

### 2025-12-20: Models Base Repair Reconfirmed

- **What:** Reconfirmed the `GameTimestamp` comparator implementations and noted the repair in `docs/engine/models/SYNC_Models.md`.
- **Why:** Close out repair `10-INCOMPLETE_IMPL-models-base` with an explicit verification entry.
- **Impact:** Documentation-only update; functionality unchanged.

### 2025-12-20: Graph Mutation Listener Repair Verification

- **What:** Confirmed `add_mutation_listener` and `remove_mutation_listener` in `engine/physics/graph/graph_ops_events.py` are already implemented; documented the stale repair report as a resolved conflict.
- **Why:** Repair issue #16 flagged these helpers as incomplete.
- **Impact:** No code changes; graph SYNC now records the conflict resolution.

### 2025-12-20: Moment graph traversal helpers verification

- **What:** Verified `make_dormant` and `process_wait_triggers` in
  `engine/moment_graph/traversal.py` already have implementations; no code
  changes required for issue #16.
- **Why:** Repair task flagged incomplete implementations for the traversal
  helpers.
- **Impact:** Documentation updated to record the verification; functionality
  unchanged.

### 2025-12-20: Node Helper Properties Verified (Repair 12)

- **What:** Verified `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` in `engine/models/nodes.py` already have concrete implementations; no code changes required for issue #16.
- **Why:** Repair 12 (INCOMPLETE_IMPL-models-nodes) flagged these helpers as incomplete.
- **Impact:** Documentation updated to record the verification; functionality unchanged.

### 2025-12-20: Moment graph query helpers verification

- **What:** Verified `get_dormant_moments` and `get_wait_triggers` are already
  implemented in `engine/moment_graph/queries.py`.
- **Why:** Repair task flagged incomplete implementations for issue #16.
- **Impact:** No code changes; moment graph SYNC updated to record verification.

### 2025-12-20: Link Helper Accessors Verified

- **What:** Verified `engine/models/links.py` helpers (`belief_intensity`, `is_present`, `has_item`, `is_here`) already have implementations; no code changes required for issue #16.
- **Why:** Repair 11 (INCOMPLETE_IMPL-models-links) flagged empty implementations that are already complete.
- **Impact:** Documentation-only update in `docs/engine/models/SYNC_Models.md`; functionality unchanged.

### 2025-12-20: Models Base Verification

- **What:** Verified `engine/models/base.py` already implements `GameTimestamp.__str__`, `__le__`, and `__gt__`; logged the verification in `docs/engine/models/SYNC_Models.md`.
- **Why:** Repair task flagged incomplete implementations for issue #16.
- **Impact:** No code changes; documentation now reflects the verification-only repair.

### 2025-12-20: World Builder Cache Helpers Verification

- **What:** Re-verified `_hash_query` and `clear_cache` in `engine/infrastructure/world_builder/world_builder.py` already have concrete implementations for issue #16; no code changes required.
- **Why:** Repair run 09-INCOMPLETE_IMPL-world_builder-world_builder flagged empty implementations that are already complete.
- **Impact:** Documentation-only update in world-builder SYNC; functionality unchanged.

### 2025-12-20: Discussion Tree Branch Counting Fix

- **What:** Updated discussion tree branch counting to track remaining leaf paths and documented helper behavior.
- **Why:** Align regeneration thresholds with actual remaining branch paths.
- **Impact:** Regeneration triggers now match discussion tree lifecycle expectations.

### 2025-12-20: World Builder Cache Helpers Verified

- **What:** Verified `_hash_query` and `clear_cache` in `engine/infrastructure/world_builder/world_builder.py` already have implementations; updated world-builder SYNC.
- **Why:** Repair #16 flagged empty implementations that are already complete.
- **Impact:** No code changes; documentation now records the verification.

### 2025-12-20: History Conversations Verification

- **What:** Verified `ConversationThread` path helper methods are already implemented in `engine/infrastructure/history/conversations.py`; no code changes required for issue #16.
- **Why:** The repair task flagged empty implementations that are already filled.
- **Impact:** Documentation updated to record the verification; functionality unchanged.

### 2025-12-20: Base Timestamp Comparators Verified

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are already implemented in `engine/models/base.py`; no code changes required for issue #16.
- **Why:** The INCOMPLETE_IMPL repair flagged empty implementations that are already present.
- **Impact:** Documentation updated to record the verification; reconfirmed during repair `10-INCOMPLETE_IMPL-models-base`.

### 2025-12-20: Moment Processor Repair Verification

- **What:** Verified `engine/infrastructure/memory/moment_processor.py` already
  implements the functions flagged by repair #16; logged verification in
  `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.
- **Why:** Repair task targeted incomplete helpers that are already implemented.
- **Impact:** No code changes; documentation now records the verification-only pass.

### 2025-12-20: Opening Flow Docs + Dev Startup Fix

- **What:** Updated opening implementation/health docs to include seed graph init and clarified steps; fixed backend entrypoint in `run.sh`.
- **Why:** Close doc/code drift and resolve missing SSE route in local dev.
- **Impact:** Clearer opening data flow; local SSE endpoint mounts correctly when using `run.sh`.

### 2025-12-20: MomentSurface implementation restored

- **What:** Implemented missing `MomentSurface` in `engine/moment_graph/surface.py`.
- **Why:** FastAPI boot failed when importing the moment graph module.
- **Impact:** Backend can start; SSE and tempo endpoints can mount.

### 2025-12-20: SSE route collision fixed

- **What:** Reordered `/api/moments/stream/{playthrough_id}` ahead of the generic
  `/{playthrough_id}/{moment_id}` route.
- **Why:** The generic route was capturing `/stream/{id}` and returning 404.
- **Impact:** SSE stream responds with 200.

### 2025-12-20: Conversation Thread Helpers Verified

- **What:** Verified `ConversationThread` path helper implementations in `engine/infrastructure/history/conversations.py` already exist for issue #16; no code changes required.
- **Why:** The INCOMPLETE_IMPL repair targeted functions that are already implemented.
- **Impact:** Recorded no-op repair to keep the repair ledger accurate.

### 2025-12-20: Graph Health Repair Verification

- **What:** Re-verified `engine/graph/health/check_health.py` helper implementations for issue #16; no code edits required.
- **Why:** Confirm the incomplete-impl report is stale and note the verification in project state.
- **Impact:** Repair is documentation-only; code remains unchanged.

### 2025-12-20: Graph Mutation Listener Verification

- **What:** Verified `add_mutation_listener` and `remove_mutation_listener` in `engine/physics/graph/graph_ops_events.py` are already implemented.
- **Why:** Repair #16 flagged them as incomplete; verified no code change is needed.
- **Impact:** Documentation-only update in graph SYNC; functionality unchanged.

### 2025-12-20: Principles Escalation Marker Wording

- **What:** Reworded the escalation marker reference in `.ngram/PRINCIPLES.md` to avoid being parsed as an active escalation marker.
- **Why:** Prevent false-positive escalation detection in the principles doc.
- **Impact:** Escalation scan no longer flags the principles reference as unresolved.

### 2025-12-20: Escalation View Marker Escaped

- **What:** Escaped the escalation marker example in `.ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md`.
- **Why:** Prevent the example from being parsed as a live escalation marker.
- **Impact:** Escalation scans no longer flag the view's example block as unresolved.

### 2025-12-20: Agents Escalation Marker Wording

- **What:** Reworded the escalation marker reference in `AGENTS.md` to avoid being parsed as an active escalation marker.
- **Why:** Prevent false-positive escalation detection in the agent guidance doc.
- **Impact:** Escalation scan no longer flags the agent guidance reference as unresolved.

### 2025-12-20: GEMINI Escalation Review

- **What:** Reviewed `.ngram/GEMINI.md` for escalation markers tied to issue #16; no conflicts or escalation markers were present to resolve.
- **Why:** Ensure the escalation repair task is assessed even when the target file has no actionable conflicts.
- **Impact:** No changes required to `.ngram/GEMINI.md`; issue handled as a no-op with verification recorded here.

### 2025-12-20: CLAUDE Escalation Review

- **What:** Reviewed `.ngram/CLAUDE.md` for escalation markers tied to issue #16; no conflicts or escalation markers were present to resolve.
- **Why:** Ensure the escalation repair task is assessed even when the target file has no actionable conflicts.
- **Impact:** No changes required to `.ngram/CLAUDE.md`; issue handled as a no-op with verification recorded here.

### 2025-12-20: Escalation View Marker Encoding

- **What:** Encoded the proposition marker examples in the escalation view to avoid false-positive marker detection.
- **Why:** Prevent the escalation/proposition examples from being flagged as unresolved markers during health scans.
- **Impact:** The escalation view remains instructional without triggering the escalation scanner.
- **Repair run:** Confirmed during repair `03-ESCALATION-CLAUDE`; no further action needed.

### 2025-12-20: Playthrough API Repair Verification

- **What:** Verified `_count_branches` and `create_scenario_playthrough` in
  `engine/infrastructure/api/playthroughs.py` already have real logic; no code
  changes required for issue #16.
- **Why:** Repair task flagged empty implementations that are already complete.
- **Impact:** Documented verification in opening SYNC to prevent repeat repairs.

### 2025-12-20: Graph Health Check Helpers Verified

- **What:** Verified `engine/graph/health/check_health.py` already implements health report helper methods tied to issue #16; no code edits required.
- **Why:** The incomplete-implementation repair targeted helper functions that were already filled in.
- **Impact:** Documentation sync updated to record the no-op repair.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| SSE stream 404 when backend is started with the old module path | high | `run.sh` | Use `engine.infrastructure.api.app:app` so `/api/moments/stream/{id}` is mounted |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Implement_Write_Or_Modify_Code.md

**Current focus:** Keep opening/playthrough bootstrap docs aligned with code, verify SSE endpoint behavior.

**Key context:**
Playthrough creation seeds a fresh graph via `engine/init_db.py`, then applies scenario YAML, creates opening moments, and returns `scene.json`.

**Watch out for:**
Local dev scripts may point at outdated FastAPI module paths; SSE 404 is a symptom.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Opening docs now describe the real bootstrap flow, including seed graph init and opening moment creation.
Local dev `run.sh` now targets the correct API entrypoint so the moment SSE route is available.

**Decisions made recently:**
Documented seed graph init as a first-class step in the opening flow and added a health indicator for it.

**Needs your input:**
Confirm whether playthrough bootstrap should hard-fail when seed graph loading fails (currently logs and continues).

**Concerns:**
If deployment uses a different entrypoint than `engine.infrastructure.api.app:app`, the SSE route may still be missing.

---

## TODO

### High Priority

- [ ] Decide if seed-load failures should abort playthrough creation.

### Backlog

- [ ] Add automated opening health checks (`engine/tests/test_opening_health.py`).
- IDEA: Add a lightweight smoke test that hits `/api/moments/stream/{id}` after playthrough creation.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Stable; small documentation alignment and dev startup fixes.

**Architectural concerns:**
Seed graph init is best-effort today; drift risk if scenarios assume missing seed nodes.

**Opportunities noticed:**
Automate opening health checks to validate graph + scene outputs together.

---

## Agent Observations

### Remarks
- Conversation thread helper functions are already implemented; the repair task is a verification-only update.

### Suggestions
- [ ] Consider aligning `engine/models/base.py` NarrativeSource file example with `engine/infrastructure/history/README.md` and tests (`conversations/aldric.md` vs `conversations/char_aldric.md`).

### Propositions
- None.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `design/opening/` | active | `docs/design/opening/SYNC_Opening.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| opening | `engine/infrastructure/api/playthroughs.py` | `docs/design/opening/` | CANONICAL |

**Unmapped code:** (run `ngram validate` to check)
- {List any code directories without module mappings}

**Coverage notes:**
Module manifest needs to include docs for opening if you want full mapping coverage.


---

## SOURCE: docs/infrastructure/api/SYNC_Api.md
# API — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- API app factory, router wiring, and current playthrough/moment endpoints are live and documented.
- Debug and gameplay SSE streams are established with separate queues.

What's still being designed:
- Auth, rate limiting, and API gateway decisions.

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/api/app.py`

The API module hosts the FastAPI application, including playthrough endpoints, moment APIs, and debug streaming.

## RECENT CHANGES

### 2025-12-20: Broadcast player moments on SSE

- **What:** Emit `moment_spoken` SSE events when `/api/moment` creates a player moment.
- **Why:** UI relies on SSE to refresh; player messages were not appearing.
- **Impact:** Frontend receives a refresh trigger after player input.

### 2025-12-20: Fix moment stream route collision

- **What:** Moved `/api/moments/stream/{playthrough_id}` above the generic
  `/{playthrough_id}/{moment_id}` route in `engine/infrastructure/api/moments.py`.
- **Why:** The generic route was capturing `/stream/{id}` and returning 404.
- **Impact:** SSE stream endpoint responds with 200 as expected.

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Api.md` and updated `TEST_Api.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** API module documentation is now compliant; Health checks are anchored to concrete docking points.

### 2025-12-20: Discussion Tree Branch Counting

- **What:** Count discussion tree branches by remaining leaf paths and document the helper behavior.
- **Why:** Ensure regeneration triggers reflect actual remaining branch paths.
- **Impact:** Branch count now aligns with discussion tree lifecycle expectations.

## GAPS

- [ ] Automated regression for SSE stream delivery under load.
- [ ] Schema validation tests for all router endpoints.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code when touching API routers. Ensure new endpoints are extracted from `app.py` to keep it from growing further.

## TODO

- [ ] Split remaining legacy endpoints from `app.py` into router modules.
- [ ] Implement API versioning strategy.

## POINTERS

- `docs/infrastructure/api/PATTERNS_Api.md` for scope and design rationale.
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` for endpoint-level data flow notes.

## CHAIN

```
THIS:            SYNC_Api.md (you are here)
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
ALGORITHM:       ./ALGORITHM_Api.md
VALIDATION:      ./VALIDATION_Api.md
IMPLEMENTATION:  ./IMPLEMENTATION_Api.md
HEALTH:          ./HEALTH_Api.md
```


---

## SOURCE: docs/frontend/SYNC_Frontend.md
# Frontend — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: CANONICAL
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
THIS:            SYNC_Frontend.md (you are here)

IMPL:            frontend/app/page.tsx
```

---

## CURRENT STATE

The frontend is a functional Next.js 16 application with React 19. It serves as the presentation layer for The Blood Ledger game.

**Tech Stack:**
- Next.js 16.0.10
- React 19.2.1
- Tailwind CSS 4
- TypeScript 5

**Key Files:**
| Path | Purpose |
|------|---------|
| `frontend/app/page.tsx` | Main entry, loads GameClient |
| `frontend/app/start/page.tsx` | Opening/start screen |
| `frontend/app/map/page.tsx` | Map view |
| `frontend/app/playthroughs/[id]/page.tsx` | Playthrough-specific view |
| `frontend/app/scenarios/page.tsx` | Scenario selection |
| `frontend/components/GameClient.tsx` | Main game client, handles loading states |
| `frontend/components/GameLayout.tsx` | Layout with scene + right panel |
| `frontend/hooks/useGameState.ts` | State management, API integration |
| `frontend/hooks/useMoments.ts` | Moment system state |
| `frontend/types/game.ts` | TypeScript types for game state |
| `frontend/lib/api.ts` | API client functions |

**Component Organization:**
- `components/scene/` — Scene rendering (SceneView, CenterStage, SceneImage, etc.)
- `components/moment/` — Moment system (MomentDisplay, MomentStream, ClickableText)
- `components/map/` — Map display (MapCanvas, MapClient)
- `components/panel/` — Right panel tabs
- `components/voices/` — Internal thoughts
- `components/chronicle/` — Chronicle display
- `components/debug/` — Debug panel

---

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- Next.js App Router entry points and layout flow.
- Backend-driven state hooks with REST + SSE updates.
- Scene, moment, map, panel, and voice component hierarchy.

What's still being designed:
- Testing strategy and coverage expectations for frontend modules.
- Long-term consolidation plan for `useGameState` and `useMoments`.

What's proposed (v2):
- Replace remaining static fallbacks with scenario-specific mocks.
- Expand automated UI coverage for core playthrough flows.

---

## IN PROGRESS

- Align frontend testing approach with backend CI constraints.
- Track when the moment system can fully replace legacy scene state.

---

## RECENT CHANGES

### 2025-12-20: Use placeId for moment fetches

- **What:** CenterStage now passes `currentScene.placeId` as the location for moment fetches.
- **Why:** Scene IDs are not place IDs; spoken moments were filtered out.
- **Impact:** Player-sent moments surface in the chat after refresh/SSE.

### 2025-12-20: Stop using deprecated scene ids

- **What:** Scene `id` now defaults to `placeId` in view/narrator transforms and fallback scenes.
- **Why:** Scene IDs are deprecated; downstream logic expects place ids.
- **Impact:** Moment fetches and scene references stay aligned.

### 2025-12-20: Consolidated frontend implementation docs

- **What:** Merged code structure details into `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` and removed the duplicate `IMPLEMENTATION_Code_Structure.md`.
- **Why:** Resolve documentation duplication in the frontend implementation folder.
- **Files:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md`, `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`, `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md`

---

## KNOWN ISSUES

No critical issues currently tracked, but automated frontend tests are sparse
and the dual state hooks (`useGameState` + `useMoments`) add maintenance risk.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Stable; frontend surface area is mapped and documented, with tests as the main gap.

**Attention points:**
Keep hook ownership clear as the moment system evolves to prevent drift.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement or VIEW_Extend

**Where things are:**
- Entry point: `frontend/app/page.tsx`
- State management: `frontend/hooks/useGameState.ts`
- Types: `frontend/types/game.ts`
- API client: `frontend/lib/api.ts`

**Key context:**
The frontend talks to a Python FastAPI backend via REST + SSE. The moment system (`useMoments`) is newer and may eventually replace `useGameState`. Both currently coexist.

**Watch out for:**
- Two state systems (useGameState and useMoments) — understand which one handles what
- Backend must be running for live mode; otherwise falls back to static data

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Frontend is a working Next.js app that renders the game. It connects to the Python backend for state. The moment system is the newer approach for displaying narrative content.

**Decisions made:**
- Using Next.js 16 with App Router (modern React patterns)
- Tailwind for styling (consistent with dark atmospheric theme)
- Separate hooks for different concerns (game state vs moments)

**Needs your input:**
- Should the moment system fully replace the old scene system?
- Testing strategy — currently minimal

---

## TODO

### Immediate

- [x] Add DOCS reference to main entry file (frontend/app/page.tsx)

### Later

- [x] Create IMPLEMENTATION doc with detailed file structure
- [x] Create TEST doc when testing strategy is decided
- [ ] Set up test framework (Vitest/Jest)
- [ ] Add unit tests for transform functions
- IDEA: Add Playwright tests for key flows

---

## POINTERS

| What | Where |
|------|-------|
| Game state hook | `frontend/hooks/useGameState.ts` |
| Moment hook | `frontend/hooks/useMoments.ts` |
| API client | `frontend/lib/api.ts` |
| Types | `frontend/types/game.ts` |
| Scene components | `frontend/components/scene/` |
| Moment components | `frontend/components/moment/` |
| Backend API docs | `docs/physics/API_Physics.md` |

---

## Agent Observations

### Remarks
- The frontend doc chain is now centered on the implementation overview entry point.
- The algorithm doc now captures data flow, complexity, and helper calls in one place.

### Suggestions
- [ ] If `useGameState.ts` and `api.ts` continue to grow, consider extracting transformers and moment-specific API helpers.

### Propositions
- Keep component inventories in the `docs/frontend/scene/` module to avoid repeating long file lists here.

---

## GAPS

- Completed: Filled SCOPE and expanded short sections in `docs/frontend/PATTERNS_Presentation_Layer.md`.
- Completed: Logged the update in `docs/frontend/SYNC_Frontend.md`.
- Remaining: Commit the doc updates once the unexpected staged change in `docs/frontend/scenarios/SYNC_Scenario_Selection.md` is resolved.

--- 

## ARCHIVE

Older content archived to: `docs/frontend/archive/SYNC_archive_2024-12.md`


---

## ARCHIVE

Older content archived to: `SYNC_Frontend_archive_2025-12.md`


---

## SOURCE: docs/physics/SYNC_Physics.md
# Physics — Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL. The physics module behavior is stable and documented. 
Core implementation exists for:
- Physics Tick (`engine/physics/tick.py`)
- Graph Ops/Queries
- Canon Holder (`engine/infrastructure/canon/canon_holder.py` - Core logic built, integration pending)

Still pending:
- Character Handlers (`engine/handlers/`)
- Speed Controller (`engine/infrastructure/orchestration/speed.py`)

## CURRENT STATE

Physics documentation is consolidated in `docs/physics/`, the algorithm is canonical. Implementation exists for core tick + graph ops and the base Canon Holder. Runtime integration with the Orchestrator and specific character handlers are planned but not yet built.

## RECENT CHANGES

### 2025-12-20: Physics tick energy helpers verified

- **What:** Verified `_flow_energy_to_narratives`, `_propagate_energy`, `_decay_energy`, and `_update_narrative_weights` in `engine/physics/tick.py` already contain concrete implementations.
- **Why:** Repair #16 flagged these helpers as empty; confirmed they are implemented and align with the physics algorithm.
- **Impact:** No code changes required; verification recorded to prevent repeat repairs.
- **Repair run:** `18-INCOMPLETE_IMPL-physics-tick`.

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Physics.md` and renamed `TEST_Physics.md` to its new format (Health content).
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** Physics module documentation is now compliant with the latest protocol; Health checks are anchored to concrete docking points.

## GAPS

- [ ] Automated check for "The Snap" transition display rules.
- [ ] Real-time monitoring of energy levels across large graph clusters.

## KNOWN ISSUES

`ngram validate` still reports pre-existing doc gaps and broken CHAIN links in other modules; no physics-specific defects are currently open.

## HANDOFF: FOR AGENTS

If you touch physics code, use VIEW_Implement_Write_Or_Modify_Code and update this SYNC plus any impacted doc chain entries (ALGORITHM/IMPLEMENTATION/TEST).

## HANDOFF: FOR HUMAN

Physics documentation is aligned and no behavior changes were made; the only remaining work is optional implementation of planned handlers/canon/speed.

## TODO

- [ ] Create `engine/handlers/` and wire flip-triggered handler dispatch.
- [ ] Implement canon holder and speed controller runtime scaffolding.

## CONSCIOUSNESS TRACE

Focus stayed on doc-template alignment with minimal scope; no code paths were changed, so confidence is high in the consistency of this sync update.

## POINTERS

- `docs/physics/ALGORITHM_Physics.md` for the canonical physics mechanics.
- `docs/physics/IMPLEMENTATION_Physics.md` for current code entry points.

## CHAIN

```
THIS:            SYNC_Physics.md (you are here)
PATTERNS:        ./PATTERNS_Physics.md
BEHAVIORS:       ./BEHAVIORS_Physics.md
ALGORITHMS:      ./ALGORITHM_Physics.md (consolidated: energy, tick, canon, handlers, input, actions, QA, speed)
SCHEMA:          ../schema/SCHEMA_Moments.md
API:             ./API_Physics.md
VALIDATION:      ./VALIDATION_Physics.md
IMPLEMENTATION:  ./IMPLEMENTATION_Physics.md (+ Runtime Patterns from INFRASTRUCTURE.md)
HEALTH:          ./HEALTH_Physics.md
IMPL (existing): ../../engine/physics/tick.py, ../../engine/physics/graph/
IMPL (planned):  ../../engine/handlers/, ../../engine/canon/, ../../engine/infrastructure/orchestration/speed.py
```

---

## Architecture Summary

**The graph is the only truth.**

| Component | Purpose | Status |
|-----------|---------|--------|
| Energy System | Characters pump, links route, decay drains | ALGORITHM_Physics.md ✓ |
| Physics Tick | Pump, transfer, decay, detect flips | ALGORITHM_Physics.md ✓ |
| Character Handlers | One handler per character, triggered on flip | ALGORITHM_Physics.md ✓ |
| Flip Detection | Status progression, salience threshold | ALGORITHM_Physics.md ✓ |
| Canon Holder | Record what becomes real, THEN links | ALGORITHM_Physics.md ✓ |
| Speed Controller | 1x/2x/3x display modes | ALGORITHM_Physics.md ✓ |

---

## Handoff Notes

- v2 architecture is fully documented in ALGORITHM files.
- **ALGORITHM_Physics.md** is the master document.
- **Weight vs Energy**: All nodes have both weight (importance over time, slow) and energy (current activation, fast).
- **Salience = weight × energy** — determines surfacing (threshold = 0.3).
- Tension is computed from structure, not stored.
- **Energy IS proximity** — no separate proximity calculation.
