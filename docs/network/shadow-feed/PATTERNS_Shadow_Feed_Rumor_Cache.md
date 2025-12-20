# Shadow Feed — Patterns: Rumor Cache for Distant Events

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

---

## CHAIN

```
THIS:            PATTERNS_Shadow_Feed_Rumor_Cache.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Rumor_Import.md
MECHANISMS:      ./MECHANISMS_Shadow_Feed_Filtering.md
VERIFICATION:    ./VALIDATION_Shadow_Feed_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_Shadow_Feed.md
TEST:            ./TEST_Shadow_Feed.md
SYNC:            ./SYNC_Shadow_Feed.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Shadow_Feed.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Shadow_Feed.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

Distant world events are expensive to generate, but reusing them as facts can break local causality. The Shadow Feed solves this by importing distant events as low-truth rumors, keeping local canon safe while reducing content costs.

---

## THE PATTERN

**Rumor-first caching.** Only cache lore, ambient content, and distant events—and import them as rumors with low truth values. Never cache local consequences or player-caused events.

Current source content embedded here:
- Safe-to-cache vs never-cache lists.
- Shadow Feed pipeline (import distant events as rumors).
- Three locks: causality, proximity, canon.

---

## PRINCIPLES

### Principle 1: Rumors are safe, facts are not
Cross-world imports must be uncertain by default.

### Principle 2: Distance protects immersion
Only far-away events are eligible for rumor reuse.

### Principle 3: Player agency is never cached
Anything the player caused must be unique and fresh.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/network/transposition | Convert conflicts into rumors |
| docs/infrastructure/canon | Truth values and canon checks |
| docs/network/world-scavenger | Uses the Shadow Feed for reuse |

---

## INSPIRATIONS

- Cluster State Cache spec
- Fog-of-war / misinformation framing

---

## SCOPE

### In Scope

- Rumor import for distant events
- Safe caching rules (lore, ambient, distant news)
- Shadow feed population and retrieval

### Out of Scope

- Ghost NPC injection (World Scavenger)
- Export/import of characters (Voyager System)
- Storm overlays (Storms)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define storage for the Shadow Feed and retention duration
- [ ] Define content moderation for rumors
- IDEA: Add rumor provenance tags for player investigation
- QUESTION: Can rumors be promoted to truth on local confirmation?
