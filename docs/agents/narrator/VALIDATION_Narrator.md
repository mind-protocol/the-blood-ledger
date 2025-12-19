# Narrator — Validation: Behavioral Invariants and Output Verification

```
STATUS: DRAFT
CREATED: 2024-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
THIS:            VALIDATION_Narrator.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            agents/narrator/CLAUDE.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run validation checks.

---

## INVARIANTS (Must Always Hold)

### V1: Action Classification

- Conversational (<5 min): `scene: {}` and no `time_elapsed`.
- Significant (>=5 min): full SceneTree and `time_elapsed`.

### V2: Immediate Response

- First dialogue chunk must stream before any graph query.

### V3: Invention Persistence

- Every invented fact appears as a mutation.
- Mutations must link to existing graph nodes (or nodes in same batch).

### V4: Character Voice Consistency

- Dialogue matches each character's defined tone and style.

### V5: Clickable Validity

- Clickable keys appear in the text they annotate.
- Each clickable has either a response or a waitingMessage.

### V6: Mutation Schema Compliance

- Mutations validate against `engine/models/` schemas.

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds (classification + time_elapsed)
[ ] V2 holds (first chunk < 2s)
[ ] V3 holds (inventions persisted)
[ ] V4 holds (voice consistency)
[ ] V5 holds (clickables valid)
[ ] V6 holds (schemas validate)
```

### Automated (if available)

```bash
pytest engine/tests/test_narrator_integration.py
python tools/validate_narrator_output.py --check clickables
```

---

## TEST COVERAGE (Snapshot)

| Requirement | Status |
|-------------|--------|
| V1 Classification | Spot-checked |
| V2 Immediate response | Not automated |
| V3 Invention persistence | Partial |
| V4 Voice consistency | Manual |
| V5 Clickable validity | Spot-checked |
| V6 Mutation schema | Covered |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Automated voice consistency scoring
- [ ] Property-based tests for mutation integrity
- [ ] Regression tests for classification drift
- QUESTION: How to validate seeds -> payoff tracking?
