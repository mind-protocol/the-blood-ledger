# Shadow Feed — Behaviors: Rumor Imports and Fog of War

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Shadow_Feed_Rumor_Cache.md
THIS:            BEHAVIORS_Rumor_Import.md (you are here)
MECHANISMS:      ./MECHANISMS_Shadow_Feed_Filtering.md
VERIFICATION:    ./VALIDATION_Shadow_Feed_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_Shadow_Feed.md
TEST:            ./TEST_Shadow_Feed.md
SYNC:            ./SYNC_Shadow_Feed.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Distant events appear as rumors

```
GIVEN:  a distant event from another world
WHEN:   imported via the Shadow Feed
THEN:   it appears as a rumor with low truth value
```

### B2: Contradictions become fog-of-war

```
GIVEN:  an imported rumor contradicts local canon
WHEN:   it surfaces to the player
THEN:   it remains as misinformation rather than being removed
```

### B3: Local events are never reused

```
GIVEN:  a player-caused or proximate event
WHEN:   caching is evaluated
THEN:   the event is generated fresh and excluded from Shadow Feed
```

---

## INPUTS / OUTPUTS

### Primary Function: `import_distant_event()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| event | object | Source world event |
| target_world | object | Local world context |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| rumor | object | Rumor narrative node |

**Side Effects:**

- Adds rumor narrative to local graph

---

## EDGE CASES

### E1: No matching events in feed

```
GIVEN:  no feed entries match the target region
THEN:   system generates a fresh event
```

### E2: Event involves player action

```
GIVEN:  event involves a player's action in source world
THEN:   the event is excluded from the feed
```

---

## ANTI-BEHAVIORS

### A1: Importing local consequences

```
GIVEN:   event is causally linked to player actions
WHEN:    importing rumors
MUST NOT: reuse or import it
INSTEAD: generate fresh local content
```

### A2: Treat rumors as canon

```
GIVEN:   rumor imported from feed
WHEN:    used in narrative logic
MUST NOT: set truth=1.0 automatically
INSTEAD: keep low truth until verified
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define visibility rules for rumor surfacing
- [ ] Define how long rumors persist in the ledger
- IDEA: Add "rumor source" UI to let players investigate
