# Map System — Algorithm: Routes

```
CREATED: 2024-12-16
STATUS: Canonical
UPDATED: 2025-12-19 (condensed)
```

---

## CHAIN

PATTERNS:        ../PATTERNS_Map.md
BEHAVIORS:       ../BEHAVIORS_Map.md
ALGORITHM:       ../ALGORITHM_Map.md
RENDERING:       ./ALGORITHM_Rendering_Pipeline.md
PLACES:          ./ALGORITHM_Places.md
THIS:            ./ALGORITHM_Routes.md
VALIDATION:      ../VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ../TEST_Map_Test_Coverage.md
SYNC:            ../SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Role in the Map

Routes connect places with a traced path, distance, and travel time.

---

## ROUTE Link Schema

```
ROUTE:
  from: place_id
  to: place_id
  waypoints: [[lat, lng], ...]
  road_type: roman | road | trail | river | sea
  distance_km: float
  travel_minutes: int
  difficulty: easy | normal | hard | dangerous
  detail: string
```

### Route Types

- `roman`: fastest, safest
- `road`: standard
- `trail`: slower, uncertain
- `river/sea`: requires passage rules

---

## Distance Computation

Haversine over waypoint segments.

```
for each segment (a, b):
  distance += haversine(a, b)
```

## Travel Time

```
base_speed_kmh = {
  roman: 5.0,
  road: 4.0,
  trail: 3.0,
  river: 4.0,
  sea: 6.0
}
travel_minutes = (distance_km / base_speed_kmh[type]) * 60
```

---

## Creation Flow

### Cypher (Sketch)

```
MATCH (a:Place {id: $from}), (b:Place {id: $to})
CREATE (a)-[:ROUTE {waypoints, road_type, distance_km, travel_minutes}]->(b)
```

### Bidirectional

- Use two ROUTE links for two-way travel.
- Use one ROUTE link for one-way constraints.

---

## Movement Rules

- Within same place: no route required.
- Between places: route required.
- For nested places: resolve containing settlement before routing.

---

## Route Queries

- Direct route: from -> to
- All routes from place: outgoing ROUTE
- Multi-hop: Dijkstra/A* over place graph

---

## Position Along Route

```
progress in [0, 1]
segment_index = floor(progress * (n_segments - 1))
lerp between segment endpoints
```

---

## Data File (Seed)

`data/world/routes.yaml` (seed source for initial graph load).

---

## Route Tracing Tool

If adding new routes, trace in a GIS tool and export waypoint list.
