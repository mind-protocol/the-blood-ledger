# Map System — Behaviors: Visibility & Interaction

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Rendering.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Visibility System

Player knowledge of places and routes. Stored per playthrough, not in global graph.

### Visibility Levels

| Level | Description | Map Appearance |
|-------|-------------|----------------|
| `unknown` | Player doesn't know it exists | Hidden |
| `rumored` | Heard about, never seen | Faded, "Name?", approximate position |
| `known` | Seen or detailed description | Clear, accurate position |
| `familiar` | Visited, well-understood | Bright, bold name, travel times shown |

---

## PlayerVisibility Schema

```yaml
PlayerVisibility:
  place_id: string
  level: unknown | rumored | known | familiar
  discovered_at: int     # Game tick when first learned
  visited_at: int        # Game tick when visited (null if never)
```

### Storage

```yaml
# playthroughs/{id}/visibility.yaml
places:
  place_york:
    level: familiar
    discovered_at: 0      # Starting location
    visited_at: 0

  place_durham:
    level: rumored
    discovered_at: 1250
    visited_at: null

  place_whitby:
    level: known
    discovered_at: 3400
    visited_at: null

routes:
  place_york_to_place_durham:
    level: rumored
    discovered_at: 1250
```

---

## Visibility Update Rules

```python
def update_place_visibility(player_vis: dict, place_id: str, event: str, tick: int) -> str:
    """
    Update visibility based on event.

    Args:
        player_vis: Current visibility state
        place_id: Place being updated
        event: What happened
        tick: Current game tick

    Returns:
        New visibility level
    """
    current = player_vis.get(place_id, {}).get('level', 'unknown')

    if event == 'visited':
        # Visiting makes it familiar
        return 'familiar'

    if event == 'passed_through':
        # Passing through while traveling → at least known
        if current in ['unknown', 'rumored']:
            return 'known'
        return current

    if event == 'told_about':
        # Hearing about it → rumored if unknown
        if current == 'unknown':
            return 'rumored'
        return current

    if event == 'saw_on_map':
        # Seeing on a physical map → rumored
        if current == 'unknown':
            return 'rumored'
        return current

    if event == 'detailed_description':
        # Detailed description from someone who's been there → known
        if current in ['unknown', 'rumored']:
            return 'known'
        return current

    return current
```

### Event Sources

| Event | Source | Result |
|-------|--------|--------|
| `visited` | Player arrives at location | → `familiar` |
| `passed_through` | On route between two places | → `known` |
| `told_about` | NPC mentions the place | → `rumored` |
| `saw_on_map` | Player examines a map item | → `rumored` |
| `detailed_description` | NPC gives detailed directions | → `known` |

---

## Route Visibility

Routes become visible when:
1. Both endpoints are at least `rumored`
2. Player has traveled the route OR heard about it

```python
def get_route_visibility(route, player_vis):
    """Determine route visibility from endpoint visibility."""
    from_vis = player_vis.get(route.from_place, {}).get('level', 'unknown')
    to_vis = player_vis.get(route.to_place, {}).get('level', 'unknown')

    # Both ends must be known
    if from_vis == 'unknown' or to_vis == 'unknown':
        return 'unknown'

    # Route-specific visibility
    route_vis = player_vis.get(f"route_{route.from_place}_{route.to_place}", {})
    route_level = route_vis.get('level', 'unknown')

    # If route itself is known, show it
    if route_level in ['known', 'familiar']:
        return route_level

    # If both ends are at least rumored, show as rumored
    if from_vis in ['rumored', 'known', 'familiar'] and \
       to_vis in ['rumored', 'known', 'familiar']:
        return 'rumored'

    return 'unknown'
```

---

## What Shows at Each Level

### Places

| Level | Icon | Label | Position | Detail on Hover |
|-------|------|-------|----------|-----------------|
| `unknown` | — | — | — | — |
| `rumored` | Faded (50% opacity) | "Name?" | ±10km approximate | "You've heard of this place" |
| `known` | Clear (85% opacity) | Name | Accurate | Basic description |
| `familiar` | Bright (100% opacity) | **Name** (bold) | Accurate | Full description |

### Routes

| Level | Line | Travel Time | Detail |
|-------|------|-------------|--------|
| `unknown` | Hidden | — | — |
| `rumored` | Dotted, faded | Hidden | "A road is said to connect..." |
| `known` | Solid, clear | Shown | Road type, difficulty |
| `familiar` | Solid, bold | Shown + landmarks | Full description |

---

## Position Uncertainty

Rumored places have approximate positions:

```python
def get_display_position(place, visibility, rng_seed):
    """Get display position, with uncertainty for rumored places."""
    base_lat, base_lng = place.coordinates

    if visibility == 'rumored':
        # Add random offset (consistent per place)
        rng = seeded_random(rng_seed + hash(place.id))
        offset_km = 5 + rng() * 10  # 5-15 km off

        # Convert to degrees (~111 km per degree lat, ~70 km per degree lng at this latitude)
        lat_offset = (rng() - 0.5) * 2 * (offset_km / 111)
        lng_offset = (rng() - 0.5) * 2 * (offset_km / 70)

        return [base_lat + lat_offset, base_lng + lng_offset]

    return [base_lat, base_lng]
```

When the player visits, the position "snaps" to correct location.

---

## Interaction Behaviors

### Click on Place

```typescript
interface PlaceClickEvent {
  place: Place;
  visibility: VisibilityLevel;
  action: 'select' | 'travel' | 'info';
}

function handlePlaceClick(place: Place, visibility: string): PlaceClickEvent {
  if (visibility === 'unknown') {
    return null;  // Can't click unknown places
  }

  if (visibility === 'rumored') {
    return {
      place,
      visibility,
      action: 'info'  // Can only view what we've heard
    };
  }

  // known or familiar
  return {
    place,
    visibility,
    action: 'select'  // Can select as destination or view info
  };
}
```

### Hover on Place

```typescript
interface PlaceHoverInfo {
  name: string;
  type: string;
  visibility: string;
  detail: string | null;
  travelTime: number | null;  // From current location, if known
}

function getPlaceHoverInfo(place: Place, visibility: string, playerLocation: string): PlaceHoverInfo {
  if (visibility === 'unknown') return null;

  const info: PlaceHoverInfo = {
    name: visibility === 'rumored' ? `${place.name}?` : place.name,
    type: place.type,
    visibility,
    detail: null,
    travelTime: null
  };

  // Detail based on visibility
  if (visibility === 'rumored') {
    info.detail = "You've heard of this place.";
  } else if (visibility === 'known') {
    info.detail = place.detail || `A ${place.type}.`;
  } else if (visibility === 'familiar') {
    info.detail = place.detail || `A ${place.type} you know well.`;
  }

  // Travel time only if we know the route
  if (visibility !== 'rumored') {
    const route = getRoute(playerLocation, place.id);
    if (route) {
      info.travelTime = route.travel_minutes;
    }
  }

  return info;
}
```

### Click to Travel

```typescript
function handleTravelClick(destination: Place, playerLocation: string) {
  const route = getRoute(playerLocation, destination.id);

  if (!route) {
    // No direct route
    return {
      type: 'no_route',
      message: "You don't know a way there."
    };
  }

  // Emit travel request to Narrator
  return {
    type: 'travel_request',
    from: playerLocation,
    to: destination.id,
    route: route,
    estimatedTime: route.travel_minutes
  };
}
```

---

## Map Component Props

```typescript
interface MapProps {
  // Data
  places: Place[];
  routes: Route[];
  playerVisibility: Record<string, VisibilityState>;

  // Player state
  playerPosition: string | [number, number];  // Place ID or [lat, lng]
  playerDestination?: string;
  travelProgress?: number;  // 0-1 if traveling

  // Dynamic elements
  npcsMoving: {
    characterId: string;
    route: Route;
    progress: number;
  }[];
  tensions: {
    placeId: string;
    level: number;  // 0-1
  }[];

  // Animation
  animationTick: number;

  // Callbacks
  onSelectPlace: (place: Place) => void;
  onHoverPlace: (place: Place | null) => void;
  onRequestTravel: (from: string, to: string) => void;
}
```

---

## Visibility Changes During Play

### Starting the Game

```python
def initialize_visibility(starting_place: str) -> dict:
    """Set initial visibility for new game."""
    return {
        'places': {
            starting_place: {
                'level': 'familiar',
                'discovered_at': 0,
                'visited_at': 0
            }
        },
        'routes': {}
    }
```

### After Conversation

When NPC mentions a place:

```python
def on_narrator_mentions_place(place_id: str, detail_level: str, tick: int, visibility: dict):
    """Update visibility when Narrator mentions a place."""
    current = visibility['places'].get(place_id, {}).get('level', 'unknown')

    if detail_level == 'vague':
        # "I've heard of a monastery to the north..."
        new_level = update_place_visibility(visibility, place_id, 'told_about', tick)
    elif detail_level == 'specific':
        # "Whitby is two days north along the coast..."
        new_level = update_place_visibility(visibility, place_id, 'detailed_description', tick)

    visibility['places'][place_id] = {
        'level': new_level,
        'discovered_at': visibility['places'].get(place_id, {}).get('discovered_at', tick),
        'visited_at': visibility['places'].get(place_id, {}).get('visited_at')
    }
```

### After Travel

```python
def on_travel_complete(from_place: str, to_place: str, route_waypoints: list, tick: int, visibility: dict):
    """Update visibility after completing travel."""

    # Destination becomes familiar
    visibility['places'][to_place] = {
        'level': 'familiar',
        'discovered_at': visibility['places'].get(to_place, {}).get('discovered_at', tick),
        'visited_at': tick
    }

    # Route becomes familiar
    route_key = f"route_{from_place}_{to_place}"
    visibility['routes'][route_key] = {
        'level': 'familiar',
        'discovered_at': visibility['routes'].get(route_key, {}).get('discovered_at', tick)
    }

    # Places passed through become known
    for waypoint_place in get_places_on_route(route_waypoints):
        if waypoint_place not in [from_place, to_place]:
            current = visibility['places'].get(waypoint_place, {}).get('level', 'unknown')
            if current in ['unknown', 'rumored']:
                visibility['places'][waypoint_place] = {
                    'level': 'known',
                    'discovered_at': visibility['places'].get(waypoint_place, {}).get('discovered_at', tick),
                    'visited_at': None
                }
```

---

## Map Interaction Flow

```
Player clicks on York (familiar)
    │
    └── Map emits: onSelectPlace(place_york)
            │
            ▼
        UI shows: Place panel with
            - Name: "York"
            - Description: "The second city..."
            - Options: [Travel] [View]
            │
            └── Player clicks [Travel]
                    │
                    ▼
                Map emits: onRequestTravel("place_camp", "place_york")
                    │
                    ▼
                Narrator receives travel request
                    │
                    ▼
                Narrator: "You set out for York. Two days on foot."
                    │
                    ▼
                Narrator calls Runner with max_minutes=2880
```

---

## Discovery Moments

The map creates discovery experiences:

### "I found a new place"

```
Player travels to York
    │
    ▼
Route passes near Ripon
    │
    ▼
Visibility: Ripon becomes 'known'
    │
    ▼
Map: Ripon icon appears, fog clears
    │
    ▼
Player: "Oh, there's a town here!"
```

### "The rumor was wrong"

```
Player hears about "a crossing to the east"
    │
    ▼
Visibility: Crossing becomes 'rumored' at approximate position
    │
    ▼
Map: Faded icon appears, "Crossing?"
    │
    ▼
Player travels there
    │
    ▼
Visibility: Becomes 'familiar', position corrects
    │
    ▼
Map: Icon snaps to correct location
    │
    ▼
Player: "It wasn't where I thought!"
```

### "The world grew"

```
Player talks to merchant in York
    │
    ▼
Merchant mentions Durham, Whitby, Scarborough
    │
    ▼
Visibility: All become 'rumored'
    │
    ▼
Map: Three new faded icons appear
    │
    ▼
Player: "There's so much more to explore"
```

---

## Integration with Narrator

The Narrator informs visibility changes:

```yaml
# In Narrator's graph_mutations
visibility_updates:
  - place: place_durham
    event: told_about
    source: char_merchant
    detail: "A great cathedral city to the north"

  - place: place_whitby
    event: detailed_description
    source: char_aldric
    detail: "I know the way. Two days along the coast."
```

The engine applies these updates after each Narrator response.

---

*"The map shows what you know. And you learn by exploring, traveling, and listening."*
