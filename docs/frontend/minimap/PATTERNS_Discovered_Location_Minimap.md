# Minimap — Patterns: Discovered Location Snapshot

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Discovered_Location_Minimap.md
SYNC:  ./SYNC_Minimap.md
IMPL:  frontend/components/minimap/Minimap.tsx
```

---

## THE PROBLEM

Players need a quick spatial cue for where they are and what nearby locations
have been discovered without leaving the main scene. Opening the full map for
every check interrupts the narrative flow.

---

## THE PATTERN

Render a compact, read-only minimap that plots discovered locations and
highlights the current location. The minimap acts as a lightweight preview that
invites opening the full map view when more context is needed.

---

## SCOPE

This pattern covers the UI snapshot rendered inside the minimap button,
including location dots, connection lines, and current-location emphasis. It
does not cover map navigation, pathfinding, or any state mutation beyond the
single "open full map" action delegated to parent components.

---

## PRINCIPLES

### Principle 1: Snapshot Over Navigation

The minimap is a status display, not an interactive map. Interaction is limited
to a single action that opens the full map.

### Principle 2: Discovered-Only Rendering

Only discovered locations and their connections are shown to avoid spoiling
unseen areas.

### Principle 3: Current Location Emphasis

The player's current location is visually distinct to anchor the scene in
space at a glance.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/types/game` | MapRegion and location data shapes for rendering |
| `frontend/components/map` | Full map view opened from the minimap action |

---

## INSPIRATIONS

Compact minimap widgets from strategy titles and action RPGs influenced the
idea of a glanceable, low-friction spatial cue, while tabletop map handouts
inspired the "peek without leaving the scene" interaction posture.

---

## WHAT THIS DOES NOT SOLVE

- Editing or navigating the map directly from the minimap.
- Handling undiscovered location hints or fog-of-war transitions.
- Persisting map state beyond what the parent passes in.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm if connection lines should fade when locations are only partially discovered.
- [ ] Decide if the minimap should display region names or remain location-only.
