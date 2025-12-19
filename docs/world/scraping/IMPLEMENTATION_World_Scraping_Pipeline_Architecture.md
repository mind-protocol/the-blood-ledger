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

## SCHEMA

The YAML schema is enforced by the expectations in `data/scripts/inject_world.py`,
which maps each file into specific `GraphOps` calls. The schema contracts live
in the script and align with the engine models documented under `docs/schema/`.

| YAML Input | Inject Function | GraphOps Method |
|------------|-----------------|-----------------|
| `data/world/places.yaml` | `inject_places` | `add_place` |
| `data/world/routes.yaml` | `inject_routes` | `add_geography` |
| `data/world/characters.yaml` | `inject_characters` | `add_character` |
| `data/world/holdings.yaml` | `inject_holdings` | `add_presence` |
| `data/world/events.yaml` | `inject_events` | `add_narrative` |
| `data/world/narratives.yaml` | `inject_narratives` | `add_narrative` |
| `data/world/beliefs.yaml` | `inject_beliefs` | `add_belief` |
| `data/world/tensions.yaml` | `inject_tensions` | `add_tension` |
| `data/world/things.yaml` | `inject_things` | `add_thing` |
| `data/world/thing_locations.yaml` | `inject_thing_locations` | `add_thing_location` |
| `data/world/thing_ownership.yaml` | `inject_thing_ownership` | `add_character_thing` |

---

## LOGIC CHAINS

1. Phase scripts write YAML to `data/world/` in order: geography → political →
   events → narratives → tensions, plus curated minor places and things.
2. `data/scripts/inject_world.py` optionally clears the graph, then injects
   YAML in dependency order: places → routes → characters → holdings → things →
   thing locations → thing ownership → events → narratives → beliefs → tensions.
3. Verification queries run after injection to confirm counts and connectivity.

---

## MODULE DEPENDENCIES

- `engine/physics/graph/graph_ops.py` provides the `GraphOps` API used by
  `data/scripts/inject_world.py`.
- `pyyaml` serialization for loading and writing YAML artifacts.
- FalkorDB for the target graph database; connection details are passed via CLI.
- `data/world/` acts as the intermediate contract between scrape and injection.

---

## STATE MANAGEMENT

Pipeline state is stored in filesystem YAML outputs under `data/world/`.
`data/scripts/inject_world.py` mutates the FalkorDB graph; optional `--clear`
removes prior state before insertion. There is no additional shared state or
incremental checkpoint store outside these artifacts.

---

## RUNTIME BEHAVIOR

The pipeline is a manual, offline batch process. Each phase script is executed
as a one-shot generator, and injection runs synchronously as a CLI command.
There is no resident service or scheduler; reruns overwrite YAML outputs and
reseed the graph as needed.

---

## CONCURRENCY MODEL

The scripts run single-process and sequentially; there is no built-in parallel
execution, locking, or queueing. Concurrency risk is limited to running two
injects at the same time against the same graph, which is not supported.

---

## CONFIGURATION

`data/scripts/inject_world.py` exposes CLI flags for connectivity and control:
`--host`, `--port`, `--graph`, and `--clear`. File paths are hard-coded to
`data/world/` and the phase scripts embed the source lists and constants used
for output generation.

---

## BIDIRECTIONAL LINKS

- `data/scripts/inject_world.py` includes a `DOCS:` reference back to this
  implementation doc for traceability.
- Phase scripts in `data/scripts/scrape/` do not currently include `DOCS:`
  references, so `ngram context` cannot navigate from those files to docs yet.

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

## GAPS / IDEAS / QUESTIONS

The pipeline is documented but still missing a few implementation-facing
anchors: formalized schema definitions for each YAML file, DOCS references in
all phase scripts, and a clearer split between curated constants and generated
outputs. The extraction targets below are still pending.

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `data/scripts/scrape/phase2_political.py` | ~792L | <400L | `data/manual/` (planned YAML split) | `HISTORICAL_CHARACTERS`, `HOLDINGS`, helper mappings. |
| `data/scripts/scrape/phase1_geography.py` | ~435L | <400L | `data/manual/` (planned YAML split) + `data/scripts/scrape/` (new helpers) | `HISTORICAL_PLACES`, OSM fetch helpers, terrain rules. |
| `data/scripts/scrape/phase4_narratives.py` | ~431L | <400L | `data/scripts/scrape/` (new rules module) | Narrative templates and belief spread rules. |
| `data/scripts/inject_world.py` | ~476L | <400L | `data/scripts/` (planned inject split) | Per-entity injectors (places, narratives, beliefs, tensions). |
