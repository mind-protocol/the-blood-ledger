# Map View — Patterns: Interactive Travel Map

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Interactive_Travel_Map.md
SYNC:  ./SYNC_Map_View.md
IMPL:  frontend/components/map/MapClient.tsx
```

---

## THE PROBLEM

Players need a full map view that communicates geography, travel routes, and
fog-of-war in one glance. The scene view alone cannot convey spatial
relationships or travel context.

---

## THE PATTERN

Render a full-screen parchment-style map using a layered canvas renderer.
The map exposes a hoverable, selectable surface that explains places and
routes without forcing navigation or state changes.

---

## PRINCIPLES

### Principle 1: Layered Visual Storytelling

Terrain, coastline, routes, fog, and markers are drawn in a fixed order so the
map reads like a hand-drawn chart.

### Principle 2: Visibility Gating

Unknown places and routes are hidden. Known information is revealed through
partial fog cutouts and muted colors rather than full disclosure.

### Principle 3: Read-Only Interaction

Hover and selection provide context without mutating game state. Travel actions
are presented but not executed in the map layer.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/types/map` | Place, route, and visibility shapes for rendering |
| `frontend/lib/map` | Projection and distance helpers for layout |
| `frontend/data/map-data` | Sample place/route data and coastline points |

---

## WHAT THIS DOES NOT SOLVE

- Synchronizing map data with live game state.
- Persisting player travel decisions.
- Editing or annotating the map.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Replace sample map data with live state from the game backend.
- [ ] Decide how travel actions should flow back into the scene state.
- [ ] Confirm visibility radius tuning for rumored vs known places.
