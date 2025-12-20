# World Scraping — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2024-12-17
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the World Scraping pipeline. It ensures that historical data remains accurate, geographically sound, and properly linked when injected into the simulation graph.

What it protects:
- **Historical Fidelity**: Correct placement of characters and holdings for 1067.
- **Geographic Realism**: Accuracy of routes, travel times, and river crossings.
- **Referential Integrity**: Stable connections between places, people, and narratives.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Scraping.md
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
THIS:            TEST_World_Scraping.md
SYNC:            ./SYNC_World_Scraping.md

IMPL:            data/scripts/scrape/phase1_geography.py
```

> **Contract:** HEALTH checks verify the intermediate data quality and final graph state.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: world_seeding
    purpose: Seed the graph with authentic 1067 data.
    triggers:
      - type: manual
        source: bin/inject-world.sh
    frequency:
      expected_rate: rare (weekly or on data updates)
      peak_rate: 1/hr (during active development)
      burst_behavior: Synchronous, blocks further updates until completion.
    risks:
      - Broken route connections
      - Missing historical actors
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: route_traversability
    flow_id: world_seeding
    priority: high
    rationale: If major cities aren't connected, travel narration fails.
  - name: historical_accuracy
    flow_id: world_seeding
    priority: high
    rationale: Misplaced characters break narrative immersion.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: logs
  result:
    representation: enum
    value: OK
    updated_at: 2025-12-20T10:25:00Z
    source: data_validation_script
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: geography_validator
    purpose: Check travel times and river crossing rules.
    status: active
    priority: high
  - name: density_checker
    purpose: Verify node and link counts against targets.
    status: active
    priority: med
```

---

## INDICATOR: route_traversability

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: route_traversability
  client_value: Guarantees players can travel between known historical locations.
  validation:
    - validation_id: V1 (Geography)
      criteria: York and Durham are connected by Roman roads.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: yaml_output
    method: data.scripts.scrape.phase1_geography.write_yaml
    location: data/scripts/scrape/phase1_geography.py:400
  output:
    id: graph_injection
    method: data.scripts.inject_world.inject_places
    location: data/scripts/inject_world.py:150
```

---

## HOW TO RUN

```bash
# Run data validation scripts
python data/scripts/validate_yaml.py
```

---

## KNOWN GAPS

- [ ] Automated check for river/crossing intersection logic.
- [ ] Visual verification of place coordinates on medieval map.