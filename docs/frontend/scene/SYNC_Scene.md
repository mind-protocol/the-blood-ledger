# Scene View — Sync: Current State

```
LAST_UPDATED: 2024-12-17
UPDATED_BY: Codex agent
STATUS: DESIGNING → IMPLEMENTING
```

---

## Snapshot

| Area | Status | Owner | Notes |
|------|--------|-------|-------|
| Layout skeleton | Not started | Frontend | Need wireframe for header/voices/moments sidebar |
| Data contract | Specced | Engine | `/api/view` definition lives in docs/physics/API_Physics.md |
| Click/Wait loop | Specced | Engine/Frontend | Requires moment graph implementation |
| Image integration | Ready | Image-gen | Use banner assets from SYNC_Image_Generation.md |

---

## Open Questions

| Question | Decision Needed By | Impact |
|----------|--------------------|--------|
| Voice slots per view | Before UI build | Determines layout + emphasis |
| Choice surfacing | Before hook implementation | Affects UX + backend contract |
| Idle/Wait feedback | Before first playtest | Ensures players notice auto-advances |
| Ledger linking UI | After basic view works | Aligns with ledger team work |

---

## Next Deliverables

1. **UI wireframe** (Figma or low-fi) showing: atmosphere header, moment stack, voices, choices.
2. **Frontend stub** hitting mocked `/api/view` data (use `docs/physics/API_Physics.md` example).
3. **Interaction loop** handling click + wait + SSE events once backend ready.

Each deliverable should update this SYNC with owner + ETA.

---

## Dependencies

- Moment graph implementation (docs/physics/SYNC_Physics.md)
- Opening conversion so first scene emits moments
- Image generation banners for every place (see SYNC_Image_Generation.md)

---

## Handoff Notes

- Treat current state as design baseline; no production UI exists yet.
- Prioritize feel (voices/weight) before polish (animations/audio).
- Capture playtest learnings under “What We Learned” next time you update this file.
