# Map System — Algorithm: Places

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## Place Schema

```yaml
Place:
  id: string              # place_york, place_york_market
  name: string            # "York", "York Market"
  coordinates: [float, float]  # [lat, lng]
  scale: string           # region | settlement | district | building | room
  type: string            # city | village | monastery | hold | crossing | etc
  detail: string          # Atmosphere, description
  detail_embedding: float[]  # Embedded if detail > 20 chars
```

### Field Details

| Field | Required | Notes |
|-------|----------|-------|
| `id` | Yes | Unique, prefixed `place_` |
| `name` | Yes | Display name |
| `coordinates` | Yes | [latitude, longitude] |
| `scale` | Yes | Determines movement rules |
| `type` | Yes | Determines icon |
| `detail` | No | Atmosphere/description for Narrator |
| `detail_embedding` | Auto | Generated if detail > 20 chars |

---

## Scale Levels

Five hierarchical scales:

| Scale | Examples | Typical Area | Movement Within |
|-------|----------|--------------|-----------------|
| `region` | Northumbria, Yorkshire | 1000+ km² | Requires ROUTE |
| `settlement` | York, Durham, Whitby | 1-10 km² | Free (~15 min between districts) |
| `district` | York Market, Minster Quarter | 0.1-1 km² | Free (~5 min between buildings) |
| `building` | Merchant's Hall, The Minster | 100-10000 m² | Free (~1 min between rooms) |
| `room` | Back Room, Crypt | 10-500 m² | Instant |

### Scale Rules

```python
SCALE_HIERARCHY = ['region', 'settlement', 'district', 'building', 'room']

def can_contain(parent_scale, child_scale):
    """Check if parent scale can contain child scale."""
    parent_idx = SCALE_HIERARCHY.index(parent_scale)
    child_idx = SCALE_HIERARCHY.index(child_scale)
    return child_idx == parent_idx + 1

# region can contain settlement
# settlement can contain district
# district can contain building
# building can contain room
# room contains nothing
```

---

## Place Types

Types determine map icons:

| Type | Icon | Typical Scale |
|------|------|---------------|
| `city` | ⬡ | settlement |
| `town` | ◆ | settlement |
| `village` | ● | settlement |
| `monastery` | † | settlement/building |
| `hold` | ▲ | settlement/building |
| `crossing` | ═ | settlement |
| `landmark` | ★ | any |
| `market` | ◇ | district |
| `quarter` | □ | district |
| `hall` | ⌂ | building |
| `church` | ✝ | building |
| `tavern` | ⌐ | building |
| `house` | ⌂ | building |

---

## CONTAINS Link (Hierarchy)

Binary relationship — no attributes:

```cypher
(parent:Place)-[:CONTAINS]->(child:Place)
```

### Example Hierarchy

```
place_northumbria (region)
    │
    └── CONTAINS
            │
            ▼
        place_york (settlement)
            │
            ├── CONTAINS → place_york_market (district)
            │                  │
            │                  └── CONTAINS → place_merchants_hall (building)
            │                                     │
            │                                     └── CONTAINS → place_back_room (room)
            │
            └── CONTAINS → place_york_minster (building)
```

### Query: Get Parent

```cypher
MATCH (parent:Place)-[:CONTAINS]->(child:Place {id: $place_id})
RETURN parent
```

### Query: Get Children

```cypher
MATCH (parent:Place {id: $place_id})-[:CONTAINS]->(child:Place)
RETURN child
ORDER BY child.name
```

### Query: Get Full Path

```cypher
MATCH path = (region:Place {scale: 'region'})-[:CONTAINS*]->(place:Place {id: $place_id})
RETURN [node IN nodes(path) | node.name] AS path_names
```

---

## Creating Places

### Validation

```python
def validate_place(place: dict) -> bool:
    """Validate place before creation."""

    # Required fields
    required = ['id', 'name', 'coordinates', 'scale', 'type']
    for field in required:
        if field not in place:
            raise ValueError(f"Missing required field: {field}")

    # ID format
    if not place['id'].startswith('place_'):
        raise ValueError("Place ID must start with 'place_'")

    # Coordinates
    lat, lng = place['coordinates']
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise ValueError("Invalid coordinates")

    # Scale
    if place['scale'] not in SCALE_HIERARCHY:
        raise ValueError(f"Invalid scale: {place['scale']}")

    return True
```

### Cypher: Create Place

```cypher
CREATE (p:Place {
  id: $id,
  name: $name,
  coordinates: $coordinates,
  scale: $scale,
  type: $type,
  detail: $detail
})
RETURN p
```

### Cypher: Add to Hierarchy

```cypher
MATCH (parent:Place {id: $parent_id})
MATCH (child:Place {id: $child_id})
CREATE (parent)-[:CONTAINS]->(child)
```

---

## Example Places

### Region

```yaml
- id: place_northumbria
  name: Northumbria
  coordinates: [54.5, -1.5]
  scale: region
  type: region
  detail: "The great northern kingdom, now under Norman control."
```

### Settlement

```yaml
- id: place_york
  name: York
  coordinates: [53.96, -1.08]
  scale: settlement
  type: city
  detail: "The second city of England. Norman banners fly from its walls."
```

### District

```yaml
- id: place_york_market
  name: York Market
  coordinates: [53.959, -1.082]
  scale: district
  type: market
  detail: "The heart of trade. Stalls crowd the square. Voices in English and Norman."
```

### Building

```yaml
- id: place_merchants_hall
  name: Merchant's Hall
  coordinates: [53.958, -1.081]
  scale: building
  type: hall
  detail: "Stone and timber. The smell of wool and coin."
```

### Room

```yaml
- id: place_back_room
  name: Back Room
  coordinates: [53.958, -1.081]
  scale: room
  type: room
  detail: "Private. A table, two chairs, a locked chest."
```

---

## Coordinate System

### Northern England Bounds

```python
BOUNDS = {
    'north': 55.5,
    'south': 53.0,
    'east': 0.5,
    'west': -3.0
}
```

### Reference Coordinates

| Place | Lat | Lng |
|-------|-----|-----|
| York | 53.96 | -1.08 |
| Durham | 54.78 | -1.57 |
| Scarborough | 54.28 | -0.40 |
| Whitby | 54.49 | -0.61 |
| Ripon | 54.14 | -1.52 |
| Newcastle | 54.97 | -1.61 |

### Rooms Share Parent Coordinates

Rooms within a building use the building's coordinates. No sub-meter precision needed.

```python
def get_display_coordinates(place: Place, graph) -> tuple:
    """Get coordinates for display. Rooms inherit from building."""
    if place.scale == 'room':
        parent = graph.get_parent(place)
        return parent.coordinates
    return place.coordinates
```

---

## Scale-Based Defaults

When Narrator needs movement time within a location:

```python
WITHIN_SCALE_MINUTES = {
    'room': 0,        # Instant
    'building': 1,    # ~1 min between rooms
    'district': 5,    # ~5 min between buildings
    'settlement': 15  # ~15 min between districts
}

def get_movement_within(place: Place) -> int:
    """Default movement time within a place."""
    return WITHIN_SCALE_MINUTES.get(place.scale, 0)
```

---

## Embedding Detail

For semantic search of places by description:

```python
def maybe_embed_detail(place: dict, embed_fn) -> dict:
    """Embed detail if long enough."""
    detail = place.get('detail', '')

    if len(detail) > 20:
        place['detail_embedding'] = embed_fn(detail)

    return place
```

### Query: Find Places by Description

```python
def find_places_by_description(query: str, embed_fn, graph, top_k=5):
    """Semantic search for places."""
    query_embedding = embed_fn(query)

    # Get all places with embeddings
    places = graph.query("""
        MATCH (p:Place)
        WHERE p.detail_embedding IS NOT NULL
        RETURN p.id, p.name, p.detail_embedding
    """)

    # Compute similarities
    scored = []
    for place in places:
        sim = cosine_similarity(query_embedding, place['detail_embedding'])
        scored.append((place, sim))

    # Return top-k
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored[:top_k]]
```

---

## Data File

Places stored in `data/world/places.yaml`:

```yaml
places:
  # Regions
  - id: place_northumbria
    name: Northumbria
    coordinates: [54.5, -1.5]
    scale: region
    type: region
    contains:
      - place_york
      - place_durham
      - place_whitby

  # Settlements
  - id: place_york
    name: York
    coordinates: [53.96, -1.08]
    scale: settlement
    type: city
    detail: "The second city of England."
    contains:
      - place_york_market
      - place_york_minster

  # Districts
  - id: place_york_market
    name: York Market
    coordinates: [53.959, -1.082]
    scale: district
    type: market
    contains:
      - place_merchants_hall
```

---

*"Places nest. Settlements contain districts. Districts contain buildings. The hierarchy is the map."*
