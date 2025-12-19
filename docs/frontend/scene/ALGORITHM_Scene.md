# Scene View — Algorithm

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
BEHAVIORS:   ./BEHAVIORS_Scene.md
THIS:        ALGORITHM_Scene.md (you are here)
VALIDATION:  ./VALIDATION_Scene.md
TEST:        ./TEST_Scene.md
SYNC:        ./SYNC_Scene.md
```

---

1. **Load CurrentView**
   - Call `/api/view/{playthrough}`
   - Response contains location, characters, things, moments, transitions
2. **Render Sections**
   - Atmosphere header (location name, weather snippet)
   - Presence list (portraits + quick stats)
   - Moment stack ordered by weight
3. **Annotate Moments**
   - Resolve speaker from payload (if missing, treat as narration)
   - Highlight clickable words by matching transitions
   - Insert ledger callouts for references to debts/oaths
4. **Interaction Loop**
   - Click → POST `/api/click`
   - Free text → POST `/api/moment`
   - Wait → local timer triggers after `wait_ticks`
5. **Streaming Updates**
   - Subscribe to `/api/scene/stream`
   - Apply incremental patches (moment_created, transition_added, etc.) to the rendered state
6. **Ledger/Map Hooks**
   - Hover on characters opens Faces panel; ledger button jumps to linked entry referencing the active moment
```
