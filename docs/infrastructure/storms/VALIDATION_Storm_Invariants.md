# Storms — Validation: Overlay Integrity

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storms_As_Crisis_Overlays.md
BEHAVIORS:       ./BEHAVIORS_Storm_Overlay_Behavior.md
MECHANISMS:      ./MECHANISMS_Storm_Application.md
THIS:            VALIDATION_Storm_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Storms.md
TEST:            ./TEST_Storms.md
SYNC:            ./SYNC_Storms.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: Storms are diffs only

```
Storm payloads must not contain full topology.
```

**Checked by:** Schema validation

### V2: Missing node references do not crash

```
Storms with unknown node IDs log warnings and continue.
```

**Checked by:** Loader log review

### V3: Energy floods propagate via physics

```
Storm energy changes must be handled by tick physics.
```

**Checked by:** Simulation trace

---

## PROPERTIES

### P1: Idempotent application

```
FORALL storms:
    applying twice yields same graph state
```

**Tested by:** NOT YET TESTED

---

## ERROR CONDITIONS

### E1: Schema mismatch

```
WHEN:    required keys missing
THEN:    storm is rejected with validation errors
SYMPTOM: partial mutation or silent failures
```

**Tested by:** NOT YET TESTED

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Diffs only | — | ⚠ NOT YET TESTED |
| V2: Missing node resilience | — | ⚠ NOT YET TESTED |
| V3: Physics propagation | — | ⚠ NOT YET TESTED |
| P1: Idempotent apply | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Storm payload contains only overlay directives
[ ] Missing node references log warnings
[ ] Energy floods propagate normally in tick
```

### Automated

```bash
pytest tests/infrastructure/test_storms.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
    test: tests/infrastructure/test_storms.py (not present)
VERIFIED_BY: Codex
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define schema validation tooling
- [ ] Add idempotency tests
- IDEA: Storm mutation diff view for debugging
