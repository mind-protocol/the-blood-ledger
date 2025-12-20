# Transposition — Behaviors: Conflict Resolution Cascade

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Local_Canon_Primary.md
THIS:            BEHAVIORS_Conflict_Resolution_Cascade.md (you are here)
MECHANISMS:      ./MECHANISMS_Transposition_Pipeline.md
VERIFICATION:    ./VALIDATION_Transposition_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Transposition.md
TEST:            ./TEST_Transposition.md
SYNC:            ./SYNC_Transposition.md

IMPL:            data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Role conflicts are detected and renamed

```
GIVEN:  an imported character with a high-status role
WHEN:   the role semantically matches a local role
THEN:   the imported role is renamed to a non-conflicting equivalent
```

### B2: Place conflicts are resolved by relocation

```
GIVEN:  an imported narrative tied to a local place with conflicting history
WHEN:   transposition runs
THEN:   the narrative is remapped to a distant, generated location
```

### B3: Canon contradictions become rumors

```
GIVEN:  a belief contradicting local ground truth
WHEN:   transposition runs
THEN:   the belief is fuzzed into a low-truth rumor
```

---

## INPUTS / OUTPUTS

### Primary Function: `transpose_entity()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| imported_entity | object | Character/narrative to transpose |
| local_graph | object | Canon + context |
| thresholds | object | Similarity/conflict thresholds |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| transposed_entity | object | Canon-safe variant |

**Side Effects:**

- None (pure transformation)

---

## EDGE CASES

### E1: Multiple conflicts in one entity

```
GIVEN:  a character conflicts on role and location
THEN:   rename and relocation are both applied in order
```

### E2: Unresolvable conflicts

```
GIVEN:  conflicts cannot be resolved by rename/relocate/fuzz
THEN:   discard conflicting fragments or reject import
```

---

## ANTI-BEHAVIORS

### A1: Override local presence

```
GIVEN:   local presence is confirmed
WHEN:    an import would collide physically
MUST NOT: place imported entity in the same location
INSTEAD: defer, relocate, or reject
```

### A2: Rewrite local truth

```
GIVEN:   local canon contradicts imported belief
WHEN:    transposition runs
MUST NOT: edit local canon to fit import
INSTEAD: downgrade import to rumor
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define rejection criteria thresholds
- [ ] Decide if fuzzing always creates a rumor or can create a belief with truth=0
- IDEA: Add provenance tags for transposition decisions
