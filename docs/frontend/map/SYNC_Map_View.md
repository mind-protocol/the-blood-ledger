# Map View — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:  ./PATTERNS_Parchment_Map_View.md
THIS:      SYNC_Map_View.md (you are here)
IMPL:      frontend/components/map/MapClient.tsx
```

---

## MATURITY

**What's canonical (v1):**
- Full map view renders a parchment canvas with routes, places, fog, and markers.
- Hover and selection surface place details in the UI.

**What's still being designed:**
- Real game-state wiring for visibility and player position.
- Interaction model for travel and map navigation.

**What's proposed (v2+):**
- Zoom/pan gestures and region-level navigation.

---

## CURRENT STATE

The map view uses `MapClient` to host a full-screen layout with header, map
canvas, selected-place panel, and legend. `MapCanvas` draws layered terrain,
routes, places, fog-of-war masks, and player markers using seeded randomness
for a parchment feel. State is currently seeded from static map data and a
fixed player position, with hover and selection callbacks for detail display.

---

## RECENT CHANGES

### 2025-12-19: Documented map view module

- **What:** Added map view module docs, mapping, and DOCS reference.
- **Why:** Repair task flagged `frontend/components/map` as undocumented.
- **Files:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`, `docs/frontend/map/SYNC_Map_View.md`, `modules.yaml`, `frontend/components/map/MapClient.tsx`

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documented the map view module and linked the entrypoint.

**What you need to understand:**
The map view is currently a self-contained UI using sample data. Any gameplay
travel or discovery logic still needs to be wired to backend state.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Update docs if the map view data flow changes.

### Tests to Run

```bash
npm test
```
