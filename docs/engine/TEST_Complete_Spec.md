# TEST: Complete Spec Test Index

**This file indexes all tests and their relationships to implementation files.**

See: `VALIDATION_Complete_Spec.md` for what invariants these tests verify.

---

## Test Files Overview

| Test File | Purpose | Requires DB | Status |
|-----------|---------|-------------|--------|
| `test_spec_consistency.py` | Spec internal consistency | No | PASSING |
| `test_models.py` | Pydantic model validation | No | PASSING |
| `test_behaviors.py` | Game mechanics formulas | No | PASSING |
| `test_integration_scenarios.py` | Experience invariant structure | No | PASSING |
| `test_implementation.py` | Full system integration | Yes | STUBS |

---

## Bidirectional Links: Tests ↔ Implementation

### Models Layer

| Implementation | Tests | Validates |
|----------------|-------|-----------|
| `engine/models/base.py` | `test_models.py::TestCharacterModel`, `test_models.py::TestModifier`, `test_models.py::TestGameTimestamp` | V2 Node enums, V3 Link enums |
| `engine/models/nodes.py` | `test_models.py::TestCharacterModel`, `test_models.py::TestPlaceModel`, `test_models.py::TestThingModel`, `test_models.py::TestNarrativeModel`, `test_models.py::TestMomentModel` | V2.1-V2.6 Node invariants |
| `engine/models/links.py` | `test_models.py::TestCharacterNarrativeLink`, `test_models.py::TestNarrativeNarrativeLink`, `test_models.py::TestCharacterPlaceLink`, `test_models.py::TestCharacterThingLink`, `test_models.py::TestThingPlaceLink`, `test_models.py::TestPlacePlaceLink` | V3.1-V3.3 Link invariants |
| `engine/models/tensions.py` | `test_models.py::TestTensionModel`, `test_behaviors.py::TestTensionAndFlips` | V2.5 Tension invariants |

### Physics Layer

| Implementation | Tests | Validates |
|----------------|-------|-----------|
| `engine/physics/constants.py` | `test_behaviors.py::TestEnergyFlow`, `test_behaviors.py::TestDecaySystem`, `test_behaviors.py::TestTensionAndFlips`, `test_behaviors.py::TestCriticality`, `test_behaviors.py::TestProximity` | V4 Behavioral constants |
| `engine/physics/tick.py` | `test_implementation.py::TestEnergyFlowImplementation`, `test_implementation.py::TestDecayImplementation`, `test_implementation.py::TestTensionImplementation` | V4.2-V4.5 Physics engine |

### Database Layer

| Implementation | Tests | Validates |
|----------------|-------|-----------|
| `engine/db/graph_ops.py` | `test_implementation.py::TestGraphOpsImplementation` | Data write operations |
| `engine/db/graph_queries.py` | `test_implementation.py::TestGraphQueriesImplementation` | Data read operations, V5.1 |

### Orchestration Layer

| Implementation | Tests | Validates |
|----------------|-------|-----------|
| `engine/orchestration/world_runner.py` | `test_implementation.py::TestWorldRunnerImplementation` | V5.3 "The world moved" |
| `engine/orchestration/narrator.py` | `test_implementation.py::TestNarratorImplementation` | Scene generation |

### Memory Layer

| Implementation | Tests | Validates |
|----------------|-------|-----------|
| `engine/memory/moment_processor.py` | `test_moment.py`, `test_implementation.py::TestMomentImplementation` | V5.2 "They remembered" |

---

## Test Class Index

### test_spec_consistency.py

| Class | Tests | Validates |
|-------|-------|-----------|
| `TestSchemaSpecAlignment` | `test_node_types_exist`, `test_character_type_enum`, `test_narrative_type_enum` | V7.1 Schema matches spec |
| `TestEnumConsistency` | `test_character_types_complete`, `test_place_scales_hierarchical`, `test_narrative_types_cover_all_categories`, `test_skill_levels_ordered`, `test_pressure_types_complete`, `test_moment_types_cover_all_sources` | V7.2 Enum consistency |
| `TestConstantsConsistency` | `test_belief_flow_rate_valid`, `test_max_propagation_hops_positive`, `test_decay_rate_valid`, `test_min_weight_small`, `test_breaking_point_valid`, `test_link_factors_sum_reasonable`, `test_link_factors_all_positive`, `test_supersedes_has_drain_effect`, `test_contradicts_highest_factor` | V7.3 Constants consistency |
| `TestSpecInternalConsistency` | `test_core_types_for_slow_decay`, `test_character_flaws_distinct`, `test_voice_styles_cover_emotional_range`, `test_modifier_types_cover_all_node_types`, `test_road_types_have_speed_ordering` | V7 Internal consistency |
| `TestCrossReferences` | `test_tension_references_narratives`, `test_belief_source_types_make_sense`, `test_narrative_about_fields_valid` | V7 Cross-references |

### test_models.py

| Class | Tests | Implementation |
|-------|-------|----------------|
| `TestCharacterModel` | 8 tests | `engine/models/nodes.py:Character` |
| `TestPlaceModel` | 5 tests | `engine/models/nodes.py:Place` |
| `TestThingModel` | 6 tests | `engine/models/nodes.py:Thing` |
| `TestNarrativeModel` | 7 tests | `engine/models/nodes.py:Narrative` |
| `TestTensionModel` | 9 tests | `engine/models/tensions.py:Tension` |
| `TestMomentModel` | 5 tests | `engine/models/nodes.py:Moment` |
| `TestCharacterNarrativeLink` | 5 tests | `engine/models/links.py:CharacterNarrative` |
| `TestNarrativeNarrativeLink` | 3 tests | `engine/models/links.py:NarrativeNarrative` |
| `TestCharacterPlaceLink` | 3 tests | `engine/models/links.py:CharacterPlace` |
| `TestCharacterThingLink` | 2 tests | `engine/models/links.py:CharacterThing` |
| `TestThingPlaceLink` | 2 tests | `engine/models/links.py:ThingPlace` |
| `TestPlacePlaceLink` | 3 tests | `engine/models/links.py:PlacePlace` |
| `TestModifier` | 4 tests | `engine/models/base.py:Modifier` |
| `TestGameTimestamp` | 4 tests | `engine/models/base.py:GameTimestamp` |

### test_behaviors.py

| Class | Tests | Implementation |
|-------|-------|----------------|
| `TestTimeProgression` | 4 tests | Time formulas (no file, pure math) |
| `TestEnergyFlow` | 7 tests | `engine/physics/constants.py` |
| `TestWeightComputation` | 4 tests | `engine/physics/constants.py:MIN_WEIGHT` |
| `TestDecaySystem` | 8 tests | `engine/physics/constants.py:DECAY_*`, `CORE_*` |
| `TestTensionAndFlips` | 9 tests | `engine/physics/constants.py`, `engine/models/tensions.py` |
| `TestCriticality` | 3 tests | `engine/physics/constants.py:CRITICALITY_*` |
| `TestProximity` | 5 tests | `engine/physics/constants.py:distance_to_proximity` |
| `TestExperienceStructure` | 4 tests | `engine/models/nodes.py:Narrative`, `engine/models/tensions.py:Tension` |

### test_integration_scenarios.py

| Class | Tests | Validates |
|-------|-------|-----------|
| `TestIKnowThem` | 4 tests | V5.1 Character knowledge queryable |
| `TestTheyRemembered` | 4 tests | V5.2 Narratives persist |
| `TestTheWorldMoved` | 4 tests | V5.3 Time passes, events happen |
| `TestIWasWrong` | 4 tests | V5.4 False beliefs discoverable |
| `TestAntiPatterns` | 4 tests | V6.1-V6.4 Anti-patterns prevented |
| `TestCompleteGameplayLoop` | 5 tests | Full loop structure |

### test_implementation.py (STUBS)

| Class | Tests | Implementation Required |
|-------|-------|------------------------|
| `TestGraphOpsImplementation` | 4 tests | `engine/db/graph_ops.py` |
| `TestGraphQueriesImplementation` | 5 tests | `engine/db/graph_queries.py` |
| `TestEnergyFlowImplementation` | 3 tests | `engine/physics/tick.py:GraphTick._flow_*` |
| `TestDecayImplementation` | 3 tests | `engine/physics/tick.py:GraphTick._decay_energy` |
| `TestTensionImplementation` | 3 tests | `engine/physics/tick.py:GraphTick._tick_pressures`, `_detect_flips` |
| `TestWorldRunnerImplementation` | 2 tests | `engine/orchestration/world_runner.py` |
| `TestNarratorImplementation` | 3 tests | `engine/orchestration/narrator.py` |
| `TestFullGameplayLoop` | 2 tests | All systems |
| `TestSemanticSearchImplementation` | 2 tests | `engine/embeddings/service.py`, `engine/queries/semantic.py` |
| `TestMomentImplementation` | 2 tests | `engine/memory/moment_processor.py` |

---

## Running Tests

```bash
cd /home/mind-protocol/the-blood-ledger/engine

# Run all unit tests (no DB required)
python3 -m pytest tests/test_spec_consistency.py tests/test_models.py tests/test_behaviors.py tests/test_integration_scenarios.py -v

# Run integration tests (requires FalkorDB)
python3 -m pytest tests/test_implementation.py -v -m integration

# Run specific test class
python3 -m pytest tests/test_models.py::TestNarrativeModel -v

# Run with coverage
python3 -m pytest tests/ --cov=engine --cov-report=html
```

---

## Adding New Tests

When adding tests:

1. **Identify the invariant** from `VALIDATION_Complete_Spec.md`
2. **Find or create the test class** in the appropriate file
3. **Name the test** after what it validates: `test_V2_1_character_id_required`
4. **Add docstring** with REQUIRES/VALIDATES
5. **Update this file** with the new test
6. **Update implementation file** header with test reference
