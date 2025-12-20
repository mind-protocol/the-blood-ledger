# World Scavenger — Validation: Reuse Safety Locks

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scavenge_Before_Generate.md
BEHAVIORS:       ./BEHAVIORS_Scavenger_Priority_Stack.md
MECHANISMS:      ./MECHANISMS_Scavenger_Caches.md
THIS:            VALIDATION_Scavenger_Locks.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scavenger.md
TEST:            ./TEST_World_Scavenger.md
SYNC:            ./SYNC_World_Scavenger.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: No reuse in player causal chain

```
Content within the player's causal chain must be generated fresh.
```

**Checked by:** Causality lock check

### V2: No reuse near player

```
Content within proximity threshold of player must be unique.
```

**Checked by:** Proximity lock

### V3: Canon lock preserved

```
Imported content must enter as low-truth or be validated by canon.
```

**Checked by:** Canon lock validation

---

## PROPERTIES

### P1: State reset on reuse

```
FORALL reused topology:
    state_reset == true
```

**Tested by:** NOT YET TESTED

---

## ERROR CONDITIONS

### E1: Cache contains player-caused events

```
WHEN:    cache candidate includes player-caused consequences
THEN:    candidate rejected
SYMPTOM: causality break
```

**Tested by:** NOT YET TESTED

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: No causal reuse | — | ⚠ NOT YET TESTED |
| V2: Proximity lock | — | ⚠ NOT YET TESTED |
| V3: Canon lock | — | ⚠ NOT YET TESTED |
| P1: State reset | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Reuse never occurs within player causal chain
[ ] Proximity threshold enforces uniqueness
[ ] Imported rumors are low-truth
[ ] Topology reuse resets state
```

### Automated

```bash
pytest tests/network/test_world_scavenger.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
    test: tests/network/test_world_scavenger.py (not present)
VERIFIED_BY: Codex
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define causality graph for reuse filtering
- [ ] Implement proximity threshold logic
- IDEA: Add cache eligibility tagging at creation time
