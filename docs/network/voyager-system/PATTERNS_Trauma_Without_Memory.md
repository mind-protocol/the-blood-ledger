# Voyager System — Patterns: Trauma Without Memory

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

---

## CHAIN

```
THIS:            PATTERNS_Trauma_Without_Memory.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Voyager_Import_Experience.md
MECHANISMS:      ./MECHANISMS_Export_Import_Transposition.md
VERIFICATION:    ./VALIDATION_Voyager_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Voyager_System.md
TEST:            ./TEST_Voyager_System.md
SYNC:            ./SYNC_Voyager_System.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Voyager_System.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Voyager_System.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

Players want to share characters across worlds, but importing a full history breaks local canon and destroys the "single coherent reality" promise. The Voyager System solves the contradiction: **transfer trauma and patterns without importing specific memories or named relationships**, preserving a cohesive world while still delivering the emotional scar tissue that makes the character feel real.

Without this system:
- Imports become multiverse lore that violates the setting rule
- Canon conflicts force either retcons or implausible rewrites
- Cross-world sharing feels shallow (just stats) or incoherent (too much history)

---

## THE PATTERN

**Trauma Without Memory.** Export a character's core identity (traits, skills, generalized beliefs, behavioral scars). Strip specific memories, named relationships, and place knowledge. On import, rehydrate those scars into *behavioral responses* and *relationship templates* that are compatible with local canon.

Current source content embedded here:
- Export keeps **traits, skills, general beliefs**, relationship templates, and behavioral scars.
- Export **cuts specific memories, named relationships, location knowledge, narrative nodes**, and explicit debts.
- Import applies the scars and templates, spawns an arrival narrative, and places the character at an edge entry point.

---

## PRINCIPLES

### Principle 1: Local Canon Is Absolute
Imported characters never overwrite local history. Any specific memory that would conflict is stripped or generalized.

### Principle 2: Trauma Survives Translation
Behavioral scars are the core artifact. They preserve emotional truth without importing contradictory facts.

### Principle 3: Mystery Is the Feature
The arrival is a question mark: the player sees the scars but never gets a definitive origin story in this world.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/network/transposition | Resolve conflicts in names/places and protect local canon |
| docs/infrastructure/canon | Canon Holder defines what cannot be overwritten |
| docs/infrastructure/world-builder | Generates distant places when relocation is needed |

---

## INSPIRATIONS

- Refugee System spec: trauma without memory
- Character Import spec: transposition for named conflicts
- Subjective truth model: belief ≠ fact

---

## SCOPE

### In Scope

- Export format for voyager characters (YAML or JSON)
- Behavioral scar extraction and import application
- General belief preservation and relationship templates
- Arrival narrative injection and placement at entry points

### Out of Scope

- Ghost injection / bleed-through (handled in Bleed-Through)
- Cross-world topology reuse (handled in World Scavenger)
- Storm overlays or crises (handled in Storms)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define website/UX flow for exporting and importing voyagers
- [ ] Define moderation/consent rules for sharing characters
- [ ] Clarify exporter notes visibility and privacy policy
- [ ] Specify API or file endpoints for voyager upload/download
- IDEA: Add "voyager tags" for filtering by theme (war, betrayal, exile)
- IDEA: Add opt-in "reunion event" seeds for imported characters
- QUESTION: How are multi-character parties serialized and validated?
- QUESTION: Do we allow a voyager to re-enter their original world?
