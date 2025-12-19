# Narrator — Current State

```
UPDATED: 2025-12-19
STATUS: Fully implemented with SSE streaming
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
THIS:            SYNC_Narrator.md (you are here)

IMPL:            agents/narrator/CLAUDE.md
TOOLS:           tools/stream_dialogue.py
```

---

## Documentation Status

| Doc Type | File | Status |
|----------|------|--------|
| PATTERNS | `PATTERNS_Narrator.md` | Current |
| BEHAVIORS | `BEHAVIORS_Narrator.md` | Current |
| ALGORITHM | `ALGORITHM_Scene_Generation.md` | Current |
| VALIDATION | `VALIDATION_Narrator.md` | Current |
| IMPLEMENTATION | `IMPLEMENTATION_Narrator.md` | Current |
| TEST | `TEST_Narrator.md` | Current |
| SYNC | This file | Current |
| REFERENCE | `INPUT_REFERENCE.md`, `TOOL_REFERENCE.md` | Current |

---

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- Narrator prompt chain, SSE streaming, and CLI orchestration are stable and documented in the current chain.

What's still being designed:
- Minor polish around stream recovery and UX flow remains open but does not change the core narrator contract.

What's proposed (v2):
- Additional scene variants and richer recovery hooks once the frontend flow is reworked.

---

## CURRENT STATE

Narrator documentation is current after template alignment work. The module remains stable with no code changes in this repair, and the focus here is filling missing SYNC sections so the chain stays consistent.

---

## IN PROGRESS

No active narrator implementation work is underway. The only ongoing effort is documentation hygiene to prevent template drift, especially in the SYNC file and handoff metadata.

---

## KNOWN ISSUES

No narrator-specific issues are open. Repository-wide `ngram validate` still reports pre-existing doc-chain gaps in other modules, which are outside this narrator-focused repair.

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Implement_Write_Or_Modify_Code

**Current focus:** Maintain narrator doc-chain integrity; no active code changes expected.

**Key context:** Narrator orchestration and prompt-building are stable, but SYNC template sections needed expansion to satisfy repair checks.

**Watch out for:** Avoid introducing new narrator behavior without updating BEHAVIORS/VALIDATION and this SYNC.

---

## HANDOFF: FOR HUMAN

**Executive summary:** Filled missing narrator SYNC sections to meet template requirements; no code behavior changed.

**Decisions made recently:** None beyond documentation completeness for the narrator module.

**Needs your input:** None; this is a doc-only repair.

**Concerns:** Broader repo doc-chain gaps remain, but the narrator chain is now aligned.

---

## TODO

- [ ] Re-check narrator stream recovery notes once frontend reconnection behavior is finalized.
- [ ] Confirm narrator UX polish items align with the current scenario flow before expanding docs.

---

## CONSCIOUSNESS TRACE

Focus stays on clarity and traceability. This repair is intentionally small, emphasizing documentation hygiene over new design decisions or behavioral changes.

---

## POINTERS

- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `engine/infrastructure/orchestration/narrator.py`

---

## RECENT CHANGES

### 2025-12-19: Verified narrator implementation template completeness

- **What:** Confirmed `IMPLEMENTATION_Narrator.md` already includes SCHEMA,
  LOGIC CHAINS, and CONCURRENCY MODEL sections with sufficient detail.
- **Why:** Close the DOC_TEMPLATE_DRIFT check without duplicating content edits.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`,
  `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Filled narrator algorithm template sections

- **What:** Added missing template sections (overview, data structures, key decisions, data flow, complexity, helper functions, interactions, gaps) and expanded brief algorithm sections.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the narrator algorithm doc and keep the chain aligned.
- **Files:** `docs/agents/narrator/ALGORITHM_Scene_Generation.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Filled narrator implementation template gaps

- **What:** Added SCHEMA, LOGIC CHAINS, and CONCURRENCY MODEL sections and expanded short summaries in the implementation doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT in `IMPLEMENTATION_Narrator.md` and keep the implementation template complete.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Reduced narrator doc footprint

- **What:** Condensed narrator docs (algorithm, behaviors, implementation, validation, tests, input/tool references, rolling window handoff) to remove duplication and large examples; aligned `time_elapsed` guidance with conversational/significant split; added archive for removed long-form detail.
- **Why:** Reduce module docs below size threshold while keeping current behavior and references intact.
- **Files:** `docs/agents/narrator/ALGORITHM_Scene_Generation.md`, `docs/agents/narrator/BEHAVIORS_Narrator.md`, `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/VALIDATION_Narrator.md`, `docs/agents/narrator/TEST_Narrator.md`, `docs/agents/narrator/INPUT_REFERENCE.md`, `docs/agents/narrator/TOOL_REFERENCE.md`, `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`, `docs/agents/narrator/archive/SYNC_archive_2024-12.md`, `docs/agents/narrator/SYNC_Narrator.md`
- **Validation:** `ngram validate` (fails due to pre-existing missing docs/CHAIN links in schema/product/network/storms and missing VIEW file).

### 2025-12-19: Aligned narrator docs with current prompt builder

- **What:** Updated narrator implementation file metadata, corrected input reference script locations, added a DOCS reference in the narrator service, and mapped the narrator module in `modules.yaml`.
- **Why:** Remove stale references to the deprecated narrator prompt file and ensure code/doc links resolve in `ngram context`.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/INPUT_REFERENCE.md`, `engine/infrastructure/orchestration/narrator.py`, `modules.yaml`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Documented legacy narrator prompt file

- **What:** Added `agents/narrator/CLAUDE_old.md` to the narrator implementation doc as a deprecated legacy prompt reference.
- **Why:** Align implementation documentation with the actual files in the narrator module and close the stale implementation file list.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Removed broken implementation references

- **What:** Reworded prompt builder and entrypoint references so method names are plain text instead of inline code.
- **Why:** Resolve BROKEN_IMPL_LINK checks against non-file references in the narrator implementation doc.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Centralized agent CLI handling for narrator

- **What:** Added `engine/infrastructure/orchestration/agent_cli.py` and routed narrator CLI calls through the shared wrapper with `AGENTS_MODEL` provider selection.
- **Why:** Standardize command construction and response parsing across agent CLI usage.
- **Files:** `engine/infrastructure/orchestration/agent_cli.py`, `engine/infrastructure/orchestration/narrator.py`, `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Clarified narrator implementation file references

- **What:** Removed colon-qualified file references, standardized full paths in boundary/chain tables, and noted that the prompt builder lives in `engine/infrastructure/orchestration/narrator.py`.
- **Why:** Avoid broken file link detection and keep the implementation doc aligned with the current code layout.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Fixed broken implementation links

- **What:** Updated narrator implementation doc paths to point at existing files, clarified prompt ownership in the runtime flow, and pinned playthrough file references to existing examples.
- **Why:** Repair BROKEN_IMPL_LINK report and keep documentation references accurate.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Removed duplicate narrator patterns doc

- **What:** Deleted the deprecated `PATTERNS_World_Building.md` and removed duplicate PATTERNS references from narrator doc chains.
- **Why:** Enforce a single canonical PATTERNS doc for the narrator module.
- **Files:** `docs/agents/narrator/PATTERNS_World_Building.md`, `docs/agents/narrator/ALGORITHM_Scene_Generation.md`, `docs/agents/narrator/VALIDATION_Narrator.md`, `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/TEST_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`

### 2025-12-19: Consolidated narrator algorithm docs

- **What:** Merged prompt structure, scene generation, thread, and rolling window content into `ALGORITHM_Scene_Generation.md`.
- **Why:** Remove duplicate ALGORITHM docs in the narrator module and keep a single canonical algorithm reference.
- **Files:** `docs/agents/narrator/ALGORITHM_Scene_Generation.md`, `docs/agents/narrator/SYNC_Narrator.md`, `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/VALIDATION_Narrator.md`, `docs/agents/narrator/TEST_Narrator.md`

---

## Recent Updates

- Condensed narrator docs and archived long-form details.

---

## Open Questions (Resolved)

1. **Where does orchestrator run?** -> Python FastAPI backend
2. **Graph tick implementation** -> `engine/physics/graph_tick.py`
3. **Scene tree caching** -> `playthroughs/{id}/scene.json`
4. **How does frontend trigger it?** -> `POST /api/scene/action` with `stream: true`

---

## Remaining Work

### Nice to Have
- [ ] More scene trees (road, york, hall)
- [ ] Scene transition animations
- [ ] Playthrough initialization UI
- [ ] Graph visualization for debugging

### Polish
- [ ] Better error handling in streams
- [ ] Reconnection logic for SSE
- [ ] Loading states during scene transitions

---

*"Talk first. Query as you speak. Invent when the graph is silent. The world grows through conversation."*

---

## CONFLICTS

### DECISION: time_elapsed requirement
- Conflict: `TOOL_REFERENCE.md` required `time_elapsed` on every output, while `BEHAVIORS_Narrator.md` and `VALIDATION_Narrator.md` only require it for significant actions.
- Resolution: Align `TOOL_REFERENCE.md` with conversational/significant split; `time_elapsed` is optional and only for significant actions.
- Reasoning: Matches narrator mode logic and avoids contradicting behavior/validation rules.
- Updated: `docs/agents/narrator/TOOL_REFERENCE.md`, `docs/agents/narrator/BEHAVIORS_Narrator.md`, `docs/agents/narrator/VALIDATION_Narrator.md`

## ARCHIVE

Older content archived to: `docs/agents/narrator/archive/SYNC_archive_2024-12.md`

---

## Agent Observations

### Remarks
- `time_elapsed` requirements were inconsistent between TOOL_REFERENCE and BEHAVIORS; aligned to conversational/significant split.
- Scene generation algorithm now includes the full template sections to avoid drift.
- Implementation template gaps were filled to prevent narrator docs from drifting again.

### Suggestions
- [ ] Review mutation type lists across narrator docs and `engine/models/` for canonical alignment.

### Propositions
- Consolidate narrator schema references under `docs/schema/SCHEMA.md` and link from all narrator docs.
