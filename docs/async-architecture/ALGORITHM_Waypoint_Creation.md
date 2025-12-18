# Waypoint Creation — Algorithm

**Purpose:** How places materialize during travel.

---

## Principle

Runner creates ALL intermediate places during travel.
No skeleton. No pre-authored waypoints.
The world materializes as Runner writes to graph.
Images generate automatically on creation.

---

## Creation Flow

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

---

## Place Node Schema

```json
{
  "id": "place_humber_crossing",
  "name": "The Humber Crossing",
  "type": "crossing",
  "terrain": ["river", "mudflats", "reeds"],
  "atmosphere": "Grey water. Cold wind. The smell of salt and decay.",
  "position": { "lat": 53.7, "lng": -0.5 },
  "image_url": null,
  "created_by": "runner",
  "created_during": "travel_camp_to_york"
}
```

---

## Naming Patterns

| Type | Pattern | Examples |
|------|---------|----------|
| road | The [Adjective] [Road/Way/Path] | The Muddy Way, The North Road |
| crossing | [River] Crossing, [River] Ford | Humber Crossing, Ouse Ford |
| landmark | The [Feature], [Name]'s [Feature] | The Standing Stone, Aldric's Ridge |
| ruin | The [Ruined/Burned/Old] [Building] | The Burned Hall, The Old Chapel |
| camp | A [Terrain] [Clearing/Hollow/Ridge] | A Wooded Hollow, A Windy Ridge |

---

## Persistence

**Places are canon the moment they enter the graph.**

All created places persist forever:
- Player may return
- characters reference locations
- Events can occur there later
- World builds through travel

There's no "tentative" state. Once written, it's real.

---

## Graph Write

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
