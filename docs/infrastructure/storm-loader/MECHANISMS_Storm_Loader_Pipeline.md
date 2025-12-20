# Storm Loader — Mechanisms: Application Pipeline

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storm_Loader_As_Diff.md
BEHAVIORS:       ./BEHAVIORS_Storm_Loader_Mutations.md
THIS:            MECHANISMS_Storm_Loader_Pipeline.md (you are here)
VERIFICATION:    ./VALIDATION_Storm_Loader_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storm_Loader.md
TEST:            ./TEST_Storm_Loader.md
SYNC:            ./SYNC_Storm_Loader.md

IMPL:            data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The Storm Loader ingests a storm overlay and applies it in a deterministic sequence: validate → facts/tensions → secrets → energy floods/drains → goals/hooks. It is designed to be idempotent and resilient to missing nodes.

---

## DATA STRUCTURES

### StormMutation

```
type: facts | tensions | secrets | energy
node: string
payload: object
```

---

## MECHANISM: Load and Apply

### Step 1: Acquire base world

Load the base graph from the World Scavenger.

### Step 2: Validate schema

Ensure required keys and overlay fields exist.

### Step 3: Apply facts/tensions

Set tension pressure values and mutate node states.

### Step 4: Apply secrets

Insert hidden beliefs with visibility=false.

### Step 5: Apply energy floods/drains

Adjust potential energy to drive presence.

---

## KEY DECISIONS

### D1: Validation failure behavior

```
IF schema invalid:
    reject storm and halt
```

### D2: Missing node behavior

```
IF node missing:
    log warning and continue
```

---

## DATA FLOW

```
Storm file
    ↓
Schema validation
    ↓
Graph mutations
    ↓
Energy adjustments
    ↓
Tick simulation
```

---

## COMPLEXITY

**Time:** O(n) directives

**Space:** O(1) additional

**Bottlenecks:**
- Node lookup latency

---

## HELPER FUNCTIONS

### `apply_secret()`

**Purpose:** Add a hidden belief.

**Logic:** Create belief edge with visible_to_player=false.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/world-scavenger | get_default_world | Base graph |
| docs/physics | tick | Energy propagation |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define transaction/rollback behavior
- [ ] Define hook registration for chronicle hooks
- IDEA: Add a preflight report of mutations
