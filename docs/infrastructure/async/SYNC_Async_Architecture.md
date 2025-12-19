# Async Architecture — State & Implementation Plan

**Last Updated:** 2024-12-16
**Status:** DESIGNING
**Version:** 2.0

---

## Overview

This document tracks what exists, what needs to be built, and the implementation path for the async architecture.

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
| Hook script | Not implemented | `check_injection.py` | **BUILD** |
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

- Consolidated async algorithm docs into `ALGORITHM_Async_Architecture.md` and removed per-topic algorithm files to keep a single canonical algorithm reference.


---

## ARCHIVE

Older content archived to: `SYNC_Async_Architecture_archive_2025-12.md`
