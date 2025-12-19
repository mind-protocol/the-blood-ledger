# Async Architecture — State & Implementation Plan

**Last Updated:** 2025-12-19
**Status:** DESIGNING
**Version:** 2.0

---

## Overview

This document tracks what exists, what needs to be built, and the implementation path for the async architecture.

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

## Recent Changes

- Verified the async implementation doc already lists the `engine/scripts/inject_to_narrator.py` code-to-docs link and aligned the hook-script path in this SYNC table.
- Updated async implementation doc to replace runtime-only file references with configured script paths so all references point to tracked files.
- Refreshed the async implementation doc to match current queue file formats/paths (JSONL default queue, JSON array per playthrough) and updated entry point lines and config table; noted the playthrough initialization mismatch as a gap.
- Reverified `IMPLEMENTATION_Async_Architecture.md` after the broken-link report; no additional path corrections were needed.
- Split async algorithm docs into `docs/infrastructure/async/ALGORITHM/` with an overview and focused parts (Runner, Hook, Graph SSE, Waypoints/Fog, Image Generation, Discussion Trees), added `ALGORITHM_Async_Architecture.md` as the entry point, and updated CHAIN references.
- Added `IMPLEMENTATION_Async_Architecture.md`, linked CHAIN references, and added DOCS pointer in `engine/scripts/check_injection.py`.
- Added DOCS pointer in `engine/scripts/inject_to_narrator.py` so the manual injector resolves to the async implementation chain.
- Archived verbose discussion tree details and the data flow diagram to `docs/infrastructure/async/archive/SYNC_archive_2024-12.md` to keep module docs under size limits.

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
