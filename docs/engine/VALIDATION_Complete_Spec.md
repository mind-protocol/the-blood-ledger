# VALIDATION: Complete Spec

This document defines all invariants, properties, and behaviors that must hold for The Blood Ledger.

---

## V1: CORE PRINCIPLES

### V1.1: "The game is a web of narratives under tension"
- Everything in the game state can be expressed as narratives and their relationships
- There is no separate "relationship system" — relationships ARE narratives
- Characters don't have attributes like `trust: 0.65`, they have narrative links

**Test:** Given any game state, all relationship information should be queryable via BELIEVES links to narratives.

### V1.2: Characters Never See Truth
- `narrative.truth` is director-only
- Characters believe narratives, they don't know facts
- The player's beliefs may be wrong

**Test:** No player-facing query should return `truth` field. Character queries should only return belief-weighted information.

### V1.3: Physical State is Ground Truth
- Position (AT), possession (CARRIES), location (LOCATED_AT) are binary facts
- These are NOT narratives — they are physical reality
- Separate from beliefs about ownership/control

**Test:** Ground truth links must have `present/carries/located` values of exactly 0 or 1.

---

## V2: NODE INVARIANTS

### V2.1: Character Invariants

| Property | Constraint | Test |
|----------|------------|------|
| `id` | Required, unique | `test_character_id_required`, `test_character_id_unique` |
| `name` | Required | `test_character_name_required` |
| `type` | Enum: player, companion, major, minor, background | `test_character_type_enum` |
| `alive` | Boolean, default true | `test_character_alive_boolean` |
| `skills.*` | Enum: untrained, capable, skilled, master | `test_character_skills_enum` |
| `voice.tone` | Enum: quiet, sharp, warm, bitter, measured, fierce | `test_character_voice_tone_enum` |
| `voice.style` | Enum: direct, questioning, sardonic, gentle, blunt | `test_character_voice_style_enum` |
| `personality.approach` | Enum: direct, cunning, cautious, impulsive, deliberate | `test_character_approach_enum` |
| `personality.flaw` | Enum: pride, fear, greed, wrath, doubt, rigidity, softness, envy, sloth | `test_character_flaw_enum` |

**Special constraints:**
- Exactly one character must have `type: player`
- Living characters (`alive: true`) must have an AT link to a Place
- Dead characters should not have AT links (optional: keep for death location)

### V2.2: Place Invariants

| Property | Constraint | Test |
|----------|------------|------|
| `id` | Required, unique | `test_place_id_required` |
| `name` | Required | `test_place_name_required` |
| `coordinates` | [lat, lng] if provided | `test_place_coordinates_format` |
| `scale` | Enum: region, settlement, district, building, room | `test_place_scale_enum` |
| `type` | Enum: region, city, hold, village, monastery, camp, road, room, wilderness, ruin | `test_place_type_enum` |
| `atmosphere.mood` | Enum: welcoming, hostile, indifferent, fearful, watchful, desperate, peaceful, tense | `test_place_mood_enum` |

**Hierarchy constraints:**
- CONTAINS links must respect scale hierarchy (region > settlement > district > building > room)
- ROUTE links should only connect settlement-level or higher places

### V2.3: Thing Invariants

| Property | Constraint | Test |
|----------|------------|------|
| `id` | Required, unique | `test_thing_id_required` |
| `name` | Required | `test_thing_name_required` |
| `type` | Valid thing type | `test_thing_type_enum` |
| `significance` | Enum: mundane, personal, political, sacred, legendary | `test_thing_significance_enum` |
| `quantity` | Integer >= 1 | `test_thing_quantity_positive` |
| `portable` | Boolean, default true | `test_thing_portable_boolean` |

**Location constraint:**
- Every Thing must be either: CARRIED by a Character OR LOCATED_AT a Place (not both, not neither)

### V2.4: Narrative Invariants

| Property | Constraint | Test |
|----------|------------|------|
| `id` | Required, unique | `test_narrative_id_required` |
| `name` | Required | `test_narrative_name_required` |
| `content` | Required | `test_narrative_content_required` |
| `interpretation` | Required | `test_narrative_interpretation_required` |
| `type` | Valid narrative type | `test_narrative_type_enum` |
| `weight` | Float [0, 1] | `test_narrative_weight_range` |
| `focus` | Float [0.1, 3.0], default 1.0 | `test_narrative_focus_range` |
| `truth` | Float [0, 1], default 1, director-only | `test_narrative_truth_range` |
| `tone` | Valid tone enum | `test_narrative_tone_enum` |
| `voice.style` | Valid voice style | `test_narrative_voice_style_enum` |

**Relationship constraint:**
- Every Narrative should have at least one BELIEVES link (someone believes it)
- Narratives with `weight: 0` should be cleaned up or archived

### V2.5: Tension Invariants

| Property | Constraint | Test |
|----------|------------|------|
| `id` | Required, unique | `test_tension_id_required` |
| `narratives` | Non-empty array of narrative IDs | `test_tension_has_narratives` |
| `pressure` | Float [0, 1] | `test_tension_pressure_range` |
| `breaking_point` | Float [0, 1], default 0.9 | `test_tension_breaking_point_range` |
| `pressure_type` | Enum: gradual, scheduled, hybrid | `test_tension_pressure_type_enum` |
| `base_rate` | Float >= 0 (for gradual/hybrid) | `test_tension_base_rate_positive` |

**Logic constraint:**
- When `pressure >= breaking_point`, tension should flip
- Scheduled tensions must have `progression` array
- Hybrid tensions must have both `base_rate` and `progression`

### V2.6: Moment Invariants

| Property | Constraint | Test |
|----------|------------|------|
| `id` | Required, format: `{place}_{day}_{time}_{type}_{suffix}` | `test_moment_id_format` |
| `text` | Required | `test_moment_text_required` |
| `type` | Enum: narration, dialogue, hint, player_click, player_freeform, player_choice | `test_moment_type_enum` |
| `tick` | Integer >= 0 | `test_moment_tick_positive` |
| `embedding` | 768-dim vector if text > 20 chars | `test_moment_embedding_length` |

---

## V3: LINK INVARIANTS

### V3.1: BELIEVES (Character -> Narrative)

| Property | Constraint |
|----------|------------|
| `heard` | Float [0, 1] |
| `believes` | Float [0, 1] |
| `doubts` | Float [0, 1] |
| `denies` | Float [0, 1] |
| `hides` | Float [0, 1] |
| `spreads` | Float [0, 1] |
| `originated` | Float [0, 1] |
| `source` | Enum: none, witnessed, told, inferred, assumed, taught |

**Tests:**
- `test_believes_link_from_character`
- `test_believes_link_to_narrative`
- `test_believes_values_in_range`

### V3.2: NARRATIVE_NARRATIVE Links

| Property | Constraint |
|----------|------------|
| `contradicts` | Float [0, 1] |
| `supports` | Float [0, 1] |
| `elaborates` | Float [0, 1] |
| `subsumes` | Float [0, 1] |
| `supersedes` | Float [0, 1] |

**Logic constraints:**
- If A contradicts B, then B contradicts A (symmetric)
- If A supersedes B, B does NOT supersede A (asymmetric)
- supersedes drains source narrative weight

**Tests:**
- `test_narrative_link_between_narratives`
- `test_contradiction_symmetry`
- `test_supersession_asymmetry`

### V3.3: Ground Truth Links

| Link | From | To | Constraint |
|------|------|-----|------------|
| AT | Character | Place | `present` is 0 or 1 |
| CARRIES | Character | Thing | `carries` is 0 or 1 |
| LOCATED_AT | Thing | Place | `located` is 0 or 1 |
| CONTAINS | Place | Place | Binary (no attributes) |
| ROUTE | Place | Place | `travel_minutes` > 0 |

**Tests:**
- `test_at_link_structure`
- `test_carries_link_structure`
- `test_located_at_link_structure`
- `test_contains_link_hierarchy`
- `test_route_link_travel_time`

---

## V4: BEHAVIORAL INVARIANTS

### V4.1: Time Progression

- Ticks are measured in minutes
- 1 day = 1440 ticks
- Time only advances via player actions (Narrator)
- World Runner does NOT advance time, only responds to flips

**Tests:**
- `test_tick_to_day_conversion`
- `test_time_of_day_calculation`

### V4.2: Energy Flow (Graph Physics)

- Characters pump energy into narratives they believe
- Energy flows through narrative links
- Contradicting narratives under pressure accumulate tension
- Supersession drains source by 50%

**Constants:**
```python
BELIEF_FLOW_RATE = 0.1
MAX_PROPAGATION_HOPS = 3
LINK_FACTORS = {
    'contradicts': 0.30,
    'supports': 0.20,
    'elaborates': 0.15,
    'subsumes': 0.10,
    'supersedes': 0.25,
}
```

**Tests:**
- `test_energy_flows_from_characters`
- `test_energy_propagation_hops`
- `test_supersession_drain`

### V4.3: Weight Computation

```
weight = belief × player_connection × (1 + contradiction) × recency × focus
```

- Weight is always [0, 1]
- Higher weight = appears more in scenes
- Weight affects which narratives become Voices

**Tests:**
- `test_weight_never_negative`
- `test_weight_never_exceeds_one`
- `test_weight_respects_focus`

### V4.4: Decay System

- All narratives decay over time
- Core types (oath, blood, debt) decay at 0.25x rate
- MIN_WEIGHT = 0.01 (below this, narrative is negligible)
- Decay rate adjusts to maintain total energy

**Tests:**
- `test_decay_reduces_weight`
- `test_core_types_decay_slower`
- `test_min_weight_floor`

### V4.5: Tension & Flips

- Pressure accumulates over time (gradual, scheduled, or hybrid)
- When pressure >= breaking_point, tension FLIPS
- Flips cascade (max depth 5)
- World Runner determines what happens when tension flips

**Tests:**
- `test_flip_detection`
- `test_cascade_depth_limit`
- `test_gradual_pressure_accumulation`
- `test_scheduled_pressure_follows_timeline`

### V4.6: Belief Propagation

- Characters in same place can share narratives
- Trust affects whether beliefs spread
- Contradicting beliefs create tension when believers meet

**Tests:**
- `test_belief_spreads_through_proximity`
- `test_contradiction_creates_tension`

---

## V5: EXPERIENCE INVARIANTS

### V5.1: "I know them" Test

Given a companion character:
- Can query all narratives they believe
- Can query their history with player
- Can predict behavior based on beliefs

**Test:** `test_character_knowledge_queryable`

### V5.2: "They remembered" Test

Given a narrative created in scene N:
- Can surface in scene N+M if weight remains high
- References to past events are accurate

**Test:** `test_narrative_persistence`

### V5.3: "The world moved" Test

Given time elapsed while player is in conversation:
- Tensions tick in background
- Events can happen without player presence
- Player can discover what happened

**Test:** `test_world_ticks_without_player`

### V5.4: "I was wrong" Test

Given a narrative with truth < 1:
- Player can believe something false
- Discovery mechanism exists
- Belief update propagates

**Test:** `test_false_belief_discovery`

---

## V6: ANTI-PATTERNS (What MUST NOT Happen)

### V6.1: "Quest Log" Anti-Pattern
- Ledger should NOT be a checklist of tasks
- No "complete this to progress" mechanics
- Debts/oaths are relationship markers, not quests

**Test:** `test_ledger_not_quest_log`

### V6.2: "Optimal Choice" Anti-Pattern
- No single "best" answer to any situation
- Choices have trade-offs
- Min-maxing relationships should be impossible

**Test:** `test_no_optimal_path`

### V6.3: "Skip Dialog" Anti-Pattern
- Text should be engaging enough to read
- Voice lines should be character-specific
- No generic NPC dialogue

**Test:** `test_voice_consistency` (validate voice matches character)

### V6.4: "Who is this again?" Anti-Pattern
- Characters should be memorable
- Distinctive voice, flaw, backstory
- Relationships should be clear

**Test:** `test_character_distinctiveness`

---

## V7: SPEC CONSISTENCY

### V7.1: Schema Matches Spec

All node types, link types, and attributes defined in SCHEMA.md must match the complete spec.

**Test:** `test_schema_spec_alignment`

### V7.2: Enum Values Consistent

Enum values must be the same across all documents.

**Test:** `test_enum_consistency`

### V7.3: Constants Defined Once

All magic numbers should be defined as constants and used consistently.

**Test:** `test_constants_consistency`

---

## TEST STATUS

### Unit Tests (No DB Required) — PASSING

| Invariant | Status | Test File | Notes |
|-----------|--------|-----------|-------|
| V2.1-V2.6 | TESTED | `test_models.py` | Pydantic model validation |
| V3.1-V3.3 | TESTED | `test_models.py` | Link model validation |
| V4.1 | TESTED | `test_behaviors.py` | Time conversion formulas |
| V4.2 | PARTIAL | `test_behaviors.py` | Constants only, not flow |
| V4.3 | PARTIAL | `test_behaviors.py` | Clamp logic only |
| V4.4 | PARTIAL | `test_behaviors.py` | Formula only, not DB |
| V4.5 | PARTIAL | `test_behaviors.py` | Tension model methods |
| V4.6 | TESTED | `test_behaviors.py` | Proximity formula |
| V5.1-V5.4 | STRUCTURAL | `test_integration_scenarios.py` | Model structure only |
| V6.1-V6.4 | TESTED | `test_integration_scenarios.py` | Anti-pattern prevention |
| V7.1-V7.3 | TESTED | `test_spec_consistency.py` | Spec internal consistency |

### Integration Tests (Require DB) — NOT YET PASSING

| Invariant | Status | Test File | Requires |
|-----------|--------|-----------|----------|
| V1.1 | STUB | `test_implementation.py` | Full graph operations |
| V1.2 | STUB | `test_implementation.py` | Query layer hiding truth |
| V1.3 | STUB | `test_implementation.py` | Ground truth validation |
| V4.2 | STUB | `test_implementation.py` | GraphTick energy flow |
| V4.4 | STUB | `test_implementation.py` | GraphTick decay |
| V4.5 | STUB | `test_implementation.py` | GraphTick flip detection |
| V5.1 | STUB | `test_implementation.py` | GraphQueries.get_character_beliefs |
| V5.2 | STUB | `test_implementation.py` | Moment search |
| V5.3 | STUB | `test_implementation.py` | World Runner |
| V5.4 | STUB | `test_implementation.py` | Truth discovery |

---

## IMPLEMENTATION CHECKLIST

Based on test stubs, these components need implementation:

### Phase 1: Data Layer
- [ ] `GraphOps.add_character()` — Create character nodes
- [ ] `GraphOps.add_narrative()` — Create narrative nodes
- [ ] `GraphOps.add_belief()` — Create BELIEVES links
- [ ] `GraphOps.add_tension()` — Create tension nodes
- [ ] `GraphOps.add_route()` — Create ROUTE links
- [ ] `GraphOps.set_character_location()` — Create/update AT links

### Phase 2: Query Layer
- [ ] `GraphQueries.get_character_beliefs()` — V5.1 "I know them"
- [ ] `GraphQueries.get_narratives_about()` — Query by character/place/thing
- [ ] `GraphQueries.get_characters_at()` — Who is at location
- [ ] `GraphQueries.get_path_between()` — Travel time
- [ ] `GraphQueries.get_tension()` — Tension state

### Phase 3: Physics Engine
- [ ] `GraphTick._compute_character_energies()` — V4.2
- [ ] `GraphTick._flow_energy_to_narratives()` — V4.2
- [ ] `GraphTick._propagate_energy()` — V4.2
- [ ] `GraphTick._decay_energy()` — V4.4
- [ ] `GraphTick._tick_pressures()` — V4.5
- [ ] `GraphTick._detect_flips()` — V4.5

### Phase 4: Orchestration
- [ ] `WorldRunner.resolve_flip()` — V5.3
- [ ] `NarratorPromptBuilder.build_context()` — Scene generation
- [ ] `Orchestrator.run_loop()` — Full gameplay loop

### Phase 5: Memory
- [ ] `MomentProcessor` integration — V5.2
- [ ] Semantic search for moments — "When did Aldric mention..."
