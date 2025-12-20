# Shadow Feed — Validation: Causality and Canon Locks

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
MECHANISMS:      ./MECHANISMS_Shadow_Feed_Filtering.md
THIS:            VALIDATION_Shadow_Feed_Locks.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Shadow_Feed.md
TEST:            ./TEST_Shadow_Feed.md
SYNC:            ./SYNC_Shadow_Feed.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: No player-caused events imported

```
Events involving player action are excluded from the feed.
```

**Checked by:** Causality lock audit

### V2: Rumor truth is low by default

```
Rumors enter with truth <= 0.3 unless locally verified.
```

**Checked by:** Narrative truth inspection

### V3: Proximity lock enforced

```
Events within proximity threshold are generated fresh.
```

**Checked by:** Proximity filter logs

---

## PROPERTIES

### P1: Canon contradictions create misinformation

```
FORALL rumors that contradict canon:
    truth == 0.0
```

**Tested by:** NOT YET TESTED

---

## ERROR CONDITIONS

### E1: Missing canon reference

```
WHEN:    canon lookup fails
THEN:    treat as unknown and set truth=0.3
SYMPTOM: rumor missing truth value
```

**Tested by:** NOT YET TESTED

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: No player-caused imports | — | ⚠ NOT YET TESTED |
| V2: Low truth default | — | ⚠ NOT YET TESTED |
| V3: Proximity lock | — | ⚠ NOT YET TESTED |
| P1: Misinformation on conflict | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Player-caused events are excluded from feed
[ ] Rumors default to truth <= 0.3
[ ] Proximity filter prevents local reuse
```

### Automated

```bash
pytest tests/network/test_shadow_feed.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
    test: tests/network/test_shadow_feed.py (not present)
VERIFIED_BY: Codex
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define canonical rumor audit format
- [ ] Create property-based tests for truth values
- IDEA: Add "rumor confidence" slider for design tuning
