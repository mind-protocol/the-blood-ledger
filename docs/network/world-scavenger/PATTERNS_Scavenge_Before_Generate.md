# World Scavenger — Patterns: Scavenge Before Generate

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

---

## CHAIN

```
THIS:            PATTERNS_Scavenge_Before_Generate.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Scavenger_Priority_Stack.md
MECHANISMS:      ./MECHANISMS_Scavenger_Caches.md
VERIFICATION:    ./VALIDATION_Scavenger_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scavenger.md
TEST:            ./TEST_World_Scavenger.md
SYNC:            ./SYNC_World_Scavenger.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_World_Scavenger.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_World_Scavenger.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

LLM generation costs scale with player count; without reuse, content becomes expensive and shallow. World Scavenger flips the curve by reusing topology, NPCs, dialogue, and rumors from other players—while resetting state to keep each world coherent.

---

## THE PATTERN

**Find → Adapt → Steal → Generate.** Treat generation as the last resort. Reuse content at the topology and narrative layer while keeping local state unique.

Current source content embedded here:
- Topology vs state split.
- Priority stack (exact match → ghost → rumor → synthesize → generate).
- Village cache + ghost injection + shadow feed.
- Ghost dialogue index for real lines.

---

## PRINCIPLES

### Principle 1: Topology is reusable, state is not
Copy map/NPC structure, reset local state.

### Principle 2: Ghosts are better than prompts
NPCs with lived histories outperform fresh generation.

### Principle 3: Canon locks prevent reuse from harming causality
Reuse is allowed only when it cannot touch local causal chains.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/network/shadow-feed | Rumor imports for distant events |
| docs/network/transposition | Conflict resolution for imported content |
| docs/infrastructure/canon | Canon guardrails for reuse safety |

---

## INSPIRATIONS

- World Scavenger spec
- Shadow feed caching model
- Ghost dialogue indexing idea

---

## SCOPE

### In Scope

- Topology reuse and state reset
- Ghost character injection
- Rumor/ambient cache usage
- Priority stack for content sourcing

### Out of Scope

- Voyager export/import (Voyager System)
- Storm overlays (Storms)
- Monetization (Billing)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define global cache storage and indexing strategy
- [ ] Clarify data retention and deletion policies
- IDEA: Add quality scoring rubric for scavenged content
- QUESTION: How to avoid homogenization across worlds over time?
