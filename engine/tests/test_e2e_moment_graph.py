#!/usr/bin/env python3
"""
End-to-End Integration Test for Moment Graph Architecture.

Tests the full flow:
1. Create moments with clickables via stream_dialogue.py --graph-mode
2. Query moments via get_current_view()
3. Click a word to trigger transition via handle_click()
4. Verify weight transfer and flip to active
5. Test decay and lifecycle

REQUIRES: FalkorDB running on localhost:6379

Run: python3 -m pytest engine/tests/test_e2e_moment_graph.py -v -s
"""

import pytest
import sys
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test graph name (separate from production)
TEST_GRAPH = "test_e2e_moments"


@pytest.fixture(scope="module")
def graph_ops():
    """Create GraphOps connected to test graph."""
    from engine.physics.graph.graph_ops import GraphOps
    ops = GraphOps(graph_name=TEST_GRAPH)

    # Clean up any existing test data
    try:
        ops._query("MATCH (n) DETACH DELETE n")
    except:
        pass

    yield ops

    # Cleanup after tests
    try:
        ops._query("MATCH (n) DETACH DELETE n")
    except:
        pass


@pytest.fixture(scope="module")
def graph_queries():
    """Create GraphQueries connected to test graph."""
    from engine.physics.graph.graph_queries import GraphQueries
    return GraphQueries(graph_name=TEST_GRAPH)


@pytest.fixture
def setup_location(graph_ops):
    """Create a test location for moments."""
    graph_ops._query("""
        MERGE (p:Place {id: 'place_test_camp'})
        SET p.name = 'Test Camp', p.type = 'camp'
    """)
    return "place_test_camp"


@pytest.fixture
def setup_character(graph_ops):
    """Create a test character."""
    graph_ops._query("""
        MERGE (c:Character {id: 'char_test_aldric'})
        SET c.name = 'Test Aldric', c.type = 'companion'
    """)

    # Set character at location
    graph_ops._query("""
        MATCH (c:Character {id: 'char_test_aldric'})
        MATCH (p:Place {id: 'place_test_camp'})
        MERGE (c)-[r:AT]->(p)
        SET r.present = 1.0
    """)
    return "char_test_aldric"


class TestE2EMomentCreation:
    """Test creating moments with the full stack."""

    def test_create_moment_basic(self, graph_ops, setup_location):
        """Test creating a basic moment in the graph."""
        moment_id = graph_ops.add_moment(
            id="e2e_moment_1",
            text="The fire crackles softly in the darkness.",
            type="narration",
            tick=1440,
            place_id=setup_location,
            status="active",
            weight=1.0,
            tone="peaceful"
        )

        assert moment_id == "e2e_moment_1"

        # Verify it's in the graph
        result = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_moment_1'})
            RETURN m.text, m.status, m.weight, m.tone
        """)

        assert len(result) == 1
        text, status, weight, tone = result[0]
        assert text == "The fire crackles softly in the darkness."
        assert status == "active"
        assert weight == 1.0
        assert tone == "peaceful"
        print(f"✓ Created moment: {moment_id}")

    def test_create_moment_with_clickables(self, graph_ops, setup_location, setup_character):
        """Test creating a moment with CAN_LEAD_TO links for clickables."""
        # Main moment (dialogue)
        main_id = graph_ops.add_moment(
            id="e2e_dialogue_main",
            text="My niece Edda is the finest archer in the north.",
            type="dialogue",
            tick=1440,
            speaker=setup_character,
            place_id=setup_location,
            status="active",
            weight=1.0,
            tone="proud"
        )

        # Target moment (response to clicking "Edda")
        target_id = graph_ops.add_moment(
            id="e2e_dialogue_edda",
            text="",  # Empty - narrator fills this in
            type="dialogue",
            tick=1440,
            place_id=setup_location,
            status="possible",
            weight=0.5
        )

        # Create CAN_LEAD_TO link
        graph_ops.add_can_lead_to(
            from_moment_id=main_id,
            to_moment_id=target_id,
            trigger="player",
            require_words=["Edda"],
            weight_transfer=0.4
        )

        # Verify the link exists
        result = graph_ops._query("""
            MATCH (m1:Moment {id: 'e2e_dialogue_main'})-[r:CAN_LEAD_TO]->(m2:Moment {id: 'e2e_dialogue_edda'})
            RETURN r.trigger, r.require_words, r.weight_transfer
        """)

        assert len(result) == 1
        trigger, words, transfer = result[0]
        assert trigger == "player"
        assert "Edda" in words
        assert transfer == 0.4
        print(f"✓ Created moment with clickable: {main_id} -> {target_id}")


class TestE2EViewQuery:
    """Test querying the current view."""

    def test_get_current_view(self, graph_queries, graph_ops, setup_location, setup_character):
        """Test that get_current_view returns correct moments."""
        # Create some moments first
        graph_ops.add_moment(
            id="e2e_view_1",
            text="View test moment 1",
            type="narration",
            tick=1440,
            place_id=setup_location,
            status="active",
            weight=0.9
        )

        graph_ops.add_moment(
            id="e2e_view_2",
            text="View test moment 2",
            type="dialogue",
            tick=1440,
            speaker=setup_character,
            place_id=setup_location,
            status="spoken",
            weight=1.0
        )

        # Query the view
        view = graph_queries.get_current_view(
            player_id="char_player",
            location_id=setup_location
        )

        assert view is not None
        assert "active_moments" in view or "moments" in view
        print(f"✓ Got current view with moments")


class TestE2EClickHandling:
    """Test the click-to-flip flow."""

    def test_click_triggers_weight_transfer(self, graph_ops, setup_location, setup_character):
        """Test that clicking a word transfers weight and can flip status."""
        # Setup: Main moment and possible target
        graph_ops.add_moment(
            id="e2e_click_main",
            text="He mentioned his brother once.",
            type="dialogue",
            tick=1440,
            speaker=setup_character,
            place_id=setup_location,
            status="active",
            weight=1.0
        )

        graph_ops.add_moment(
            id="e2e_click_target",
            text="",
            type="dialogue",
            tick=1440,
            place_id=setup_location,
            status="possible",
            weight=0.5  # Below 0.8 threshold
        )

        graph_ops.add_can_lead_to(
            from_moment_id="e2e_click_main",
            to_moment_id="e2e_click_target",
            trigger="player",
            require_words=["brother"],
            weight_transfer=0.4  # 0.5 + 0.4 = 0.9 > 0.8 threshold
        )

        # Click "brother"
        result = graph_ops.handle_click(
            moment_id="e2e_click_main",
            clicked_word="brother",
            player_id="char_player"
        )

        assert result["flipped"] == True
        assert len(result["flipped_moments"]) > 0
        assert result["queue_narrator"] == False  # We found a match

        # Verify target moment is now active
        check = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_click_target'})
            RETURN m.status, m.weight
        """)

        status, weight = check[0]
        assert status == "active"
        assert weight >= 0.8
        print(f"✓ Click triggered flip: weight={weight:.2f}, status={status}")

    def test_click_no_match(self, graph_ops, setup_location):
        """Test clicking a word with no matching transition."""
        graph_ops.add_moment(
            id="e2e_nomatch_main",
            text="Nothing special here.",
            type="narration",
            tick=1440,
            place_id=setup_location,
            status="active",
            weight=1.0
        )

        result = graph_ops.handle_click(
            moment_id="e2e_nomatch_main",
            clicked_word="nonexistent",
            player_id="char_player"
        )

        assert result["flipped"] == False
        assert result["queue_narrator"] == True  # Should queue narrator since no match
        print("✓ No match correctly handled")


class TestE2ELifecycle:
    """Test moment lifecycle: decay, dormancy, reactivation."""

    def test_decay_reduces_weight(self, graph_ops, setup_location):
        """Test that decay reduces weight of possible moments."""
        # Create a possible moment
        graph_ops.add_moment(
            id="e2e_decay_test",
            text="A fading possibility",
            type="dialogue",
            tick=1440,
            place_id=setup_location,
            status="possible",
            weight=0.5
        )

        # Apply decay multiple times
        for i in range(10):
            graph_ops.decay_moments(decay_rate=0.9, decay_threshold=0.1)

        # Check weight decreased
        result = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_decay_test'})
            RETURN m.weight, m.status
        """)

        # After 10 iterations at 0.9 rate: 0.5 * 0.9^10 ≈ 0.17
        weight, status = result[0]
        assert weight < 0.5
        print(f"✓ Decay reduced weight: 0.5 -> {weight:.3f}")

    def test_decay_to_decayed_status(self, graph_ops, setup_location):
        """Test that weight below threshold marks as decayed."""
        graph_ops.add_moment(
            id="e2e_decay_threshold",
            text="Will decay away",
            type="dialogue",
            tick=1440,
            place_id=setup_location,
            status="possible",
            weight=0.15  # Just above 0.1 threshold
        )

        # Apply decay
        graph_ops.decay_moments(decay_rate=0.5, decay_threshold=0.1, current_tick=1500)

        # Check status changed to decayed
        result = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_decay_threshold'})
            RETURN m.status, m.tick_decayed
        """)

        status, tick_decayed = result[0]
        assert status == "decayed"
        assert tick_decayed == 1500
        print(f"✓ Moment decayed at tick 1500")

    def test_dormancy_on_leave(self, graph_ops, setup_location):
        """Test that persistent moments go dormant when player leaves."""
        # Create moment attached to location with persistent=true
        graph_ops.add_moment(
            id="e2e_dormant_test",
            text="Location-specific dialogue",
            type="dialogue",
            tick=1440,
            place_id=setup_location,
            status="possible",
            weight=0.6
        )

        graph_ops.add_attached_to(
            moment_id="e2e_dormant_test",
            target_id=setup_location,
            presence_required=True,
            persistent=True
        )

        # Player leaves location
        result = graph_ops.on_player_leaves_location(setup_location)

        # Check moment is dormant
        check = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_dormant_test'})
            RETURN m.status
        """)

        status = check[0][0]
        assert status == "dormant"
        print(f"✓ Moment went dormant: {result}")

    def test_reactivation_on_arrive(self, graph_ops, setup_location):
        """Test that dormant moments reactivate when player returns."""
        # Create dormant moment
        graph_ops.add_moment(
            id="e2e_reactivate_test",
            text="Dormant dialogue",
            type="dialogue",
            tick=1440,
            place_id=setup_location,
            status="dormant",
            weight=0.6
        )

        graph_ops.add_attached_to(
            moment_id="e2e_reactivate_test",
            target_id=setup_location,
            presence_required=True,
            persistent=True
        )

        # Player arrives at location
        result = graph_ops.on_player_arrives_location(setup_location)

        # Check moment is possible again
        check = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_reactivate_test'})
            RETURN m.status
        """)

        status = check[0][0]
        assert status == "possible"
        print(f"✓ Moment reactivated: {result}")


class TestE2EFullFlow:
    """Test the complete narrator -> click -> response flow."""

    def test_complete_conversation_flow(self, graph_ops, graph_queries, setup_location, setup_character):
        """Simulate a complete conversation flow."""
        print("\n" + "="*60)
        print("E2E TEST: Complete Conversation Flow")
        print("="*60)

        # 1. Narrator creates dialogue with clickable
        print("\n1. Narrator creates dialogue...")
        main_id = graph_ops.add_moment(
            id="e2e_flow_main",
            text="The road to York is dangerous. Norman patrols everywhere.",
            type="dialogue",
            tick=1440,
            speaker=setup_character,
            place_id=setup_location,
            status="active",
            weight=1.0,
            tone="warning"
        )

        # Create possible responses
        york_response = graph_ops.add_moment(
            id="e2e_flow_york",
            text="York fell three months ago. The Normans hold it now.",
            type="dialogue",
            tick=1440,
            speaker=setup_character,
            place_id=setup_location,
            status="possible",
            weight=0.5,
            tone="grim"
        )

        norman_response = graph_ops.add_moment(
            id="e2e_flow_norman",
            text="They're ruthless. Burn villages for sport.",
            type="dialogue",
            tick=1440,
            speaker=setup_character,
            place_id=setup_location,
            status="possible",
            weight=0.5,
            tone="bitter"
        )

        # Link clickables
        graph_ops.add_can_lead_to(main_id, york_response, trigger="player",
                                  require_words=["York"], weight_transfer=0.4)
        graph_ops.add_can_lead_to(main_id, norman_response, trigger="player",
                                  require_words=["Norman"], weight_transfer=0.4)

        print(f"   Created: {main_id} with 2 clickables [York, Norman]")

        # 2. Query the view
        print("\n2. Frontend queries current view...")
        view = graph_queries.get_current_view(
            player_id="char_player",
            location_id=setup_location
        )
        print(f"   View has {len(view.get('active_moments', []))} active moments")

        # 3. Player clicks "York"
        print("\n3. Player clicks 'York'...")
        click_result = graph_ops.handle_click(
            moment_id=main_id,
            clicked_word="York",
            player_id="char_player"
        )

        print(f"   Flipped: {click_result['flipped']}")
        print(f"   Flipped moments: {len(click_result.get('flipped_moments', []))}")
        print(f"   Queue narrator: {click_result.get('queue_narrator')}")

        # 4. Verify York response is now active
        print("\n4. Verifying York response activated...")
        york_check = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_flow_york'})
            RETURN m.status, m.weight, m.text
        """)

        york_status, york_weight, york_text = york_check[0]
        assert york_status == "active"
        print(f"   Status: {york_status}")
        print(f"   Weight: {york_weight:.2f}")
        print(f"   Text: \"{york_text}\"")

        # 5. Time passes, decay applied
        print("\n5. Time passes (5 ticks of decay)...")
        for _ in range(5):
            graph_ops.decay_moments(decay_rate=0.95, decay_threshold=0.1)

        # 6. Check Norman response decayed slightly
        norman_check = graph_ops._query("""
            MATCH (m:Moment {id: 'e2e_flow_norman'})
            RETURN m.status, m.weight
        """)

        norman_status, norman_weight = norman_check[0]
        print(f"   Norman response weight: {norman_weight:.3f}")
        print(f"   (Started at 0.5, decayed by 0.95^5 = ~0.39)")

        print("\n" + "="*60)
        print("✓ E2E FLOW COMPLETE")
        print("="*60 + "\n")

        assert click_result["flipped"] == True
        assert york_status == "active"


# Run directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
