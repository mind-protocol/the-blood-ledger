# Ghost Dialogue — Behaviors: Replay of Lived Lines

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ghost_Dialogue_Index.md
THIS:            BEHAVIORS_Ghost_Dialogue_Replay.md (you are here)
MECHANISMS:      ./MECHANISMS_Dialogue_Index.md
VERIFICATION:    ./VALIDATION_Ghost_Dialogue_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ghost_Dialogue.md
TEST:            ./TEST_Ghost_Dialogue.md
SYNC:            ./SYNC_Ghost_Dialogue.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Dialogue lines are indexed after generation

```
GIVEN:  a dialogue line is generated in play
WHEN:   logging occurs
THEN:   the line is stored in the dialogue index with metadata
```

### B2: Ghost line reuse is preferred when relevant

```
GIVEN:  a matching line exists in the index
WHEN:   an NPC responds
THEN:   the system replays the ghost line after transposition
```

### B3: Player reactions boost line quality

```
GIVEN:  a player reacts emotionally or continues the conversation
WHEN:   logging occurs
THEN:   the line’s quality score increases
```

---

## INPUTS / OUTPUTS

### Primary Function: `get_ghost_dialogue()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| npc_profile | object | Traits, role, context |
| topic | string | Dialogue topic |
| emotion | string | Emotional context |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| line | string | Reused or generated dialogue |

**Side Effects:**

- May update quality scores based on player reaction

---

## EDGE CASES

### E1: No suitable ghost line

```
GIVEN:  no line meets similarity threshold
THEN:   fallback to fresh generation
```

### E2: Ghost line conflicts with local canon

```
GIVEN:  a ghost line references a local contradiction
THEN:   transposition rewrites or rejects the line
```

---

## ANTI-BEHAVIORS

### A1: Reuse without consent

```
GIVEN:   a player opted out of dialogue reuse
WHEN:    indexing occurs
MUST NOT: store their lines in the index
INSTEAD: discard or anonymize
```

### A2: Unsafe content replay

```
GIVEN:   a line flagged for safety
WHEN:    ghost selection runs
MUST NOT: replay the line
INSTEAD: filter it out
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define opt-out mechanics and defaults
- [ ] Define safety/abuse filters for dialogue index
- IDEA: Use reaction heatmaps to surface "legendary" lines
