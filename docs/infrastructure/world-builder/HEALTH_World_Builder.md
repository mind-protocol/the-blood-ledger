# World Builder — Health: Sparse Enrichment Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers sparse query enrichment and mutation output. It exists
to prevent silent failures where enrichment does not generate usable mutations.
It does not verify creative quality of generated content.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:      ./VALIDATION/VALIDATION_Overview.md
IMPLEMENTATION:  ./IMPLEMENTATION/IMPLEMENTATION_Overview.md
THIS:            HEALTH_World_Builder.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/query.py
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: world_builder_emits_mutation
    flow_id: sparse_enrichment
    priority: high
    rationale: Sparse queries must yield mutation output for downstream apply.
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
    source: world_builder_emits_mutation
```

---

## HOW TO RUN

```bash
# Manual: run enrichment and confirm a YAML mutation is created
python3 - <<'PY'
from engine.infrastructure.world_builder.query import query_sync
print(query_sync(playthrough_id="default", query="princes"))
PY
```

---

## KNOWN GAPS

- [ ] No automated verification that YAML mutations are valid and applied.
