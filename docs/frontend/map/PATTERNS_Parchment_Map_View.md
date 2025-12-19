# Map View — Patterns: Parchment Map With Fog Of War

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Parchment_Map_View.md
SYNC:  ./SYNC_Map_View.md
IMPL:  frontend/components/map/MapClient.tsx
```

---

## THE PROBLEM

Players need a full-screen map to explore geography, routes, and place details
without breaking the fiction of a medieval atlas. The scene view alone does not
provide spatial context for travel or regional relationships.

---

## THE PATTERN

Render an atmospheric parchment map on a canvas with layered terrain, routes,
places, and fog of war. Use visibility levels to control what is revealed and
provide hover/select affordances for place detail without mutating game state.

---

## PRINCIPLES

### Principle 1: Layered Canvas Rendering

Canvas layers let the map feel handcrafted while keeping rendering performant
for dense route and place overlays.

### Principle 2: Visibility Drives Revelation

All routes and places flow through visibility state so the map respects
discovery progression, using partial fog cutouts and muted colors instead of
full disclosure.

### Principle 3: Read-Only Interaction

Hover and selection provide context without triggering travel or state updates,
keeping the map focused on exploration.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/types/map` | Shared map and visibility types used by the canvas and client UI |
| `frontend/lib/map` | Projection and distance helpers for rendering and travel estimates |
| `frontend/data/map-data` | Seed data for places, routes, and coastline geometry |

---

## WHAT THIS DOES NOT SOLVE

- Live travel or backend-driven state updates.
- Persisting player travel decisions from the map itself.
- Editing map data from the UI.
- Mobile-first interaction or pinch/zoom controls.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Replace sample data with backend-provided map state.
- [ ] Wire travel actions into the real playthrough flow.
- [ ] Decide how map zoom/pan should behave for large regions.
- [ ] Confirm visibility radius tuning for rumored vs known places.
