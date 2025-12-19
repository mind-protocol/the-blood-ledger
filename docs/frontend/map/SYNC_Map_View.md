# Map View — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:  ./PATTERNS_Interactive_Travel_Map.md
THIS:      SYNC_Map_View.md (you are here)
IMPL:      frontend/components/map/MapClient.tsx
```

---

## MATURITY

**What's canonical (v1):**
- Full-screen map view with parchment styling and layered rendering.
- Hover tooltips and selectable places in the canvas.

**What's still being designed:**
- Integration with live game state instead of sample data.
- Travel action wiring and map-to-scene transitions.

**What's proposed (v2+):**
- Animated reveals for newly discovered locations.

---

## CURRENT STATE

The map view is implemented as a client-side container (`MapClient`) and a
canvas renderer (`MapCanvas`). It uses sample data and visibility state to
render terrain, routes, fog-of-war, and place markers, plus hover and selection
interactions.

---

## RECENT CHANGES

### 2025-12-19: Documented map view module

- **What:** Added map module docs, mapping, and DOCS reference.
- **Why:** Repair task flagged map components as undocumented.
- **Files:** `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`, `docs/frontend/map/SYNC_Map_View.md`, `modules.yaml`, `frontend/components/map/MapClient.tsx`

### 2025-12-19: Mapped map route entrypoint

- **What:** Added the app route (`frontend/app/map/**`) to the map module mapping and linked the route to map docs.
- **Why:** Ensure the map view entrypoint is discoverable from docs and manifest.
- **Files:** `modules.yaml`, `frontend/app/map/page.tsx`

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documented the map module and linked the entrypoint.

**What you need to understand:**
The map UI is read-only and uses sample data. Any real travel behavior must be
handled outside the map view.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Update docs if map behavior changes beyond read-only display.

### Tests to Run

```bash
npm test
```
