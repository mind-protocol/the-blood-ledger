# Async Architecture — State & Implementation Plan

**Last Updated:** 2025-12-19
**Status:** DESIGNING
**Version:** 2.0

---

## MATURITY

**What's canonical (v1):**
- Async architecture scope and component boundaries are documented with the
  graph as coordinator and hook interruptions scoped to travel only.

**What's still being designed:**
- SSE event payload formats, injection queue lifecycle, and discussion tree
  persistence rules remain in flux while implementation planning continues.

**What's proposed (v2):**
- Expanded orchestration for non-travel async flows and richer map rendering
  decisions are sketched but not committed to v1.

---

## CURRENT STATE

Async architecture documentation is comprehensive and aligned to templates,
with implementation gaps tracked in the capability tables below. The system
is still in the planning phase with no code changes in this repair, but the
SYNC now captures state, gaps, and handoffs explicitly.

---

## IN PROGRESS

### Sync Template Repair (DOC_TEMPLATE_DRIFT #16)

- **Started:** 2025-12-19
- **By:** Codex (repair agent)
- **Status:** in progress
- **Context:** Filling missing SYNC template sections ensures future agents
  can read the async state without reverse engineering.

---

## Overview

This document tracks what exists, what needs to be built, and the implementation path for the async architecture.

---

## Maturity

STATUS: DESIGNING

What's canonical (v1): Core framing is stable: graph-as-orchestrator, SSE-first updates, TaskOutput for completion, and hook-driven interruptions only.

What's still being designed: The exact queue formats, reconnection semantics, and multi-runner conflict resolution remain open.

What's proposed (v2): Dedicated queue broker, richer interruption prioritization, and a unified event bus spanning API + scripts.

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Async_Architecture.md
BEHAVIORS:      ./BEHAVIORS_Travel_Experience.md
ALGORITHM:      ./ALGORITHM_Async_Architecture.md
VALIDATION:     ./VALIDATION_Async_Architecture.md
IMPLEMENTATION: ./IMPLEMENTATION_Async_Architecture.md
TEST:           ./TEST_Async_Architecture.md
THIS:           SYNC_Async_Architecture.md
```

---

## CURRENT STATE

Async architecture is documented and partially scaffolded, but real-time SSE emission, background Runner execution, and injection queue handling are not implemented in the runtime code paths.

---

## IN PROGRESS

The immediate focus is stabilizing the async architecture docs and reconciling queue format drift so later implementation work can proceed without ambiguity.

---

## Current State vs Target State

### Graph

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Store state | FalkorDB operational | Same | None |
| Read API | `graph_queries.py` exists | Same | None |
| Write API | `graph_ops.py` exists | Same | None |
| SSE streaming | Not implemented | Emit events on write | **BUILD** |
| Image generation trigger | Not implemented | Queue on place creation | **BUILD** |
| Character activation → injection | Not implemented | Write to injection queue | **BUILD** |

### Runner (World Runner)

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Tick energy/pressure | `physics/tick.py` exists | Same | None |
| Create narratives | `world_runner.py` exists | Same | Minor updates |
| Background execution | Not implemented | `run_in_background=true` | **BUILD** |
| Write to graph during execution | Not implemented | Direct graph writes | **BUILD** |
| Output via TaskOutput | Not implemented | JSON stdout, read via TaskOutput | **BUILD** |
| Waypoint creation | Not implemented | Create places during travel | **BUILD** |

### Narrator

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Generate scenes | `narrator.py` exists | Same | None |
| Stream narration | Partial (SSE endpoint exists) | Full streaming | **ENHANCE** |
| Spawn Runner | Not implemented | `bash(run_in_background=true)` | **BUILD** |
| Read TaskOutput | Not implemented | On system reminder | **BUILD** |
| Handle hook injection | Not implemented | Read additionalContext | **BUILD** |
| Travel narration | Not implemented | Stream journey beats | **BUILD** |

### Hook Injection

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Injection queue file | Not implemented | `injection_queue.jsonl` | **BUILD** |
| Hook script | Not implemented | `engine/scripts/check_injection.py` | **BUILD** |
| Character activation writing | Not implemented | Graph → queue | **BUILD** |
| Frontend UI writing | Not implemented | API → queue | **BUILD** |

### Frontend

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Scene display | Implemented | Same | None |
| Character portraits | Implemented | Add click → topics | **ENHANCE** |
| SSE subscription | Not implemented | Subscribe to graph | **BUILD** |
| Map component | Not implemented | Show places, fog, position | **BUILD** |
| Position animation | Not implemented | Animate player token | **BUILD** |
| Stop button | Not implemented | Write to injection queue | **BUILD** |
| Image crossfade | Partial | Crossfade on place change | **ENHANCE** |

### Discussion Trees

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Tree structure | SceneTree exists (similar) | Adapt for discussions | **ENHANCE** |
| Background generation | Not implemented | Subagent generation | **BUILD** |
| Tree storage | Not implemented | Per-character .md files | **BUILD** |
| Branch deletion | Not implemented | Delete on use | **BUILD** |
| Regeneration trigger | Not implemented | When branches < 5 | **BUILD** |
| Idle initiation | Not implemented | After 10s silence | **BUILD** |

### Image Generation

| Capability | Current | Target | Gap |
|------------|---------|--------|-----|
| Manual generation | `generate_images_for_existing.py` | Automatic on place creation | **ENHANCE** |
| Prompt construction | Exists | Same | None |
| Storage path | `frontend/public/images/` | Same | None |
| SSE notification | Not implemented | `image_ready` event | **BUILD** |

---

## Key Decisions Made

1. **No orchestrator** — Graph is the orchestrator
2. **TaskOutput for completion** — Not hook injection
3. **Hook for interruptions only** — Character speaks, player UI
4. **Ephemeral discussion trees** — Generated, used, deleted
5. **Automatic image generation** — Triggered by graph

---

## Open Questions

1. **SSE reconnection** — How to handle dropped connections?
2. **Image generation queue** — Rate limiting for many places?
3. ~~**Discussion tree format**~~ — **Resolved: JSON**
4. **Map rendering** — Leaflet, Mapbox, or custom?

---

## Next Action

Start with **Phase 1: Graph SSE Foundation**

This unlocks real-time updates for all other phases.

---

## KNOWN ISSUES

### Injection queue format mismatch

- **Severity:** medium
- **Symptom:** Hook readers consume JSONL while some manual tooling expects
  a JSON array, causing confusion and divergent tooling paths.
- **Suspected cause:** Legacy scripts and newer async hooks evolved separately
  without consolidation into a single queue contract.
- **Attempted:** Documented the split and flagged follow-up in TODO to unify
  or retire legacy paths before implementation begins.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Updated the SYNC to restore missing sections and left
the capability tables intact for implementation planning.

**What you need to understand:**
The async system is still design-only; no code changes are part of this repair.
Use the capability tables and the injection queue decision as the source of
truth until implementation begins.

**Watch out for:**
Do not treat `injection_queue.json` and `.jsonl` as interchangeable; the
hook scripts and API currently expect JSONL.

**Open questions I had:**
Should the legacy JSON array queue be deprecated or migrated to JSONL before
frontend wiring starts?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
This repair fills missing SYNC template sections for async architecture so the
module state is explicit and compliant. No code changes were made; the doc
now spells out maturity, handoffs, and known issues.

**Decisions made:**
None beyond documenting existing queue format mismatch and aligning SYNC
headings with the template requirements.

**Needs your input:**
Confirm whether we should deprecate the legacy JSON array queue or migrate it
to JSONL as the canonical format before implementation.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Focused and confident once the missing sections were enumerated; primary
concern is keeping the detailed tables without losing template compliance.

**Threads I was holding:**
The queue format mismatch, SSE schema needs, and how to stage implementation
without violating the async design principles.

**Intuitions:**
Resolve the queue format early to avoid compounding tool divergence later.

**What I wish I'd known at the start:**
That the SYNC template expects explicit handoff and TODO sections even when
the document already contains detailed planning tables.

---

## Known Issues

- Queue format drift persists across hook scripts and API endpoints; the JSONL vs JSON split still needs reconciliation to avoid runtime confusion.
- SSE emission remains unimplemented, so real-time state updates are documented but not yet proven in runtime behavior.

---

## HANDOFF: FOR AGENTS

Likely VIEW: VIEW_Implement_Write_Or_Modify_Code. Focus on aligning queue formats and adding SSE emissions; verify changes against PATTERNS/ALGORITHM/IMPLEMENTATION before touching runtime code.

---

## HANDOFF: FOR HUMAN

Async travel remains a design-first architecture; no runtime SSE or injection queue wiring is complete, so implementation sequencing needs product confirmation before execution.

---

## TODO

- [ ] Reconcile injection queue format (JSONL vs JSON array) across scripts and API endpoints.
- [ ] Define SSE reconnection and replay semantics before implementation work begins.

---

## CONSCIOUSNESS TRACE

This update fills missing SYNC template sections to keep the async architecture audit trail consistent and to reduce drift between design docs and implementation intent.

---

## POINTERS

- `docs/infrastructure/async/ALGORITHM_Async_Architecture.md` for procedural flow and decision points.
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` for file paths and runtime expectations.

---

## CONFLICTS

### DECISION: Injection queue format split
- Conflict: `engine/scripts/check_injection.py` and `/api/inject` use `injection_queue.jsonl`, while `engine/scripts/inject_to_narrator.py` and `engine/infrastructure/api/playthroughs.py` use `injection_queue.json`.
- Resolution: Treat `injection_queue.jsonl` as the async hook queue for interruptions; `injection_queue.json` is legacy/manual tooling and should be reconciled in a follow-up.
- Reasoning: The hook reader and API endpoint already operate on JSONL, which matches the async architecture design docs.
- Updated: `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`, `docs/infrastructure/async/SYNC_Async_Architecture.md`.

---

## ARCHIVE

Older content archived to:
- `docs/infrastructure/async/SYNC_Async_Architecture_archive_2025-12.md`
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`

---

## Agent Observations

### Remarks
- The discussion tree details and data flow diagram were valuable but pushed the module over size limits, so they are now stored in the archive file.

### Suggestions
- [ ] If this module grows again, consider splitting other large docs (like `PATTERNS_Async_Architecture.md`) into overview + parts to keep the chain lean.

### Propositions
- A dedicated `docs/infrastructure/async/diagrams/` folder could host future visual assets without bloating core docs.


---

## ARCHIVE

Older content archived to: `SYNC_Async_Architecture_archive_2025-12.md`
