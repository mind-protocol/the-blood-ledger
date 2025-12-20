# Ghost Dialogue — Mechanisms: Dialogue Index and Retrieval

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ghost_Dialogue_Index.md
BEHAVIORS:       ./BEHAVIORS_Ghost_Dialogue_Replay.md
THIS:            MECHANISMS_Dialogue_Index.md (you are here)
VERIFICATION:    ./VALIDATION_Ghost_Dialogue_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ghost_Dialogue.md
TEST:            ./TEST_Ghost_Dialogue.md
SYNC:            ./SYNC_Ghost_Dialogue.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The Ghost Dialogue system stores all generated lines in a vector index and replays high-quality matches for similar contexts. Player reactions influence line quality scores.

---

## DATA STRUCTURES

### DialogueIndexEntry

```
text: string
character_type: string
traits: list
emotion: string
topic: string
quality_score: float
source_world: string
```

---

## MECHANISM: Indexing

### Step 1: Capture line and context

Store the line with character traits, emotion, and topic.

### Step 2: Embed and index

Compute embeddings and add to vector store.

---

## MECHANISM: Retrieval

### Step 1: Query by context

Search vector store using the target context embedding.

### Step 2: Filter by quality

Reject lines below a minimum quality threshold.

### Step 3: Transpose references

Rewrite names/places to match local canon.

---

## KEY DECISIONS

### D1: Similarity threshold

```
IF similarity >= threshold:
    candidate accepted
ELSE:
    fallback to generation
```

### D2: Quality boost on reaction

```
IF player_reaction == emotional:
    quality_score += boost
```

---

## DATA FLOW

```
Generated line
    ↓
Index entry + embedding
    ↓
Vector search
    ↓
Transpose references
    ↓
Output line
```

---

## COMPLEXITY

**Time:** O(log n) retrieval from vector store.

**Space:** O(n) for dialogue corpus.

**Bottlenecks:**
- Embedding compute cost
- Index growth without pruning

---

## HELPER FUNCTIONS

### `transpose_dialogue()`

**Purpose:** Replace named entities with local equivalents.

**Logic:** Use transposition rules and local entity lookups.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/transposition | transpose_dialogue | Canon-safe line |
| docs/network/world-scavenger | select_ghost | Candidate sources |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define pruning/retention policy for dialogue index
- [ ] Define safety filter pipeline
- IDEA: Add multilingual indexing support
