# Business Model — Mechanisms: Margin Defense

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Whale_Economics.md
BEHAVIORS:       ./BEHAVIORS_Unit_Economics.md
THIS:            MECHANISMS_Margin_Defense.md (you are here)
VERIFICATION:    ./VALIDATION_Business_Model_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Business_Model.md
TEST:            ./TEST_Business_Model.md
SYNC:            ./SYNC_Business_Model.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Margin defense relies on free simulation, selective generation, caching, and scavenging to keep costs below pricing thresholds even for high-usage players.

---

## DATA STRUCTURES

### CostProfile

```
moment_type: string
input_tokens: int
output_tokens: int
unit_cost: float
frequency: float
```

---

## MECHANISM: Margin Calculation

### Step 1: Compute weighted average cost

Multiply unit cost by frequency for each moment type.

### Step 2: Apply caching savings

Reduce cost for cached queries (grandmother, lore).

### Step 3: Compare against pricing

Compute margin given $0.04 per moment.

---

## KEY DECISIONS

### D1: Cache hit rate assumptions

```
IF cache_hit_rate increases:
    costs decrease
```

### D2: Hallucination defense overhead

```
IF rejection rate increases:
    margin decreases
```

---

## DATA FLOW

```
Interaction mix
    ↓
Cost profile
    ↓
Caching adjustments
    ↓
Margin output
```

---

## COMPLEXITY

**Time:** O(n) per cost profile

**Space:** O(n)

---

## HELPER FUNCTIONS

### `apply_cache_savings()`

**Purpose:** Reduce cost by cache hit rate.

**Logic:** Multiply cacheable cost by (1 - hit_rate).

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/world-scavenger | cache_hit_rates | Cost reduction inputs |
| docs/product/billing | pricing | Revenue per moment |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define real-world token usage metrics
- [ ] Define alert thresholds for margin erosion
- IDEA: Add scenario simulator for pricing changes
