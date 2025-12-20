# Transposition — Mechanisms: Conflict Detection & Resolution

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Local_Canon_Primary.md
BEHAVIORS:       ./BEHAVIORS_Conflict_Resolution_Cascade.md
THIS:            MECHANISMS_Transposition_Pipeline.md (you are here)
VERIFICATION:    ./VALIDATION_Transposition_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Transposition.md
TEST:            ./TEST_Transposition.md
SYNC:            ./SYNC_Transposition.md

IMPL:            data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Transposition is a pipeline that compares imported entities against local canon and resolves conflicts via a cascading strategy: rename → relocate → fuzz (rumor). The pipeline enforces safety locks to prevent physical presence overrides and canon edits.

---

## DATA STRUCTURES

### ImportedEntity

```
role: string
beliefs: list[narrative_ref]
locations: list[place_ref]
```

### Conflict

```
type: role | belief | location
severity: float
local_reference: string
```

---

## MECHANISM: Conflict Detection

### Step 1: Role similarity check

Compare imported role labels to local high-status roles using embeddings.

### Step 2: Belief vs truth check

Compare imported high-intensity beliefs to local canon truth values.

### Step 3: Presence check

Ensure imported placement does not collide with local presence facts.

---

## MECHANISM: Conflict Resolution Cascade

### Step 1: Rename

If role conflict, replace with semantically similar non-conflicting title.

### Step 2: Relocate

If location conflict, map to a distant, generated place.

### Step 3: Fuzz

If belief conflict, downgrade to rumor with low truth value.

### Step 4: Safety locks

If any step would override local presence or canon, discard or reject.

---

## KEY DECISIONS

### D1: Role similarity threshold

```
IF cosine_similarity(role, local_role) > threshold:
    conflict
```

### D2: Belief contradiction threshold

```
IF belief_intensity > 0.5 AND local_truth < 0.2:
    conflict
```

---

## DATA FLOW

```
Imported entity
    ↓
Conflict detection
    ↓
Rename/relocate/fuzz
    ↓
Canon-safe entity
```

---

## COMPLEXITY

**Time:** O(n*m) where n=imported refs, m=local high-status roles.

**Space:** O(n) for conflict list.

**Bottlenecks:**
- Embedding similarity searches
- Canon queries in large graphs

---

## HELPER FUNCTIONS

### `find_role_conflicts()`

**Purpose:** Identify role collisions.

**Logic:** Embed and compare imported role vs local roles.

### `fuzz_belief()`

**Purpose:** Convert belief to rumor.

**Logic:** Set narrative_type=rumor, truth <= 0.3.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/shadow-feed | create_rumor | Rumor narrative for fuzzing |
| docs/infrastructure/canon | query_truth | Ground truth checks |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define policy for deferred imports vs hard rejection
- [ ] Define embedding model + similarity thresholds
- IDEA: Add per-role whitelist for safe duplicates
