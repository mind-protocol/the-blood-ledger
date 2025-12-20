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
