# History — Test Overview

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:    ../PATTERNS_History.md
BEHAVIORS:   ../BEHAVIORS_History.md
ALGORITHM:   ../ALGORITHM/ALGORITHM_Overview.md
VALIDATION:  ../VALIDATION_History.md
THIS:        TEST_Overview.md
DETAILS:     ./TEST_Cases.md
IMPLEMENTATION: ../IMPLEMENTATION_History_Service_Architecture.md
SYNC:        ../SYNC_History.md
```

---

## TEST STRATEGY

1. **Invariant tests** — ensure data integrity (no orphans, valid references)
2. **Query tests** — belief filtering works correctly
3. **Recording tests** — both player-experienced and world-generated paths
4. **Integration tests** — full flows from event to retrieval
5. **Experience tests** — manual validation of memory feel

---

## HOW TO RUN

```bash
pytest tests/engine/test_history.py -v
pytest tests/engine/test_history.py -k "invariant" -v
```

---

## ARCHIVED DETAIL

Detailed scenario scripts, fixtures, and manual experience test scripts were archived to keep the test overview concise.
See: `../archive/SYNC_archive_2024-12.md`
