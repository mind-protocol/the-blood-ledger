# Embeddings — Health: Vector Service Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers embedding generation and vector consistency. It exists
to reduce the risk of invalid or inconsistent embeddings that would corrupt
semantic search. It does not verify downstream graph indexing or UI usage.

---

## WHY THIS PATTERN

Embedding failures often surface late (empty search, mismatched dimensions).
Dock-based verification provides runtime signals without changing core code.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Embeddings.md
BEHAVIORS:       ./BEHAVIORS_Embeddings.md
ALGORITHM:       ./ALGORITHM_Embeddings.md
VALIDATION:      ./VALIDATION_Embeddings.md
IMPLEMENTATION:  ./IMPLEMENTATION_Embeddings.md
THIS:            HEALTH_Embeddings.md
SYNC:            ./SYNC_Embeddings.md

IMPL:            engine/infrastructure/embeddings/service.py
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: text_vectorization
    purpose: Produce deterministic embeddings for text inputs.
    triggers:
      - type: event
        source: EmbeddingService.embed
        notes: Called by search or indexing.
    frequency:
      expected_rate: 10/min
      peak_rate: 100/min
      burst_behavior: Batch calls during seeding or indexing.
    risks:
      - V3
      - V4
      - E4
    notes: Requires model availability and consistent vector size.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: embedding_vector_shape
    flow_id: text_vectorization
    priority: high
    rationale: Incorrect vector dimensions break all downstream search.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: embedding_vector_shape
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: embedding_vector_shape
    purpose: Ensure embeddings return the expected vector length.
    status: pending
    priority: high
```

---

## INDICATOR: embedding_vector_shape

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: embedding_vector_shape
  client_value: Stable semantic search and consistent indexing.
  validation:
    - validation_id: V3
      criteria: Vector dimension matches model output.
    - validation_id: V4
      criteria: Deterministic embeddings for identical text.
    - validation_id: E4
      criteria: Model load failures surface clearly.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (vector length matches), ERROR (length mismatch or exception)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: embedding_input
    method: EmbeddingService.embed
    location: engine/infrastructure/embeddings/service.py:1
  output:
    id: embedding_output
    method: EmbeddingService.embed
    location: engine/infrastructure/embeddings/service.py:1
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Embed a fixed string and validate vector length and determinism.
  steps:
    - Embed a constant string twice.
    - Confirm both vectors are identical and length is 768.
  data_required: Embedding vectors.
  failure_mode: Exception or incorrect vector length.
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 1/hour
  burst_limit: 1
  backoff: none
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: logs
      transport: file
      notes: Manual run output for troubleshooting.
display:
  locations:
    - surface: CLI
      location: stdout
      signal: enum
      notes: Manual run output.
```

### MANUAL RUN

```yaml
manual_run:
  command: python3 - <<'PY'\nfrom engine.infrastructure.embeddings.service import EmbeddingService\nservice = EmbeddingService()\nvec = service.embed(\"princes\")\nprint(len(vec))\nprint(service.embed(\"princes\") == vec)\nPY
  notes: Requires embedding model dependencies installed.
```

---

## HOW TO RUN

```bash
python3 - <<'PY'
from engine.infrastructure.embeddings.service import EmbeddingService
service = EmbeddingService()
vec = service.embed("princes")
print(len(vec))
print(service.embed("princes") == vec)
PY
```

---

## KNOWN GAPS

- [ ] EmbeddingService implementation file is missing from this repo; health check is pending reconciliation.
- [ ] No automated health checker writes a status marker.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm canonical EmbeddingService location after graph runtime move.
