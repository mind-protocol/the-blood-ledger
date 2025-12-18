# Phase 1: Geography — Algorithm

**Purpose:** Places & Routes

---

## Sources

| Source | URL | Provides | Filter |
|--------|-----|----------|--------|
| Domesday | `https://opendomesday.org/api/` | settlements, holders, values | Yorkshire, Northumbria, Durham |
| OSM | Overpass API | coordinates, rivers, terrain | — |
| Ancient Roam | GitHub | roman_roads as GeoJSON | — |

---

## Output

### places.yaml

**Count:** ~215

```yaml
- id: place_york
  name: York
  historical_name: Eoforwic
  type: city
  position: { lat: 53.958, lng: -1.080 }

- id: place_york_castle
  name: York Castle
  type: hold
  position: { lat: 53.957, lng: -1.078 }
```

**Fields:**
- `id` — Unique identifier (`place_*`)
- `name` — Display name
- `historical_name` — Saxon/Latin name if different
- `type` — city, town, village, hold, crossing, etc.
- `position` — lat/lng coordinates

### routes.yaml

**Count:** ~400

```yaml
- from: place_york
  to: place_durham
  path: 1.0
  path_km: 100
  path_hours: 48
  path_terrain: roman_road
```

**Fields:**
- `from`, `to` — Place IDs
- `path` — Existence (0.0-1.0)
- `path_km` — Distance
- `path_hours` — Travel time on foot
- `path_terrain` — roman_road, track, moor, forest, etc.

---

## Script

```python
# scripts/scrape/phase1_geography.py

from domesday import DomesdayAPI
from osm import OverpassAPI
import yaml

# 1. Get Domesday settlements
dom = DomesdayAPI()
settlements = dom.query(
  regions=["Yorkshire", "Northumbria"],
  min_value=100  # Filter to significant places
)

# 2. Enrich with coordinates
osm = OverpassAPI()
for s in settlements:
  coords = osm.geocode(s.name, s.region)
  s.position = coords

# 3. Add Roman roads
roads = load_geojson("data/raw/roman_roads.geojson")
routes = compute_routes(settlements, roads)

# 4. Compute travel times
for r in routes:
  r.path_hours = compute_travel_time(
    km=r.path_km,
    terrain=r.path_terrain,
    method="foot"
  )

# 5. Output
save_yaml(settlements, "data/clean/places.yaml")
save_yaml(routes, "data/clean/routes.yaml")
```

---

## Travel Time Calculation

| Terrain | km/hour | Notes |
|---------|---------|-------|
| roman_road | 4.0 | Paved, direct |
| track | 3.0 | Clear path |
| forest | 2.0 | Slow going |
| moor | 2.5 | Open but rough |
| marsh | 1.5 | Dangerous |

**Formula:** `hours = km / terrain_speed`

---

## Verification

- [ ] York-Durham route: ~48 hours (matches Google walking ~46h)
- [ ] No routes cross rivers without crossing points
- [ ] Roman roads faster than alternatives
- [ ] Coordinates match modern maps
