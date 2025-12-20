# The Opening — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines health checks for the Opening sequence. It ensures that new playthroughs are correctly initialized, that scenarios are injected into the graph, and that the initial user experience (`scene.json`) is generated and valid.

What it protects:
- **User Entry**: Ensures the very first interaction with the game works.
- **State Integrity**: Verifies that the graph is seeded with the correct scenario data.
- **Content Validity**: Checks that the generated opening scene matches the template and scenario.

---

## WHY THIS PATTERN

HEALTH checks for the Opening are critical because failures here block the user immediately. We use docking points to verify the *result* of initialization (files and graph state) without interfering with the creation process itself. Throttling is naturally handled by the frequency of playthrough creation, but we can also run synthetic checks.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Opening.md
BEHAVIORS:       ./BEHAVIORS_Opening.md
ALGORITHM:       ./ALGORITHM_Opening.md
VALIDATION:      ./VALIDATION_Opening.md
IMPLEMENTATION:  ./IMPLEMENTATION_Opening.md
THIS:            HEALTH_Opening.md
SYNC:            ./SYNC_Opening.md

IMPL:            engine/infrastructure/api/playthroughs.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: initialization_and_opening
    purpose: Bootstrap a new playthrough.
    triggers:
      - type: manual
        source: API /api/playthrough/scenario
        notes: User clicks "Start Game"
    frequency:
      expected_rate: Low (once per session)
      peak_rate: Low
      burst_behavior: Parallel creations are isolated by ID.
    risks:
      - Graph injection failure (partial state).
      - Scene generation failure (empty or broken UI).
      - File permission errors.
    notes: Critical path.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: opening_integrity
    flow_id: initialization_and_opening
    priority: high
    rationale: If the opening fails, the user cannot play.
  - name: seed_graph_initialized
    flow_id: initialization_and_opening
    priority: high
    rationale: Without base world data, scenario injection has broken references.
  - name: scenario_injection
    flow_id: initialization_and_opening
    priority: high
    rationale: If the graph isn't seeded, the world is empty.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: stdout
  result:
    representation: enum
    value: OK
    updated_at: 2025-12-20T12:00:00Z
    source: opening_integrity_checker
```

---

## DOCK TYPES (COMPLETE LIST)

- `graph_ops` (graph operations)
- `file` (filesystem)

---

## CHECKER INDEX

```yaml
checkers:
  - name: opening_integrity_checker
    purpose: Verify scene.json and player.yaml exist and are valid.
    status: active
    priority: high
  - name: seed_graph_checker
    purpose: Verify base world seed nodes exist in the playthrough graph.
    status: active
    priority: high
  - name: scenario_graph_checker
    purpose: Verify graph contains scenario nodes.
    status: active
    priority: high
```

---

## INDICATOR: opening_integrity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: opening_integrity
  client_value: Users enter a working game state.
  validation:
    - validation_id: V1
      criteria: scene.json must exist and contain valid SceneTree.
    - validation_id: V2
      criteria: player.yaml must match request parameters.
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - binary
  semantics:
    binary: 1 = Files exist and are valid JSON/YAML. 0 = Missing or corrupt.
  aggregation:
    method: AND
    display: CLI
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: scene_generation
    method: engine.infrastructure.api.playthroughs.create_playthrough
    location: engine/infrastructure/api/playthroughs.py:300
  output:
    id: scene_generation
    method: engine.infrastructure.api.playthroughs.create_playthrough
    location: engine/infrastructure/api/playthroughs.py:300
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Check filesystem for generated files.
  steps:
    - Locate playthrough directory.
    - Read scene.json, validate keys (id, location, narration).
    - Read player.yaml, validate keys (name, gender, scenario).
  data_required: Playthrough ID
  failure_mode: FileNotFound or JSONDecodeError.
```

---

## INDICATOR: seed_graph_initialized

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: seed_graph_initialized
  client_value: Base world entities exist before scenario injection.
  validation:
    - validation_id: V0
      criteria: Seed nodes/links exist in the playthrough graph.
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - binary
  semantics:
    binary: 1 = Seed nodes found. 0 = Seed missing.
  aggregation:
    method: AND
    display: CLI
```

### DOCKS SELECTED

```yaml
docks:
  output:
    id: seed_graph
    method: engine.infrastructure.api.playthroughs.create_playthrough
    location: engine/infrastructure/api/playthroughs.py:270
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Query graph for expected seed nodes.
  steps:
    - Use a known seed node ID (e.g., place_york or char_aldric).
    - Query FalkorDB: MATCH (n {id: $id}) RETURN count(n).
    - Fail if count == 0.
  data_required: Playthrough ID
  failure_mode: Seed node not found.
```

---

## INDICATOR: scenario_injection

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: scenario_injection
  client_value: The world has content (characters, places).
  validation:
    - validation_id: V3
      criteria: Graph contains nodes defined in scenario YAML.
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - float_0_1
  semantics:
    float_0_1: % of expected nodes found in graph.
  aggregation:
    method: mean
    display: CLI
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: scenario_injection
    method: engine.infrastructure.api.playthroughs.create_playthrough
    location: engine/infrastructure/api/playthroughs.py:250
  output:
    id: scenario_injection
    method: engine.infrastructure.api.playthroughs.create_playthrough
    location: engine/infrastructure/api/playthroughs.py:250
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Query graph for expected nodes.
  steps:
    - Load scenario YAML.
    - Extract node IDs.
    - Query FalkorDB: MATCH (n) WHERE n.id IN [...] RETURN count(n).
    - Compare count to expected.
  data_required: Playthrough ID, Scenario ID
  failure_mode: Count < Expected.
```

---

## HOW TO RUN

```bash
# Run opening health checks
pytest engine/tests/test_opening_health.py  # (Proposed)
```

---

## KNOWN GAPS

- [ ] Automated checker implementation (`engine/tests/test_opening_health.py`).
- [ ] Validation of `opening.json` template integrity itself.

---

## GAPS / IDEAS / QUESTIONS

- QUESTION: Should we perform a "dry run" of scenario injection as a CI step?
