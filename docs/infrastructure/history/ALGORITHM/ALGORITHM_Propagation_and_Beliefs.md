# History — Algorithm: Propagation and Beliefs

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
THIS:        ALGORITHM_Propagation_and_Beliefs.md
OVERVIEW:    ./ALGORITHM_Overview.md
QUERY_RECORD: ./ALGORITHM_Query_and_Record.md
VALIDATION:  ../VALIDATION_History.md
IMPLEMENTATION: ../IMPLEMENTATION_History_Service_Architecture.md
TEST:        ../TEST/TEST_Overview.md
SYNC:        ../SYNC_History.md
```

---

## PROPAGATION OVERVIEW

Propagation spreads a narrative beyond direct witnesses, degrading confidence with distance and time. This is optional and invoked after world-generated events.

### Step 1: Identify Nearby Characters

Characters at the origin location learn immediately with high confidence.

### Step 2: Spread to Connected Places

For connected places, apply a delay and reduce confidence proportionally to distance.

### Step 3: Avoid Cycles

Track visited characters to prevent infinite propagation loops.

---

## CONFIDENCE GUIDELINES

Use a simple heard-factor model that reduces confidence with distance and indirectness:

```
heard_directly = 1.0
secondhand = 0.6
rumor = 0.4

confidence = base_confidence * heard_factor * time_decay
```

---

## DATA FLOW

```
World event
    -> record_world_history
    -> create direct BELIEVES
    -> propagate_beliefs (optional)
```

---

## ARCHIVED DETAIL

Detailed helper-function sketches and Cypher examples are archived at:
`../archive/SYNC_archive_2024-12.md`
