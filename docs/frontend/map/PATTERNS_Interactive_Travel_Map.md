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

Players need a clear, low-friction way to initiate travel from the map without
leaving the fiction or losing spatial context. The current read-only view does
not yet express intent, confirmations, or travel cost feedback.

---

## THE PATTERN

Use the map as an interaction surface where route selection, destination
preview, and travel intent flow through a lightweight confirmation layer before
any backend actions are triggered.

---

## SCOPE

This pattern covers destination selection, route preview, and travel intent UI
states within the map view, including confirmation and feedback affordances
that keep players grounded in place.

---

## PRINCIPLES

### Principle 1: Intent Before Action

Travel starts as an intent state with clear confirmation so the player can
review the route and cost without accidental state changes.

### Principle 2: Context-Preserving Feedback

Route details, distance, and estimated impact render inline on the map so the
player never has to leave the spatial context to decide.

### Principle 3: Map Remains the Anchor

Interactions should reinforce the map as the primary surface, avoiding modal
flows that distract from geography.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/types/map` | Map route and location shapes for destination selection UI |
| `frontend/lib/map` | Distance and path helpers needed for travel previews |
| `frontend/components/map` | Canvas and interaction surfaces that capture intent |

---

## INSPIRATIONS

- Strategy travel overlays that show route intent and movement costs without
  committing the action until the player confirms.
- RPG travel screens that keep a map visible while surfacing journey risks,
  distance, or time to travel.

---

## WHAT THIS DOES NOT SOLVE

- Backend travel execution or server-side validation of routes.
- Persisting travel history or route optimization decisions.
- Advanced map navigation like zoom, drag inertia, or touch gestures.
- Multiplayer or concurrent route selection states.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide the minimum confirmation UI before travel requests are sent.
- [ ] Define the travel cost vocabulary (time, danger, supplies) for previews.
- [ ] Determine how intent interacts with fog-of-war visibility rules.
- [ ] Coordinate map actions with the main scene timeline and narration.
