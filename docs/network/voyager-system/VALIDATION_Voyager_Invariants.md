# Voyager System — Validation: Canon-Safe Imports

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Trauma_Without_Memory.md
BEHAVIORS:       ./BEHAVIORS_Voyager_Import_Experience.md
MECHANISMS:      ./MECHANISMS_Export_Import_Transposition.md
THIS:            VALIDATION_Voyager_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Voyager_System.md
TEST:            ./TEST_Voyager_System.md
SYNC:            ./SYNC_Voyager_System.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: No specific memory import

```
Imported data must not include named memories or named relationships.
```

**Checked by:** Manual export inspection (export capsule audit)

### V2: Trauma preserved

```
At least one behavioral scar must survive export/import for traumatized characters.
```

**Checked by:** Sample import simulation

### V3: Local canon integrity

```
Imported characters must not overwrite local canon nodes or presence facts.
```

**Checked by:** Canon guardrails + transposition log review

---

## PROPERTIES

### P1: Scar triggers are deterministic

```
FORALL scars:
    scar.trigger in allowed_trigger_set
```

**Tested by:** NOT YET TESTED — define allowed_trigger_set and tests

### P2: Relationship templates are archetypal

```
FORALL templates:
    template.type in archetype_set
```

**Tested by:** NOT YET TESTED — need archetype registry

---

## ERROR CONDITIONS

### E1: Import references missing entry point

```
WHEN:    no entry point exists
THEN:    import falls back to default border/coast location
SYMPTOM: voyager spawns in undefined place
```

**Tested by:** NOT YET TESTED — requires entry point selection policy

### E2: Export includes forbidden memory keys

```
WHEN:    export payload contains named events or named relationships
THEN:    export rejects or strips forbidden fields
SYMPTOM: local canon contradictions on import
```

**Tested by:** NOT YET TESTED — needs export validator

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: No specific memory import | — | ⚠ NOT YET TESTED |
| V2: Trauma preserved | — | ⚠ NOT YET TESTED |
| V3: Canon integrity | — | ⚠ NOT YET TESTED |
| P1: Deterministic triggers | — | ⚠ NOT YET TESTED |
| P2: Archetype templates | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Export capsule has no named memories/relationships
[ ] Scars preserved with intensity values
[ ] Import creates arrival narrative
[ ] Transposition resolves conflicts without canon edits
```

### Automated

```bash
# Placeholder tests (not implemented yet)
pytest tests/network/test_voyager_system.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
    test: tests/network/test_voyager_system.py (not present)
VERIFIED_BY: Codex
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define automated tests for export/import validation
- [ ] Specify audit log format for transposition decisions
- IDEA: Add a "consent_required" flag to export metadata
- QUESTION: How to detect repeated re-import of the same voyager?
