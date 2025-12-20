# Embeddings — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2024-12-16
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the Embedding Service. It ensures that the high-dimensional vectors representing game concepts remain consistent, correctly dimensioned, and capable of supporting relevant semantic searches.

What it protects:
- **Search Precision**: Ensuring the model correctly maps similar concepts to proximal vectors.
- **Data Integrity**: Guaranteeing all node embeddings follow the 768-dimension standard.
- **Resource Stability**: Monitoring model loading and memory consumption.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Embeddings.md
BEHAVIORS:       ./BEHAVIORS_Embeddings.md
ALGORITHM:       ./ALGORITHM_Embeddings.md
VALIDATION:      ./VALIDATION_Embeddings.md
IMPLEMENTATION:  ./IMPLEMENTATION_Embeddings.md
THIS:            TEST_Embeddings.md
SYNC:            ./SYNC_Embeddings.md

IMPL:            engine/infrastructure/embeddings/service.py
```

> **Contract:** HEALTH checks verify vector output and model health without rewriting inference logic.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: text_vectorization
    purpose: Convert story elements into searchable vectors.
    triggers:
      - type: manual
        source: data/scripts/inject_world.py
      - type: event
        source: Narrator (invention phase)
    frequency:
      expected_rate: 10/min (during play)
      peak_rate: 100/min (during batch world seed)
      burst_behavior: Synchronous, potential CPU spike during batch.
    risks:
      - Model load failure (OOM or missing weights)
      - Empty vectors for important narratives
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: vector_validity
    flow_id: text_vectorization
    priority: high
    rationale: Zeroed or wrongly dimensioned vectors break semantic search.
  - name: model_readiness
    flow_id: text_vectorization
    priority: high
    rationale: Without the transformer model, no discovery is possible.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: logs
  result:
    representation: binary
    value: 1
    updated_at: 2025-12-20T10:35:00Z
    source: internal_health_check
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: dimension_checker
    purpose: Confirm all output vectors are exactly 768 floats (V3).
    status: active
    priority: high
  - name: consistency_checker
    purpose: Verify identical strings produce identical vectors (V4).
    status: active
    priority: high
```

---

## INDICATOR: vector_validity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: vector_validity
  client_value: Enables the system to "remember" and find related story beats.
  validation:
    - validation_id: V3 (Embeddings)
      criteria: Vector dimensions match model output (768).
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: embedding_input
    method: engine.infrastructure.embeddings.service.EmbeddingService.embed
    location: engine/infrastructure/embeddings/service.py:48
  output:
    id: embedding_output
    method: engine.infrastructure.embeddings.service.EmbeddingService.embed
    location: engine/infrastructure/embeddings/service.py:61
```

---

## HOW TO RUN

```bash
# Run embeddings unit tests
pytest engine/tests/test_embeddings.py -v
```

---

## KNOWN GAPS

- [ ] Real-time monitoring of inference latency.
- [ ] Automated drift detection for model version changes.
