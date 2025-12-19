# Interactive Travel Map — Patterns (Deprecated)

```
STATUS: DEPRECATED
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
THIS:       PATTERNS_Interactive_Travel_Map.md (deprecated)
CANONICAL:  ./PATTERNS_Parchment_Map_View.md
SYNC:       ./SYNC_Map_View.md
IMPL:       frontend/components/map/MapClient.tsx
```

---

## THE PROBLEM

The earlier map work framed the view as a travel planner with route actions,
which was removed to avoid duplicating the canonical parchment map patterns.

---

## THE PATTERN

The interactive travel pattern has been folded into the parchment map view.
Keep this doc only as a legacy pointer to the canonical map view patterns.

---

## SCOPE

This legacy scope covered interactive route selection, confirmations, and
travel intent previews; the canonical map view now owns the active UI design.

---

## PRINCIPLES

### Principle 1: Map First, Actions Second

Travel actions should follow map comprehension, not interrupt the scan of
routes, landmarks, and fog-of-war cues.

### Principle 2: Confirm Before Committing

Any travel action should require explicit confirmation so players do not
accidentally advance the world state from exploration clicks.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/types/map` | Shared map and visibility types used by the canvas and client UI |
| `frontend/lib/map` | Projection and distance helpers for rendering and travel estimates |
| `frontend/data/map-data` | Seed data for places, routes, and coastline geometry |

---

## INSPIRATIONS

- Strategy RPG travel screens that separate route planning from the map scan.
- Narrative atlas interfaces that keep the map readable before any action.

---

## WHAT THIS DOES NOT SOLVE

- Current map interactions remain read-only; this doc does not reintroduce
  travel state mutations or backend integration.
- Mobile-first gesture handling is still out of scope for the map view module.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide if interactive travel actions re-enter the map view or live in a
  separate travel confirmation panel.
- [ ] Confirm how travel intent should be communicated to the backend when it
  becomes available.
