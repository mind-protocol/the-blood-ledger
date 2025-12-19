# World Scraping — Implementation (Pipeline Architecture)

**Version:** 1.0
**Status:** DESIGNING

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Scraping.md
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
THIS:            IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md (you are here)
TEST:            ./TEST_World_Scraping.md
SYNC:            ./SYNC_World_Scraping.md

IMPL:            data/scripts/scrape/phase1_geography.py
```

---

## CODE STRUCTURE

```
data/
  scripts/
    inject_world.py
    scrape/
      phase1_geography.py
      phase2_political.py
      phase3_events.py
      phase4_narratives.py
      phase5_tensions.py
  world/
    places.yaml
    routes.yaml
    characters.yaml
    holdings.yaml
    events.yaml
    narratives.yaml
    beliefs.yaml
    tensions.yaml
```

---

## FILE RESPONSIBILITIES

| File | Purpose | Lines | Status |
|------|---------|------:|:------:|
| `data/scripts/scrape/phase1_geography.py` | Pulls OSM/Nominatim data, defines historical places, computes routes and travel times, writes `places.yaml` and `routes.yaml`. | ~435 | WATCH |
| `data/scripts/scrape/phase2_political.py` | Defines historical characters and holdings, writes `characters.yaml` and `holdings.yaml`. | ~792 | SPLIT |
| `data/scripts/scrape/phase3_events.py` | Curates events list and writes `events.yaml`. | ~332 | OK |
| `data/scripts/scrape/phase4_narratives.py` | Generates narratives and belief network from prior phases, writes `narratives.yaml` and `beliefs.yaml`. | ~431 | WATCH |
| `data/scripts/scrape/phase5_tensions.py` | Generates tensions from narrative contradictions, writes `tensions.yaml`. | ~361 | OK |
| `data/scripts/inject_world.py` | Loads `data/world/*.yaml` and injects into FalkorDB via `engine/db/graph_ops.py`. | ~476 | WATCH |

---

## ENTRY POINTS

- `data/scripts/scrape/phase1_geography.py` (first pipeline phase)
- `data/scripts/inject_world.py` (database injection)

---

## DATA FLOW

```
OSM / manual sources
  -> phase1_geography.py -> data/world/places.yaml, routes.yaml
  -> phase2_political.py -> data/world/characters.yaml, holdings.yaml
  -> phase3_events.py -> data/world/events.yaml
  -> phase4_narratives.py -> data/world/narratives.yaml, beliefs.yaml
  -> phase5_tensions.py -> data/world/tensions.yaml
  -> inject_world.py -> FalkorDB (GraphOps)
```

Notes:
- Each phase reads prior phase outputs from `data/world/`.
- `inject_world.py` maps YAML fields into graph nodes/edges and normalizes values (e.g., travel difficulty).

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline/ETL.

**Why this pattern:** Each phase emits deterministic YAML that becomes the next phase's input, keeping the transformation auditable, rerunnable, and debuggable without touching the graph layer.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Batch phase script | `data/scripts/scrape/phase1_geography.py` | Single-shot generation from sources into `data/world/*.yaml`. |
| Data-as-code constants | `data/scripts/scrape/phase2_political.py` | Captures historical data in one place for deterministic output. |
| Distance-decay rule | `data/scripts/scrape/phase4_narratives.py` | Spreads beliefs based on geography with a simple decay function. |
| Injection adapter | `data/scripts/inject_world.py` | Maps YAML records onto GraphOps calls and normalizes fields. |

### Anti-Patterns to Avoid

- **Cross-phase mutation without versioning**: makes runs non-deterministic → only update YAML via the phase that owns it.
- **Mixing scraping with injection**: complicates auditability → keep graph writes in `inject_world.py`.
- **Bypassing YAML intermediates**: breaks traceability → always persist phase outputs to `data/world/`.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Scrape pipeline | `data/scripts/scrape/*.py` | `engine/` runtime | `data/world/*.yaml` outputs |
| Injection layer | `data/scripts/inject_world.py` | `engine/db/graph_ops.py` | `GraphOps` API |

---

## EXTERNAL DEPENDENCIES

- OSM/Nominatim API (phase 1 geocoding)
- YAML serialization (`pyyaml`)
- FalkorDB via `engine/db/graph_ops.py`

---

## GAPS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `data/scripts/scrape/phase2_political.py` | ~792L | <400L | `data/manual/characters.yaml` + `data/manual/holdings.yaml` | `HISTORICAL_CHARACTERS`, `HOLDINGS`, helper mappings. |
| `data/scripts/scrape/phase1_geography.py` | ~435L | <400L | `data/manual/places.yaml` + `data/scripts/scrape/osm_utils.py` | `HISTORICAL_PLACES`, OSM fetch helpers, terrain rules. |
| `data/scripts/scrape/phase4_narratives.py` | ~431L | <400L | `data/scripts/scrape/narrative_rules.py` | Narrative templates and belief spread rules. |
| `data/scripts/inject_world.py` | ~476L | <400L | `data/scripts/inject/` | Per-entity injectors (places, narratives, beliefs, tensions). |
