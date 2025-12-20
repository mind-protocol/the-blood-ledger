# World Scraping — Implementation: Pipeline Architecture and Data Flow

```
STATUS: STABLE
CREATED: 2024-12-16
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Scraping.md
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
THIS:            IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
HEALTH:          ./HEALTH_World_Scraping.md
SYNC:            ./SYNC_World_Scraping.md

IMPL:            data/scripts/scrape/phase1_geography.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
data/
├── scripts/
│   ├── inject_world.py          # Database injection logic
│   └── scrape/
│       ├── phase1_geography.py  # Geography layer
│       ├── phase2_political.py  # Actors & holdings
│       ├── phase3_events.py     # Historical timeline
│       ├── phase4_narratives.py # Knowledge graph
│       └── phase5_tensions.py   # Conflict layer
└── world/
    ├── places.yaml              # Canonical YAML artifacts
    ├── routes.yaml
    └── ...
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `data/scripts/scrape/phase1_geography.py` | Geodata collection | `fetch_osm`, `build_routes` | ~435 | WATCH |
| `data/scripts/scrape/phase2_political.py` | Actor seeding | `seed_characters` | ~792 | SPLIT |
| `data/scripts/inject_world.py` | FalkorDB loader | `inject_all` | ~476 | WATCH (graph runtime moved to ngram repo) |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline / ETL.

**Why this pattern:** Each phase produces deterministic YAML intermediates that can be audited, diffed, and reviewed manually before being injected into the persistent graph database.

---

## SCHEMA

### PlaceRecord (YAML)

```yaml
Place:
  required:
    - id: string          # place_name
    - name: string        # Display name
    - type: string        # city | town | hold
    - position: object    # {lat, lng}
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| World Injection | `inject_world.py:100` | Manual CLI Command |
| Pipeline Start | `phase1_geography.py:10` | Manual CLI Command |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Seed Data Pipeline: External Sources → YAML → Graph

This flow handles the generation of the world's static data, moving from historical records to the final living graph.

```yaml
flow:
  name: world_seeding
  purpose: Populate the graph with authentic 1067 data.
  scope: APIs/Manual -> YAML Intermediate -> FalkorDB
  steps:
    - id: step_1_scrape
      description: Extract geography and political data into clean YAML.
      file: data/scripts/scrape/phase1_geography.py
      function: main
      input: External APIs (OSM, Domesday)
      output: data/world/places.yaml, routes.yaml
      trigger: Manual execution
      side_effects: local filesystem writes
    - id: step_2_inject
      description: Load YAML records into FalkorDB via GraphOps (ngram repo graph runtime).
      file: data/scripts/inject_world.py
      function: inject_all
      input: data/world/*.yaml
      output: Graph nodes and edges
      trigger: Manual execution
      side_effects: FalkorDB state modified
  docking_points:
    guidance:
      include_when: data is transformed or references are validated
    available:
      - id: yaml_output
        type: file
        direction: output
        file: data/scripts/scrape/phase1_geography.py
        function: write_yaml
        trigger: phase completion
        payload: YAML file
        async_hook: not_applicable
        needs: none
        notes: Canonical intermediate for audit
      - id: graph_injection
        type: graph_ops
        direction: input
        file: data/scripts/inject_world.py
        function: inject_places
        trigger: GraphOps.add_place (ngram repo graph runtime)
        payload: PlaceRecord
        async_hook: required
        needs: none
        notes: Critical for referential integrity
    health_recommended:
      - dock_id: yaml_output
        reason: Verification of data volume and schema compliance.
      - dock_id: graph_injection
        reason: Verification of connectivity and ID consistency.
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
data/scripts/inject_world.py
    └── imports → GraphOps (ngram repo graph runtime; see `data/ARCHITECTURE — Cybernetic Studio.md`)
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Canonical Data | `data/world/*.yaml` | filesystem | persistent artifacts |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Pipeline Scripts | Sync | Batch processing, one phase at a time |
