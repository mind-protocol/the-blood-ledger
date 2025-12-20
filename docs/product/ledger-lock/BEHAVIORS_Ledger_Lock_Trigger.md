# Ledger Lock — Behaviors: Conversion Trigger

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ledger_Lock_Crisis.md
THIS:            BEHAVIORS_Ledger_Lock_Trigger.md (you are here)
MECHANISMS:      ./MECHANISMS_Ledger_Lock_Flow.md
VERIFICATION:    ./VALIDATION_Ledger_Lock_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ledger_Lock.md
TEST:            ./TEST_Ledger_Lock.md
SYNC:            ./SYNC_Ledger_Lock.md

IMPL:            data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Trigger fires only after meaningful investment

```
GIVEN:  player has met engagement heuristics
WHEN:   they attempt to save or close
THEN:   Ledger Lock modal appears
```

### B2: Modal copy references player history

```
GIVEN:  Ledger Lock modal is shown
WHEN:   rendered
THEN:   it includes 2-3 personalized ledger lines
```

### B3: Payment flow resolves the crisis

```
GIVEN:  player chooses "Secure Your Chronicle"
WHEN:   payment succeeds
THEN:   play resumes and history is preserved
```

---

## INPUTS / OUTPUTS

### Primary Function: `should_trigger_lock()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| session_metrics | object | time, choices, ledger depth |
| relationship_state | object | tension presence |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| trigger | bool | Whether to show modal |

**Side Effects:**

- None

---

## EDGE CASES

### E1: Player has no ledger depth

```
GIVEN:  insufficient ledger entries
THEN:   do not trigger
```

### E2: Player closes modal without choice

```
GIVEN:  modal dismissed
THEN:   show confirmation before erasing history
```

---

## ANTI-BEHAVIORS

### A1: Trigger too early

```
GIVEN:   player has not invested
WHEN:    save/close
MUST NOT: show Ledger Lock
INSTEAD: allow free exit
```

### A2: Generic, unpersonalized modal

```
GIVEN:   Ledger Lock modal
WHEN:    rendered
MUST NOT: show generic warnings
INSTEAD: include specific ledger/relationship lines
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define exact heuristic thresholds
- [ ] Define UI/UX for repeated deferrals
- IDEA: Add "preview your Chronicle" before payment
