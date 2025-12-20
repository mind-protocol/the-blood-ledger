# Ghost Dialogue — Patterns: Real Lines Beat Prompts

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md
```

---

## CHAIN

```
THIS:            PATTERNS_Ghost_Dialogue_Index.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Ghost_Dialogue_Replay.md
MECHANISMS:      ./MECHANISMS_Dialogue_Index.md
VERIFICATION:    ./VALIDATION_Ghost_Dialogue_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ghost_Dialogue.md
TEST:            ./TEST_Ghost_Dialogue.md
SYNC:            ./SYNC_Ghost_Dialogue.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Ghost_Dialogue.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Ghost_Dialogue.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

Fresh dialogue is expensive and inconsistent. Ghost Dialogue reuses real, player-validated lines to improve quality, lower cost, and create a sense that NPCs have lived histories.

---

## THE PATTERN

**Index real lines, replay them with transposition.** Every generated dialogue line becomes searchable; high-reaction lines are prioritized for reuse.

Current source content embedded here:
- Dialogue index with vector search
- Reaction-based quality boosts
- Ghost lines outperform 0-shot generation

---

## PRINCIPLES

### Principle 1: Real dialogue has gravity
Lines that provoked real reactions are higher quality.

### Principle 2: Transpose, don’t copy
References must be re-mapped to local canon.

### Principle 3: Safety and consent first
Shared lines must respect player privacy and moderation rules.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/network/world-scavenger | Ghost character sourcing |
| docs/network/transposition | Reference replacement |
| docs/infrastructure/canon | Canon consistency checks |

---

## INSPIRATIONS

- Ghost Dialogue section of Feedback Integration doc
- World Scavenger ghost injection concept

---

## SCOPE

### In Scope

- Dialogue line indexing
- Vector search and scoring
- Reaction-weighted quality boosts

### Out of Scope

- Full character import (Voyager)
- Storm overlays (Storms)
- Billing logic (Billing)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define moderation policy for dialogue reuse
- [ ] Define player consent and opt-out defaults
- IDEA: Add topic filters for content safety tiers
- QUESTION: How to handle sensitive or personal content in ghost lines?
