# World Scavenger — Behaviors: Priority Stack Reuse

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scavenge_Before_Generate.md
THIS:            BEHAVIORS_Scavenger_Priority_Stack.md (you are here)
MECHANISMS:      ./MECHANISMS_Scavenger_Caches.md
VERIFICATION:    ./VALIDATION_Scavenger_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scavenger.md
TEST:            ./TEST_World_Scavenger.md
SYNC:            ./SYNC_World_Scavenger.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Scavenger prefers reuse over generation

```
GIVEN:  a content request for a new location or NPC
WHEN:   the scavenger resolves the request
THEN:   it returns cached/ghost content if available
```

### B2: Topology reuse resets local state

```
GIVEN:  a cached cluster is injected
WHEN:   it enters a new world
THEN:   local state (loyalties, tensions) is reset
```

### B3: Ghost dialogue supersedes fresh generation

```
GIVEN:  a suitable ghost dialogue line exists
WHEN:   an NPC responds
THEN:   the ghost line is used after transposition
```

---

## INPUTS / OUTPUTS

### Primary Function: `resolve_content()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| request | object | Content request (role, location, context) |
| world | object | Local world context |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| content | object | Reused or generated content |

**Side Effects:**

- May write new topology into local graph

---

## EDGE CASES

### E1: No matching cache

```
GIVEN:  no cached or ghost content matches
THEN:   system falls back to fresh generation
```

### E2: Cached content conflicts with local canon

```
GIVEN:  cached content conflicts with local canon
THEN:   transposition applies or reuse is rejected
```

---

## ANTI-BEHAVIORS

### A1: Reuse local consequences

```
GIVEN:   content in the player's causal chain
WHEN:    scavenger evaluates reuse
MUST NOT: reuse it
INSTEAD: generate fresh
```

### A2: Preserve foreign state

```
GIVEN:   cached topology from another world
WHEN:    injected
MUST NOT: carry over loyalties/tensions/state
INSTEAD: reset state for local simulation
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define cache hit metrics surfaced to telemetry
- [ ] Specify rejection path when transposition fails
- IDEA: Add a "quality floor" for ghost dialogue lines
