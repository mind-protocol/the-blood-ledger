# Bleed-Through — Behaviors: Ghosts, Rumors, Reports

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scars_Cross_Worlds.md
THIS:            BEHAVIORS_Ghosts_Rumors_Reports.md (you are here)
ALGORITHM:       ./ALGORITHM_Bleed_Through_Pipeline.md
VERIFICATION:    ./VALIDATION_Bleed_Through_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Bleed_Through.md
TEST:            ./TEST_Bleed_Through.md
SYNC:            ./SYNC_Bleed_Through.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Ghost characters feel lived-in

```
GIVEN:  a new NPC required in a location
WHEN:   the system sources a ghost character
THEN:   the NPC carries scars, quirks, and history from prior play
```

### B2: Rumors cross worlds as uncertain truths

```
GIVEN:  a distant event in another world
WHEN:   imported into a local world
THEN:   it appears as a rumor with low truth value
```

### B3: Player legacy persists after logout

```
GIVEN:  a player exports or completes a significant arc
WHEN:   bleed reports are generated
THEN:   the player sees where their character appeared elsewhere
```

---

## INPUTS / OUTPUTS

### Primary Function: `inject_bleed_through()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| content_request | object | NPC or rumor needed |
| local_graph | object | Local world graph |
| bleed_sources | list | External worlds/content pools |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| injected_entity | object | Ghost NPC or rumor narrative |

**Side Effects:**

- Adds NPC or narrative nodes
- Adds attribution metadata for bleed reporting

---

## EDGE CASES

### E1: Conflict with local canon

```
GIVEN:  imported ghost conflicts with local canon
THEN:   transposition is applied or ghost is rejected
```

### E2: Rumor contradicts local truth

```
GIVEN:  rumor is false in local canon
THEN:   rumor remains visible as misinformation
```

---

## ANTI-BEHAVIORS

### A1: Reveal caching as the reason

```
GIVEN:   player-facing narrative
WHEN:    bleed-through is explained
MUST NOT: mention caching, reuse, or cost-saving
INSTEAD: frame as scars crossing worlds
```

### A2: Override local truth

```
GIVEN:   imported content conflicts with local canon
WHEN:    integration occurs
MUST NOT: overwrite local ground truth
INSTEAD: downgrade to rumor or relocate
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define UI placement for bleed reports (email vs in-game panel)
- [ ] Specify ghost/rumor attribution metadata for analytics
- IDEA: Player opt-in toggle for bleed-through visibility
- QUESTION: How to handle disputes around offensive imported content?
