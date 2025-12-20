# Shadow Feed — Mechanisms: Safe Import Filtering

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Shadow_Feed_Rumor_Cache.md
BEHAVIORS:       ./BEHAVIORS_Rumor_Import.md
THIS:            MECHANISMS_Shadow_Feed_Filtering.md (you are here)
VERIFICATION:    ./VALIDATION_Shadow_Feed_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_Shadow_Feed.md
TEST:            ./TEST_Shadow_Feed.md
SYNC:            ./SYNC_Shadow_Feed.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Shadow Feed filters cross-world events into a rumor-only cache. It enforces three locks—causality, proximity, canon—to ensure imported content cannot alter local reality.

---

## DATA STRUCTURES

### ShadowEvent

```
content_template: string
source_world: string
tension_pattern: string
is_player_caused: bool
```

---

## MECHANISM: Import Filter

### Step 1: Causality lock

Reject events tied to any player action.

### Step 2: Proximity lock

Reject events within N hops of player.

### Step 3: Canon lock

If contradiction, import as rumor with truth=0.0.

### Step 4: Rumor creation

Create a narrative node with low truth and a rumor source.

---

## KEY DECISIONS

### D1: Proximity threshold

```
IF distance_from_player < threshold:
    reject
```

### D2: Contradiction handling

```
IF contradicts_local_canon:
    truth = 0.0
ELSE:
    truth = 0.3
```

---

## DATA FLOW

```
External event
    ↓
Causality/proximity checks
    ↓
Canon check
    ↓
Rumor narrative node
```

---

## COMPLEXITY

**Time:** O(n) per event evaluation.

**Space:** O(n) for Shadow Feed storage.

**Bottlenecks:**
- Canon queries for contradiction checks

---

## HELPER FUNCTIONS

### `contradicts_local_canon()`

**Purpose:** Determine if event conflicts with ground truth.

**Logic:** Compare event claims with canonical narratives.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/infrastructure/canon | get_truth | Canon truth values |
| docs/network/transposition | transpose_event | Canon-safe rumor wording |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define hop distance metric
- [ ] Define rumor expiry policy
- IDEA: Add a rumor confidence decay function
