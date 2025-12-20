# Map System — Algorithm: Overview

```
CREATED: 2024-12-16
STATUS: Canonical
UPDATED: 2025-12-20 (consolidated Places/Routes/Rendering)
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
RENDERING:       ./ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md
PLACES:          ./ALGORITHM/places/ALGORITHM_Places.md
ROUTES:          ./ALGORITHM/routes/ALGORITHM_Routes.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Purpose

Define the canonical logic for map rendering, place/route representation, and movement rules.
This overview is the canonical location; part files link here.

---

## Rendering Summary

1. Build static layers once: parchment, coastline, routes.
2. Build dynamic layers per frame: fog, markers, overlay UI.
3. Apply projection for all coordinates.
4. Use seeded jitter for hand-drawn effect (deterministic per feature).
5. Cache static layers; redraw dynamic layers each frame.

---

## Rendering Pipeline

See `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md` for the
layer ordering, projection, caching, and hit-test details.

---

## Places

### Role in the Map

Places are nodes with scale, type, and coordinates. They nest via CONTAINS links.

### Place Schema

```
Place:
  id: string
  name: string
  type: region | settlement | district | building | room
  scale: region | settlement | district | building | room
  lat: float
  lng: float
  detail: string
  tags: [string]
```

#### Scale Rules

```
region -> settlement -> district -> building -> room
room contains nothing
```

#### Place Types

```
region:    kingdom, county, wilderness
settlement: city, town, village
district:  market, docks, temple
building:  inn, manor, guildhall
room:      interior space
```

### CONTAINS Link (Hierarchy)

```
CONTAINS:
  from: parent_place_id
  to: child_place_id
```

Queries:
- Parent: traverse incoming CONTAINS
- Children: traverse outgoing CONTAINS
- Full path: walk parents to root

### Creation Flow

**Validation**

- `scale` must match `type` family (e.g., building -> building).
- `lat/lng` required for all except rooms (inherit parent coordinates).

**Cypher (Sketch)**

```
CREATE (p:Place {id, name, type, scale, lat, lng, detail})
CREATE (parent)-[:CONTAINS]->(p)
```

### Coordinate System

Reference bounds (Northern England) match projection in this file.

Rooms share parent coordinates to avoid false precision.

### Scale-Based Defaults

```
region:     label only, no icon
settlement: icon + label
district:   label only (when zoomed)
building:   icon only (when zoomed)
room:       hidden at map scale
```

### Embedding Detail

Places can carry a short textual `detail` used by semantic search.

Query sketch:
```
MATCH (p:Place)
WHERE p.detail CONTAINS $text
RETURN p
```

### Data File (Seed)

`data/world/places.yaml` (seed source for initial graph load).

---

## Routes

### Role in the Map

Routes connect places with a traced path, distance, and travel time.

### ROUTE Link Schema

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

#### Route Types

- `roman`: fastest, safest
- `road`: standard
- `trail`: slower, uncertain
- `river/sea`: requires passage rules

### Distance Computation

Haversine over waypoint segments.

```
for each segment (a, b):
  distance += haversine(a, b)
```

### Travel Time

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

### Creation Flow

**Cypher (Sketch)**

```
MATCH (a:Place {id: $from}), (b:Place {id: $to})
CREATE (a)-[:ROUTE {waypoints, road_type, distance_km, travel_minutes}]->(b)
```

**Bidirectional**

- Use two ROUTE links for two-way travel.
- Use one ROUTE link for one-way constraints.

### Movement Rules

- Within same place: no route required.
- Between places: route required.
- For nested places: resolve containing settlement before routing.

### Route Queries

- Direct route: from -> to
- All routes from place: outgoing ROUTE
- Multi-hop: Dijkstra/A* over place graph

### Position Along Route

```
progress in [0, 1]
segment_index = floor(progress * (n_segments - 1))
lerp between segment endpoints
```

### Data File (Seed)

`data/world/routes.yaml` (seed source for initial graph load).

### Route Tracing Tool

If adding new routes, trace in a GIS tool and export waypoint list.

---

## Inputs and Outputs

**Inputs:** place nodes, route links, player visibility state, player location.
**Outputs:** canvas layers + interaction events (select, hover, travel request).

---

## Constraints

- Rendering is layered; each layer has one responsibility.
- Map shows player knowledge, not omniscience.
- Routes exist only when endpoints are known or traveled.
