# Map System — Algorithm: Routes

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## ROUTE Link Schema

Routes connect settlements and regions. Not used within settlements.

```yaml
ROUTE:
  # Stored (traced input)
  waypoints: float[][]      # [[lat, lng], [lat, lng], ...]
  road_type: string         # roman | track | path | river | none

  # Computed at creation
  distance_km: float
  travel_minutes: int
  difficulty: string        # easy | moderate | hard | dangerous

  # Optional
  detail: string            # "Crosses marshland near Humber"
```

### Field Details

| Field | Source | Notes |
|-------|--------|-------|
| `waypoints` | Traced | Array of [lat, lng] points |
| `road_type` | Manual | Determines speed and difficulty |
| `distance_km` | Computed | Sum of haversine distances |
| `travel_minutes` | Computed | distance / speed |
| `difficulty` | Derived | From road_type |
| `detail` | Optional | For Narrator flavor |

---

## Route Types

| Type | Speed (km/h) | Difficulty | Description |
|------|--------------|------------|-------------|
| `roman` | 5.0 | easy | Paved roads from Roman era |
| `track` | 3.5 | moderate | Unpaved but clear path |
| `path` | 2.5 | hard | Rough trail through terrain |
| `river` | 8.0 | moderate | Downstream by boat |
| `none` | 1.5 | dangerous | Cross-country, no path |

---

## Distance Computation

### Haversine Formula

```python
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1: list, coord2: list) -> float:
    """
    Distance in km between two [lat, lng] points.
    Uses haversine formula for great-circle distance.
    """
    R = 6371  # Earth radius in km

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c
```

### Route Distance

```python
def compute_route_distance(waypoints: list) -> float:
    """Total distance along waypoints in km."""
    total = 0
    for i in range(len(waypoints) - 1):
        total += haversine(waypoints[i], waypoints[i+1])
    return round(total, 2)
```

---

## Travel Time Computation

```python
SPEEDS_KMH = {
    "roman": 5.0,      # Good road, on foot
    "track": 3.5,      # Unpaved but clear
    "path": 2.5,       # Rough trail
    "river": 8.0,      # Downstream by boat
    "none": 1.5        # Cross-country
}

DIFFICULTIES = {
    "roman": "easy",
    "track": "moderate",
    "path": "hard",
    "river": "moderate",
    "none": "dangerous"
}

def compute_travel_time(distance_km: float, road_type: str) -> int:
    """Compute travel time in minutes."""
    speed = SPEEDS_KMH[road_type]
    travel_hours = distance_km / speed
    return int(travel_hours * 60)
```

---

## Creating Routes

```python
def create_route(
    from_place: str,
    to_place: str,
    waypoints: list,
    road_type: str,
    detail: str = None
) -> dict:
    """
    Create a route with computed attributes.

    Args:
        from_place: Starting place ID
        to_place: Destination place ID
        waypoints: List of [lat, lng] coordinates
        road_type: Type of road (roman, track, path, river, none)
        detail: Optional description

    Returns:
        Route dict ready for graph insertion
    """
    distance_km = compute_route_distance(waypoints)
    travel_minutes = compute_travel_time(distance_km, road_type)

    return {
        "from": from_place,
        "to": to_place,
        "waypoints": waypoints,
        "road_type": road_type,
        "distance_km": distance_km,
        "travel_minutes": travel_minutes,
        "difficulty": DIFFICULTIES[road_type],
        "detail": detail
    }
```

### Example

```python
route = create_route(
    from_place="place_york",
    to_place="place_durham",
    waypoints=[
        [53.96, -1.08],   # York
        [54.12, -1.20],   # Waypoint
        [54.35, -1.45],   # Waypoint
        [54.78, -1.57]    # Durham
    ],
    road_type="roman",
    detail="The old Roman road north. Well-maintained."
)

# Result:
# {
#   "from": "place_york",
#   "to": "place_durham",
#   "waypoints": [...],
#   "road_type": "roman",
#   "distance_km": 96.5,
#   "travel_minutes": 1158,  # ~19.3 hours
#   "difficulty": "easy",
#   "detail": "The old Roman road north..."
# }
```

---

## Graph Storage

### Cypher: Create Route

```cypher
MATCH (from:Place {id: $from_id})
MATCH (to:Place {id: $to_id})
CREATE (from)-[r:ROUTE {
  waypoints: $waypoints,
  road_type: $road_type,
  distance_km: $distance_km,
  travel_minutes: $travel_minutes,
  difficulty: $difficulty,
  detail: $detail
}]->(to)
```

### Bidirectional Routes

Most routes work both ways. Create two links:

```python
def create_bidirectional_route(route_data: dict, graph):
    """Create route in both directions."""
    # Forward
    graph.create_route(
        from_place=route_data['from'],
        to_place=route_data['to'],
        **route_data
    )

    # Reverse (swap endpoints, reverse waypoints)
    graph.create_route(
        from_place=route_data['to'],
        to_place=route_data['from'],
        waypoints=list(reversed(route_data['waypoints'])),
        road_type=route_data['road_type'],
        distance_km=route_data['distance_km'],
        travel_minutes=route_data['travel_minutes'],
        difficulty=route_data['difficulty'],
        detail=route_data.get('detail')
    )
```

**Exception: Rivers.** Downstream is faster than upstream.

```python
def create_river_route(route_data: dict, graph):
    """River routes with different upstream/downstream speeds."""
    # Downstream (fast)
    graph.create_route(
        from_place=route_data['from'],
        to_place=route_data['to'],
        road_type='river',
        travel_minutes=route_data['travel_minutes'],
        **route_data
    )

    # Upstream (slower - 3 km/h instead of 8)
    upstream_time = int(route_data['distance_km'] / 3.0 * 60)
    graph.create_route(
        from_place=route_data['to'],
        to_place=route_data['from'],
        waypoints=list(reversed(route_data['waypoints'])),
        road_type='river',
        travel_minutes=upstream_time,
        difficulty='hard',
        detail="Upstream. Slow going."
    )
```

---

## Movement Rules

### Within Same Place

No route needed. Use scale-based defaults:

```python
WITHIN_SCALE_MINUTES = {
    'room': 0,        # Instant
    'building': 1,    # ~1 min between rooms
    'district': 5,    # ~5 min between buildings
    'settlement': 15  # ~15 min between districts
}
```

### Between Different Places

```python
def get_travel_time(from_place: Place, to_place: Place, graph) -> int | None:
    """
    Get travel time between two places.

    Returns:
        Travel time in minutes, or None if no route exists.
    """
    # Same place
    if from_place.id == to_place.id:
        return 0

    # Get parents
    from_parent = graph.get_parent(from_place)
    to_parent = graph.get_parent(to_place)

    # Same parent → use scale-based default
    if from_parent and from_parent.id == to_parent.id:
        return WITHIN_SCALE_MINUTES.get(from_place.scale, 15)

    # Different parents → check for route at settlement level
    from_settlement = graph.get_containing_settlement(from_place)
    to_settlement = graph.get_containing_settlement(to_place)

    if from_settlement.id == to_settlement.id:
        # Same settlement, different districts
        return 15

    # Different settlements → need route
    route = graph.get_route(from_settlement.id, to_settlement.id)
    if route:
        return route['travel_minutes']

    # No direct route
    return None
```

### Finding Containing Settlement

```python
def get_containing_settlement(place: Place, graph) -> Place:
    """Walk up hierarchy to find settlement."""
    current = place

    while current.scale != 'settlement':
        parent = graph.get_parent(current)
        if parent is None:
            return current  # Already at top
        current = parent

    return current
```

---

## Route Queries

### Get Direct Route

```cypher
MATCH (from:Place {id: $from_id})-[r:ROUTE]->(to:Place {id: $to_id})
RETURN r
```

### Get All Routes From Place

```cypher
MATCH (from:Place {id: $place_id})-[r:ROUTE]->(to:Place)
RETURN to.id, to.name, r.travel_minutes, r.difficulty
ORDER BY r.travel_minutes
```

### Find Path (Multi-Hop)

```cypher
MATCH path = shortestPath(
  (from:Place {id: $from_id})-[:ROUTE*..5]->(to:Place {id: $to_id})
)
RETURN [node IN nodes(path) | node.id] AS places,
       [rel IN relationships(path) | rel.travel_minutes] AS times
```

---

## Position Along Route

For showing player/NPC during travel:

```python
def get_position_at_progress(route: dict, progress: float) -> list:
    """
    Get [lat, lng] position along route.

    Args:
        route: Route with waypoints
        progress: 0.0 (start) to 1.0 (end)

    Returns:
        [lat, lng] coordinate
    """
    waypoints = route['waypoints']
    total_dist = route['distance_km']
    target_dist = total_dist * progress

    accumulated = 0
    for i in range(1, len(waypoints)):
        segment_dist = haversine(waypoints[i-1], waypoints[i])

        if accumulated + segment_dist >= target_dist:
            # Interpolate within segment
            t = (target_dist - accumulated) / segment_dist
            lat = waypoints[i-1][0] + (waypoints[i][0] - waypoints[i-1][0]) * t
            lng = waypoints[i-1][1] + (waypoints[i][1] - waypoints[i-1][1]) * t
            return [lat, lng]

        accumulated += segment_dist

    # At end
    return waypoints[-1]
```

---

## Data File

Routes stored in `data/world/routes.yaml`:

```yaml
routes:
  # York to Durham (Roman road)
  - from: place_york
    to: place_durham
    waypoints:
      - [53.96, -1.08]
      - [54.12, -1.20]
      - [54.35, -1.45]
      - [54.78, -1.57]
    road_type: roman
    detail: "The old Roman road north."

  # York to Scarborough (track)
  - from: place_york
    to: place_scarborough
    waypoints:
      - [53.96, -1.08]
      - [54.05, -0.85]
      - [54.15, -0.60]
      - [54.28, -0.40]
    road_type: track
    detail: "East through the wolds."

  # York to Whitby (path through moors)
  - from: place_york
    to: place_whitby
    waypoints:
      - [53.96, -1.08]
      - [54.15, -0.90]
      - [54.30, -0.75]
      - [54.49, -0.61]
    road_type: path
    detail: "Hard going through the North York Moors."
```

---

## Route Tracing Tool

One-time dev tool to trace routes on the map:

```javascript
function RouteTracer({ onSaveRoute }) {
  const [waypoints, setWaypoints] = useState([]);
  const [roadType, setRoadType] = useState('track');
  const [selectedFrom, setSelectedFrom] = useState(null);
  const [selectedTo, setSelectedTo] = useState(null);

  const handleMapClick = (e) => {
    const [lat, lng] = unproject(e.offsetX, e.offsetY, width, height);
    setWaypoints([...waypoints, [lat, lng]]);
  };

  const handleSave = () => {
    if (!selectedFrom || !selectedTo || waypoints.length < 2) return;

    onSaveRoute({
      from: selectedFrom,
      to: selectedTo,
      waypoints,
      road_type: roadType
    });

    // Reset
    setWaypoints([]);
    setSelectedFrom(null);
    setSelectedTo(null);
  };

  const handleUndo = () => {
    setWaypoints(waypoints.slice(0, -1));
  };

  // Render map with click handler and current waypoints
  // ...
}
```

**Usage:**
1. Select "from" place
2. Select "to" place
3. Click map to add waypoints
4. Choose road type
5. Save → exports to YAML

---

*"Routes are real paths, not teleportation. Distance matters. Road type matters. The journey is part of the story."*
