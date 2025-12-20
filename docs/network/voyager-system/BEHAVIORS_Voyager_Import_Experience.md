# Voyager System — Behaviors: Importing Trauma Without Breaking Canon

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Trauma_Without_Memory.md
THIS:            BEHAVIORS_Voyager_Import_Experience.md (you are here)
MECHANISMS:      ./MECHANISMS_Export_Import_Transposition.md
VERIFICATION:    ./VALIDATION_Voyager_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Voyager_System.md
TEST:            ./TEST_Voyager_System.md
SYNC:            ./SYNC_Voyager_System.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Export produces a trauma-preserving capsule

```
GIVEN:  a character with lived narratives in a source world
WHEN:   export is requested
THEN:   traits, skills, generalized beliefs, and behavioral scars are included
AND:    named memories, named relationships, and place knowledge are stripped
```

### B2: Import preserves the mystery of origin

```
GIVEN:  a voyager export file
WHEN:   the voyager is imported
THEN:   the character appears with scars and generalized beliefs
AND:    an arrival narrative is created without revealing specific past events
```

### B3: Canon conflicts are resolved without retcon

```
GIVEN:  a voyager reference conflicts with local canon
WHEN:   import runs transposition
THEN:   names/places/events are generalized, renamed, or relocated
```

### B4: Behavioral scars trigger in play

```
GIVEN:  a voyager with a fire-related scar
WHEN:   a fire narrative occurs nearby
THEN:   the voyager exhibits the scar response
```

---

## INPUTS / OUTPUTS

### Primary Function: `export_voyager()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| character_id | string | Character node identifier |
| graph_snapshot | object | Access to narratives/beliefs |
| export_options | object | Flags for privacy and sharing |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| voyager_export | object | Export capsule (traits, scars, templates) |

**Side Effects:**

- None (read-only export)

### Primary Function: `import_voyager()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| voyager_export | object | Export capsule |
| destination_graph | object | Local world graph |
| entry_point | string | Arrival location ID |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| voyager_id | string | New character node ID |

**Side Effects:**

- Adds new character node
- Adds arrival narrative
- Adds behavioral scars and relationship templates

---

## EDGE CASES

### E1: Party import with shared scars

```
GIVEN:  a voyager party export with shared scars
THEN:   all members import with consistent shared triggers
```

### E2: Missing entry point

```
GIVEN:  a destination world with no defined entry point
THEN:   import selects a default border/coast location
```

---

## ANTI-BEHAVIORS

### A1: Specific memories leak into local canon

```
GIVEN:   a voyager with named memories
WHEN:    import runs
MUST NOT: write those memories into local canon
INSTEAD: convert to generalized scars or rumor-like beliefs
```

### A2: Multiverse framing enters the fiction

```
GIVEN:   player-facing narrative generation
WHEN:    voyager origin is referenced
MUST NOT: state that multiple universes exist
INSTEAD: present as unknown origin, exile, or silence
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define UX copy for "voyager arrival" scenes and journal entries
- [ ] Clarify how exporter notes are revealed (if at all)
- IDEA: Add configurable severity thresholds for scar extraction
- QUESTION: How does voyager import interact with faction reputation?
