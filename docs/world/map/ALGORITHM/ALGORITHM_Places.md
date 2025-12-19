# Map System — Algorithm: Places

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
THIS:            ./ALGORITHM_Places.md
ROUTES:          ./ALGORITHM_Routes.md
VALIDATION:      ../VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ../TEST_Map_Test_Coverage.md
SYNC:            ../SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Role in the Map

Places are nodes with scale, type, and coordinates. They nest via CONTAINS links.

---

## Place Schema

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

### Scale Rules

```
region -> settlement -> district -> building -> room
room contains nothing
```

### Place Types

```
region:    kingdom, county, wilderness
settlement: city, town, village
district:  market, docks, temple
building:  inn, manor, guildhall
room:      interior space
```

---

## CONTAINS Link (Hierarchy)

```
CONTAINS:
  from: parent_place_id
  to: child_place_id
```

Queries:
- Parent: traverse incoming CONTAINS
- Children: traverse outgoing CONTAINS
- Full path: walk parents to root

---

## Creation Flow

### Validation

- `scale` must match `type` family (e.g., building -> building).
- `lat/lng` required for all except rooms (inherit parent coordinates).

### Cypher (Sketch)

```
CREATE (p:Place {id, name, type, scale, lat, lng, detail})
CREATE (parent)-[:CONTAINS]->(p)
```

---

## Coordinate System

Reference bounds (Northern England) match projection in `ALGORITHM_Map.md`.

Rooms share parent coordinates to avoid false precision.

---

## Scale-Based Defaults

```
region:     label only, no icon
settlement: icon + label
district:   label only (when zoomed)
building:   icon only (when zoomed)
room:       hidden at map scale
```

---

## Embedding Detail

Places can carry a short textual `detail` used by semantic search.

Query sketch:
```
MATCH (p:Place)
WHERE p.detail CONTAINS $text
RETURN p
```

---

## Data File (Seed)

`data/world/places.yaml` (seed source for initial graph load).
