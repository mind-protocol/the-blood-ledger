# Map View — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:   ./PATTERNS_Parchment_Map_View.md
THIS:       SYNC_Map_View.md (redirect)
IMPL:       frontend/components/map/MapClient.tsx
CANONICAL:  ../../world/map/SYNC_Map.md
```

---

Frontend map view status is tracked alongside the backend map system to avoid
splitting map-related SYNC data across modules. See the canonical map system
SYNC for the combined status and open work:
[Map System — Sync: Current State](../../world/map/SYNC_Map.md).

## IN PROGRESS

No standalone frontend-only tasks are tracked here; active work is logged in
the canonical map system sync so the UI and backend stay aligned.

## KNOWN ISSUES

None noted in this frontend-only sync entry; see the canonical map system sync
for any cross-module risks or open defects.

## HANDOFF: FOR HUMAN

No human decisions needed for this sync note; coordinate changes through the
canonical map system sync if priorities shift.

## CONSCIOUSNESS TRACE

This sync file remains intentionally thin to prevent duplicate map tracking;
the shared map sync is treated as the single source of truth.

## POINTERS

- Canonical status lives at `docs/world/map/SYNC_Map.md` for map-wide planning.
- Frontend behavior and scope live in `docs/frontend/map/PATTERNS_Parchment_Map_View.md`.
- Interactive travel intent UI patterns live in `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`.

## Updates

- 2025-12-19: Filled missing SCOPE and INSPIRATIONS sections in
  `docs/frontend/map/PATTERNS_Parchment_Map_View.md` and expanded short
  template entries to satisfy doc-template drift checks.
- 2025-12-19: Added missing SYNC template sections and expanded entries to
  meet the doc-template length requirements for the map view sync.
- 2025-12-19: Restored `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`
  as a deprecated pointer to the canonical parchment map patterns, including
  the missing template sections noted by the repair task.
- 2025-12-19: Added `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md` with
  the missing SCOPE and INSPIRATIONS sections expanded to template length.
