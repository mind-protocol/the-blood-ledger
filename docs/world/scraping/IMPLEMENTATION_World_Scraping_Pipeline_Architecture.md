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
data/scripts/inject_world.py
data/scripts/scrape/phase1_geography.py
data/scripts/scrape/phase2_political.py
data/scripts/scrape/phase3_events.py
data/scripts/scrape/phase4_narratives.py
data/scripts/scrape/phase5_tensions.py
data/world/places.yaml
data/world/places_minor.yaml
data/world/routes.yaml
data/world/characters.yaml
data/world/holdings.yaml
data/world/things.yaml
data/world/thing_locations.yaml
data/world/thing_ownership.yaml
data/world/events.yaml
data/world/narratives.yaml
data/world/beliefs.yaml
data/world/tensions.yaml
```

---

## FILE RESPONSIBILITIES

| File | Purpose | Lines | Status |
|------|---------|------:|:------:|
| `data/scripts/scrape/phase1_geography.py` | Pulls OSM/Nominatim data, defines historical places, computes routes and travel times, writes `data/world/places.yaml` and `data/world/routes.yaml`. | ~435 | WATCH |
| `data/scripts/scrape/phase2_political.py` | Defines historical characters and holdings, writes `data/world/characters.yaml` and `data/world/holdings.yaml`. | ~792 | SPLIT |
| `data/scripts/scrape/phase3_events.py` | Curates events list and writes `data/world/events.yaml`. | ~332 | OK |
| `data/scripts/scrape/phase4_narratives.py` | Generates narratives and belief network from prior phases, writes `data/world/narratives.yaml` and `data/world/beliefs.yaml`. | ~431 | WATCH |
| `data/scripts/scrape/phase5_tensions.py` | Generates tensions from narrative contradictions, writes `data/world/tensions.yaml`. | ~361 | OK |
| `data/scripts/inject_world.py` | Loads `data/world/` YAML and injects into FalkorDB via `engine/physics/graph/graph_ops.py`. | ~476 | WATCH |
| `data/world/places_minor.yaml` | Curated minor locations merged with `places.yaml` during injection. | n/a | OK |
| `data/world/things.yaml` | Curated world objects injected as Thing nodes. | n/a | OK |
| `data/world/thing_locations.yaml` | Thing-to-place links injected as LOCATED_AT relationships. | n/a | OK |
| `data/world/thing_ownership.yaml` | Character-to-thing links injected as CARRIES relationships. | n/a | OK |

---

## ENTRY POINTS

- `data/scripts/scrape/phase1_geography.py` (first pipeline phase)
- `data/scripts/inject_world.py` (database injection)

---

## DATA FLOW

```
OSM / manual sources
  -> data/scripts/scrape/phase1_geography.py -> data/world/places.yaml, data/world/routes.yaml
  -> data/scripts/scrape/phase2_political.py -> data/world/characters.yaml, data/world/holdings.yaml
  -> data/scripts/scrape/phase3_events.py -> data/world/events.yaml
  -> data/scripts/scrape/phase4_narratives.py -> data/world/narratives.yaml, data/world/beliefs.yaml
  -> data/scripts/scrape/phase5_tensions.py -> data/world/tensions.yaml
  -> data/world/places_minor.yaml, data/world/things.yaml, data/world/thing_locations.yaml, data/world/thing_ownership.yaml
  -> data/scripts/inject_world.py -> FalkorDB (GraphOps)
```

Notes:
- Each phase reads prior phase outputs from `data/world/`.
- `data/scripts/inject_world.py` maps YAML fields into graph nodes/edges and normalizes values (e.g., travel difficulty).
- `data/world/places_minor.yaml` is merged into `places.yaml` during injection; thing YAMLs are loaded directly for Thing, LOCATED_AT, and CARRIES relationships.

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline/ETL.

**Why this pattern:** Each phase emits deterministic YAML that becomes the next phase's input, keeping the transformation auditable, rerunnable, and debuggable without touching the graph layer.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Batch phase script | `data/scripts/scrape/phase1_geography.py` | Single-shot generation from sources into `data/world/` YAML. |
| Data-as-code constants | `data/scripts/scrape/phase2_political.py` | Captures historical data in one place for deterministic output. |
| Distance-decay rule | `data/scripts/scrape/phase4_narratives.py` | Spreads beliefs based on geography with a simple decay function. |
| Injection adapter | `data/scripts/inject_world.py` | Maps YAML records onto GraphOps calls and normalizes fields. |

### Anti-Patterns to Avoid

- **Cross-phase mutation without versioning**: makes runs non-deterministic → only update YAML via the phase that owns it.
- **Mixing scraping with injection**: complicates auditability → keep graph writes in `data/scripts/inject_world.py`.
- **Bypassing YAML intermediates**: breaks traceability → always persist phase outputs to `data/world/`.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Scrape pipeline | `data/scripts/scrape/` | `engine/` runtime | `data/world/` outputs |
| Injection layer | `data/scripts/inject_world.py` | `engine/physics/graph/graph_ops.py` | `GraphOps` API |

---

## EXTERNAL DEPENDENCIES

- OSM/Nominatim API (phase 1 geocoding)
- YAML serialization (`pyyaml`)
- FalkorDB via `engine/physics/graph/graph_ops.py`

---

## GAPS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `data/scripts/scrape/phase2_political.py` | ~792L | <400L | `data/manual/` (planned YAML split) | `HISTORICAL_CHARACTERS`, `HOLDINGS`, helper mappings. |
| `data/scripts/scrape/phase1_geography.py` | ~435L | <400L | `data/manual/` (planned YAML split) + `data/scripts/scrape/` (new helpers) | `HISTORICAL_PLACES`, OSM fetch helpers, terrain rules. |
| `data/scripts/scrape/phase4_narratives.py` | ~431L | <400L | `data/scripts/scrape/` (new rules module) | Narrative templates and belief spread rules. |
| `data/scripts/inject_world.py` | ~476L | <400L | `data/scripts/` (planned inject split) | Per-entity injectors (places, narratives, beliefs, tensions). |
