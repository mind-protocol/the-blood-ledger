# Frontend — Sync Archive: 2025-12

```
ARCHIVED_ON: 2025-12-19
ARCHIVED_BY: Codex (repair agent)
SOURCE: SYNC_Frontend.md (pre-condensed)
```

---

## CURRENT STATE

This archive captures the late-2025 frontend sync snapshot, preserving the
pre-condensed state notes before the frontend docs were trimmed to stay under
module size thresholds.

---

## IN PROGRESS

No active work remains in this archive. The live workstream moved back to
`docs/frontend/SYNC_Frontend.md`, where updates now continue.

---

## KNOWN ISSUES

Frontend tests remain sparse and the dual-hook setup (`useGameState` plus
`useMoments`) increases coordination risk when refactoring state flows.

---

## HANDOFF: FOR AGENTS

If you need current status, read `docs/frontend/SYNC_Frontend.md` first, then
use this archive only for historical context about 2025-12 changes.

---

## HANDOFF: FOR HUMAN

This archive is for traceability only; it preserves earlier sync narratives.
Current decisions and active questions are tracked in the live SYNC file.

---

## TODO

- Review frontend test strategy notes in the live SYNC file before changing
  state management or component architecture.

---

## CONSCIOUSNESS TRACE

The archive reflects a period focused on documentation hygiene and alignment;
most remaining risk was around tests and state-hook consolidation.

---

## POINTERS

| What | Where |
|------|-------|
| Current frontend sync | `docs/frontend/SYNC_Frontend.md` |
| Condensed archive note | `docs/frontend/archive/SYNC_archive_2024-12.md` |
| Frontend patterns | `docs/frontend/PATTERNS_Presentation_Layer.md` |



---

# Archived: SYNC_Frontend.md

Archived on: 2025-12-20
Original file: SYNC_Frontend.md

---

## RECENT CHANGES

### 2025-12-19: PATTERNS scope completion
- Added the missing SCOPE section to the presentation layer patterns doc.
- Expanded dependencies, inspirations, and gaps to match template expectations.
- Ran `cd frontend && npm run build` and `ngram validate` (remaining failures are pre-existing doc-chain gaps).

### 2025-12-19: Restored frontend sync archive file
- Recreated `docs/frontend/SYNC_Frontend_archive_2025-12.md` with full template
  sections to resolve doc-template drift for the archived snapshot.

### 2025-12-19: Algorithm template completion
- Added missing template sections (CHAIN, data structures, complexity, helpers).
- Expanded data flow narrative and clarified interactions for SSE + REST paths.

### 2025-12-19: Implementation overview fill-in
- Added LOGIC CHAINS and CONCURRENCY MODEL sections to the frontend implementation overview entry point.
- Ran `cd frontend && npm run build` to verify the doc update against the current frontend build.

### 2025-12-19: Size verification
- Confirmed the frontend doc chain is ~32K chars (below the 50K module threshold).

### 2025-12-19: Split implementation doc
- Replaced the monolithic implementation doc with an overview entry point and two focused parts.
- Line counts: 394L → 233L across `IMPLEMENTATION_Frontend_Code_Architecture.md`, `IMPLEMENTATION_Code_Structure.md`, `IMPLEMENTATION_Runtime_And_Config.md`.

### 2025-12-19: Archive consolidation
- Moved the previous SYNC archive to `docs/frontend/archive/SYNC_archive_2024-12.md` and condensed it.

### 2025-12-19: DOCS reference updates
- Updated frontend DOCS pointers to use the new implementation entry point.

---



---

# Archived: SYNC_Frontend.md

Archived on: 2025-12-20
Original file: SYNC_Frontend.md

---

## RECENT CHANGES

### 2025-12-21: Resume SSE subscription for default playthrough

- **What:** `frontend/hooks/useGameState.ts` now subscribes to `/api/moments/stream/{playthrough_id}` whenever a playthrough ID is available, including the default `'beorn'` dev playthrough.
- **Why:** The demo/default path previously hit the guard that skipped SSE, so player input never triggered `moment_spoken`/`moment_activated` refreshes. Energy/canon documentation underlines that action → energy → canon should always flow through the stream.
- **Impact:** Sending messages on the default playthrough now triggers the documented SSE-driven refresh, closing the "no response" experience loop.

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

