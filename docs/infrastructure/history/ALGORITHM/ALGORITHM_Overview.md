# History — Algorithm Overview

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
THIS:        ALGORITHM_Overview.md
DETAILS_1:   ./ALGORITHM_Query_and_Record.md
DETAILS_2:   ./ALGORITHM_Propagation_and_Beliefs.md
VALIDATION:  ../VALIDATION_History.md
IMPLEMENTATION: ../IMPLEMENTATION_History_Service_Architecture.md
TEST:        ../TEST/TEST_Overview.md
SYNC:        ../SYNC_History.md
```

---

## OVERVIEW

The History system has two primary operations:

1. **Retrieval** — Querying the graph for what a character knows about the past
2. **Recording** — Creating narratives and beliefs when events occur

Both operations are graph-native. History isn't a separate data structure — it's narrative nodes with BELIEVES edges, queryable through Cypher.

---

## WHERE TO LOOK NEXT

- Retrieval and recording flows: `./ALGORITHM_Query_and_Record.md`
- Propagation and belief confidence: `./ALGORITHM_Propagation_and_Beliefs.md`

---

## ARCHIVED DETAIL

Long-form Cypher examples, helper-function sketches, and query catalog were archived to keep the core algorithm concise.
See: `../archive/SYNC_archive_2024-12.md`
