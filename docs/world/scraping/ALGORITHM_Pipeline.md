# Scraping Pipeline — Algorithm

**Purpose:** Five phases. Each builds on the previous.

---

## CHAIN

```
PATTERNS:    ./PATTERNS_World_Scraping.md
BEHAVIORS:   ./BEHAVIORS_World_Scraping.md
THIS:        ALGORITHM_Pipeline.md (you are here)
VALIDATION:  ./VALIDATION_World_Scraping.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
TEST:        ./TEST_World_Scraping.md
SYNC:        ./SYNC_World_Scraping.md
```

---

## Overview

```
Raw scrape → Clean → Enrich → Link → Verify
```

```
data/
├── raw/           # Scraped JSON
├── clean/         # Processed YAML
├── world/         # Final game data
└── scripts/       # Scraping tools
```

---

## Phases

| Phase | Name | Output |
|------:|------|--------|
| 1 | Geography | `places.yaml`, `routes.yaml` |
| 2 | Political | `characters.yaml`, `holdings.yaml` |
| 3 | Events | `events.yaml` |
| 4 | Narratives | `narratives.yaml`, `beliefs.yaml` |
| 5 | Tensions | `tensions.yaml` |

---

## Phase 1: Geography

**Purpose:** Places & routes.

### Sources

| Source | URL | Provides | Filter |
|--------|-----|----------|--------|
| Domesday | `https://opendomesday.org/api/` | settlements, holders, values | Yorkshire, Northumbria, Durham |
| OSM | Overpass API | coordinates, rivers, terrain | — |
| Ancient Roam | `https://github.com/ancient-roam` | roman_roads as GeoJSON | — |

### Output

#### places.yaml

**Count:** ~215

```yaml
- id: place_york
  name: York
  historical_name: Eoforwic
  type: city
  position: { lat: 53.958, lng: -1.080 }
```

**Fields:**
- `id` — Unique identifier (`place_*`)
- `name` — Display name
- `historical_name` — Saxon/Latin name if different
- `type` — city, town, village, hold, crossing, etc.
- `position` — lat/lng coordinates

#### routes.yaml

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

### Procedure (Script)

```python
# scripts/scrape/phase1_geography.py

from domesday import DomesdayAPI
from osm import OverpassAPI
import yaml

# 1. Get Domesday settlements
DomesdayAPI().query(
  regions=["Yorkshire", "Northumbria"],
  min_value=100
)

# 2. Enrich with coordinates (OSM)
# 3. Add Roman roads
# 4. Compute travel times
# 5. Output places.yaml + routes.yaml
```

### Travel Time Calculation

| Terrain | km/hour | Notes |
|---------|---------|-------|
| roman_road | 4.0 | Paved, direct |
| track | 3.0 | Clear path |
| forest | 2.0 | Slow going |
| moor | 2.5 | Open but rough |
| marsh | 1.5 | Dangerous |

**Formula:** `hours = km / terrain_speed`

### Verification

- [ ] York-Durham route: ~48 hours (matches Google walking ~46h)
- [ ] No routes cross rivers without crossing points
- [ ] Roman roads faster than alternatives
- [ ] Coordinates match modern maps

---

## Phase 2: Political Structure

**Purpose:** Who holds what.

### Sources

| Source | Provides |
|--------|----------|
| Domesday | tenants_in_chief, subtenants, 1066_holders |
| Anglo-Saxon Chronicle | 1067 political state, appointments |
| PASE database | family relationships, titles |

### Output

#### characters.yaml

**Count:** ~70 historical + ~50 minor

```yaml
- id: char_malet
  name: William Malet
  type: major
  faction: norman
  voice: { tone: cold, style: measured }
```

**Fields:**
- `id` — Unique identifier (`char_*`)
- `name` — Full name
- `type` — major, minor, companion
- `faction` — norman, saxon_noble, saxon_common, church
- `voice` — Tone and style for dialogue

#### holdings.yaml

**Count:** ~150

```yaml
- character: char_malet
  place: place_york
  type: holds
  since: 1067
```

**Fields:**
- `character` — Character ID
- `place` — Place ID
- `type` — holds, controls, claims
- `since` / `lost` — When acquired/lost

### Procedure (Script)

```python
# scripts/scrape/phase2_political.py

# 1. Get Norman lords from Domesday
# 2. Pull holdings for each lord
# 3. Get dispossessed Saxons (1066 holders)
# 4. Cross-reference with Chronicle for 1067 state
# 5. Output characters.yaml + holdings.yaml
```

### Verification

- [ ] Malet holds York (Domesday confirms)
- [ ] No dead characters present (cross-ref death dates)
- [ ] Holdings match Domesday 1086 (extrapolated to 1067)
- [ ] Political relationships match Chronicle

---

## Phase 3: Historical Events

**Purpose:** What happened.

### Sources

| Source | Provides |
|--------|----------|
| Anglo-Saxon Chronicle | events 1065-1070, dates, places, people |
| Secondary sources | Harrying details, rebellion timeline |

### Output

#### events.yaml

**Count:** ~40

```yaml
- id: event_hastings
  name: Battle of Hastings
  content: "Harold falls at Hastings. William claims the throne."
  date: 1066-10-14
  places: [place_hastings]
  characters: [char_william, char_harold]
```

**Fields:**
- `id` — Unique identifier (`event_*`)
- `name` — Short title
- `content` — Narrative description
- `date` — ISO date or year-month
- `places` — Place IDs involved
- `characters` — Character IDs involved

### Procedure (Script)

```python
# scripts/scrape/phase3_events.py

# Mostly manual curation from Chronicle
# Script validates and links to places/characters
```

### Verification

- [ ] Dates match Chronicle
- [ ] All place references valid
- [ ] All character references valid
- [ ] No anachronistic events

---

## Phase 4: Narratives & Beliefs

**Purpose:** Stories & knowledge.

### Sources

| Source | Provides |
|--------|----------|
| Phase 2 | characters, holdings |
| Phase 3 | events |
| Manual | relationship_patterns |

### Output

#### narratives.yaml

**Count:** ~250

```yaml
- id: narr_malet_holds_york
  name: "Malet controls York"
  content: "William Malet, Sheriff of Yorkshire, holds York for the King"
  type: control
  about:
    characters: [char_malet]
    places: [place_york]
  truth: 1.0
```

**Fields:**
- `id` — Unique identifier (`narr_*`)
- `name` — Short title
- `content` — Full narrative text
- `type` — control, claim, memory, rumor, secret
- `about` — Characters and places involved
- `truth` — 0.0-1.0 (director knowledge)

#### beliefs.yaml

**Count:** ~800

```yaml
- character: char_malet
  narrative: narr_malet_holds_york
  believes: 1.0
  heard: 1.0
  originated: 0.0
```

**Fields:**
- `character` — Who holds this belief
- `narrative` — What they believe
- `believes` — How strongly (0.0-1.0)
- `heard` — Whether they've heard it (0.0-1.0)
- `originated` — Whether they started it (0.0-1.0)

### Narrative Templates

Holdings, dispossession, and events generate default narratives. See template
rules in Phase 4 inputs and relationship patterns.

### Belief Distribution Rules

- Lords know their holdings at `believes=1.0`.
- Locals know local events with `heard` and `believes` decay.
- News spreads with distance decay for major events.

### Verification

- [ ] Every character believes at least 5 narratives
- [ ] Every narrative believed by at least 1 character
- [ ] At least 30 contradicting narrative pairs
- [ ] Belief network is connected (no isolated clusters)

---

## Phase 5: Tensions

**Purpose:** What is about to break.

### Sources

| Source | Provides |
|--------|----------|
| Phase 4 | narratives, beliefs |
| Manual | conflict_patterns |

### Output

#### tensions.yaml

**Count:** ~50

```yaml
- id: tension_york_claim
  narratives: [narr_malet_holds_york, narr_waltheof_claim_york]
  pressure_type: gradual
  pressure: 0.6
  base_rate: 0.001
  breaking_point: 0.9
  description: "Waltheof has not forgotten York"
```

**Fields:**
- `id` — Unique identifier (`tension_*`)
- `narratives` — Conflicting narratives (2+)
- `pressure_type` — gradual, event, scheduled
- `pressure` — Current pressure (0.0-1.0)
- `base_rate` — Increase per tick (gradual)
- `breaking_point` — When it breaks (0.0-1.0)
- `description` — Narrator context

### Tension Templates

- Norman-Saxon holdings become gradual tensions.
- Historical rivalries become scheduled tensions.
- Contradicting narrative pairs become local tensions.

### Verification

- [ ] No tension at 0.0 pressure (world should feel alive)
- [ ] At least 10 tensions above 0.5 pressure
- [ ] All scheduled tensions have valid dates
- [ ] Breaking points are achievable

---

## Output Files (Summary)

| File | Location | Count |
|------|----------|-------|
| `places.yaml` | `data/world/` | ~215 |
| `routes.yaml` | `data/world/` | ~400 |
| `characters.yaml` | `data/world/` | ~120 |
| `narratives.yaml` | `data/world/` | ~250 |
| `beliefs.yaml` | `data/world/` | ~800 |
| `tensions.yaml` | `data/world/` | ~50 |
