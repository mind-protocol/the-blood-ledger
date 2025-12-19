# World Builder — Validation Overview

```
STATUS: CANONICAL
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_World_Builder.md
BEHAVIORS:       ../BEHAVIORS_World_Builder.md
ALGORITHM:       ../ALGORITHM/ALGORITHM_Overview.md
THIS:            VALIDATION_Overview.md (you are here)
DETAILS:         ./VALIDATION_Checks.md
IMPLEMENTATION:  ../IMPLEMENTATION/IMPLEMENTATION_Overview.md
TEST:            ../TEST/TEST_Overview.md
SYNC:            ../SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/
```

---

## Invariants

- V1: Every query creates a thought moment with energy=0.3, status=possible.
- V2: Query moments link to results via ABOUT with weight=similarity.
- V3: Enriched content links back to the query moment via ABOUT.
- V4: Enriched nodes are marked `generated: true`.
- V5: All World Builder moments are `type="thought"`.
- V6: Sparsity thresholds match constants (0.6, 2, 0.3, 1.5).
- V7: Cache prevents repeat enrichment within 60 seconds.
- V8: Recursion guard blocks concurrent enrichments.

---

## Properties

- P1: `query()` always returns a list.
- P2: `is_sparse()` returns a fully populated `SparsityResult`.
- P3: Empty results always sparse with reason `no_results`.
- P4: LLM response parsing never raises; returns dict or None.
- P5: Character-linked moments create ATTACHED_TO and CAN_SPEAK.

---

## Error Conditions

- E1: No API key → enrichment returns None.
- E2: LLM call failure → enrichment returns None.
- E3: Invalid YAML → parse returns None.
- E4: Semantic search failure → query returns empty list.
- E5: Graph query failure → logs and continues.
- E6: Missing embeddings → sparsity falls back to heuristic.

---

## Archive Note

Integration scenarios and benchmark tables were trimmed; see `../archive/SYNC_archive_2024-12.md`.
