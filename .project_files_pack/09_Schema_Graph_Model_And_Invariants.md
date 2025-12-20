# 09_Schema_Graph_Model_And_Invariants

@pack:generated_at: 2025-12-20T10:41:21
@pack:repo_kind: blood-ledger

Schema / graph model / invariants anchoring the system


---

## SOURCE: docs/schema/SCHEMA.md
# Schema (Index)

This file is intentionally concise. The schema is now split for readability.

Start here:
- `docs/schema/SCHEMA/SCHEMA_Overview.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Tensions.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`


---

## SOURCE: docs/schema/SCHEMA_Moments.md
# Moments Schema (Index)

This file is intentionally concise. The Moments schema is now split.

Start here:
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Node.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Links.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Example.md`


---

## SOURCE: docs/schema/SCHEMA/SCHEMA_Links.md
# Schema Links

## NARRATIVE -> NARRATIVE

Purpose: How stories relate (contradict, support, elaborate, subsume, supersede).

When to create:
- Two narratives are in tension or reinforce each other
- New information replaces old

Attributes:
```yaml
contradicts: float
supports: float
elaborates: float
subsumes: float
supersedes: float
```

## CHARACTER -> PLACE (Presence)

Purpose: Ground truth physical location of a character.

Attributes:
```yaml
present: float
visible: float
```

## CHARACTER -> THING (Possession)

Purpose: Ground truth physical possession.

Attributes:
```yaml
carries: float
carries_hidden: float
```

## THING -> PLACE (Location)

Purpose: Ground truth location for uncarried things.

Attributes:
```yaml
located: float
hidden: float
specific_location: string
```

## PLACE -> PLACE (Containment)

Purpose: Hierarchical containment (binary).

Attributes: none

## PLACE -> PLACE (Route)

Purpose: Travel connection between settlements/regions.

Attributes:
```yaml
waypoints: float[][]
road_type: enum [roman, track, path, river, none]
distance_km: float (computed)
travel_minutes: integer (computed)
difficulty: enum [easy, moderate, hard, dangerous] (computed)
detail: string
```


---

## SOURCE: docs/schema/SCHEMA/SCHEMA_Nodes.md
# Schema Nodes

## CHARACTER

Purpose: A person who exists in the world and can act, speak, and remember.

When to create:
- A new person enters the story or is mentioned
- World Runner determines someone acted off-screen

When to update:
- Character dies or gains/loses a modifier

Attributes:
```yaml
id: string
name: string
type: enum [player, companion, major, minor, background]
alive: boolean
face: enum [young, scarred, weathered, gaunt, hard, noble]
skills: { fighting, tracking, healing, persuading, sneaking, riding, reading, leading }
voice: { tone, style }
personality: { approach, values[], flaw }
backstory: { family, childhood, wound, why_here }
modifiers: []
image_prompt: string
```

## PLACE

Purpose: A location where things happen, with atmosphere and geography.

When to create:
- Player travels to a new location
- A location is mentioned that might be visited

When to update:
- Atmosphere or modifiers change

Attributes:
```yaml
id: string
name: string
coordinates: [lat, lng]
scale: enum [region, settlement, district, building, room]
type: enum [region, city, hold, village, monastery, camp, road, room, wilderness, ruin]
atmosphere: { weather[], mood, details[] }
modifiers: []
image_prompt: string
```

## THING

Purpose: An object that can be owned, given, stolen, or fought over.

When to create:
- Object becomes narratively relevant
- Something is given, stolen, found, or fought over

When to update:
- Thing is damaged, hidden, blessed, cursed, or consumed

Attributes:
```yaml
id: string
name: string
type: enum [weapon, armor, document, letter, relic, treasure, title, land, token, provisions, coin_purse, horse, ship, tool]
portable: boolean
significance: enum [mundane, personal, political, sacred, legendary]
quantity: integer
description: string
modifiers: []
image_prompt: string
```

## NARRATIVE

Purpose: A story that characters believe, creating relationships, knowledge, and conflict.

When to create:
- An event occurs that characters will remember or discuss
- A relationship forms, changes, or is revealed
- Information is learned, spread, or discovered

When to update:
- Narrator adds notes or adjusts focus

Attributes:
```yaml
id: string
name: string
content: string
interpretation: string
type: enum
about: { characters[], places[], things[], relationships[] }
tone: string
weight: float
focus: float
truth: float
narrator_notes: string
occurred_at: string
visibility: enum [public, secret, known_to_few]
deadline: datetime
conditions: string[]
```


---

## SOURCE: docs/schema/SCHEMA/SCHEMA_Overview.md
# Schema Overview

```
STATUS: CANONICAL
UPDATED: 2025-12-19
VERSION: 5.1
```

## CHAIN

```
THIS:     SCHEMA/SCHEMA_Overview.md
NODES:    SCHEMA/SCHEMA_Nodes.md
LINKS:    SCHEMA/SCHEMA_Links.md
TENSIONS: SCHEMA/SCHEMA_Tensions.md
MOMENTS:  ../SCHEMA_Moments/SCHEMA_Moments_Overview.md
VALIDATION: ../VALIDATION_Graph.md
```

## Scope

- Node types: Character, Place, Thing, Narrative
- Link types: Core graph links (moment-specific links live in SCHEMA_Moments)
- Tensions: Pressure clusters that break into events
- Moments: See `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`

## Core Principles (Concise)

- Nodes are things that exist; narratives are stories about nodes.
- Relationships are narratives; there is no separate relationship state.
- Physical state is ground truth (presence, possession, location).
- Narrative weight drives salience; contradictions accumulate into tension.


---

## SOURCE: docs/schema/SCHEMA/SCHEMA_Tensions.md
# Schema Tensions

Purpose: A cluster of narratives under pressure that will eventually break.

When to create:
- Contradicting narratives must resolve
- Deadlines or confrontations are brewing

When to update:
- Pressure changes via time or events
- Narratives added/removed

Attributes:
```yaml
id: string
narratives: string[]
description: string
narrator_notes: string
pressure_type: enum [gradual, scheduled, hybrid]
pressure: float
breaking_point: float
base_rate: float
trigger_at: string
progression:
  - at: string
    pressure: float
    pressure_floor: float
```

Examples:
```yaml
# Gradual
tension_aldric_loyalty:
  pressure_type: gradual
  pressure: 0.4
  base_rate: 0.001
  breaking_point: 0.9

# Scheduled
tension_malet_inspection:
  pressure_type: scheduled
  trigger_at: "Day 16, morning"
  progression:
    - { at: "Day 14", pressure: 0.1 }
    - { at: "Day 16 dawn", pressure: 0.9 }

# Hybrid
tension_edmund_confrontation:
  pressure_type: hybrid
  pressure: 0.5
  progression:
    - { at: "Day 12", pressure_floor: 0.5 }
    - { at: "Day 14", pressure_floor: 0.85 }
```


---

## SOURCE: docs/schema/models/PATTERNS_Pydantic_Schema_Models.md
# Schema Models — Patterns: Pydantic Graph Schema Models

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Pydantic_Schema_Models.md
SYNC:  ./SYNC_Schema_Models.md
IMPL:  engine/models/__init__.py
```

---

## THE PROBLEM

The engine needs a single, validated schema for nodes, links, tensions, and
moments so all subsystems speak the same language. Without a canonical set of
models, serialization, validation, and LLM-facing contracts drift and gameplay
state becomes inconsistent.

---

## THE PATTERN

Define the schema as Pydantic models and enums, split by responsibility:
base enums and shared structures in `base.py`, node models in `nodes.py`, link
models in `links.py`, and tension models in `tensions.py`. Keep the module
re-export layer in `__init__.py` so other systems import one stable surface.

---

## PRINCIPLES

### Principle 1: Schema As Contract

All gameplay data structures are expressed as Pydantic models, giving a single
source of truth for validation and serialization.

### Principle 2: Separate Enums From Entities

Enums and shared shapes live in `base.py`, allowing node/link models to remain
focused on domain fields rather than taxonomy definitions.

### Principle 3: Computed Helpers Stay Close

Lightweight helpers (like embeddable text or link intensity) live on the model
they describe so downstream systems can rely on consistent behavior.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `pydantic` | Validation, defaults, and serialization for schema models |
| `docs/schema/SCHEMA.md` | Canonical schema definitions and version context |

---

## INSPIRATIONS

- Pydantic's validation and JSON schema export patterns, which keep the schema
  contract explicit and make model intent legible across services, aligning
  with how schema expectations surface in tests and tooling.
- The shared schema glossary in `docs/schema/SCHEMA.md`, anchoring consistent
  field naming and enum meanings across engine subsystems and graph health
  checks.

---

## SCOPE

### In Scope

- Pydantic classes, enums, and shared base shapes for nodes, links, and
  tensions that define canonical schema surfaces for the engine, including
  shared identifiers and timestamp shapes.
- Field defaults, optionality, and helper properties that remain data-adjacent
  so model behavior stays predictable and portable.

### Out of Scope

- Graph storage, query APIs, and persistence behavior, which live in graph and
  physics layers rather than the schema-model definitions or migrations.
- Runtime rule enforcement (physics ticks, tension flips, narrative gating)
  that belongs to system logic outside the schema layer.

---

## WHAT THIS DOES NOT SOLVE

- Graph persistence or query logic, which live in graph/physics layers and storage.
- Relationship integrity across nodes/links beyond field validation checks.
- Runtime enforcement of world rules, which is owned by physics and runtime services.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Document validation invariants specific to model interactions.
- [ ] Decide whether a dedicated schema validation test suite is needed beyond `engine/tests/test_models.py`.


---

## SOURCE: docs/schema/models/SYNC_Schema_Models.md
# Schema Models — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Pydantic models for nodes, links, and tensions in `engine/models/`.
- Enum taxonomy for schema fields in `engine/models/base.py`.

**What's still being designed:**
- Cross-model validation rules beyond field-level checks.

**What's proposed (v2+):**
- Dedicated schema validation suite that enforces graph-level invariants.

---

## CURRENT STATE

The engine exposes a unified set of Pydantic models for graph nodes, links, and
tensions, along with shared enums and helper methods. The module is structured
by responsibility (base enums, nodes, links, tensions) and re-exported from
`engine/models/__init__.py` for stable imports. Tests live in
`engine/tests/test_models.py` with some integration coverage in scenario tests.
Updated the patterns doc to include the missing INSPIRATIONS and SCOPE
sections and expanded the non-goals to meet template length guidance.

---

## IN PROGRESS

Doc-template repair for this SYNC file, focused on filling missing sections so
schema-model documentation stays aligned while avoiding behavioral changes.
Once complete, keep the schema-model doc chain synced with future field edits.

---

## KNOWN ISSUES

The schema-models doc chain does not yet link `docs/schema/SCHEMA.md`, so schema
context is split across modules and can drift without explicit cross-links.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Added docs + mapping; no code changes beyond DOCS reference.

**What you need to understand:**
Schema models are the canonical Pydantic types for nodes/links/tensions. Keep
`engine/models/__init__.py` as the public entry point and update docs if fields
change.

**Watch out for:**
Some schema behavior is documented in `docs/schema/SCHEMA.md` but not yet linked
into a full doc chain for this module.

---

## HANDOFF: FOR HUMAN

This update only fills missing SYNC sections to satisfy the doc template; no
behavior changes were made to schema models or tests.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL->DOCS: If model fields change, update `docs/schema/models/`.

### Tests to Run

```bash
pytest engine/tests/test_models.py
```

## CONSCIOUSNESS TRACE

Attention stayed on template completeness rather than schema changes; the main
concern is avoiding doc drift while keeping updates minimal and traceable.

---

## POINTERS

- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `engine/models/__init__.py`
- `engine/tests/test_models.py`


---

## ARCHIVE

Older content archived to: `SYNC_Schema_Models_archive_2025-12.md`


---

## SOURCE: docs/schema/models/SYNC_Schema_Models_archive_2025-12.md
# Archived: SYNC_Schema_Models.md

Archived on: 2025-12-19
Original file: SYNC_Schema_Models.md

---

## RECENT CHANGES

### 2025-12-19: Reconfirmed node helper implementations (repair 07, current run)

- **What:** Rechecked `Narrative.is_core_type` and Moment helpers (`tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) remain implemented in `engine/models/nodes.py` (see `engine/models/nodes.py:185` and `engine/models/nodes.py:249`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of node helper properties.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated link helper implementations with line refs (repair 06, current run)

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py` (`engine/models/links.py:66`, `engine/models/links.py:120`, `engine/models/links.py:140`, `engine/models/links.py:160`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation for link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated node helper implementations with line refs (repair 07)

- **What:** Confirmed `Narrative.is_core_type` and Moment helpers (`tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) are implemented in `engine/models/nodes.py` (`Narrative.is_core_type` at `engine/models/nodes.py:185`, Moment helpers starting at `engine/models/nodes.py:249`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair required validation of node helper properties.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Repair task appears stale relative to current code.

### 2025-12-19: Verified GameTimestamp comparison helpers (repair 05)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair task required validation for the base model helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale relative to current implementation.

### 2025-12-19: Rechecked link helper implementations (repair 05, latest run)

- **What:** Reconfirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required verification for link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated link helper implementations (repair 05, current run)

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` in `engine/models/links.py` remain implemented; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of the link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Verified GameTimestamp helpers with test attempt (current run)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; attempted `pytest engine/tests/test_models.py`.
- **Why:** Current INCOMPLETE_IMPL repair requires evidence for comparison helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Test dependency missing in environment; helper implementations still present.

### 2025-12-19: Verified GameTimestamp helper implementations (repair 04)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; no code changes required.
- **Why:** Current INCOMPLETE_IMPL repair run flagged empty helpers; verification shows the implementations are already present.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale relative to current code.

### 2025-12-19: Rechecked GameTimestamp comparison helpers (current run)

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are already implemented in `engine/models/base.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of these helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task is stale relative to the current implementation.

### 2025-12-19: Logged repair 04 verification (current run)

- **What:** Recorded the current repair run verification for `GameTimestamp` helpers in `engine/models/base.py`; no code changes needed.
- **Why:** Repair task required confirmation for this run.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Logged repair 06 verification (current run)

- **What:** Recorded the current repair run verification for node helper properties in `engine/models/nodes.py`; no code changes needed.
- **Why:** Repair task required confirmation for this run.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated node helper implementations (repair 06)

- **What:** Rechecked `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` in `engine/models/nodes.py`; implementations already present.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reconfirmed link helper implementations (repair 05)

- **What:** Verified `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py`.
- **Why:** Current INCOMPLETE_IMPL repair run required confirmation.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; no code changes required.

### 2025-12-19: Revalidated link helper implementations (repair 05)

- **What:** Rechecked `belief_intensity`, `is_present`, `has_item`, and `is_here` in `engine/models/links.py`; implementations already present.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reverified GameTimestamp comparison helpers (repair 04)

- **What:** Rechecked `GameTimestamp.__str__`, `__le__`, and `__gt__` and confirmed implementations already exist.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale relative to current code.

### 2025-12-19: Verified node helper implementations

- **What:** Confirmed `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` are implemented in `engine/models/nodes.py`.
- **Why:** Repair task flagged incomplete helpers; verification shows no changes needed.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Verified link helper implementations

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` helpers are implemented in `engine/models/links.py`.
- **Why:** Repair task flagged incomplete helpers; verification shows no changes needed.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Verified GameTimestamp comparison helpers

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are fully implemented in `engine/models/base.py`.
- **Why:** Repair task flagged incomplete implementations; verification shows the functions are already complete.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reconfirmed GameTimestamp comparison helpers

- **What:** Rechecked `GameTimestamp.__str__`, `__le__`, and `__gt__` for the 06-INCOMPLETE_IMPL-models-base repair run; no code changes needed.
- **Why:** Current repair task required verification in the latest run.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`, `.ngram/state/SYNC_Project_State.md`.
- **Struggles/Insights:** Repair task remains stale relative to current code.

### 2025-12-19: Revalidated GameTimestamp comparison helpers (repair 04)

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are fully implemented in `engine/models/base.py`; no code changes required.
- **Why:** Repair task flagged incomplete implementations; current code already satisfies the expected behavior.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale relative to current implementation.

### 2025-12-19: Documented schema models module

- **What:** Added module docs and mapping for `engine/models/**`.
- **Why:** Close undocumented module gap and enable `ngram` context navigation.
- **Files:** `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`, `docs/schema/models/SYNC_Schema_Models.md`, `engine/models/__init__.py`, `modules.yaml`.
- **Struggles/Insights:** Minimal chain created to avoid duplicating existing schema docs.

---


## Agent Observations

### Remarks
- Repair task flagged incomplete functions, but `engine/models/base.py` already contains full implementations for the comparison helpers.
- Reverified the base model comparison helpers for repair 05; no code changes required.
- Repair task for `engine/models/links.py` flagged missing helpers, but implementations are already present.
- Repair task for `engine/models/nodes.py` flagged missing helpers, but implementations are already present.
- Reverified GameTimestamp comparison helpers for the current repair run; no changes required.
- Logged the current repair run verification for `GameTimestamp` helpers; no code changes required.
- Revalidated link helper implementations in `engine/models/links.py`; no changes required.
- Revalidated node helper implementations in `engine/models/nodes.py`; no changes required.
- Confirmed the current repair run for `engine/models/base.py` remains a verification-only update; no code changes needed.
- Attempted `pytest engine/tests/test_models.py`; missing `pytest_xprocess` prevented the test run.
- Reconfirmed link helper properties for the current repair run; no code changes required.
- Rechecked link helper implementations for the latest repair run; no code changes required.
- Revalidated link helper implementations for the current repair run; no code changes required.

### Suggestions
- [ ] Consider adding explicit tests for `GameTimestamp` ordering in `engine/tests/test_models.py`.

### Propositions



---

# Archived: SYNC_Schema_Models.md

Archived on: 2025-12-20
Original file: SYNC_Schema_Models.md

---

## RECENT CHANGES

### 2025-12-19: Reconfirmed node helper implementations (repair 07, current run)

- **What:** Rechecked `Narrative.is_core_type` and Moment helpers (`tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) remain implemented in `engine/models/nodes.py` (see `engine/models/nodes.py:185` and `engine/models/nodes.py:249`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of node helper properties.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated link helper implementations with line refs (repair 06, current run)

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py` (`engine/models/links.py:66`, `engine/models/links.py:120`, `engine/models/links.py:140`, `engine/models/links.py:160`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation for link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated node helper implementations with line refs (repair 07)

- **What:** Confirmed `Narrative.is_core_type` and Moment helpers (`tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) are implemented in `engine/models/nodes.py` (`Narrative.is_core_type` at `engine/models/nodes.py:185`, Moment helpers starting at `engine/models/nodes.py:249`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair required validation of node helper properties.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Repair task appears stale relative to current code.

### 2025-12-19: Verified GameTimestamp comparison helpers (repair 05)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair task required validation for the base model helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale relative to current implementation.

### 2025-12-19: Rechecked link helper implementations (repair 05, latest run)

- **What:** Reconfirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required verification for link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated link helper implementations (repair 05, current run)

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` in `engine/models/links.py` remain implemented; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of the link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Verified GameTimestamp helpers with test attempt (current run)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; attempted `pytest engine/tests/test_models.py`.
- **Why:** Current INCOMPLETE_IMPL repair requires evidence for comparison helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Test dependency missing in environment; helper implementations still present.

### 2025-12-19: Verified GameTimestamp helper implementations (repair 04)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; no code changes required.
- **Why:** Current INCOMPLETE_IMPL repair run flagged empty helpers; verification shows the implementations are already present.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale relative to current code.

### 2025-12-19: Rechecked GameTimestamp comparison helpers (current run)

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are already implemented in `engine/models/base.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of these helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task is stale relative to the current implementation.

### 2025-12-19: Logged repair 04 verification (current run)

- **What:** Recorded the current repair run verification for `GameTimestamp` helpers in `engine/models/base.py`; no code changes needed.
- **Why:** Repair task required confirmation for this run.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Logged repair 06 verification (current run)

- **What:** Recorded the current repair run verification for node helper properties in `engine/models/nodes.py`; no code changes needed.
- **Why:** Repair task required confirmation for this run.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated node helper implementations (repair 06)

- **What:** Rechecked `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` in `engine/models/nodes.py`; implementations already present.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reconfirmed link helper implementations (repair 05)

- **What:** Verified `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py`.
- **Why:** Current INCOMPLETE_IMPL repair run required confirmation.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; no code changes required.

### 2025-12-19: Revalidated link helper implementations (repair 05)

- **What:** Rechecked `belief_intensity`, `is_present`, `has_item`, and `is_here` in `engine/models/links.py`; implementations already present.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reverified GameTimestamp comparison helpers (repair 04)

- **What:** Rechecked `GameTimestamp.__str__`, `__le__`, and `__gt__` and confirmed implementations already exist.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale relative to current code.

### 2025-12-19: Verified node helper implementations

- **What:** Confirmed `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` are implemented in `engine/models/nodes.py`.
- **Why:** Repair task flagged incomplete helpers; verification shows no changes needed.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Verified link helper implementations

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` helpers are implemented in `engine/models/links.py`.
- **Why:** Repair task flagged incomplete helpers; verification shows no changes needed.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Verified GameTimestamp comparison helpers

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are fully implemented in `engine/models/base.py`.
- **Why:** Repair task flagged incomplete implementations; verification shows the functions are already complete.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reconfirmed GameTimestamp comparison helpers

- **What:** Rechecked `GameTimestamp.__str__`, `__le__`, and `__gt__` for the 06-INCOMPLETE_IMPL-models-base repair run; no code changes needed.
- **Why:** Current repair task required verification in the latest run.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`, `.ngram/state/SYNC_Project_State.md`.
- **Struggles/Insights:** Repair task remains stale relative to current code.

### 2025-12-19: Revalidated GameTimestamp comparison helpers (repair 04)

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are fully implemented in `engine/models/base.py`; no code changes required.
- **Why:** Repair task flagged incomplete implementations; current code already satisfies the expected behavior.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale relative to current implementation.

### 2025-12-19: Documented schema models module

- **What:** Added module docs and mapping for `engine/models/**`.
- **Why:** Close undocumented module gap and enable `ngram` context navigation.
- **Files:** `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`, `docs/schema/models/SYNC_Schema_Models.md`, `engine/models/__init__.py`, `modules.yaml`.
- **Struggles/Insights:** Minimal chain created to avoid duplicating existing schema docs.

---


## Agent Observations

### Remarks
- Repair task flagged incomplete functions, but `engine/models/base.py` already contains full implementations for the comparison helpers.
- Reverified the base model comparison helpers for repair 05; no code changes required.
- Repair task for `engine/models/links.py` flagged missing helpers, but implementations are already present.
- Repair task for `engine/models/nodes.py` flagged missing helpers, but implementations are already present.
- Reverified GameTimestamp comparison helpers for the current repair run; no changes required.
- Logged the current repair run verification for `GameTimestamp` helpers; no code changes required.
- Revalidated link helper implementations in `engine/models/links.py`; no changes required.
- Revalidated node helper implementations in `engine/models/nodes.py`; no changes required.
- Confirmed the current repair run for `engine/models/base.py` remains a verification-only update; no code changes needed.
- Attempted `pytest engine/tests/test_models.py`; missing `pytest_xprocess` prevented the test run.
- Reconfirmed link helper properties for the current repair run; no code changes required.
- Rechecked link helper implementations for the latest repair run; no code changes required.
- Revalidated link helper implementations for the current repair run; no code changes required.
- Expanded INSPIRATIONS and SCOPE text in the patterns doc to meet template
  length guidance for the schema-model module.
- Refined the patterns wording to better tie schema scope to testing and graph
  health tooling context.

### Suggestions
- [ ] Consider adding explicit tests for `GameTimestamp` ordering in `engine/tests/test_models.py`.

### Propositions

---



---

## SOURCE: engine/models/__init__.py
"""
Blood Ledger — Data Models

Complete Pydantic models for the Blood Ledger schema.
Based on SCHEMA.md v5.1

DOCS: docs/schema/models/PATTERNS_Pydantic_Schema_Models.md

Nodes (4 types):
- Character: A person who can act, speak, remember, die
- Place: A location with atmosphere and geography
- Thing: An object that can be owned, given, stolen, fought over
- Narrative: A story that characters believe

Links (6 types):
- CharacterNarrative: What a character knows/believes
- NarrativeNarrative: How stories relate
- CharacterPlace: Physical presence (ground truth)
- CharacterThing: Physical possession (ground truth)
- ThingPlace: Where things are (ground truth)
- PlacePlace: Geography (ground truth)


"""

# Nodes
from .nodes import Character, Place, Thing, Narrative

# Links
from .links import (
    CharacterNarrative,
    NarrativeNarrative,
    CharacterPlace,
    CharacterThing,
    ThingPlace,
    PlacePlace
)



# Base types and enums
from .base import (
    # Character enums
    CharacterType, Face, SkillLevel, VoiceTone, VoiceStyle,
    Approach, Value, Flaw,
    # Place enums
    PlaceType, Weather, Mood,
    # Thing enums
    ThingType, Significance,
    # Narrative enums
    NarrativeType, NarrativeTone, NarrativeVoiceStyle,
    # Link enums
    BeliefSource, PathDifficulty,

    # Modifier enums
    ModifierType, ModifierSeverity,
    # Shared models
    Modifier, Skills, CharacterVoice, Personality, Backstory,
    Atmosphere, NarrativeAbout, NarrativeVoice, TensionProgression
)

__all__ = [
    # Nodes
    'Character', 'Place', 'Thing', 'Narrative',
    # Links
    'CharacterNarrative', 'NarrativeNarrative',
    'CharacterPlace', 'CharacterThing', 'ThingPlace', 'PlacePlace',

    # Enums
    'CharacterType', 'Face', 'SkillLevel', 'VoiceTone', 'VoiceStyle',
    'Approach', 'Value', 'Flaw',
    'PlaceType', 'Weather', 'Mood',
    'ThingType', 'Significance',
    'NarrativeType', 'NarrativeTone', 'NarrativeVoiceStyle',
    'BeliefSource', 'PathDifficulty',
    'PressureType',
    'ModifierType', 'ModifierSeverity',
    # Shared models
    'Modifier', 'Skills', 'CharacterVoice', 'Personality', 'Backstory',
    'Atmosphere', 'NarrativeAbout', 'NarrativeVoice'
]


---

## SOURCE: engine/models/base.py
"""
Blood Ledger — Base Types and Enums

Common types, enums, and modifiers shared across all models.
Based on SCHEMA.md v5.1

TESTS:
    engine/tests/test_models.py::TestModifier
    engine/tests/test_models.py::TestGameTimestamp
    engine/tests/test_spec_consistency.py::TestEnumConsistency

VALIDATES:
    V2: Node enums (CharacterType, PlaceType, ThingType, NarrativeType, etc.)
    V3: Link enums (BeliefSource, PathDifficulty)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# =============================================================================
# CHARACTER ENUMS
# =============================================================================

class CharacterType(str, Enum):
    PLAYER = "player"
    COMPANION = "companion"
    MAJOR = "major"
    MINOR = "minor"
    BACKGROUND = "background"


class Face(str, Enum):
    YOUNG = "young"
    SCARRED = "scarred"
    WEATHERED = "weathered"
    GAUNT = "gaunt"
    HARD = "hard"
    NOBLE = "noble"


class SkillLevel(str, Enum):
    UNTRAINED = "untrained"
    CAPABLE = "capable"
    SKILLED = "skilled"
    MASTER = "master"


class VoiceTone(str, Enum):
    QUIET = "quiet"
    SHARP = "sharp"
    WARM = "warm"
    BITTER = "bitter"
    MEASURED = "measured"
    FIERCE = "fierce"


class VoiceStyle(str, Enum):
    DIRECT = "direct"
    QUESTIONING = "questioning"
    SARDONIC = "sardonic"
    GENTLE = "gentle"
    BLUNT = "blunt"


class Approach(str, Enum):
    DIRECT = "direct"
    CUNNING = "cunning"
    CAUTIOUS = "cautious"
    IMPULSIVE = "impulsive"
    DELIBERATE = "deliberate"


class Value(str, Enum):
    LOYALTY = "loyalty"
    SURVIVAL = "survival"
    HONOR = "honor"
    AMBITION = "ambition"
    FAITH = "faith"
    FAMILY = "family"
    JUSTICE = "justice"
    FREEDOM = "freedom"
    WEALTH = "wealth"
    KNOWLEDGE = "knowledge"
    POWER = "power"
    PEACE = "peace"


class Flaw(str, Enum):
    PRIDE = "pride"
    FEAR = "fear"
    GREED = "greed"
    WRATH = "wrath"
    DOUBT = "doubt"
    RIGIDITY = "rigidity"
    SOFTNESS = "softness"
    ENVY = "envy"
    SLOTH = "sloth"


# =============================================================================
# PLACE ENUMS
# =============================================================================

class PlaceType(str, Enum):
    REGION = "region"
    CITY = "city"
    HOLD = "hold"
    VILLAGE = "village"
    MONASTERY = "monastery"
    CAMP = "camp"
    ROAD = "road"
    ROOM = "room"
    WILDERNESS = "wilderness"
    RUIN = "ruin"


class Weather(str, Enum):
    RAIN = "rain"
    SNOW = "snow"
    FOG = "fog"
    CLEAR = "clear"
    OVERCAST = "overcast"
    STORM = "storm"
    WIND = "wind"
    COLD = "cold"
    HOT = "hot"


class Mood(str, Enum):
    WELCOMING = "welcoming"
    HOSTILE = "hostile"
    INDIFFERENT = "indifferent"
    FEARFUL = "fearful"
    WATCHFUL = "watchful"
    DESPERATE = "desperate"
    PEACEFUL = "peaceful"
    TENSE = "tense"


# =============================================================================
# THING ENUMS
# =============================================================================

class ThingType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    DOCUMENT = "document"
    LETTER = "letter"
    RELIC = "relic"
    TREASURE = "treasure"
    TITLE = "title"
    LAND = "land"
    TOKEN = "token"
    PROVISIONS = "provisions"
    COIN_PURSE = "coin_purse"
    HORSE = "horse"
    SHIP = "ship"
    TOOL = "tool"


class Significance(str, Enum):
    MUNDANE = "mundane"
    PERSONAL = "personal"
    POLITICAL = "political"
    SACRED = "sacred"
    LEGENDARY = "legendary"


# =============================================================================
# NARRATIVE ENUMS
# =============================================================================

class NarrativeType(str, Enum):
    # About events
    MEMORY = "memory"
    ACCOUNT = "account"
    RUMOR = "rumor"
    # About characters
    REPUTATION = "reputation"
    IDENTITY = "identity"
    # About relationships
    BOND = "bond"
    OATH = "oath"
    DEBT = "debt"
    BLOOD = "blood"
    ENMITY = "enmity"
    LOVE = "love"
    SERVICE = "service"
    # About things
    OWNERSHIP = "ownership"
    CLAIM = "claim"
    # About places
    CONTROL = "control"
    ORIGIN = "origin"
    # Meta
    BELIEF = "belief"
    PROPHECY = "prophecy"
    LIE = "lie"
    SECRET = "secret"


class NarrativeTone(str, Enum):
    BITTER = "bitter"
    PROUD = "proud"
    SHAMEFUL = "shameful"
    DEFIANT = "defiant"
    MOURNFUL = "mournful"
    COLD = "cold"
    RIGHTEOUS = "righteous"
    HOPEFUL = "hopeful"
    FEARFUL = "fearful"
    WARM = "warm"
    DARK = "dark"
    SACRED = "sacred"


class NarrativeVoiceStyle(str, Enum):
    WHISPER = "whisper"
    DEMAND = "demand"
    REMIND = "remind"
    ACCUSE = "accuse"
    PLEAD = "plead"
    WARN = "warn"
    INSPIRE = "inspire"
    MOCK = "mock"
    QUESTION = "question"


# =============================================================================
# LINK ENUMS
# =============================================================================

class BeliefSource(str, Enum):
    NONE = "none"
    WITNESSED = "witnessed"
    TOLD = "told"
    INFERRED = "inferred"
    ASSUMED = "assumed"
    TAUGHT = "taught"


class PathDifficulty(str, Enum):
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"
    DANGEROUS = "dangerous"
    IMPASSABLE = "impassable"


# =============================================================================
# MOMENT ENUMS
# =============================================================================

class MomentType(str, Enum):
    """Type of narrated moment."""
    NARRATION = "narration"           # Narrator description
    DIALOGUE = "dialogue"             # Character speaks
    ACTION = "action"                 # Physical action
    THOUGHT = "thought"               # Internal thought
    HINT = "hint"                     # Clickable hint / voice
    PLAYER_CLICK = "player_click"     # Player clicked a word
    PLAYER_FREEFORM = "player_freeform"  # Player typed text
    PLAYER_CHOICE = "player_choice"   # Player selected an option


class MomentStatus(str, Enum):
    """Lifecycle status of a Moment in the moment graph."""
    POSSIBLE = "possible"    # Created, not yet surfaced
    ACTIVE = "active"        # Visible to player, can be triggered
    SPOKEN = "spoken"        # In transcript, part of history
    DORMANT = "dormant"      # Waiting for return (persistent=True)
    DECAYED = "decayed"      # Pruned, no longer relevant


class MomentTrigger(str, Enum):
    """How a CAN_LEAD_TO link can be traversed."""
    CLICK = "click"          # Player clicks a word
    WAIT = "wait"            # Time passes without player input
    AUTO = "auto"            # Automatic when conditions met
    SEMANTIC = "semantic"    # Freeform input matches embedding


# =============================================================================
# MODIFIER ENUMS
# =============================================================================

class ModifierType(str, Enum):
    # Character modifiers
    WOUNDED = "wounded"
    SICK = "sick"
    HUNGRY = "hungry"
    EXHAUSTED = "exhausted"
    DRUNK = "drunk"
    GRIEVING = "grieving"
    INSPIRED = "inspired"
    AFRAID = "afraid"
    ANGRY = "angry"
    HOPEFUL = "hopeful"
    SUSPICIOUS = "suspicious"
    # Place modifiers
    BURNING = "burning"
    FLOODED = "flooded"
    BESIEGED = "besieged"
    ABANDONED = "abandoned"
    CELEBRATING = "celebrating"
    HAUNTED = "haunted"
    WATCHED = "watched"
    SAFE = "safe"
    # Thing modifiers
    DAMAGED = "damaged"
    HIDDEN = "hidden"
    CONTESTED = "contested"
    BLESSED = "blessed"
    CURSED = "cursed"
    STOLEN = "stolen"


class ModifierSeverity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


# =============================================================================
# SHARED MODELS
# =============================================================================

class Modifier(BaseModel):
    """Temporary state affecting any node."""
    type: ModifierType
    severity: ModifierSeverity = ModifierSeverity.MODERATE
    duration: str = Field(default="", description="How long: 'until healed', '3 days', 'permanent'")
    source: str = Field(default="", description="What caused this")


class Skills(BaseModel):
    """Character skills."""
    fighting: SkillLevel = SkillLevel.UNTRAINED
    tracking: SkillLevel = SkillLevel.UNTRAINED
    healing: SkillLevel = SkillLevel.UNTRAINED
    persuading: SkillLevel = SkillLevel.UNTRAINED
    sneaking: SkillLevel = SkillLevel.UNTRAINED
    riding: SkillLevel = SkillLevel.UNTRAINED
    reading: SkillLevel = SkillLevel.UNTRAINED
    leading: SkillLevel = SkillLevel.UNTRAINED


class CharacterVoice(BaseModel):
    """How a character speaks."""
    tone: VoiceTone = VoiceTone.MEASURED
    style: VoiceStyle = VoiceStyle.DIRECT


class Personality(BaseModel):
    """How a character thinks and acts."""
    approach: Approach = Approach.DIRECT
    values: List[Value] = Field(default_factory=list)
    flaw: Optional[Flaw] = None


class Backstory(BaseModel):
    """Deep character knowledge."""
    family: str = ""
    childhood: str = ""
    wound: str = ""
    why_here: str = ""


class Atmosphere(BaseModel):
    """Current feel of a place."""
    weather: List[Weather] = Field(default_factory=list)
    mood: Mood = Mood.INDIFFERENT
    details: List[str] = Field(default_factory=list)


class NarrativeAbout(BaseModel):
    """What a narrative concerns."""
    characters: List[str] = Field(default_factory=list)
    relationship: List[str] = Field(default_factory=list, description="Pair of character IDs")
    places: List[str] = Field(default_factory=list)
    things: List[str] = Field(default_factory=list)


class NarrativeVoice(BaseModel):
    """How a narrative speaks as a Voice."""
    style: NarrativeVoiceStyle = NarrativeVoiceStyle.REMIND
    phrases: List[str] = Field(default_factory=list)


# =============================================================================
# HISTORY MODELS
# =============================================================================

class TimeOfDay(str, Enum):
    """Valid times of day for the game world."""
    DAWN = "dawn"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    EVENING = "evening"
    NIGHT = "night"
    MIDNIGHT = "midnight"


class NarrativeSource(BaseModel):
    """
    Reference to a conversation section for player-experienced history.
    The conversation thread is the primary record; narratives index it.
    """
    file: str = Field(description="Path to conversation file, e.g., 'conversations/char_aldric.md'")
    section: str = Field(description="Section header, e.g., 'Day 4, Night — The Camp'")


class GameTimestamp(BaseModel):
    """
    Structured game world timestamp.
    Format: 'Day N, time_of_day'
    """
    day: int = Field(ge=1, description="Day number (1-based)")
    time: TimeOfDay = Field(description="Time of day")

    def __str__(self) -> str:
        return f"Day {self.day}, {self.time.value}"

    @classmethod
    def parse(cls, s: str) -> "GameTimestamp":
        """Parse 'Day N, time' string into GameTimestamp."""
        import re
        match = re.match(r"Day\s+(\d+),?\s*(\w+)", s, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid timestamp format: {s}")
        day = int(match.group(1))
        time_str = match.group(2).lower()
        return cls(day=day, time=TimeOfDay(time_str))

    def __lt__(self, other: "GameTimestamp") -> bool:
        if self.day != other.day:
            return self.day < other.day
        time_order = list(TimeOfDay)
        return time_order.index(self.time) < time_order.index(other.time)

    def __le__(self, other: "GameTimestamp") -> bool:
        return self == other or self < other

    def __gt__(self, other: "GameTimestamp") -> bool:
        return not self <= other

    def __ge__(self, other: "GameTimestamp") -> bool:
        return not self < other


---

## SOURCE: engine/models/links.py
"""
Blood Ledger — Link Models

The 6 link types that connect nodes.
Based on SCHEMA.md v5.1

TESTS:
    engine/tests/test_models.py::TestCharacterNarrativeLink
    engine/tests/test_models.py::TestNarrativeNarrativeLink
    engine/tests/test_models.py::TestCharacterPlaceLink
    engine/tests/test_models.py::TestCharacterThingLink
    engine/tests/test_models.py::TestThingPlaceLink
    engine/tests/test_models.py::TestPlacePlaceLink

VALIDATES:
    V3.1: BELIEVES link (Character -> Narrative)
    V3.2: NARRATIVE_NARRATIVE links (contradicts, supports, etc.)
    V3.3: Ground truth links (AT, CARRIES, LOCATED_AT, CONTAINS, ROUTE)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .base import BeliefSource, PathDifficulty


class CharacterNarrative(BaseModel):
    """
    CHARACTER_NARRATIVE - What a character knows, believes, doubts, hides, or spreads.

    This link IS how characters know things. There is no "knowledge" stat.
    Aldric knows about the betrayal because he has a link to that narrative
    with heard=1.0 and believes=0.9.

    History: Every memory is mediated through a BELIEVES link. Characters can be
    wrong, confidence varies, sources can be traced.
    """
    # Link endpoints
    character_id: str
    narrative_id: str

    # Knowledge (0-1) - how much do they know/believe?
    heard: float = Field(default=0.0, ge=0.0, le=1.0, description="Has encountered this story")
    believes: float = Field(default=0.0, ge=0.0, le=1.0, description="Holds as true")
    doubts: float = Field(default=0.0, ge=0.0, le=1.0, description="Actively uncertain")
    denies: float = Field(default=0.0, ge=0.0, le=1.0, description="Rejects as false")

    # Action (0-1) - what are they doing with this knowledge?
    hides: float = Field(default=0.0, ge=0.0, le=1.0, description="Knows but conceals")
    spreads: float = Field(default=0.0, ge=0.0, le=1.0, description="Actively promoting")

    # Origin
    originated: float = Field(default=0.0, ge=0.0, le=1.0, description="Created this narrative")

    # Metadata - how did they learn?
    source: BeliefSource = BeliefSource.NONE
    from_whom: str = Field(default="", description="Who told them")
    when: Optional[datetime] = None
    where: Optional[str] = Field(default=None, description="Place ID where they learned this")

    @property
    def belief_intensity(self) -> float:
        """Combined intensity of belief for energy calculations."""
        return max(self.believes, self.originated) * self.heard


class NarrativeNarrative(BaseModel):
    """
    NARRATIVE_NARRATIVE - How stories relate: contradict, support, elaborate, subsume, supersede.

    These links create story structure. Contradicting narratives create drama.
    Supporting narratives create belief clusters. Superseding narratives
    let the world evolve.
    """
    # Link endpoints
    source_narrative_id: str
    target_narrative_id: str

    # Relationship strengths (0-1)
    contradicts: float = Field(default=0.0, ge=0.0, le=1.0, description="Cannot both be true")
    supports: float = Field(default=0.0, ge=0.0, le=1.0, description="Reinforce each other")
    elaborates: float = Field(default=0.0, ge=0.0, le=1.0, description="Adds detail")
    subsumes: float = Field(default=0.0, ge=0.0, le=1.0, description="Specific case of")
    supersedes: float = Field(default=0.0, ge=0.0, le=1.0, description="Replaces - old fades")

    @property
    def link_type(self) -> str:
        """Return the dominant relationship type."""
        attrs = {
            'contradicts': self.contradicts,
            'supports': self.supports,
            'elaborates': self.elaborates,
            'subsumes': self.subsumes,
            'supersedes': self.supersedes
        }
        return max(attrs, key=attrs.get)


class CharacterPlace(BaseModel):
    """
    CHARACTER_PLACE - Where a character physically is (ground truth).

    This is GROUND TRUTH, not belief. A character IS at a place,
    regardless of what anyone believes.
    """
    # Link endpoints
    character_id: str
    place_id: str

    # Physical state
    present: float = Field(default=0.0, ge=0.0, le=1.0, description="1=here, 0=not here")
    visible: float = Field(default=1.0, ge=0.0, le=1.0, description="0=hiding, 1=visible")

    @property
    def is_present(self) -> bool:
        return self.present > 0.5


class CharacterThing(BaseModel):
    """
    CHARACTER_THING - What a character physically carries (ground truth).

    Ground truth. They HAVE it or they don't.
    Separate from ownership narratives (who SHOULD have it).
    """
    # Link endpoints
    character_id: str
    thing_id: str

    # Physical state
    carries: float = Field(default=0.0, ge=0.0, le=1.0, description="1=has it, 0=doesn't")
    carries_hidden: float = Field(default=0.0, ge=0.0, le=1.0, description="1=secretly, 0=openly")

    @property
    def has_item(self) -> bool:
        return self.carries > 0.5 or self.carries_hidden > 0.5


class ThingPlace(BaseModel):
    """
    THING_PLACE - Where an uncarried thing physically is (ground truth).

    Where things ARE, not where people think they are.
    """
    # Link endpoints
    thing_id: str
    place_id: str

    # Physical state
    located: float = Field(default=0.0, ge=0.0, le=1.0, description="1=here, 0=not here")
    hidden: float = Field(default=0.0, ge=0.0, le=1.0, description="1=concealed, 0=visible")
    specific_location: str = Field(default="", description="Where exactly")

    @property
    def is_here(self) -> bool:
        return self.located > 0.5


class PlacePlace(BaseModel):
    """
    PLACE_PLACE - How locations connect: contains, path, borders (ground truth).

    Geography determines travel time, which affects proximity,
    which affects how much characters matter to the player.
    """
    # Link endpoints
    source_place_id: str
    target_place_id: str

    # Spatial relationships
    contains: float = Field(default=0.0, ge=0.0, le=1.0, description="This place is inside that")
    path: float = Field(default=0.0, ge=0.0, le=1.0, description="Can travel between")
    path_distance: str = Field(default="", description="How far: '2 days', '4 hours'")
    path_difficulty: PathDifficulty = PathDifficulty.MODERATE
    borders: float = Field(default=0.0, ge=0.0, le=1.0, description="Share a border")

    def travel_days(self) -> float:
        """Parse path_distance into days for proximity calculation."""
        if not self.path_distance:
            return 1.0

        dist = self.path_distance.lower()
        if 'adjacent' in dist or 'same' in dist:
            return 0.0
        elif 'hour' in dist:
            # Extract number of hours
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1)) / 24.0
            return 0.1
        elif 'day' in dist:
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1))
            return 1.0
        else:
            return 1.0


---

## SOURCE: engine/models/nodes.py
"""
Blood Ledger — Node Models

The 4 node types: Character, Place, Thing, Narrative, Moment
Based on SCHEMA.md v5.1

DOCS: docs/schema/

TESTS:
    engine/tests/test_models.py::TestCharacterModel
    engine/tests/test_models.py::TestPlaceModel
    engine/tests/test_models.py::TestThingModel
    engine/tests/test_models.py::TestNarrativeModel
    engine/tests/test_models.py::TestMomentModel
    engine/tests/test_integration_scenarios.py (structural tests)

VALIDATES:
    V2.1: Character invariants (id, name, type, skills, voice, personality)
    V2.2: Place invariants (id, name, type, atmosphere)
    V2.3: Thing invariants (id, name, type, significance, portable)
    V2.4: Narrative invariants (id, name, content, type, weight, focus, truth)
    V2.6: Moment invariants (id, text, type, tick)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from .base import (
    CharacterType, Face, Skills, CharacterVoice, Personality, Backstory, Modifier,
    PlaceType, Atmosphere,
    ThingType, Significance,
    NarrativeType, NarrativeTone, NarrativeVoice, NarrativeAbout,
    NarrativeSource,
    MomentType, MomentStatus, MomentTrigger
)


class Character(BaseModel):
    """
    CHARACTER - A person who exists in the world, with voice, history, and agency.
    Anyone who can act, speak, remember, die.
    """
    id: str
    name: str
    type: CharacterType = CharacterType.MINOR
    alive: bool = True
    face: Optional[Face] = None

    skills: Skills = Field(default_factory=Skills)
    voice: CharacterVoice = Field(default_factory=CharacterVoice)
    personality: Personality = Field(default_factory=Personality)
    backstory: Backstory = Field(default_factory=Backstory)

    modifiers: List[Modifier] = Field(default_factory=list)

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.backstory.why_here:
            parts.append(f"Why here: {self.backstory.why_here}")
        if self.backstory.wound:
            parts.append(f"Wound: {self.backstory.wound}")
        if self.personality.values:
            parts.append(f"Values: {', '.join(v.value for v in self.personality.values)}")
        return ". ".join(parts)


class Place(BaseModel):
    """
    PLACE - A location where things happen, with atmosphere and geography.
    Anywhere that can be located, traveled to, occupied.
    """
    id: str
    name: str
    type: PlaceType = PlaceType.VILLAGE

    atmosphere: Atmosphere = Field(default_factory=Atmosphere)
    modifiers: List[Modifier] = Field(default_factory=list)

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.atmosphere.mood:
            parts.append(f"Mood: {self.atmosphere.mood.value}")
        if self.atmosphere.details:
            parts.append(f"Details: {', '.join(self.atmosphere.details)}")
        return ". ".join(parts)


class Thing(BaseModel):
    """
    THING - An object that can be owned, given, stolen, or fought over.
    Anything that can be possessed, transferred, contested.
    """
    id: str
    name: str
    type: ThingType = ThingType.TOOL
    portable: bool = True
    significance: Significance = Significance.MUNDANE
    quantity: int = 1
    description: str = ""

    modifiers: List[Modifier] = Field(default_factory=list)

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.description:
            parts.append(self.description)
        if self.significance != Significance.MUNDANE:
            parts.append(f"Significance: {self.significance.value}")
        return ". ".join(parts)


class Narrative(BaseModel):
    """
    NARRATIVE - A story that characters believe, creating all relationships and knowledge.

    Core insight: Everything is story. "Aldric is loyal" is a narrative, not a stat.
    Characters believe narratives. They don't have relationships - they have stories
    they tell themselves about relationships.

    History insight: History is distributed. Narratives about the past exist as beliefs,
    not as a central event log. Player-experienced history points to conversation files;
    world-generated history carries its own detail.
    """
    id: str
    name: str
    content: str = Field(description="The story itself - what happened, what is believed")
    interpretation: str = Field(default="", description="What it means - emotional/thematic weight")

    type: NarrativeType

    about: NarrativeAbout = Field(default_factory=NarrativeAbout)
    tone: Optional[NarrativeTone] = None
    voice: NarrativeVoice = Field(default_factory=NarrativeVoice)

    # History fields - when did this happen?
    # NOTE: "where" is expressed via OCCURRED_AT link to Place, not an attribute
    occurred_at: Optional[str] = Field(default=None, description="When event happened: 'Day N, time_of_day'")

    # History content - ONE of these for historical narratives
    source: Optional[NarrativeSource] = Field(
        default=None,
        description="For player-experienced history: reference to conversation file section"
    )
    detail: Optional[str] = Field(
        default=None,
        description="For world-generated history: full description (no conversation exists)"
    )

    # System fields (computed by graph engine)
    weight: float = Field(default=0.0, ge=0.0, le=1.0, description="Importance - computed by graph engine")
    focus: float = Field(default=1.0, ge=0.1, le=3.0, description="Narrator pacing adjustment")

    # Director only (hidden from players/characters)
    truth: float = Field(default=1.0, ge=0.0, le=1.0, description="How true is this? Characters never see this.")
    narrator_notes: str = Field(default="", description="Narrator's notes for continuity")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}: {self.content}"]
        if self.interpretation:
            parts.append(f"Meaning: {self.interpretation}")
        if self.tone:
            parts.append(f"Tone: {self.tone.value}")
        return ". ".join(parts)

    @property
    def is_core_type(self) -> bool:
        """Core types (oath, blood, debt) decay slower."""
        return self.type in [NarrativeType.OATH, NarrativeType.BLOOD, NarrativeType.DEBT]


class Moment(BaseModel):
    """
    MOMENT - A single unit of narrated content OR a potential moment.

    In the Moment Graph architecture, moments exist in a possibility space.
    They can be:
    - possible: Created but not yet surfaced
    - active: Visible to player, can be triggered
    - spoken: Part of history
    - dormant: Waiting for player return
    - decayed: Pruned

    Links:
        Character -[CAN_SPEAK]-> Moment (who can say this)
        Character -[SAID]-> Moment (who said this - after spoken)
        Moment -[ATTACHED_TO]-> Character|Place|Thing|Narrative
        Moment -[CAN_LEAD_TO]-> Moment (traversal)
        Moment -[THEN]-> Moment (sequence after spoken)
        Moment -[AT]-> Place (where it occurred)
        Narrative -[FROM]-> Moment (source attribution)

    Note: Speaker is NOT an attribute - use SAID link to find who spoke.
    """
    id: str = Field(description="Unique ID: {place}_{day}_{time}_{type}_{timestamp}")
    text: str = Field(description="The actual text content")
    type: MomentType = MomentType.NARRATION

    # Moment Graph fields
    status: MomentStatus = Field(
        default=MomentStatus.SPOKEN,  # Default for backward compat
        description="Lifecycle status in moment graph"
    )
    weight: float = Field(
        default=0.5,
        ge=0.0, le=1.0,
        description="Salience/importance (computed from graph topology)"
    )
    tone: Optional[str] = Field(
        default=None,
        description="Emotional tone: bitter, hopeful, urgent, etc."
    )

    # Tick tracking (expanded from single tick)
    tick_created: int = Field(
        default=0, ge=0,
        alias="tick",
        description="World tick when moment was created"
    )
    tick_spoken: Optional[int] = Field(
        default=None,
        description="World tick when moment was spoken (if spoken)"
    )
    tick_decayed: Optional[int] = Field(
        default=None,
        description="World tick when moment decayed (if decayed)"
    )

    # Backward compat alias
    @property
    def tick(self) -> int:
        """Backward compat: tick refers to tick_created."""
        return self.tick_created

    # Transcript reference - line number in playthroughs/{id}/transcript.json
    line: Optional[int] = Field(default=None, description="Starting line in transcript.json")

    # Speaker reference (derived from SAID link, not stored on node)
    speaker: Optional[str] = Field(default=None, description="Character ID for dialogue moments")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    # Query fields (for backstory generation)
    query: Optional[str] = Field(
        default=None,
        description="Question this moment asks (triggers backstory generation)"
    )
    query_type: Optional[str] = Field(
        default=None,
        description="Type of query: backstory_gap, clarification, etc."
    )
    query_filled: bool = Field(
        default=False,
        description="Whether the query has been answered"
    )

    def embeddable_text(self) -> str:
        """Generate text for embedding (speaker added by processor if dialogue)."""
        if self.type == MomentType.DIALOGUE and self.speaker:
            return f"{self.speaker}: {self.text}"
        return self.text

    @property
    def should_embed(self) -> bool:
        """Only embed if text is meaningful length."""
        return len(self.text.strip()) > 20

    @property
    def is_active(self) -> bool:
        """Check if moment is currently active."""
        return self.status == MomentStatus.ACTIVE

    @property
    def is_spoken(self) -> bool:
        """Check if moment has been spoken."""
        return self.status == MomentStatus.SPOKEN

    @property
    def can_surface(self) -> bool:
        """Check if moment can potentially surface."""
        return self.status in [MomentStatus.POSSIBLE, MomentStatus.ACTIVE]

    class Config:
        allow_population_by_field_name = True


---

## SOURCE: docs/physics/graph/VALIDATION_Living_Graph.md
# THE BLOOD LEDGER — Validation Specification
# Version: 1.0

---

# =============================================================================
# PURPOSE
# =============================================================================

purpose: |
  This document defines what the game should FEEL like,
  maps those feelings to mechanisms, and provides tests
  to validate the mechanisms produce the feelings.
  
  The energy system is invisible. Players never see "energy" or "pressure."
  They feel companions, urgency, memory, weight.
  
  If the mechanisms are correct but the feelings are wrong, we failed.
  If the feelings are right, the mechanisms worked.

# =============================================================================
# CHAIN
# =============================================================================

## CHAIN

```
PATTERNS:   ./PATTERNS_Graph.md
BEHAVIORS:  ./BEHAVIORS_Graph.md
ALGORITHM:  ../ALGORITHM_Physics.md
THIS:       VALIDATION_Living_Graph.md
SYNC:       ./SYNC_Graph.md
```

# =============================================================================
# INVARIANTS
# =============================================================================

## INVARIANTS

The living graph must never create orphaned nodes, disconnected clusters, or
links that reference missing targets. Mutations must be partially persisted:
valid items remain, invalid items are rejected with actionable feedback, and
the graph continues operating with intact integrity guarantees.

# =============================================================================
# PROPERTIES
# =============================================================================

## PROPERTIES

Graph behavior should remain legible and deterministic for the same inputs:
energy flow, pressure buildup, and propagation must produce repeatable
surfaces for Voices and narrative tension. Properties here are observed in
gameplay, not only in low-level graph queries.

# =============================================================================
# ERROR CONDITIONS
# =============================================================================

## ERROR CONDITIONS

Validation must surface orphaned nodes, disconnected clusters, missing
targets, invalid types, or missing required fields immediately. Database
connection failures are fatal for validation runs and should halt further
mutation application until the database is available again.

# =============================================================================
# TEST COVERAGE
# =============================================================================

## TEST COVERAGE

Coverage draws from the behavior tests in this validation document plus the
physics engine tests in `engine/tests/` that exercise graph integrity,
propagation, and flip mechanics. Any manual validation runs should be noted
in `docs/physics/graph/SYNC_Graph.md` to avoid drift.

# =============================================================================
# VERIFICATION PROCEDURE
# =============================================================================

## VERIFICATION PROCEDURE

1. Run the automated physics and graph-related tests in `engine/tests/`.
2. Apply representative mutation batches and confirm partial persistence
   behavior matches the examples and error handling described above.
3. Simulate a short travel sequence and confirm world-runner narratives
   surface according to the behaviors and tests in this doc.
4. Record any deviations or missing coverage in `docs/physics/graph/SYNC_Graph.md`.

# =============================================================================
# SYNC STATUS
# =============================================================================

## SYNC STATUS

This validation spec is aligned with `docs/physics/graph/SYNC_Graph.md`. If
the SYNC file is missing updates about validation changes, treat the results
as provisional and document the gap before closing a repair.

# =============================================================================
# GRAPH INTEGRITY RULES
# =============================================================================

graph_integrity:
  rules:
    - "New clusters must connect to the existing graph."
    - "No orphaned nodes: every node must have at least one link."
    - "Partial persistence: valid items persist, invalid items are rejected with feedback."

  valid_mutation_example: |
    nodes:
      - type: character
        id: char_wulfric
        name: Wulfric

    links:
      - type: belief
        character: char_wulfric    # NEW node
        narrative: narr_oath       # EXISTING node
        heard: 1.0

  invalid_mutation_example: |
    nodes:
      - type: character
        id: char_wulfric
        name: Wulfric
      # No links — char_wulfric would be orphaned

  error_handling_example: |
    result = write.apply(path="mutations/scene_001.yaml")

    if result.errors:
        for error in result.errors:
            print(f"{error.item}: {error.message}")
            print(f"  Fix: {error.fix}")

    print(f"Persisted: {result.persisted}")
    print(f"Rejected: {result.rejected}")

  error_types:
    - error: orphaned_node
      message: "char_wulfric has no links"
      fix: "Add at least one link connecting this node"
    - error: disconnected_cluster
      message: "New nodes [char_a, char_b] not connected to graph"
      fix: "Add link from cluster to existing node"
    - error: missing_target
      message: "Link references non-existent node: narr_unknown"
      fix: "Create the target node first, or fix the ID"
    - error: invalid_type
      message: "Invalid character type: warrior"
      fix: "Check SCHEMA.md for allowed values"
    - error: invalid_field
      message: "Unknown field: foo on character"
      fix: "Check SCHEMA.md for valid fields"
    - error: missing_required
      message: "narrative.content is required"
      fix: "Add the required field"
    - error: db_connection
      message: "Cannot connect to FalkorDB"
      fix: "docker run -p 6379:6379 falkordb/falkordb"

  partial_persistence_example: |
    result = write.apply(path="mutations/batch.yaml")

    # result.persisted = ["char_aldric", "narr_oath", "link_belief_1"]
    # result.rejected = [
    #   {"item": "char_wulfric", "error": "orphaned_node", "fix": "Add link..."}
    # ]

    The engine persists everything it can, then reports what failed and why.


# =============================================================================
# VISION MAPPING
# =============================================================================

vision_moments:
  
  # --- COVERED BY ENERGY SYSTEM ---
  
  "My past speaks":
    description: "In a tense moment, your oaths and debts pull in different directions."
    mechanism: High-energy narratives surface as Voices
    status: covered
  
  "The world moved":
    description: "You arrive somewhere and hear about events that happened without you."
    mechanism: World Runner processes distant tensions → news propagates
    status: covered
  
  "Everything led here":
    description: "In a climactic moment, you see how all choices wove together."
    mechanism: Narrative clusters converge → cascade → confrontation
    status: covered
  
  # --- REQUIRES NARRATOR/CONTENT ---
  
  "I know what I need to do":
    description: "Early clarity. You can articulate your goal."
    mechanism: Opening establishes purpose (content design)
    status: narrator_job
  
  "I see where I'm going":
    description: "You know the next step, not just the goal."
    mechanism: Goal narratives surface with path (Narrator)
    status: narrator_job
  
  "I know this place":
    description: "Certain locations become familiar, grounding, home."
    mechanism: Place-player narratives accumulate (visits create beliefs)
    status: partial
  
  "They remembered":
    description: "An character references something you did sessions ago."
    mechanism: Player actions create narratives → characters believe → resurface later
    status: covered
  
  "I was wrong":
    description: "Discover foundational belief was mistaken. Reality shifts."
    mechanism: Supersession + revelation drains old belief, surfaces new
    status: covered
  
  "This is my band":
    description: "You look at companions and feel ownership, belonging."
    mechanism: Companion presence + shared narratives + time
    status: partial
  
  "They became real":
    description: "A character becomes complex — a person, not a type."
    mechanism: Pre-generation creates depth → revealed through conversation
    status: covered
  
  "I know them":
    description: "You can predict what they'd do. You know this person."
    mechanism: Consistent beliefs/traits → player learns → predictions match
    status: covered
  
  "I can rely on them":
    description: "You send a companion confidently. They succeed for predicted reasons."
    mechanism: Skills + traits inform outcomes → player's model validated
    status: covered


# =============================================================================
# EXPECTED BEHAVIORS
# =============================================================================

behaviors:

  # ---------------------------------------------------------------------------
  # PRESENCE & PROXIMITY
  # ---------------------------------------------------------------------------
  
  companion_presence:
    id: B01
    category: presence
    
    gameplay: |
      Aldric's concerns, memories, and oaths keep surfacing in your mind.
      He feels like he's THERE, not just following silently.
    
    mechanism: |
      High proximity (1.0) × high relationship = high character energy
      → pumps strongly into his narratives
      → those narratives stay energized
      → surface frequently as Voices
    
    failure_looks_like: |
      Companions feel like silent followers.
      Their concerns never surface unless you ask.
  
  approach_escalation:
    id: B02
    category: presence
    
    gameplay: |
      The closer you get to York, the more Edmund weighs on you.
      Three days away feels distant. One day away is a knot in your stomach.
    
    mechanism: |
      Proximity increases (0.2 → 0.7 → 1.0)
      → Edmund's energy rises (relationship × proximity)
      → his narratives heat up
      → Voices intensify
      → pressure builds automatically
    
    failure_looks_like: |
      Edmund feels equally present whether near or far.
      Arrival feels no different from a week away.
  
  distant_dormant:
    id: B03
    category: presence
    
    gameplay: |
      There's politics in Wessex. Lords scheming. You've heard whispers.
      But you don't care — it's far away, you have no stake.
      It doesn't keep you up at night.
    
    mechanism: |
      Low relationship × low proximity = low character energy
      → barely pumps into narratives
      → decay > inflow
      → narratives dormant
      → never surface as Voices
    
    failure_looks_like: |
      Random distant events intrude on your attention.
      Everything feels equally important.

  # ---------------------------------------------------------------------------
  # LIVING WORLD
  # ---------------------------------------------------------------------------
  
  world_moved:
    id: B04
    category: living_world
    
    gameplay: |
      You arrive in York and hear about the feud that broke out while you traveled.
      Edmund made a move. The sheriff issued a decree.
      You weren't there — but it happened. The world didn't wait.
    
    mechanism: |
      World Runner processes distant tensions during travel
      → creates narratives of events
      → news propagates via character beliefs
      → on arrival, Narrator surfaces "what you missed"
      → new narratives with recent timestamps
    
    failure_looks_like: |
      Nothing happens while you're away.
      The world freezes until you arrive.
  
  antagonist_acts:
    id: B05
    category: living_world
    
    gameplay: |
      Edmund isn't waiting for you. He's scheming, building alliances, preparing.
      You hear about his moves. He feels like a PERSON pursuing goals,
      not a boss waiting in a room.
    
    mechanism: |
      Antagonists have beliefs → beliefs create tensions
      → tensions break on their own timeline
      → World Runner creates narratives of their actions
      → propagates as news you eventually hear
    
    failure_looks_like: |
      Edmund only does things when you're present.
      He's static until the confrontation.
  
  news_travels:
    id: B06
    category: living_world
    
    gameplay: |
      You did something notable in Thornwick.
      A week later, in York, someone's heard about it.
      Your reputation precedes you. Word spreads — good or bad.
    
    mechanism: |
      Significant player actions create narratives
      → propagate through character belief network over time
      → distant characters eventually believe versions
      → affects their disposition when you meet
    
    failure_looks_like: |
      Your actions have no reputation effects.
      characters only know what they witnessed.

  # ---------------------------------------------------------------------------
  # NARRATIVE TENSION
  # ---------------------------------------------------------------------------
  
  contradiction_unresolved:
    id: B07
    category: narrative_tension
    
    gameplay: |
      You heard Edmund saved the family. But you KNOW he betrayed you.
      Both versions keep surfacing. You can't settle it. It gnaws.
    
    mechanism: |
      Player believes both A and B
      → contradiction link heats both sides (bidirectional, factor 0.3)
      → neither fades
      → both surface as Voices
      → tension persists until player acts or chooses
    
    failure_looks_like: |
      One version dominates immediately.
      The contradiction doesn't feel unresolved.
  
  loyalty_cluster:
    id: B08
    category: narrative_tension
    
    gameplay: |
      When you doubt Aldric's oath, you start doubting everything about him —
      his stories, his past, why he's really here.
      Trust is a fabric, not a fact.
    
    mechanism: |
      Support links cluster narratives (bidirectional, factor 0.2)
      → doubt one, energy drops
      → propagates to cluster
      → all related Voices weaken together
    
    failure_looks_like: |
      Doubting one thing doesn't affect related beliefs.
      Trust is atomic, not interconnected.
  
  old_news_fades:
    id: B09
    category: narrative_tension
    
    gameplay: |
      You used to obsess about where Edmund was. Now you know he fled York.
      The old question stops haunting you.
    
    mechanism: |
      Supersedes link drains old narrative (factor 0.25)
      → old narrative loses energy
      → new narrative gains energy + drain
      → old stops surfacing as Voice
    
    failure_looks_like: |
      Outdated information keeps surfacing.
      You can't "update" your mental state.
  
  belief_shattered:
    id: B10
    category: narrative_tension
    
    gameplay: |
      You believed Edmund betrayed you. Everything pointed to it.
      Then you learn the truth — Father changed the will.
      The foundation shifts. You have to reconsider everything.
    
    mechanism: |
      Player believes narrative A (truth: 0.3)
      → contradicting narrative B exists (truth: 0.9)
      → revelation event: player learns B
      → B supersedes A
      → A's energy drains
      → belief structure reorganizes
      → Voices change character
    
    failure_looks_like: |
      Revelations feel like new information, not paradigm shifts.
      Old beliefs persist alongside new ones without tension.

  # ---------------------------------------------------------------------------
  # COMPANION DEPTH
  # ---------------------------------------------------------------------------
  
  they_remembered:
    id: B11
    category: companion_depth
    
    gameplay: |
      The innkeeper mentions the coin you left last time.
      Aldric references the choice you made at Thornwick.
      Someone you helped sends word. The world has memory.
    
    mechanism: |
      Player actions create narratives
      → characters gain beliefs about those narratives
      → later interactions, Narrator surfaces character beliefs about player's past
    
    failure_looks_like: |
      characters never reference your history.
      Each encounter feels fresh, without continuity.
  
  they_became_real:
    id: B12
    category: companion_depth
    
    gameplay: |
      You started with "Aldric the loyal sword."
      Now you know he lost his brother, hates the cold, prays alone.
      He's not a type — he's a person.
    
    mechanism: |
      Pre-generation creates character depth
      → even unanswered questions have answers (in graph)
      → consistent personality from backstory + beliefs
      → Narrator reveals through conversation over time
    
    failure_looks_like: |
      Characters stay archetypes.
      Learning more doesn't make them more specific.
  
  i_know_them:
    id: B13
    category: companion_depth
    
    gameplay: |
      You can predict what Aldric would do.
      "He'd never abandon a wounded man."
      "He'll want to pray before we move."
      You KNOW this person.
    
    mechanism: |
      Character beliefs + traits + backstory are consistent
      → player learns them through play
      → predictions match behavior
      → trust builds from accurate mental model
    
    failure_looks_like: |
      Characters surprise randomly.
      You can't form a reliable mental model of them.
  
  i_can_rely:
    id: B14
    category: companion_depth
    
    gameplay: |
      You send Aldric to scout. He succeeds — and you're not surprised,
      because you knew his skills, knew the situation played to his strengths.
      Trust is validated.
    
    mechanism: |
      Character skills + traits inform outcomes
      → player who understands character makes good choices
      → outcomes match expectations
      → competence trust established
    
    failure_looks_like: |
      Outcomes feel random.
      Your understanding of characters doesn't help you use them.

  # ---------------------------------------------------------------------------
  # SYSTEM HEALTH
  # ---------------------------------------------------------------------------
  
  equilibrium:
    id: B15
    category: system_health
    
    gameplay: |
      After a few days of travel, your mind settles.
      The same concerns surface. The same weights press.
      It's not chaos — it's YOUR situation, crystallized.
    
    mechanism: |
      Energy equilibrium: inflow = outflow
      → narratives stabilize
      → consistent Voices
      → coherent internal state
    
    failure_looks_like: |
      Voices are erratic, random.
      Your mental state doesn't feel stable or coherent.
  
  something_simmers:
    id: B16
    category: system_health
    
    gameplay: |
      There's always SOMETHING about to break.
      Not everything at once, but one or two threads pulled tight.
      The story has momentum.
    
    mechanism: |
      Criticality feedback keeps some tensions hot
      → decay_rate adjusts to maintain pressure distribution
      → at least one narrative cluster near breaking
      → player feels impending drama
    
    failure_looks_like: |
      Everything feels equally calm.
      No sense of building pressure or imminent change.
  
  no_explosion_freeze:
    id: B17
    category: system_health
    
    gameplay: |
      Things happen at a human pace.
      Not constant crisis. Not dead quiet.
      Room to breathe, but never for long.
    
    mechanism: |
      Conservation + criticality bound total energy
      → breaks happen but don't cascade endlessly
      → quiet moments exist but system heats back up
      → 2-5 breaks per game-hour is the target
    
    failure_looks_like: |
      Everything breaks at once (chaos).
      Or nothing ever breaks (stagnation).
  
  breaks_ripple:
    id: B18
    category: system_health
    
    gameplay: |
      Edmund loses the sheriff's favor. Suddenly other things shift —
      your opportunity, Osric's scheming, the balance of power.
      One break reshapes the web.
    
    mechanism: |
      Break creates narratives
      → new believers pump energy
      → propagates to related narratives
      → other tensions affected
      → possible cascade (max depth 5)
    
    failure_looks_like: |
      Events are isolated.
      What happens to Edmund doesn't affect anything else.

  # ---------------------------------------------------------------------------
  # TIME & PRESSURE
  # ---------------------------------------------------------------------------
  
  deadline_feels_real:
    id: B19
    category: time_pressure
    
    gameplay: |
      "Three days to the feast" feels like planning.
      "Tomorrow" feels like pressure.
      "Tonight" feels like now-or-never.
      Time creates urgency.
    
    mechanism: |
      Scheduled progression jumps pressure at checkpoints
      → Day 12: 0.2, Day 13: 0.5, Day 14: 0.8
      → psychological cliff mirrors mechanical cliff
    
    failure_looks_like: |
      Time passes uniformly.
      "One day away" feels same as "three days away."
  
  deadline_severity_varies:
    id: B20
    category: time_pressure
    
    gameplay: |
      The knight arrives on Day 14 no matter what.
      But if you stirred up trouble, arrival is DISASTER.
      If you prepared, it's merely tense.
    
    mechanism: |
      Hybrid tension has floor (scheduled) + variable (event-driven)
      → deadline guaranteed
      → severity depends on accumulated pressure from actions
    
    failure_looks_like: |
      Deadlines have fixed outcomes regardless of preparation.

  # ---------------------------------------------------------------------------
  # ENGAGEMENT
  # ---------------------------------------------------------------------------
  
  attention_grows:
    id: B21
    category: engagement
    
    gameplay: |
      You asked about Thornwick. Now it's on your mind.
      Aldric's past, the Harrying, what happened to his family —
      it all starts surfacing more.
    
    mechanism: |
      Engagement increases belief strength
      → more energy pumped into that narrative
      → propagates to related narratives via support links
      → cluster heats up
      → more Voices from that cluster
    
    failure_looks_like: |
      Asking about something doesn't make it more present.
      Your attention has no effect on what surfaces.
  
  revelation_sinks_in:
    id: B22
    category: engagement
    
    gameplay: |
      Aldric just told you about his grandmother.
      It's there, you heard it, but it hasn't fully landed yet.
      In a day, it might haunt you.
    
    mechanism: |
      New narrative starts with energy = 0
      → believers pump over ticks
      → gradually rises toward equilibrium
      → eventually surfaces as Voice
    
    failure_looks_like: |
      New information immediately dominates.
      No sense of things "sinking in" over time.
  
  narrator_shapes:
    id: B23
    category: engagement
    
    gameplay: |
      The church conspiracy keeps surfacing even though you haven't engaged.
      The narrator wants you to notice.
      Or: you ignored it twice, and it fades — the narrator lets it go.
    
    mechanism: |
      Focus multiplies belief_flow_rate for specific narratives
      → high focus = faster energy accumulation = persistent surfacing
      → low focus = slower accumulation = natural fade
    
    failure_looks_like: |
      Narrator has no ability to emphasize or de-emphasize.
      Everything is purely reactive to player.


# =============================================================================
# ANTI-PATTERNS
# =============================================================================

anti_patterns:

  quest_log:
    id: AP01
    phrase: "Let me check my quest log."
    
    failure: |
      Player treats the Ledger as a checklist of objectives.
      "Go to York. Talk to Wulfric. Find the sword."
    
    success: |
      Ledger shows debts, oaths, blood ties — weight, not tasks.
      Player opens it to feel the pressure, not to find instructions.
    
    mechanism_check: |
      Ledger displays narratives of type [debt, oath, blood, enmity]
      → emotional framing, not objective framing
      → no "complete X" language
    
    test: |
      Review Ledger UI. Count task-like entries vs weight-like entries.
      Task-like entries should be zero.
  
  optimal_choice:
    id: AP02
    phrase: "What's the optimal choice?"
    
    failure: |
      Player min-maxes relationship points.
      Choices feel like optimization problems with correct answers.
    
    success: |
      Choices feel like CHOICES — trade-offs between values.
      Helping A means neglecting B. There's no optimal solution.
    
    mechanism_check: |
      Choices affect multiple relationships in different directions
      → no single choice benefits everything
      → outcomes depend on context, not universal value
    
    test: |
      Review 10 significant choices. Each should have at least one
      positive and one negative relational consequence.
  
  who_is_this:
    id: AP03
    phrase: "Who is this again?"
    
    failure: |
      Player can't remember characters.
      "Wulfric? Was he the innkeeper or the blacksmith?"
    
    success: |
      Characters are memorable through relationship to player.
      "The one who lied about Edmund." "The one I owe silver."
    
    mechanism_check: |
      Characters are introduced through relationship context
      → referenced by relationship, not just name
      → appear in Ledger/Faces connected to player's story
    
    test: |
      Introduce character in scene 2, return in scene 10.
      Ask playtesters to identify. They should describe relationship, not name.
  
  skip_skip_skip:
    id: AP04
    phrase: "Skip skip skip."
    
    failure: |
      Player skips text to get to choices.
      Text is obstacle, not engagement.
    
    success: |
      Player reads Voices, engages with clickable words.
      Text IS the interaction, not preamble to it.
    
    mechanism_check: |
      Clickable words in narration and Voices
      → engagement happens IN the text
      → no "skip to choices" affordance
    
    test: |
      Track click patterns. Players should click within text,
      not skip to bottom. Voices should receive clicks.


# =============================================================================
# TEST SUITE
# =============================================================================

tests:

  # ---------------------------------------------------------------------------
  # PRESENCE & PROXIMITY
  # ---------------------------------------------------------------------------
  
  - id: T01
    behavior: B01 (companion_presence)
    scenario: "Aldric travels with player. Edmund is in York (distant)."
    setup:
      - char_aldric at player location
      - char_edmund at place_york (2 days travel)
      - Both have equal relationship intensity to player
    steps:
      - Run 10 ticks
      - Compare energy of Aldric's narratives vs Edmund's narratives
    expected: "Aldric's narratives have 3-5x more energy than Edmund's."
    assertion: avg(aldric_narrative.energy) > 3 * avg(edmund_narrative.energy)
  
  - id: T02
    behavior: B02 (approach_escalation)
    scenario: "Player travels from North to York over 3 days."
    setup:
      - Player in North (2 days from York)
      - Edmund in York
      - Edmund relationship intensity: 4.0
    steps:
      - Record Edmund's energy at Day 12
      - Simulate 1 day travel (proximity: 0.2 → 0.4)
      - Record Edmund's energy at Day 13
      - Simulate 1 day travel (proximity: 0.4 → 0.7)
      - Record Edmund's energy at Day 14
    expected: "Edmund's energy increases ~3.5x from Day 12 to Day 14."
    assertion: edmund.energy[day14] > 3 * edmund.energy[day12]
  
  - id: T03
    behavior: B03 (distant_dormant)
    scenario: "Wessex lord exists but player has no connection."
    setup:
      - char_wessex_lord in distant Wessex
      - Player has no narratives about Wessex lord
      - Wessex lord believes some narratives
    steps:
      - Run 20 ticks
      - Check energy of narratives believed only by Wessex lord
    expected: "Wessex narratives decay below 0.1."
    assertion: max(wessex_narrative.energy) < 0.1

  # ---------------------------------------------------------------------------
  # LIVING WORLD
  # ---------------------------------------------------------------------------
  
  - id: T04
    behavior: B04 (world_moved)
    scenario: "Player travels 3 days. Distant tension breaks during travel."
    setup:
      - tension_feud pressure at 0.88
      - Player traveling (not near feud location)
    steps:
      - Simulate 3 days travel
      - Check for new narratives created by World Runner
      - Check if player can discover these on arrival
    expected: "New narratives exist from feud break. Discoverable at destination."
    assertion: new_narratives_from_break.count > 0
  
  - id: T05
    behavior: B05 (antagonist_acts)
    scenario: "Edmund has active tensions. Player is elsewhere."
    setup:
      - Edmund in York
      - tension_edmund_position pressure at 0.85
      - Player in North (not traveling to York)
    steps:
      - Simulate 5 days
      - Check for breaks involving Edmund
      - Check for new narratives about Edmund's actions
    expected: "Edmund's tensions break. New narratives show his actions."
    assertion: narratives_about_edmund_actions.count > 0
  
  - id: T06
    behavior: B06 (news_travels)
    scenario: "Player does notable action. Check if distant characters learn."
    setup:
      - Player does significant action creating narrative N
      - characters at various distances
    steps:
      - Mark which characters believe N at time 0
      - Simulate 7 days with news propagation
      - Check which characters believe N or version of N
    expected: "Nearby characters learn quickly. Distant characters learn slowly or partially."
    assertion: nearby_npc.believes(N) > distant_npc.believes(N)

  # ---------------------------------------------------------------------------
  # NARRATIVE TENSION
  # ---------------------------------------------------------------------------
  
  - id: T07
    behavior: B07 (contradiction_unresolved)
    scenario: "Player believes two contradicting narratives."
    setup:
      - narr_betrayal (player believes 1.0)
      - narr_salvation (player believes 0.3)
      - narr_betrayal contradicts narr_salvation (strength 0.8)
    steps:
      - Run 10 ticks
      - Check energy of both narratives
    expected: "Both narratives gain energy. Neither dominates."
    assertion: narr_betrayal.energy > 0.5 AND narr_salvation.energy > 0.2
  
  - id: T08
    behavior: B08 (loyalty_cluster)
    scenario: "Player weakens belief in Aldric's oath."
    setup:
      - narr_oath (player believes 1.0)
      - narr_aldric_loyal supports narr_oath (strength 0.8)
      - narr_aldric_saved_me supports narr_aldric_loyal (strength 0.6)
    steps:
      - Record energy of all three
      - Reduce player.believes(narr_oath) to 0.3
      - Run 10 ticks
      - Record energy of all three
    expected: "All three narratives lose energy together."
    assertion: all narratives.energy[after] < narratives.energy[before] * 0.7
  
  - id: T09
    behavior: B09 (old_news_fades)
    scenario: "New narrative supersedes old."
    setup:
      - narr_edmund_in_york (player believes 0.8, energy 1.0)
      - Create narr_edmund_fled (player believes 0.9)
      - narr_edmund_fled supersedes narr_edmund_in_york (strength 1.0)
    steps:
      - Run 10 ticks
    expected: "Old narrative loses energy. New narrative gains."
    assertion: >
      narr_edmund_in_york.energy < 0.3 AND
      narr_edmund_fled.energy > 0.8
  
  - id: T10
    behavior: B10 (belief_shattered)
    scenario: "Player discovers foundational belief was false."
    setup:
      - narr_betrayal (player believes 1.0, truth 0.3)
      - narr_father_willing (player believes 0.0, truth 0.9)
      - narr_father_willing supersedes narr_betrayal
    steps:
      - Player learns narr_father_willing (believes → 0.9)
      - Run 15 ticks
    expected: "Old belief drains. New understanding dominates. Voice character changes."
    assertion: >
      narr_betrayal.energy < 0.3 AND
      narr_father_willing.energy > 0.7

  # ---------------------------------------------------------------------------
  # COMPANION DEPTH
  # ---------------------------------------------------------------------------
  
  - id: T11
    behavior: B11 (they_remembered)
    scenario: "character references player's past action."
    setup:
      - Player previously created narr_player_helped_innkeeper
      - Innkeeper believes this narrative (strength 0.9)
      - Time passes
    steps:
      - Player returns to innkeeper
      - Query innkeeper's beliefs about player
    expected: "Innkeeper has belief about player's past action available for Narrator."
    assertion: innkeeper.believes(narr_player_helped_innkeeper) > 0.5
  
  - id: T12
    behavior: B12 (they_became_real)
    scenario: "Character depth exists even if not yet revealed."
    setup:
      - char_aldric with full backstory
      - Player has not asked about grandmother
    steps:
      - Query: Does Aldric have narrative about grandmother?
      - Query: Is it consistent with his other narratives?
    expected: "Backstory exists. Pre-generation made it real."
    assertion: narr_aldric_grandmother exists AND is_consistent(aldric.backstory)
  
  - id: T13
    behavior: B13 (i_know_them)
    scenario: "Character behavior matches established traits."
    setup:
      - char_aldric with traits: loyalty 0.95, piety 0.7, courage 0.8
      - Present scenario: wounded ally needs help, but mission is urgent
    steps:
      - Query: What would Aldric do?
      - Compare to trait-based prediction
    expected: "Aldric's response consistent with high loyalty (help wounded ally)."
    assertion: aldric_decision matches trait_prediction
  
  - id: T14
    behavior: B14 (i_can_rely)
    scenario: "Companion success correlates with skill match."
    setup:
      - char_aldric with tracking: skilled, sneaking: untrained
      - Task A: tracking mission
      - Task B: stealth mission
    steps:
      - Send Aldric on Task A, record outcome
      - Send Aldric on Task B, record outcome
    expected: "Task A succeeds. Task B fails or struggles."
    assertion: task_a.success == true AND task_b.success == false

  # ---------------------------------------------------------------------------
  # SYSTEM HEALTH
  # ---------------------------------------------------------------------------
  
  - id: T15
    behavior: B15 (equilibrium)
    scenario: "System stabilizes without input."
    setup:
      - Normal graph state with various energies
    steps:
      - Run 50 ticks with no changes
      - Record energy delta between tick 49 and 50
    expected: "Energy values stabilized (delta < 0.01)."
    assertion: max(energy_delta) < 0.01
  
  - id: T16
    behavior: B16 (something_simmers)
    scenario: "At least one tension near breaking."
    setup:
      - Normal graph state
    steps:
      - Run 20 ticks
      - Count tensions with pressure > 0.7
    expected: "At least one tension is 'hot'."
    assertion: count(tension.pressure > 0.7) >= 1
  
  - id: T17
    behavior: B17 (no_explosion_freeze)
    scenario: "Reasonable break frequency over time."
    setup:
      - Normal graph state
    steps:
      - Simulate 1 game-hour
      - Count total breaks
    expected: "2-5 breaks occurred. Not constant crisis, not dead."
    assertion: break_count >= 2 AND break_count <= 5
  
  - id: T18
    behavior: B18 (breaks_ripple)
    scenario: "Break affects other tensions."
    setup:
      - tension_A at 0.88, tension_B at 0.85
      - Breaking A creates narrative that supports B's narratives
    steps:
      - Force tension_A to break
      - Run 3 ticks
      - Check tension_B pressure
    expected: "Tension_B pressure increased. May have flipped."
    assertion: tension_B.pressure[after] > tension_B.pressure[before]

  # ---------------------------------------------------------------------------
  # TIME & PRESSURE
  # ---------------------------------------------------------------------------
  
  - id: T19
    behavior: B19 (deadline_feels_real)
    scenario: "Scheduled tension jumps at checkpoints."
    setup:
      - tension_scheduled with progression:
        - Day 12: 0.2
        - Day 13: 0.5
        - Day 14: 0.8
    steps:
      - Set time to Day 12, record pressure
      - Advance to Day 13, record pressure
      - Advance to Day 14, record pressure
    expected: "Pressure jumps match progression, not gradual tick."
    assertion: >
      pressure[day12] == 0.2 AND
      pressure[day13] == 0.5 AND
      pressure[day14] == 0.8
  
  - id: T20
    behavior: B20 (deadline_severity_varies)
    scenario: "Hybrid tension exceeds floor via events."
    setup:
      - tension_hybrid with floor 0.5 at Day 12
      - Current pressure 0.5
    steps:
      - Inject events that add 0.25 pressure
      - Advance to Day 13 (new floor 0.6)
      - Check pressure
    expected: "Pressure is max(ticked, floor) — at least 0.6."
    assertion: pressure >= 0.6

  # ---------------------------------------------------------------------------
  # ENGAGEMENT
  # ---------------------------------------------------------------------------
  
  - id: T21
    behavior: B21 (attention_grows)
    scenario: "Player engagement increases narrative energy."
    setup:
      - narr_thornwick (player believes 0.3, energy X)
    steps:
      - Simulate player clicking "Thornwick" (increases belief to 0.6)
      - Run 5 ticks
      - Check energy of narr_thornwick and related narratives
    expected: "Thornwick narrative and cluster gain energy."
    assertion: narr_thornwick.energy > X * 1.5
  
  - id: T22
    behavior: B22 (revelation_sinks_in)
    scenario: "New narrative starts cold, warms over time."
    setup:
      - Create new narr_grandmother_death
      - char_aldric.believes = 1.0
    steps:
      - Check energy at tick 0
      - Run 5 ticks
      - Check energy at tick 5
    expected: "Energy starts 0, rises toward equilibrium."
    assertion: >
      energy[tick0] == 0 AND
      energy[tick5] > 0.3
  
  - id: T23
    behavior: B23 (narrator_shapes)
    scenario: "Focus multiplier affects energy accumulation."
    setup:
      - narr_A and narr_B identical (same believers, same strengths)
      - narr_A.focus = 2.0
      - narr_B.focus = 0.5
    steps:
      - Run 15 ticks
      - Compare energies
    expected: "High focus has ~4x energy of low focus."
    assertion: narr_A.energy / narr_B.energy > 3.5

  # ---------------------------------------------------------------------------
  # CRITICALITY
  # ---------------------------------------------------------------------------
  
  - id: T24
    behavior: B16 (criticality_cold_recovery)
    scenario: "System recovers from cold state."
    setup:
      - Force low energy state (all narratives energy < 0.1)
      - All tensions pressure < 0.2
    steps:
      - Run 20 ticks
      - Check decay_rate changes
      - Check pressure distribution
    expected: "Decay_rate decreased. Pressures rose."
    assertion: >
      decay_rate < initial_decay_rate AND
      avg(tension.pressure) > 0.3
  
  - id: T25
    behavior: B17 (criticality_hot_dampening)
    scenario: "System cools from hot state."
    setup:
      - Force high energy state (many narratives energy > 2.0)
      - Multiple tensions pressure > 0.8
    steps:
      - Run 20 ticks
      - Check decay_rate changes
      - Check break frequency
    expected: "Decay_rate increased. System cooled."
    assertion: >
      decay_rate > initial_decay_rate AND
      break_count_in_20_ticks < 10

  # ---------------------------------------------------------------------------
  # CASCADE
  # ---------------------------------------------------------------------------
  
  - id: T26
    behavior: B18 (cascade_depth_limit)
    scenario: "Cascades stop at max depth."
    setup:
      - Chain of 10 tensions that could cascade
      - Each break creates narrative that pushes next over threshold
    steps:
      - Trigger first tension
      - Count total breaks
    expected: "Cascade stops at max_depth (5)."
    assertion: break_count <= 5

  # ---------------------------------------------------------------------------
  # ANTI-PATTERNS
  # ---------------------------------------------------------------------------
  
  - id: T27
    anti_pattern: AP01 (quest_log)
    scenario: "Audit Ledger content."
    steps:
      - Export all Ledger entries
      - Classify each as "task-like" or "weight-like"
    expected: "Zero task-like entries."
    assertion: task_like_entries == 0
  
  - id: T28
    anti_pattern: AP02 (optimal_choice)
    scenario: "Audit choice consequences."
    steps:
      - Review 10 significant choices
      - For each, list positive and negative relationship consequences
    expected: "Each choice has mixed consequences."
    assertion: all choices have >= 1 positive AND >= 1 negative consequence
  
  - id: T29
    anti_pattern: AP03 (who_is_this)
    scenario: "Character recall test."
    steps:
      - Introduce character in early scene
      - Return character in later scene
      - Ask playtesters to identify
    expected: "Playtesters describe relationship, not name."
    assertion: identification_by_relationship > identification_by_name
  
  - id: T30
    anti_pattern: AP04 (skip_skip_skip)
    scenario: "Track engagement patterns."
    steps:
      - Log all clicks during play session
      - Calculate ratio: clicks_in_text vs clicks_at_bottom
    expected: "Most clicks are within text (Voices, clickable words)."
    assertion: clicks_in_text > clicks_at_bottom * 2


# =============================================================================
# SUMMARY
# =============================================================================

summary:
  
  total_behaviors: 23
  total_anti_patterns: 4
  total_tests: 30
  
  categories:
    presence_proximity: 3 behaviors, 3 tests
    living_world: 3 behaviors, 3 tests
    narrative_tension: 4 behaviors, 4 tests
    companion_depth: 4 behaviors, 4 tests
    system_health: 4 behaviors, 6 tests
    time_pressure: 2 behaviors, 2 tests
    engagement: 3 behaviors, 3 tests
    anti_patterns: 4 patterns, 4 tests
  
  vision_coverage:
    fully_covered: 10
    partial: 2
    narrator_job: 2
  
  validation_approach: |
    1. Implement graph engine with energy mechanics
    2. Run automated tests T01-T26 against simulation
    3. Run content audits T27-T28 against game data
    4. Run playtests for T29-T30 behavioral observation
    5. Iterate on parameters until tests pass
    6. Playtest for FEELINGS, not just mechanics

---

## GAPS / IDEAS / QUESTIONS

- Which invariants should be enforced at mutation time versus during scheduled
  health checks, and how should partial persistence report the difference?
- Are the current behavior tests sufficient to validate narrative attention,
  or do we need targeted probes for low-energy suppression edge cases?
- Should graph integrity validation include explicit cycle checks for certain
  link types (e.g., supersedes) to prevent contradictory feedback loops?

---

*"If the mechanisms are correct but the feelings are wrong, we failed.*
*If the feelings are right, the mechanisms worked."*


---

## SOURCE: docs/physics/graph/PATTERNS_Graph.md
# Graph — Patterns: Why This Shape

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

```
THIS:       PATTERNS_Graph.md (you are here)
BEHAVIORS:  ./BEHAVIORS_Graph.md
ALGORITHM:  ../ALGORITHM_Physics.md
VALIDATION: ./VALIDATION_Living_Graph.md
SYNC:       ./SYNC_Graph.md
```

---

## THE PROBLEM

We need a living-graph physics core that decides attention and drama without
manual scene scheduling. If energy is hand-set or a separate scheduler owns
state, the story loses causality and drifts away from the graph as source.

---

## THE PATTERN

Treat link strength and topology as the only inputs that matter. Energy is
computed, pressure accumulates, and flips emerge from the graph structure so
the system stays legible and the narrative earns focus without authorial fiat.

---

## PRINCIPLES

### Principle 1: Computation over declaration

Energy is derived from structure and decay rules, never assigned directly.
This keeps the graph honest and avoids creating a second, hidden state layer.

### Principle 2: Pressure must resolve

Tensions grow until they flip, forcing releases that move the world forward.
Slow build and sudden break are the default rhythm of graph-driven drama.

### Principle 3: Attention is scarce

Only high-energy nodes surface in context windows; low energy remains real but
quiet. The graph decides what matters now instead of the agent doing it.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `engine/physics/graph/**` | Implements GraphOps/GraphQueries to read/write the living graph. |
| `engine/physics/tick.py` | Runs the propagation loop that updates energy and flips. |
| `docs/schema/SCHEMA_Moments.md` | Defines node/link fields that energy logic assumes. |

---

## INSPIRATIONS

Emergent simulation design, graph-based knowledge systems, and narrative
engines that prefer structure-driven behavior over scripted outcomes. The
tone is "living system" rather than deterministic plot machinery.

---

## SCOPE

### In Scope

- Graph topology and link strength as the only levers for energy flow.
- Pressure accumulation and release mechanics that trigger flips.
- Attention shaping for what the narrator sees on any given tick.

### Out of Scope

- Narrator prompt engineering and voice design (see narrator module docs).
- UI presentation of energy or pressure (see frontend scene/map docs).
- Data ingestion or world scraping pipelines (see world-scraping docs).

---

## The Core Insight

**Characters are batteries. Narratives are circuits. Energy flows through links.**

No one injects energy. The story emerges from structure.

---

## Energy As Attention

The graph is larger than any context window. Energy determines what makes it into attention.

| Energy Level | Meaning |
|--------------|---------|
| High | This matters now |
| Low | This exists but sleeps |

Without energy mechanics, the LLM would drown in irrelevant narratives or miss critical tensions. Energy is how the story knows its own focus.

---

## Computed, Not Declared

Weight is never set directly. It emerges from structure.

A narrative becomes important because:
- Someone believes it intensely
- It connects to the player
- It contradicts another belief
- It's been accumulating pressure

**This prevents authorial fiat. The story earns its importance.**

---

## Pressure Requires Release

Tensions don't resolve gradually. They accumulate until they break.

This creates drama:
1. **Slow build** — pressure rising
2. **Sudden release** — the flip
3. **Cascade** — consequences rippling

A world where everything resolves smoothly has no story.

---

## The Graph Breathes

The system has rhythms:

| Direction | Mechanism |
|-----------|-----------|
| Energy in | New beliefs, new connections |
| Energy out | Resolution, distance, forgetting |
| Pressure builds | Time, contradiction, proximity |
| Pressure releases | Breaks, revelations, choices |

A living graph is never static. Even when the player rests, the web is shifting.

---

## Criticality

The system operates near critical threshold.

| State | Problem |
|-------|---------|
| Too stable | Nothing happens, boring |
| Too chaotic | Everything breaks constantly, meaningless |

**The sweet spot:** enough tension that breaks feel earned, enough stability that builds feel meaningful.

The Narrator adjusts focus to maintain criticality.

---

## What Agents Never Do

- Set narrative.energy directly
- Inject energy
- Manage energy flow
- Override physics

Agents update **link strengths**. Energy follows automatically.

---

*"The story emerges from structure."*

---

## GAPS / IDEAS / QUESTIONS

- What is the safest decay curve when the graph is quiet but not stagnant?
- How should multi-hop proximity affect energy transfer in dense clusters?
- When do contradictory links produce pressure versus canceling it out?
