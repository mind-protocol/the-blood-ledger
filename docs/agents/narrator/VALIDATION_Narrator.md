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

- Conversational (<5 min): `scene: {}` only, with no `time_elapsed` field
  present, keeping output lightweight for short exchanges.
- Significant (>=5 min): full SceneTree payload plus `time_elapsed` to
  signal elapsed narrative time and justify state mutation.

### V2: Immediate Response

- First dialogue chunk must stream before any graph query to preserve a
  responsive feel even if retrieval work takes longer than expected.

### V3: Invention Persistence

- Every invented fact appears as a mutation so the graph remains the
  canonical memory store for authored narrative updates.
- Mutations must link to existing graph nodes (or nodes in the same batch)
  to avoid creating dangling references in the living graph.

### V4: Character Voice Consistency

- Dialogue matches each character's defined tone, diction, and cadence so
  voices remain recognizable across repeated interactions.

### V5: Clickable Validity

- Clickable keys appear in the text they annotate, ensuring the UI can map
  highlights to visible tokens without brittle fallbacks.
- Each clickable has either a response or a waitingMessage to prevent dead
  click targets that stall player interaction.

### V6: Mutation Schema Compliance

- Mutations validate against `engine/models/` schemas so downstream services
  can safely apply them without additional defensive coercion.

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
| V1 Classification | Spot-checked in recent manual runs; no automated guard. |
| V2 Immediate response | Not automated; timing is observed ad hoc in dev. |
| V3 Invention persistence | Partial coverage via mutation schema checks only. |
| V4 Voice consistency | Manual review during authoring sessions and QA. |
| V5 Clickable validity | Spot-checked when reviewing generated scene text. |
| V6 Mutation schema | Covered by schema validation and model tests. |

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_BY: ngram repair agent
RESULT: Added missing SYNC status and expanded validation detail; runtime verification not run in this repair.
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Automated voice consistency scoring to reduce subjective review burden.
- [ ] Property-based tests for mutation integrity across edge-case payloads.
- [ ] Regression tests for classification drift on conversational thresholds.
- QUESTION: How to validate seeds -> payoff tracking without subjective tags?
