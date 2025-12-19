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

## OVERVIEW

The pipeline aggregates historical geography, politics, events, and tensions
into cohesive YAML datasets that seed the world graph. Each phase enriches the
previous outputs, adds validation hooks, and preserves provenance so the final
world data can be audited or re-scraped without losing traceability.

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

## DATA STRUCTURES

### PlaceRecord

```
Represents a real settlement or feature with stable ID and coordinates.
Fields: id, name, historical_name, type, position {lat, lng}
Constraints: id prefix place_, coordinates required for routing.
```

### RouteRecord

```
Connects two places with travel cost and terrain metadata.
Fields: from, to, path, path_km, path_hours, path_terrain
Constraints: from/to must exist in places.yaml.
```

### CharacterRecord

```
Political actor with faction alignment and voice metadata.
Fields: id, name, type, faction, voice {tone, style}
Constraints: id prefix char_, type and faction from allowed sets.
```

### NarrativeRecord

```
Narrative atom that can be believed, contradicted, or linked to tensions.
Fields: id, name, content, type, about {characters, places}, truth
Constraints: about references must exist; truth is 0.0-1.0.
```

### TensionRecord

```
Conflict descriptor that drives pressure and future events.
Fields: id, narratives, pressure_type, pressure, base_rate, breaking_point
Constraints: narratives list 2+ items; breaking_point in 0.0-1.0.
```

--- 

## ALGORITHM: run_scraping_pipeline

### Step 1: Acquire and normalize sources

Pull source datasets (Domesday, OSM, chronicles) and normalize identifiers so
all downstream phases reference the same place and character keys.

### Step 2: Build core geography layer

Create places and routes, compute travel costs, and emit YAML that becomes the
base for every later phase. Geography is the canonical reference layer.

### Step 3: Layer political actors and holdings

Generate characters and holdings, cross-check against geography, and attach
faction metadata needed for narrative generation and tension templates.

### Step 4: Curate events, narratives, and beliefs

Curate historical events, generate narrative atoms, then distribute beliefs so
characters have a minimally connected knowledge graph.

### Step 5: Derive tensions and verify outputs

Build tensions from conflicts and scheduled events, then validate referential
integrity and count expectations before writing final YAML outputs.

--- 

## KEY DECISIONS

### D1: Source fallback strategy

```
IF primary source is unavailable (e.g., OpenDomesday 404):
    use manual historical records + curated enrichment
    keep provenance notes in validation/docs for traceability
ELSE:
    ingest API results and normalize fields
```

### D2: Narrative seeding thresholds

```
IF a character has fewer than N narratives after templates:
    add curated beliefs from local events or holdings
ELSE:
    keep generated set to avoid noise
```

### D3: Tension pressure baseline

```
IF tension is scheduled event:
    set pressure_type = scheduled with date and low base_rate
ELSE:
    set gradual/event pressure with non-zero starting value
```

--- 

## DATA FLOW

```
External sources + manual notes
    ↓
Raw scrape JSON (data/raw)
    ↓
Normalized YAML (data/clean)
    ↓
World YAML outputs (data/world)
    ↓
Graph injection (data/scripts/inject_world.py)
```

--- 

## COMPLEXITY

**Time:** O(P + R + C + N + B + T) — dominated by YAML generation and cross-
reference checks across places, routes, characters, narratives, beliefs, and
tensions.

**Space:** O(P + R + C + N + B + T) — in-memory structures mirror YAML outputs
so validation can check referential integrity before write.

**Bottlenecks:**
- External API calls and geocoding latency (OSM/Overpass).
- Cross-referencing narratives/beliefs at scale for integrity checks.

--- 

## HELPER FUNCTIONS

### `fetch_domesday_settlements()`

**Purpose:** Pull and filter Domesday settlement data for target regions.

**Logic:** Query API, filter by region/value thresholds, normalize IDs.

### `enrich_coordinates()`

**Purpose:** Add lat/lng coordinates to place records.

**Logic:** Call OSM/Nominatim, cache results, apply manual overrides.

### `generate_travel_times()`

**Purpose:** Compute route travel hours from distances and terrain types.

**Logic:** Apply terrain speed table and write hours to routes.yaml.

### `distribute_beliefs()`

**Purpose:** Seed belief graph with plausible knowledge distribution.

**Logic:** Assign high certainty to owners/locals; decay with distance.

--- 

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| `data/scripts/scrape/phase1_geography.py` | build places/routes | `places.yaml`, `routes.yaml` |
| `data/scripts/scrape/phase2_political.py` | build characters/holdings | `characters.yaml`, `holdings.yaml` |
| `data/scripts/scrape/phase3_events.py` | curate events | `events.yaml` |
| `data/scripts/scrape/phase4_narratives.py` | generate narratives/beliefs | `narratives.yaml`, `beliefs.yaml` |
| `data/scripts/scrape/phase5_tensions.py` | generate tensions | `tensions.yaml` |
| `data/scripts/inject_world.py` | load YAML into graph | seeded `seed` DB |

--- 

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm OpenDomesday availability or document the long-term fallback.
- [ ] Add a provenance field to YAML outputs for multi-source traceability.
- IDEA: Automate diff reports between runs to detect data regressions.
- IDEA: Add a lightweight integrity script for minor places and things.
- QUESTION: Should phase 6 (things) be explicitly formalized in the pipeline?

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
