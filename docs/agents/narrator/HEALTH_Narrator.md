# Narrator — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2024-12-19
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the Narrator module. It ensures the authorial intelligence produces coherent, schema-compliant story beats that correctly mutate the world state.

What it protects:
- **Authorial Coherence**: Logical consistency of narrated scenes with prior canon.
- **State Integrity**: Accuracy of graph mutations proposed by the agent.
- **UX Reliability**: Validity of clickables and interaction trees.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
THIS:            HEALTH_Narrator.md
SYNC:            ./SYNC_Narrator.md
```

> **Contract:** HEALTH checks verify intent and output without rewriting agent logic.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: scene_generation
    purpose: Transform player intent into authored story beats.
    triggers:
      - type: manual
        source: User interaction
    frequency:
      expected_rate: 1/min (active play)
      peak_rate: 5/min
      burst_behavior: Limited by LLM latency.
    risks:
      - Prompt injection or drift
      - Hallucinated mutations that break schema
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: author_coherence
    flow_id: scene_generation
    priority: high
    rationale: Narrator must respect the graph's "truth".
  - name: mutation_validity
    flow_id: scene_generation
    priority: high
    rationale: Invalid mutations can corrupt the playthrough state.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: logs
  result:
    representation: score
    value: 0.98
    updated_at: 2025-12-20T10:10:00Z
    source: narrator_integration_test
```

---

## DOCK TYPES (COMPLETE LIST)

- `api` (input context)
- `graph_ops` (applied mutations)

---

## CHECKER INDEX

```yaml
checkers:
  - name: schema_validator
    purpose: Ensure JSON output matches SceneTree and NarratorOutput.
    status: active
    priority: high
  - name: mutation_safety_checker
    purpose: Verify mutations don't violate graph constraints.
    status: active
    priority: high
```

---

## INDICATOR: author_coherence

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: author_coherence
  client_value: Ensures the story feels real and choices matter.
  validation:
    - validation_id: V1 (Narrator)
      criteria: Authorial intent preserved across turns.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: narrator_input
    method: engine.infrastructure.orchestration.narrator.run_narrator
    location: engine/infrastructure/orchestration/narrator.py:50
  output:
    id: narrator_output
    method: engine.infrastructure.orchestration.narrator.run_narrator
    location: engine/infrastructure/orchestration/narrator.py:100
```

---

## HOW TO RUN

```bash
# Run narrator integration checks
pytest engine/tests/test_narrator_integration.py -v
```

---

## KNOWN GAPS

- [ ] Automated check for voice consistency across long threads.
- [ ] Hallucination detection for unprompted entity creation.