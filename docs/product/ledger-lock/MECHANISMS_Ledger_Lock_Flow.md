# Ledger Lock — Mechanisms: Trigger and Payment Flow

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ledger_Lock_Crisis.md
BEHAVIORS:       ./BEHAVIORS_Ledger_Lock_Trigger.md
THIS:            MECHANISMS_Ledger_Lock_Flow.md (you are here)
VERIFICATION:    ./VALIDATION_Ledger_Lock_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ledger_Lock.md
TEST:            ./TEST_Ledger_Lock.md
SYNC:            ./SYNC_Ledger_Lock.md

IMPL:            data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Ledger Lock uses engagement heuristics to trigger a narrative paywall and routes the player through QR or magic link flows to complete payment without breaking immersion.

---

## DATA STRUCTURES

### LedgerLockMetrics

```
session_minutes: int
meaningful_choices: int
ledger_entries: int
tension_count: int
granny_queries: int
```

---

## MECHANISM: Trigger

### Step 1: Evaluate heuristics

Check session time, meaningful choices, ledger depth, tension, and discovery queries.

### Step 2: Player initiates save/exit

Trigger only on save/close to avoid mid-scene interruptions.

---

## MECHANISM: Payment Flow

### Step 1: Present narrative modal

Insert personalized ledger lines and stakes.

### Step 2: Payment path

Primary: QR code for mobile checkout
Secondary: Magic link for desktop

### Step 3: Confirmation and resume

On webhook success, confirm and resume play.

---

## KEY DECISIONS

### D1: QR vs magic link selection

```
IF player has mobile access:
    QR flow
ELSE:
    magic link flow
```

### D2: Failure handling

```
IF payment fails:
    show confirmation to let history fade
```

---

## DATA FLOW

```
Heuristic check
    ↓
Modal render
    ↓
Payment flow
    ↓
Webhook confirmation
```

---

## COMPLEXITY

**Time:** O(1) per check

**Space:** O(1)

---

## HELPER FUNCTIONS

### `select_personalized_lines()`

**Purpose:** Choose the most resonant ledger entries.

**Logic:** Prioritize oath/debt + relationship tension + recent event.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/product/billing | start_checkout | Payment session |
| docs/product/chronicle-system | chronicle_preview | Optional preview data |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define exact thresholds for heuristics
- [ ] Define offline mode behavior
- IDEA: Provide a short "chronicle preview" snippet before purchase
