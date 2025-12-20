# Storms — Patterns: Crisis Overlays

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

---

## CHAIN

```
THIS:            PATTERNS_Storms_As_Crisis_Overlays.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Storm_Overlay_Behavior.md
MECHANISMS:      ./MECHANISMS_Storm_Application.md
VERIFICATION:    ./VALIDATION_Storm_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storms.md
TEST:            ./TEST_Storms.md
SYNC:            ./SYNC_Storms.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Storms.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Storms.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

The old seed model bundled topology, NPCs, and crisis into heavy world cartridges. This is expensive and hard to share. Storms separate *drama* from *world structure*, enabling lightweight, shareable crisis overlays that keep costs near zero.

---

## THE PATTERN

**Storms as diff overlays.** The Scavenger loads topology and default state; Storms inject tensions, secrets, facts, and energy floods to create a specific crisis. This keeps the world reusable and the scenario lightweight.

Current source content embedded here:
- Layered world instantiation (Scavenger → Bleed-Through → Storm → Tick).
- Energy floods and drains to shape presence.
- Storm types (weekly, legacy, mystery, historical, invasion).
- Storm schema and overlay structure.

---

## PRINCIPLES

### Principle 1: Topology is not in the storm
Storms are diffs, not worlds.

### Principle 2: Energy makes presence real
Energy floods/drains mechanize narrative dominance.

### Principle 3: Crisis is shareable
Weekly storms standardize challenges for comparative chronicles.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/network/world-scavenger | Provides base topology |
| docs/network/bleed-through | Optional ghost/rumor layer |
| docs/physics | Energy propagation and tension resolution |

---

## INSPIRATIONS

- Storms spec
- Weekly challenge/leaderboard structure

---

## SCOPE

### In Scope

- Storm overlay schema (tensions, facts, secrets, goals)
- Energy flood/drain mechanisms
- Storm types and program structure

### Out of Scope

- Storm loader implementation details (Storm Loader)
- Character export/import (Voyager System)
- Monetization (Billing)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define Storm authoring tooling (GUI or CLI)
- [ ] Define storm validation rules and schema enforcement
- IDEA: Add storm versioning and changelog tracking
- QUESTION: How to prevent overlapping storms from conflicting?
