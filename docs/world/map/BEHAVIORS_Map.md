# Map System — Behaviors: Visibility & Interaction

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Visibility System

Player knowledge of places and routes, stored per playthrough.

### Visibility Levels

| Level | Meaning | Map Appearance |
|-------|---------|----------------|
| `unknown` | Not known | Hidden |
| `rumored` | Heard of | Faded, approximate, "Name?" |
| `known` | Seen or described | Clear, accurate |
| `familiar` | Visited | Bright, bold, travel times shown |

---

## PlayerVisibility Schema

```yaml
PlayerVisibility:
  place_id: string
  level: unknown | rumored | known | familiar
  discovered_at: int
  visited_at: int | null
```

Storage (per playthrough): `playthroughs/{id}/visibility.yaml`.

---

## Visibility Update Rules

```python
if event == "visited":
    return "familiar"
if event == "passed_through" and current in ["unknown", "rumored"]:
    return "known"
if event == "told_about" and current == "unknown":
    return "rumored"
if event == "saw_on_map" and current == "unknown":
    return "rumored"
if event == "detailed_description" and current in ["unknown", "rumored"]:
    return "known"
return current
```

---

## Route Visibility

Rules:
1. Both endpoints must be at least `rumored`.
2. Route visibility is `known` or `familiar` only if the route itself is known.
3. Otherwise show as `rumored`.

---

## Display Rules

### Places

| Level | Icon | Label | Position |
|-------|------|-------|----------|
| `unknown` | — | — | — |
| `rumored` | 50% opacity | "Name?" | ±10km offset |
| `known` | 85% opacity | Name | Accurate |
| `familiar` | 100% opacity | **Name** | Accurate |

### Routes

| Level | Line | Travel Time | Detail |
|-------|------|-------------|--------|
| `unknown` | Hidden | — | — |
| `rumored` | Dotted, faded | Hidden | Minimal |
| `known` | Solid | Shown | Road type, difficulty |
| `familiar` | Bold | Shown | Landmarks |

---

## Interaction Behaviors

### Click on Place
- `unknown`: no interaction.
- `rumored`: info-only panel.
- `known`/`familiar`: selectable as destination.

### Hover on Place
- Shows name, type, visibility, detail.
- Travel time shown only if route is known.

### Click to Travel
- If a known route exists, emit travel request.
- If no route, return "no_route" response.

---

## Map Component Props (UI Contract)

```typescript
interface MapProps {
  places: Place[];
  routes: Route[];
  playerVisibility: Record<string, VisibilityState>;
  playerPosition: string | [number, number];
  playerDestination?: string;
  travelProgress?: number;
  npcsMoving: { characterId: string; route: Route; progress: number }[];
  tensions: { placeId: string; level: number }[];
  animationTick: number;
  onSelectPlace: (place: Place) => void;
  onHoverPlace: (place: Place | null) => void;
  onRequestTravel: (from: string, to: string) => void;
}
```

---

## Narrator Integration

Narrator emits visibility updates (e.g., `told_about`, `detailed_description`).
Engine applies updates after each response.

