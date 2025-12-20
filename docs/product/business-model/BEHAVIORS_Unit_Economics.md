# Business Model — Behaviors: Unit Economics Signals

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Whale_Economics.md
THIS:            BEHAVIORS_Unit_Economics.md (you are here)
MECHANISMS:      ./MECHANISMS_Margin_Defense.md
VERIFICATION:    ./VALIDATION_Business_Model_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Business_Model.md
TEST:            ./TEST_Business_Model.md
SYNC:            ./SYNC_Business_Model.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Average margin remains >75%

```
GIVEN:  a month of typical usage
WHEN:   costs are calculated
THEN:   gross margin remains above 75%
```

### B2: Grandmother queries remain profitable

```
GIVEN:  frequent worldbuilder queries
WHEN:   costs are aggregated
THEN:   the margin remains positive after caching
```

### B3: Hallucination defense prevents canon break

```
GIVEN:  AI proposes actions
WHEN:   physics rejects them
THEN:   output reflects rejection rather than hallucination
```

---

## INPUTS / OUTPUTS

### Primary Function: `calculate_margin()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| interaction_mix | object | Distribution of moment types |
| pricing | object | Per-moment pricing |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| margin | float | Gross margin percentage |

**Side Effects:**

- None

---

## EDGE CASES

### E1: Whale spamming expensive queries

```
GIVEN:  high volume of worldbuilder calls
THEN:   margin remains > 60% after caching
```

---

## ANTI-BEHAVIORS

### A1: Hidden cost spikes

```
GIVEN:   large context windows
WHEN:    usage increases
MUST NOT: exceed margin thresholds without alerts
INSTEAD: trigger cost monitoring
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define live margin dashboards
- [ ] Define automatic pricing adjustments
- IDEA: Add per-tier cost caps to protect margins
