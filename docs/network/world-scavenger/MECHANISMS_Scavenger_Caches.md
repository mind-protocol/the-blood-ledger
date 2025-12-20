# World Scavenger — Mechanisms: Cache and Ghost Reuse

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scavenge_Before_Generate.md
BEHAVIORS:       ./BEHAVIORS_Scavenger_Priority_Stack.md
THIS:            MECHANISMS_Scavenger_Caches.md (you are here)
VERIFICATION:    ./VALIDATION_Scavenger_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scavenger.md
TEST:            ./TEST_World_Scavenger.md
SYNC:            ./SYNC_World_Scavenger.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

World Scavenger resolves content requests by searching global caches and ghost indices before falling back to generation. It copies topology, resets state, and transposes references to the local world.

---

## DATA STRUCTURES

### ClusterTopology

```
places: list
characters: list
relationships: list
quality_score: float
source_world: string
```

### ContentRequest

```
region_type: string
traits: list
context: string
```

---

## MECHANISM: Priority Stack

### Step 1: Exact topology match

Look for a cached cluster with matching region and tension pattern.

### Step 2: Ghost character match

Search vector index for a character with matching traits/context.

### Step 3: Shadow feed rumor

Inject a rumor template for distant context.

### Step 4: Synthesize fragments

Combine partial matches into a new composite.

### Step 5: Generate fresh

Call narrator as last resort.

---

## KEY DECISIONS

### D1: Cache match threshold

```
IF cache.quality_score >= min_quality:
    reuse
ELSE:
    fallback to ghost or generate
```

### D2: State reset policy

```
FOR EACH imported character:
    clear local loyalties, tensions, and player relations
```

---

## DATA FLOW

```
ContentRequest
    ↓
Global cache lookup
    ↓
Ghost index lookup
    ↓
Shadow feed rumor
    ↓
Generate (fallback)
```

---

## COMPLEXITY

**Time:** O(log n) for indexed cache/ghost search.

**Space:** O(n) for global caches and dialogue indices.

**Bottlenecks:**
- Vector search latency at scale
- Cache storage growth

---

## HELPER FUNCTIONS

### `transpose_cluster()`

**Purpose:** Replace names/places with local equivalents.

**Logic:** Map entities via transposition rules, generate distant locales if needed.

### `reset_state()`

**Purpose:** Clear foreign state before local simulation.

**Logic:** Reset tensions, loyalties, and player relationships.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/transposition | resolve_conflicts | Canon-safe references |
| docs/network/shadow-feed | select_rumor | Distant event templates |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define storage backend for global caches
- [ ] Define data retention and pruning strategy
- IDEA: Region-specific cache pools to avoid homogenization
