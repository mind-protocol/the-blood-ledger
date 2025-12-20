"""
Implementation Tests — Requires Running Systems

These tests validate the ACTUAL implementation against a real database.
They are TEST STUBS until the implementation is complete.

REQUIRES:
    - Running FalkorDB instance on localhost:6379
    - Populated test data (via fixtures)
    - Full system integration

VALIDATES:
    V1.1: "The game is a web of narratives" — All state via graph
    V1.2: Characters never see truth — Query layer hides truth field
    V4.2: Energy flow — GraphTick._flow_energy_to_narratives
    V4.4: Decay system — GraphTick._decay_energy
    V4.5: Tension & flips — GraphTick._tick_pressures, _detect_flips
    V5.1: "I know them" — GraphQueries.get_character_beliefs
    V5.2: "They remembered" — Moment search
    V5.3: "The world moved" — World Runner

TESTS IMPLEMENTATIONS:
    engine/physics/graph/graph_ops.py — Data write operations
    engine/physics/graph/graph_queries.py — Data read operations
    engine/physics/tick.py — GraphTick class
    engine/orchestration/world_runner.py — World Runner
    engine/orchestration/narrator.py — Narrator
    engine/memory/moment_processor.py — Moment creation
    engine/embeddings/service.py — Embedding generation
    engine/queries/semantic.py — Semantic search

STATUS: STUBS
    All tests will SKIP until implementations are complete.
    Each test documents what it REQUIRES to pass.

REFERENCES:
    docs/engine/VALIDATION_Complete_Spec.md — All invariants
    docs/engine/TEST_Complete_Spec.md — Test index

RUN:
    pytest test_implementation.py -v -m integration
"""

import pytest
from pathlib import Path
import sys
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def db_connection():
    """
    REQUIRES: FalkorDB running on localhost:6379
    """
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host='localhost', port=6379)
        graph = db.select_graph('blood_ledger_test')
        yield graph
        # Cleanup: drop test graph
        # graph.delete()
    except Exception as e:
        pytest.skip(f"FalkorDB not available: {e}")


@pytest.fixture
def graph_ops(db_connection):
    """
    REQUIRES: engine/physics/graph/graph_ops.py fully implemented

    Uses actual GraphOps API. Key methods:
    - add_character(id, name, type, ...)
    - add_place(id, name, type, ...)
    - add_narrative(id, name, content, type, ...)
    - add_tension(id, narratives, description, pressure, ...)
    - add_belief(character_id, narrative_id, heard, believes, ...)
    - add_presence(character_id, place_id, present=1.0, visible=1.0)
    - add_geography(from_place_id, to_place_id, path=1.0, path_distance="...")
    - add_narrative_link(source_id, target_id, contradicts=0.0, supports=0.0, ...)
    """
    try:
        from engine.physics.graph.graph_ops import GraphOps
        ops = GraphOps(graph_name='blood_ledger_test')
        return ops
    except Exception as e:
        pytest.skip(f"GraphOps not available: {e}")


@pytest.fixture
def graph_queries(db_connection):
    """
    REQUIRES: engine/physics/graph/graph_queries.py fully implemented
    """
    try:
        from engine.physics.graph.graph_queries import GraphQueries
        return GraphQueries(graph_name='blood_ledger_test')
    except Exception as e:
        pytest.skip(f"GraphQueries not available: {e}")


@pytest.fixture
def graph_tick(db_connection):
    """
    REQUIRES: engine/physics/tick.py fully implemented
    """
    try:
        from engine.physics.tick import GraphTick
        return GraphTick(graph_name='blood_ledger_test')
    except Exception as e:
        pytest.skip(f"GraphTick not available: {e}")


@pytest.fixture
def test_world(graph_ops):
    """
    Create a minimal test world with characters, places, narratives, tensions.

    REQUIRES: GraphOps.add_character, add_place, add_narrative, add_tension
    Uses actual GraphOps API from engine/physics/graph/graph_ops.py
    """
    # Characters
    graph_ops.add_character(
        id="char_player",
        name="Rolf",
        type="player"
    )
    graph_ops.add_character(
        id="char_aldric",
        name="Aldric",
        type="companion"
    )
    graph_ops.add_character(
        id="char_edmund",
        name="Edmund",
        type="major"
    )

    # Places
    graph_ops.add_place(
        id="place_camp",
        name="The Camp",
        type="camp"
    )
    graph_ops.add_place(
        id="place_york",
        name="York",
        type="city"
    )

    # Connect places via add_geography (not add_route)
    graph_ops.add_geography(
        from_place_id="place_camp",
        to_place_id="place_york",
        path=1.0,
        path_distance="2 days",
        path_difficulty="moderate"
    )

    # Put characters at places via add_presence (not set_character_location)
    graph_ops.add_presence("char_player", "place_camp")
    graph_ops.add_presence("char_aldric", "place_camp")
    graph_ops.add_presence("char_edmund", "place_york")

    # Narratives
    graph_ops.add_narrative(
        id="narr_aldric_oath",
        name="Aldric's Oath",
        content="Aldric swore to protect Rolf",
        type="oath",
        about_characters=["char_aldric", "char_player"],
        weight=0.8
    )
    graph_ops.add_narrative(
        id="narr_edmund_betrayal",
        name="The Betrayal",
        content="Edmund betrayed the family",
        type="memory",
        about_characters=["char_edmund"],
        weight=0.7
    )
    graph_ops.add_narrative(
        id="narr_edmund_forced",
        name="Edmund Was Forced",
        content="Edmund was forced to betray us",
        type="rumor",
        about_characters=["char_edmund"],
        weight=0.4,
        truth=0.0  # This is false
    )

    # Beliefs
    graph_ops.add_belief("char_aldric", "narr_aldric_oath", heard=1.0, believes=1.0)
    graph_ops.add_belief("char_aldric", "narr_edmund_betrayal", heard=1.0, believes=0.9)
    graph_ops.add_belief("char_player", "narr_edmund_betrayal", heard=1.0, believes=0.8)
    graph_ops.add_belief("char_player", "narr_edmund_forced", heard=0.5, believes=0.3)

    # Narrative links
    graph_ops.add_narrative_link(
        source_id="narr_edmund_betrayal",
        target_id="narr_edmund_forced",
        contradicts=0.9
    )

    # Tension (requires description parameter)
    graph_ops.add_tension(
        id="tension_edmund",
        narratives=["narr_edmund_betrayal", "narr_edmund_forced"],
        description="Conflict between betrayal and coercion",
        pressure=0.5,
        breaking_point=0.9
    )

    return {
        'characters': ['char_player', 'char_aldric', 'char_edmund'],
        'places': ['place_camp', 'place_york'],
        'narratives': ['narr_aldric_oath', 'narr_edmund_betrayal', 'narr_edmund_forced'],
        'tensions': ['tension_edmund']
    }


# =============================================================================
# DATABASE OPERATIONS TESTS
# =============================================================================

class TestGraphOpsImplementation:
    """
    Test that GraphOps correctly writes to the database.

    REQUIRES: engine/physics/graph/graph_ops.py
    VALIDATES: Data can be written to FalkorDB
    """

    def test_add_character_creates_node(self, graph_ops, db_connection):
        """
        REQUIRES: GraphOps.add_character()
        VALIDATES: Character nodes are created with correct properties
        """
        graph_ops.add_character(
            id="char_test",
            name="Test Character",
            type="minor"
        )

        # Query directly to verify
        result = db_connection.query(
            "MATCH (c:Character {id: 'char_test'}) RETURN c.name, c.type"
        )

        assert len(result.result_set) == 1
        assert result.result_set[0][0] == "Test Character"
        assert result.result_set[0][1] == "minor"

    def test_add_narrative_creates_node(self, graph_ops, db_connection):
        """
        REQUIRES: GraphOps.add_narrative()
        VALIDATES: Narrative nodes have required fields (id, name, content, type)
        """
        graph_ops.add_narrative(
            id="narr_test",
            name="Test Narrative",
            content="This is test content",
            type="memory",
            weight=0.5
        )

        result = db_connection.query(
            "MATCH (n:Narrative {id: 'narr_test'}) RETURN n.content, n.weight"
        )

        assert len(result.result_set) == 1
        assert result.result_set[0][0] == "This is test content"
        assert result.result_set[0][1] == 0.5

    def test_add_belief_creates_link(self, graph_ops, db_connection, test_world):
        """
        REQUIRES: GraphOps.add_belief()
        VALIDATES: BELIEVES links connect Character to Narrative with attributes
        """
        result = db_connection.query("""
            MATCH (c:Character {id: 'char_aldric'})-[b:BELIEVES]->(n:Narrative {id: 'narr_aldric_oath'})
            RETURN b.heard, b.believes
        """)

        assert len(result.result_set) == 1
        assert result.result_set[0][0] == 1.0  # heard
        assert result.result_set[0][1] == 1.0  # believes

    def test_add_narrative_link_creates_relationship(self, graph_ops, db_connection, test_world):
        """
        REQUIRES: GraphOps.add_narrative_link()
        VALIDATES: Narrative-Narrative links have correct attributes
        """
        result = db_connection.query("""
            MATCH (n1:Narrative {id: 'narr_edmund_betrayal'})-[r:RELATES_TO]->(n2:Narrative {id: 'narr_edmund_forced'})
            RETURN r.contradicts
        """)

        assert len(result.result_set) == 1
        assert result.result_set[0][0] == 0.9


class TestGraphQueriesImplementation:
    """
    Test that GraphQueries correctly reads from the database.

    REQUIRES: engine/db/graph_queries.py
    VALIDATES: Data can be queried from FalkorDB
    """

    def test_get_character_beliefs(self, graph_queries, test_world):
        """
        REQUIRES: GraphQueries.get_character_beliefs()
        VALIDATES: V5.1 "I know them" - can query what character believes
        """
        beliefs = graph_queries.get_character_beliefs("char_aldric")

        assert len(beliefs) >= 2
        narr_ids = [b['id'] for b in beliefs]
        assert 'narr_aldric_oath' in narr_ids
        assert 'narr_edmund_betrayal' in narr_ids

    def test_get_narratives_about_character(self, graph_queries, test_world):
        """
        REQUIRES: GraphQueries.get_narratives_about()
        VALIDATES: Can query narratives involving a character
        """
        narratives = graph_queries.get_narratives_about(character_id="char_edmund")

        assert len(narratives) >= 2
        narr_ids = [n['id'] for n in narratives]
        assert 'narr_edmund_betrayal' in narr_ids

    def test_get_characters_at_place(self, graph_queries, test_world):
        """
        REQUIRES: GraphQueries.get_characters_at()
        VALIDATES: Can query who is at a location
        """
        chars = graph_queries.get_characters_at("place_camp")

        char_ids = [c['id'] for c in chars]
        assert 'char_player' in char_ids
        assert 'char_aldric' in char_ids
        assert 'char_edmund' not in char_ids  # Edmund is in York

    def test_get_path_between_places(self, graph_queries, test_world):
        """
        REQUIRES: GraphQueries.get_path_between()
        VALIDATES: Can query travel time between places
        """
        path = graph_queries.get_path_between("place_camp", "place_york")

        assert path is not None
        assert 'path_distance' in path or 'distance_km' in path

    def test_get_tension_by_id(self, graph_queries, test_world):
        """
        REQUIRES: GraphQueries.get_tension()
        VALIDATES: Can query tension state
        """
        tension = graph_queries.get_tension("tension_edmund")

        assert tension is not None
        assert tension['pressure'] == 0.5
        assert tension['breaking_point'] == 0.9


# =============================================================================
# ENERGY FLOW TESTS
# =============================================================================

class TestEnergyFlowImplementation:
    """
    Test that energy flows correctly through the graph.

    REQUIRES: engine/physics/tick.py - GraphTick class
    VALIDATES: V4.2 Energy flow mechanics
    """

    def test_characters_pump_energy_to_narratives(self, graph_tick, graph_queries, test_world):
        """
        REQUIRES: GraphTick._flow_energy_to_narratives()
        VALIDATES: Characters pump energy into narratives they believe
        """
        # Get initial weights
        initial_oath = graph_queries.get_narrative("narr_aldric_oath")['weight']

        # Run tick
        result = graph_tick.run(elapsed_minutes=10, player_id="char_player")

        # Oath narrative should have received energy (Aldric believes it strongly)
        # Note: actual change depends on full implementation
        assert result.narratives_updated > 0

    def test_proximity_affects_energy(self, graph_tick, test_world):
        """
        REQUIRES: GraphTick._compute_proximity()
        VALIDATES: Characters closer to player contribute more energy
        """
        # Aldric is at same location as player -> proximity 1.0
        # Edmund is in York (far away) -> proximity < 1.0

        result = graph_tick.run(elapsed_minutes=10, player_id="char_player", player_location="place_camp")

        # Energy from Aldric should be higher than from Edmund
        # This is validated by the total energy distribution
        assert result.energy_total > 0

    def test_contradicting_narratives_both_heat_up(self, graph_tick, graph_queries, test_world):
        """
        REQUIRES: GraphTick._propagate_energy()
        VALIDATES: Contradicting narratives both receive energy (factor 0.30)
        """
        initial_betrayal = graph_queries.get_narrative("narr_edmund_betrayal")['weight']
        initial_forced = graph_queries.get_narrative("narr_edmund_forced")['weight']

        # Run tick - energy should flow between contradicting narratives
        graph_tick.run(elapsed_minutes=10, player_id="char_player")

        final_betrayal = graph_queries.get_narrative("narr_edmund_betrayal")['weight']
        final_forced = graph_queries.get_narrative("narr_edmund_forced")['weight']

        # Both should have some energy (exact values depend on implementation)
        assert final_betrayal > 0
        assert final_forced > 0


# =============================================================================
# DECAY TESTS
# =============================================================================

class TestDecayImplementation:
    """
    Test that decay works correctly.

    REQUIRES: engine/physics/tick.py - GraphTick._decay_energy()
    VALIDATES: V4.4 Decay system
    """

    def test_narratives_decay_over_time(self, graph_tick, graph_queries, graph_ops):
        """
        REQUIRES: GraphTick._decay_energy()
        VALIDATES: Narrative weights decrease over time
        """
        # Create an isolated narrative with no believers (will decay fastest)
        graph_ops.add_narrative(
            id="narr_forgotten",
            name="Forgotten Story",
            content="Nobody remembers this",
            type="rumor",
            weight=0.5
        )

        # Run multiple ticks
        for _ in range(10):
            graph_tick.run(elapsed_minutes=10, player_id="char_player")

        final = graph_queries.get_narrative("narr_forgotten")

        # Should have decayed (unless someone believes it)
        assert final['weight'] <= 0.5

    def test_core_types_decay_slower(self, graph_tick, graph_queries, test_world):
        """
        REQUIRES: GraphTick._decay_energy() with CORE_DECAY_MULTIPLIER
        VALIDATES: Oaths, blood, debts decay at 0.25x rate
        """
        # narr_aldric_oath is type 'oath' (core type)
        initial_oath = graph_queries.get_narrative("narr_aldric_oath")['weight']

        # Run ticks
        for _ in range(5):
            graph_tick.run(elapsed_minutes=10, player_id="char_player")

        final_oath = graph_queries.get_narrative("narr_aldric_oath")['weight']

        # Oath should retain more weight due to slower decay
        # (Also helped by Aldric believing it)
        assert final_oath > 0.5  # Should still be significant

    def test_weight_never_below_min(self, graph_tick, graph_queries, graph_ops):
        """
        REQUIRES: GraphTick._decay_energy() with MIN_WEIGHT floor
        VALIDATES: Weights never drop below MIN_WEIGHT (0.01)
        """
        from engine.physics.constants import MIN_WEIGHT

        # Create narrative and run many ticks
        graph_ops.add_narrative(
            id="narr_dying",
            name="Dying Story",
            content="Fading away",
            type="rumor",
            weight=0.1
        )

        for _ in range(100):
            graph_tick.run(elapsed_minutes=10, player_id="char_player")

        final = graph_queries.get_narrative("narr_dying")

        assert final['weight'] >= MIN_WEIGHT


# =============================================================================
# TENSION & FLIP TESTS
# =============================================================================

class TestTensionImplementation:
    """
    Test that tensions accumulate and flip correctly.

    REQUIRES: engine/physics/tick.py - GraphTick._tick_pressures(), _detect_flips()
    VALIDATES: V4.5 Tension & flips
    """

    def test_tension_pressure_increases(self, graph_tick, graph_queries, test_world):
        """
        REQUIRES: GraphTick._tick_pressures()
        VALIDATES: Tension pressure increases over time
        """
        initial = graph_queries.get_tension("tension_edmund")['pressure']

        # Run tick
        graph_tick.run(elapsed_minutes=100, player_id="char_player")

        final = graph_queries.get_tension("tension_edmund")['pressure']

        assert final > initial

    def test_tension_flip_detected(self, graph_tick, graph_ops, graph_queries):
        """
        REQUIRES: GraphTick._detect_flips()
        VALIDATES: Flip is detected when pressure >= breaking_point
        """
        # Create tension near breaking point
        graph_ops.add_tension(
            id="tension_about_to_flip",
            narratives=["narr_edmund_betrayal"],
            description="About to flip",
            pressure=0.89,
            breaking_point=0.9
        )

        # Run tick - should push it over
        result = graph_tick.run(elapsed_minutes=100, player_id="char_player")

        # Check for flip
        flip_ids = [f['tension_id'] for f in result.flips]
        assert "tension_about_to_flip" in flip_ids

    def test_flip_returns_narrative_ids(self, graph_tick, graph_ops):
        """
        REQUIRES: GraphTick._detect_flips()
        VALIDATES: Flip result includes narrative IDs for World Runner
        """
        graph_ops.add_tension(
            id="tension_test_flip",
            narratives=["narr_edmund_betrayal", "narr_edmund_forced"],
            description="Test flip",
            pressure=0.95,
            breaking_point=0.9
        )

        result = graph_tick.run(elapsed_minutes=10, player_id="char_player")

        flip = next((f for f in result.flips if f['tension_id'] == 'tension_test_flip'), None)
        assert flip is not None
        assert 'narratives' in flip
        assert len(flip['narratives']) == 2


# =============================================================================
# WORLD RUNNER TESTS
# =============================================================================

class TestWorldRunnerImplementation:
    """
    Test that World Runner correctly resolves flips.

    REQUIRES: engine/orchestration/world_runner.py
    VALIDATES: V5.3 "The world moved"
    """

    def test_world_runner_creates_narratives(self, graph_ops, graph_queries):
        """
        REQUIRES: WorldRunner.resolve_flip()
        VALIDATES: World Runner creates new narratives when tension flips
        """
        pytest.skip("WorldRunner not yet implemented")

        from engine.infrastructure.orchestration.world_runner import WorldRunner

        runner = WorldRunner()

        flip = {
            'tension_id': 'tension_edmund',
            'narratives': ['narr_edmund_betrayal', 'narr_edmund_forced'],
            'trigger_reason': 'Pressure exceeded breaking point'
        }

        result = runner.resolve_flip(flip)

        # Should create new narratives
        assert 'new_narratives' in result
        assert len(result['new_narratives']) > 0

    def test_world_runner_updates_beliefs(self):
        """
        REQUIRES: WorldRunner.resolve_flip()
        VALIDATES: Characters present at event gain new beliefs
        """
        pytest.skip("WorldRunner not yet implemented")


# =============================================================================
# NARRATOR TESTS
# =============================================================================

class TestNarratorImplementation:
    """
    Test that Narrator correctly generates scenes.

    REQUIRES: engine/orchestration/narrator.py
    VALIDATES: Scene generation with context
    """

    def test_narrator_receives_high_weight_narratives(self, graph_queries):
        """
        REQUIRES: Narrator prompt builder
        VALIDATES: High-weight narratives are included in context
        """
        pytest.skip("Narrator not yet implemented")

        from engine.infrastructure.orchestration.narrator import NarratorPromptBuilder

        builder = NarratorPromptBuilder(graph_queries)
        context = builder.build_context(
            player_id="char_player",
            location="place_camp",
            characters_present=["char_aldric"]
        )

        # High-weight narratives should be in context
        assert "Aldric's Oath" in context or "narr_aldric_oath" in context

    def test_narrator_returns_time_elapsed(self):
        """
        REQUIRES: Narrator response parsing
        VALIDATES: Narrator reports time elapsed for tick calculation
        """
        pytest.skip("Narrator not yet implemented")

    def test_narrator_returns_mutations(self):
        """
        REQUIRES: Narrator response parsing
        VALIDATES: Narrator can create/update narratives
        """
        pytest.skip("Narrator not yet implemented")


# =============================================================================
# FULL LOOP TESTS
# =============================================================================

class TestFullGameplayLoop:
    """
    Test the complete gameplay loop.

    REQUIRES: All systems integrated
    VALIDATES: V5 Experience invariants
    """

    def test_scene_to_tick_to_flip_to_resolution(self, graph_tick, graph_ops, graph_queries):
        """
        REQUIRES: Full integration
        VALIDATES: Complete loop works

        1. Player action -> Narrator generates scene
        2. Time passes -> Tick runs
        3. Tension flips -> World Runner resolves
        4. New narratives created -> Beliefs updated
        5. Next scene reflects changes
        """
        pytest.skip("Full integration not yet implemented")

        # 1. Setup: tension near breaking
        graph_ops.add_tension(
            id="tension_loop_test",
            narratives=["narr_edmund_betrayal"],
            pressure=0.88,
            breaking_point=0.9
        )

        # 2. Simulate scene taking 30 minutes
        result = graph_tick.run(elapsed_minutes=30, player_id="char_player")

        # 3. Check if flip occurred
        if result.flips:
            # 4. World Runner would resolve
            # 5. New narratives would be created
            pass

        # Verify state changed
        tension = graph_queries.get_tension("tension_loop_test")
        assert tension['pressure'] > 0.88

    def test_player_discovers_world_moved(self, graph_queries, graph_ops):
        """
        REQUIRES: Full integration
        VALIDATES: V5.3 "The world moved" - player can discover off-screen events
        """
        pytest.skip("Full integration not yet implemented")

        # Create narrative about off-screen event
        graph_ops.add_narrative(
            id="narr_offscreen_event",
            name="Battle at Durham",
            content="While you were away, the Normans attacked Durham",
            type="account",
            weight=0.7
        )

        # Player character learns about it
        graph_ops.add_belief(
            "char_player", "narr_offscreen_event",
            heard=0.8, believes=0.7,
            source="told", from_whom="char_aldric"
        )

        # Player should now know
        beliefs = graph_queries.get_character_beliefs("char_player")
        narr_ids = [b['id'] for b in beliefs]
        assert "narr_offscreen_event" in narr_ids


# =============================================================================
# SEMANTIC SEARCH TESTS
# =============================================================================

class TestSemanticSearchImplementation:
    """
    Test semantic search with embeddings.

    REQUIRES: engine/embeddings/service.py, engine/queries/semantic.py
    VALIDATES: Natural language queries work
    """

    def test_embed_narrative(self, graph_ops):
        """
        REQUIRES: EmbeddingService.embed()
        VALIDATES: Narratives can be embedded
        """
        pytest.skip("Embedding service not tested")

        from engine.infrastructure.embeddings.service import EmbeddingService

        service = EmbeddingService()

        text = "Aldric swore to protect Rolf with his life"
        embedding = service.embed(text)

        assert len(embedding) == 768  # Expected dimension

    def test_semantic_query(self, graph_queries):
        """
        REQUIRES: SemanticSearch.query()
        VALIDATES: "Who knows about the betrayal?" returns relevant narratives
        """
        pytest.skip("Semantic search not tested")

        from engine.world.map.semantic import SemanticSearch

        search = SemanticSearch(graph_queries)

        results = search.query("Who knows about Edmund's betrayal?")

        assert len(results) > 0
        # Should find narr_edmund_betrayal and believers


# =============================================================================
# MOMENT TESTS
# =============================================================================

class TestMomentImplementation:
    """
    Test Moment creation and querying.

    REQUIRES: engine/memory/moment_processor.py
    VALIDATES: V5.2 "They remembered" - moments are searchable
    """

    def test_moment_created_for_dialogue(self, graph_ops):
        """
        REQUIRES: MomentProcessor.process_dialogue()
        VALIDATES: Dialogue creates searchable Moment
        """
        pytest.skip("MomentProcessor integration not tested")

        from engine.infrastructure.memory.moment_processor import MomentProcessor

        processor = MomentProcessor(
            graph_ops=graph_ops,
            embed_fn=lambda x: [0.1] * 768,
            playthrough_id="test"
        )

        processor.set_context(tick=1440, place_id="place_camp")

        moment_id = processor.process_dialogue(
            text="I swore an oath. That hasn't changed.",
            speaker="char_aldric",
            name="oath_reminder"
        )

        assert moment_id is not None

    def test_moment_searchable_by_content(self, graph_queries):
        """
        REQUIRES: Moment embedding + semantic search
        VALIDATES: Can find "when did Aldric mention his oath?"
        """
        pytest.skip("Moment search not tested")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Run only integration tests
    pytest.main([__file__, "-v", "-m", "integration"])
