# Fog of War — Algorithm

**Purpose:** How the map shows what the player knows.

---

## Principle

Unknown places are hidden. Rumors create shadows.
Travel reveals. News hints.
Graph tracks visibility. Frontend renders fog.

---

## Visibility States

| State | Map Display | Can Travel To |
|-------|-------------|---------------|
| `unknown` | Not shown (fog) | No |
| `rumored` | Name only, faded, approximate position | Yes (may get lost) |
| `known` | Full icon, accurate position | Yes |
| `familiar` | Full detail, interior layout | Yes (faster) |

---

## Reveal Triggers

| Trigger | Result |
|---------|--------|
| Travel through | Becomes `known` |
| Mentioned in conversation | Becomes `rumored` |
| News/event mentions | Becomes `rumored` |
| Detailed description given | Becomes `known` |
| Player lived there | Becomes `familiar` |

---

## Graph Storage

Link type: `player_knows_place`

```cypher
MATCH (p:Character {id: 'char_rolf'}), (place:Place {id: 'place_york'})
CREATE (p)-[:KNOWS_PLACE {
  visibility: 'rumored',
  accuracy: 0.7,
  source: 'conversation'
}]->(place)
```

---

## SSE Event

```json
{
  "type": "visibility_update",
  "place_id": "place_york",
  "visibility": "known"
}
```

---

## Frontend Rendering

```javascript
function renderPlace(place) {
  const visibility = playerKnowledge[place.id] || 'unknown';

  switch (visibility) {
    case 'unknown':
      return null; // Don't render

    case 'rumored':
      return (
        <PlaceMarker
          position={jitterPosition(place.position)} // Approximate
          opacity={0.5}
          showIcon={false}
          label={place.name}
        />
      );

    case 'known':
      return (
        <PlaceMarker
          position={place.position}
          opacity={1.0}
          showIcon={true}
          label={place.name}
        />
      );

    case 'familiar':
      return (
        <PlaceMarker
          position={place.position}
          opacity={1.0}
          showIcon={true}
          label={place.name}
          showInterior={true}
        />
      );
  }
}
```

---

## Travel Revelation

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
