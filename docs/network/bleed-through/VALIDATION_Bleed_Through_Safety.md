# Bleed-Through — Validation: Canon Safety and Messaging

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scars_Cross_Worlds.md
BEHAVIORS:       ./BEHAVIORS_Ghosts_Rumors_Reports.md
ALGORITHM:       ./ALGORITHM_Bleed_Through_Pipeline.md
THIS:            VALIDATION_Bleed_Through_Safety.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Bleed_Through.md
TEST:            ./TEST_Bleed_Through.md
SYNC:            ./SYNC_Bleed_Through.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: Local canon is never overwritten

```
Bleed-through imports must not change ground-truth canon nodes.
```

**Checked by:** Canon guardrails + transposition logs

### V2: Public messaging avoids technical terms

```
Player-facing copy must not mention caching, reuse, or topology.
```

**Checked by:** Copy review checklist

### V3: Rumors remain low-truth unless confirmed locally

```
Imported rumors retain low truth values until locally verified.
```

**Checked by:** Narrative node inspection

---

## PROPERTIES

### P1: Ghost injection is reversible

```
FORALL ghost injections:
    removing the ghost does not break local canon consistency
```

**Tested by:** NOT YET TESTED — requires rollback mechanism

---

## ERROR CONDITIONS

### E1: Ghost conflicts with local canon

```
WHEN:    conflict is detected
THEN:    transposition resolves or rejects import
SYMPTOM: duplicate or contradictory roles
```

**Tested by:** NOT YET TESTED — define conflict simulation

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Canon not overwritten | — | ⚠ NOT YET TESTED |
| V2: Messaging guardrails | — | ⚠ NOT YET TESTED |
| V3: Rumor truth low | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Ghost imports do not alter canon nodes
[ ] Rumor truth values are <= 0.3 unless locally validated
[ ] Public copy uses bleed-through vocabulary, not caching terms
```

### Automated

```bash
pytest tests/network/test_bleed_through.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
    test: tests/network/test_bleed_through.py (not present)
VERIFIED_BY: Codex
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Create copy review checklist for public materials
- [ ] Define rumor confirmation flow (when truth can increase)
- IDEA: A/B test bleed-through vocabulary on landing pages
- QUESTION: Should bleed reports include opt-out privacy controls?
