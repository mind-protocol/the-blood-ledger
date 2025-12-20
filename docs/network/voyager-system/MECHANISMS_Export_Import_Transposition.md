# Voyager System — Mechanisms: Export/Import Transposition

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Trauma_Without_Memory.md
BEHAVIORS:       ./BEHAVIORS_Voyager_Import_Experience.md
THIS:            MECHANISMS_Export_Import_Transposition.md (you are here)
VERIFICATION:    ./VALIDATION_Voyager_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Voyager_System.md
TEST:            ./TEST_Voyager_System.md
SYNC:            ./SYNC_Voyager_System.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The Voyager System exports a character into a portable capsule, strips specific memories, and imports the character into a new world by applying trauma-derived behaviors and generalized belief templates. Conflict handling is delegated to transposition logic so local canon remains intact.

---

## DATA STRUCTURES

### VoyagerExport

```
metadata:
  character_name: string
  origin_world: string (hashed)
  export_date: string
  playtime: string
  exporter_note: string (optional)
traits: list[string]
skills: list[map[string,float]]
general_beliefs: list[belief]
behavioral_scars: list[scar]
relationship_templates: list[template]
```

### BehavioralScar

```
trigger: string
response: string
intensity: float
```

### RelationshipTemplate

```
type: string
default_stance: string
intensity: float
```

---

## MECHANISM: Export Capsule

### Step 1: Extract core identity

Extract traits, skills, and generalized beliefs.

### Step 2: Derive behavioral scars

Convert high-weight narrative events into trigger/response patterns (fire, betrayal, loss, authority).

### Step 3: Generalize relationships

Convert named relationships into archetypal templates (authority figures, children, soldiers).

---

## MECHANISM: Import Capsule

### Step 1: Create new character node

Instantiate a character with traits, skills, and refugee/voyager flags.

### Step 2: Apply general beliefs

Add belief nodes with generalized targets and intensity.

### Step 3: Apply behavioral scars

Register scar triggers for future narrative events.

### Step 4: Apply relationship templates

Seed default stances toward archetype groups.

### Step 5: Inject arrival narrative

Create a narrative event describing arrival without local canonical specifics.

---

## KEY DECISIONS

### D1: Strip specific memories vs. keep

```
IF memory references named people/places/events:
    discard or generalize
ELSE:
    retain as generalized belief
```

### D2: Conflict resolution

```
IF import references collide with local canon:
    use transposition (rename/relocate/fuzz)
ELSE:
    import as-is
```

---

## DATA FLOW

```
Character + Graph
    ↓
Export Capsule (traits, scars, templates)
    ↓
Transposition (rename/relocate/fuzz)
    ↓
Import (character node + arrival narrative)
```

---

## COMPLEXITY

**Time:** O(n) — proportional to the number of narratives scanned for scars.

**Space:** O(n) — export capsule size grows with scar and template count.

**Bottlenecks:**
- Scar extraction if narrative history is very large
- Transposition lookups for place/character conflicts

---

## HELPER FUNCTIONS

### `extract_behavioral_scars()`

**Purpose:** Convert high-weight narratives into triggers/responses.

**Logic:** Scan narrative types (violence, betrayal, loss) and generate scar entries with intensity.

### `generalize_relationships()`

**Purpose:** Convert named links into archetype templates.

**Logic:** Map relationship targets to archetypes (authority, child, soldier).

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/transposition | resolve_conflicts | Renamed/relocated references |
| docs/infrastructure/canon | canon_guardrails | Protected facts and presence |
| docs/infrastructure/world-builder | create_entry_point | Arrival location if needed |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define formal schema for voyager exports (JSON schema)
- [ ] Add versioning for export format migrations
- IDEA: Add a "scar decay" model to soften old trauma
- QUESTION: Where do we store exporter notes and who can see them?
