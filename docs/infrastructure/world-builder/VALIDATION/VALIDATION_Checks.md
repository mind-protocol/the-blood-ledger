# World Builder — Validation Checks

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
OVERVIEW:        ./VALIDATION_Overview.md
THIS:            VALIDATION_Checks.md (you are here)
IMPLEMENTATION:  ../IMPLEMENTATION/IMPLEMENTATION_Overview.md
TEST:            ../TEST/TEST_Overview.md
SYNC:            ../SYNC_World_Builder.md
```

---

## Manual Checklist

- V1: Query creates moment with expected properties.
- V2: ABOUT links created to results with similarity weights.
- V3: Enriched content links back to query moment.
- V4: Generated content flagged `generated: true`.
- V5: All moments are `type="thought"`.
- V6: Sparsity thresholds align with constants.
- V7: Cache prevents re-enrichment within 60s.
- V8: Recursion guard prevents concurrent enrich.

---

## Automated Verification

```bash
pytest tests/infrastructure/world_builder/test_world_builder.py -v
```

---

## Archive Note

Extended integration and performance verification steps are summarized in `../archive/SYNC_archive_2024-12.md`.
