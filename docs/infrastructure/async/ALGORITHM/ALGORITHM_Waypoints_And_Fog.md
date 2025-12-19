# Async Architecture - Algorithm: Waypoints and Fog

**Purpose:** Waypoint creation flow and fog-of-war visibility rules.

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Async_Architecture.md
BEHAVIORS:      ../BEHAVIORS_Travel_Experience.md
VALIDATION:     ../VALIDATION_Async_Architecture.md
IMPLEMENTATION: ../IMPLEMENTATION_Async_Architecture.md
OVERVIEW:       ALGORITHM_Overview.md
THIS:           ALGORITHM_Waypoints_And_Fog.md (you are here)
SYNC:           ../SYNC_Async_Architecture.md
```

---

## Waypoint Creation

**Purpose:** How places materialize during travel.

### Principle

Runner creates ALL intermediate places during travel.
No skeleton. No pre-authored waypoints.
The world materializes as Runner writes to graph.
Images generate automatically on creation.

### Creation Flow

```
1. Runner computes travel segment
2. Runner creates place node in graph
3. Graph triggers image generation (background)
4. Graph SSE broadcasts place_created to frontend
5. Frontend updates map immediately (no image yet)
6. Image generation completes
7. Graph SSE broadcasts image_ready
8. Frontend updates left panel if current place
```

### Place Node Schema

Place nodes include an ID, name, type, terrain, atmosphere, position, and creation metadata (`created_by`, `created_during`).

### Naming Patterns

| Type | Pattern | Examples |
|------|---------|----------|
| road | The [Adjective] [Road/Way/Path] | The Muddy Way, The North Road |
| crossing | [River] Crossing, [River] Ford | Humber Crossing, Ouse Ford |
| landmark | The [Feature], [Name]'s [Feature] | The Standing Stone, Aldric's Ridge |
| ruin | The [Ruined/Burned/Old] [Building] | The Burned Hall, The Old Chapel |
| camp | A [Terrain] [Clearing/Hollow/Ridge] | A Wooded Hollow, A Windy Ridge |

### Persistence

**Places are canon the moment they enter the graph.**

All created places persist forever:
- Player may return
- characters reference locations
- Events can occur there later
- World builds through travel

There's no "tentative" state. Once written, it's real.

### Graph Write

```python
def create_waypoint(segment):
    place = {
        "id": generate_place_id(),
        "name": generate_evocative_name(segment),
        "type": segment.terrain_type,
        "terrain": segment.terrain_features,
        "atmosphere": generate_atmosphere(segment),
        "position": segment.position,
        "created_by": "runner",
        "created_during": current_travel_id
    }

    # Write to graph (triggers SSE + image generation)
    graph.create_node("Place", place)

    return place["id"]
```

---

## Fog of War

**Purpose:** How the map shows what the player knows.

### Principle

Unknown places are hidden. Rumors create shadows.
Travel reveals. News hints.
Graph tracks visibility. Frontend renders fog.

### Visibility States

| State | Map Display | Can Travel To |
|-------|-------------|---------------|
| `unknown` | Not shown (fog) | No |
| `rumored` | Name only, faded, approximate position | Yes (may get lost) |
| `known` | Full icon, accurate position | Yes |
| `familiar` | Full detail, interior layout | Yes (faster) |

### Reveal Triggers

| Trigger | Result |
|---------|--------|
| Travel through | Becomes `known` |
| Mentioned in conversation | Becomes `rumored` |
| News/event mentions | Becomes `rumored` |
| Detailed description given | Becomes `known` |
| Player lived there | Becomes `familiar` |

### Graph Storage

Link type: `player_knows_place`

```cypher
MATCH (p:Character {id: 'char_rolf'}), (place:Place {id: 'place_york'})
CREATE (p)-[:KNOWS_PLACE {
  visibility: 'rumored',
  accuracy: 0.7,
  source: 'conversation'
}]->(place)
```

### SSE Event

```json
{
  "type": "visibility_update",
  "place_id": "place_york",
  "visibility": "known"
}
```

### Frontend Rendering

Render nothing for `unknown`, render a faded label for `rumored`, and render full markers for `known`/`familiar`.

### Travel Revelation

When Runner updates player position:

```python
def update_player_position(player_id, place_id):
    # Update position
    graph.set_property(player_id, "current_place", place_id)

    # Reveal place
    existing = graph.get_link(player_id, place_id, "KNOWS_PLACE")
    if not existing or existing["visibility"] in ["unknown", "rumored"]:
        graph.upsert_link(player_id, place_id, "KNOWS_PLACE", {
            "visibility": "known",
            "accuracy": 1.0,
            "source": "travel"
        })
        # SSE broadcast handled by graph
```
