"""
Tests for the Moment Graph Architecture.

Specs:
- docs/engine/moments/VALIDATION_Moments.md
- docs/engine/moments/ALGORITHM_View_Query.md
- docs/engine/moments/ALGORITHM_Transitions.md
- docs/engine/moments/ALGORITHM_Lifecycle.md

Implementation:
- engine/physics/graph/graph_ops.py
- engine/physics/graph/graph_queries.py

Tests cover:
1. Schema/Node creation (add_moment, add_can_speak, add_attached_to, add_can_lead_to)
2. View queries (get_current_view, get_live_moments, resolve_speaker)
3. Click handling (handle_click, update_moment_weight)
4. SceneTree compatibility (view_to_scene_tree)
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_graph_ops():
    """Create a GraphOps instance with mocked database connection."""
    with patch('engine.physics.graph.graph_ops.FalkorDB') as mock_falkor:
        mock_graph = MagicMock()
        mock_falkor.return_value.select_graph.return_value = mock_graph

        from engine.physics.graph.graph_ops import GraphOps
        ops = GraphOps(graph_name="test_graph")
        ops._graph = mock_graph

        # Track queries for verification
        ops._queries = []
        original_query = ops._query

        def tracking_query(cypher, params=None):
            ops._queries.append({"cypher": cypher, "params": params})
            return []

        ops._query = tracking_query
        yield ops


@pytest.fixture
def mock_graph_queries():
    """Create a GraphQueries instance with mocked database connection."""
    with patch('engine.physics.graph.graph_queries.FalkorDB') as mock_falkor:
        mock_graph = MagicMock()
        mock_falkor.return_value.select_graph.return_value = mock_graph

        from engine.physics.graph.graph_queries import GraphQueries
        queries = GraphQueries(graph_name="test_graph")
        queries._graph = mock_graph
        queries._queries = []

        yield queries


# =============================================================================
# SCHEMA TESTS - Phase 1: Node/Link Creation
# =============================================================================

class TestMomentCreation:
    """Test add_moment() with extended schema fields."""

    def test_add_moment_basic(self, mock_graph_ops):
        """Test creating a basic moment with required fields."""
        moment_id = mock_graph_ops.add_moment(
            id="camp_d1_dawn_narration_001",
            text="The fire crackles softly.",
            type="narration",
            tick=1440
        )

        assert moment_id == "camp_d1_dawn_narration_001"
        assert len(mock_graph_ops._queries) >= 1

        # Check the MERGE query was issued
        cypher = mock_graph_ops._queries[0]["cypher"]
        assert "MERGE (n:Moment {id: $id})" in cypher

    def test_add_moment_with_status_and_weight(self, mock_graph_ops):
        """Test creating a moment with status and weight fields."""
        mock_graph_ops.add_moment(
            id="test_moment",
            text="A possible line of dialogue.",
            type="dialogue",
            tick=1440,
            status="possible",
            weight=0.6
        )

        # Verify props included status and weight
        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("status") == "possible"
        assert props.get("weight") == 0.6

    def test_add_moment_with_tone(self, mock_graph_ops):
        """Test moment with tone field."""
        mock_graph_ops.add_moment(
            id="test_moment",
            text="I swore an oath.",
            type="dialogue",
            tick=1440,
            tone="defiant"
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("tone") == "defiant"

    def test_add_moment_with_tick_spoken(self, mock_graph_ops):
        """Test moment with tick_spoken (for spoken moments)."""
        mock_graph_ops.add_moment(
            id="test_moment",
            text="Past dialogue.",
            type="dialogue",
            tick=1440,
            status="spoken",
            tick_spoken=1500
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("tick_spoken") == 1500

    def test_add_moment_with_speaker_creates_said_link(self, mock_graph_ops):
        """Test that speaker param creates SAID link."""
        mock_graph_ops.add_moment(
            id="test_dialogue",
            text="Aldric speaks.",
            type="dialogue",
            tick=1440,
            speaker="char_aldric"
        )

        # Should have moment creation + SAID link
        assert len(mock_graph_ops._queries) >= 2

        # Find the SAID query
        said_queries = [q for q in mock_graph_ops._queries if "SAID" in q["cypher"]]
        assert len(said_queries) >= 1

    def test_add_moment_with_place_creates_at_link(self, mock_graph_ops):
        """Test that place_id param creates AT link."""
        mock_graph_ops.add_moment(
            id="test_moment",
            text="At the camp.",
            type="narration",
            tick=1440,
            place_id="place_camp"
        )

        # Find the AT query
        at_queries = [q for q in mock_graph_ops._queries if "m)-[r:AT]->(p)" in q["cypher"]]
        assert len(at_queries) >= 1

    def test_add_moment_with_after_creates_then_link(self, mock_graph_ops):
        """Test that after_moment_id creates THEN link."""
        mock_graph_ops.add_moment(
            id="test_moment_2",
            text="Second line.",
            type="narration",
            tick=1440,
            after_moment_id="test_moment_1"
        )

        # Find the THEN query
        then_queries = [q for q in mock_graph_ops._queries if "THEN" in q["cypher"]]
        assert len(then_queries) >= 1


class TestCanSpeakLink:
    """Test add_can_speak() for CHARACTER -> MOMENT links."""

    def test_add_can_speak_basic(self, mock_graph_ops):
        """Test creating a CAN_SPEAK link with default weight."""
        mock_graph_ops.add_can_speak(
            character_id="char_aldric",
            moment_id="test_moment"
        )

        # Check query
        assert len(mock_graph_ops._queries) >= 1
        cypher = mock_graph_ops._queries[0]["cypher"]
        assert "CAN_SPEAK" in cypher

    def test_add_can_speak_with_weight(self, mock_graph_ops):
        """Test CAN_SPEAK with explicit weight."""
        mock_graph_ops.add_can_speak(
            character_id="char_aldric",
            moment_id="test_moment",
            weight=0.8
        )

        params = mock_graph_ops._queries[0]["params"]
        assert params.get("weight") == 0.8


class TestAttachedToLink:
    """Test add_attached_to() for MOMENT -> Target links."""

    def test_add_attached_to_basic(self, mock_graph_ops):
        """Test basic ATTACHED_TO link creation."""
        mock_graph_ops.add_attached_to(
            moment_id="test_moment",
            target_id="char_aldric"
        )

        cypher = mock_graph_ops._queries[0]["cypher"]
        assert "ATTACHED_TO" in cypher

    def test_add_attached_to_with_presence_required(self, mock_graph_ops):
        """Test ATTACHED_TO with presence_required=true."""
        mock_graph_ops.add_attached_to(
            moment_id="test_moment",
            target_id="char_aldric",
            presence_required=True
        )

        params = mock_graph_ops._queries[0]["params"]
        assert params.get("presence_required") == True

    def test_add_attached_to_non_persistent(self, mock_graph_ops):
        """Test ATTACHED_TO with persistent=false (ephemeral moment)."""
        mock_graph_ops.add_attached_to(
            moment_id="test_moment",
            target_id="place_camp",
            presence_required=True,
            persistent=False
        )

        params = mock_graph_ops._queries[0]["params"]
        assert params.get("persistent") == False

    def test_add_attached_to_dies_with_target(self, mock_graph_ops):
        """Test ATTACHED_TO with dies_with_target=true."""
        mock_graph_ops.add_attached_to(
            moment_id="test_moment",
            target_id="char_aldric",
            dies_with_target=True
        )

        params = mock_graph_ops._queries[0]["params"]
        assert params.get("dies_with_target") == True


class TestCanLeadToLink:
    """Test add_can_lead_to() for MOMENT -> MOMENT transitions."""

    def test_add_can_lead_to_basic(self, mock_graph_ops):
        """Test basic CAN_LEAD_TO link."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b"
        )

        cypher = mock_graph_ops._queries[0]["cypher"]
        assert "CAN_LEAD_TO" in cypher

    def test_add_can_lead_to_with_trigger(self, mock_graph_ops):
        """Test CAN_LEAD_TO with different triggers."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b",
            trigger="wait"
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("trigger") == "wait"

    def test_add_can_lead_to_with_require_words(self, mock_graph_ops):
        """Test CAN_LEAD_TO with clickable words."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b",
            trigger="player",
            require_words=["fire", "looks"]
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        require_words = props.get("require_words")
        assert require_words is not None
        # It should be JSON encoded
        words = json.loads(require_words)
        assert "fire" in words
        assert "looks" in words

    def test_add_can_lead_to_with_weight_transfer(self, mock_graph_ops):
        """Test CAN_LEAD_TO with custom weight transfer."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b",
            weight_transfer=0.5
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("weight_transfer") == 0.5

    def test_add_can_lead_to_bidirectional(self, mock_graph_ops):
        """Test bidirectional CAN_LEAD_TO creates two links."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b",
            bidirectional=True
        )

        # Should have created two CAN_LEAD_TO links
        can_lead_to_queries = [q for q in mock_graph_ops._queries if "CAN_LEAD_TO" in q["cypher"]]
        assert len(can_lead_to_queries) >= 2

    def test_add_can_lead_to_with_wait_ticks(self, mock_graph_ops):
        """Test CAN_LEAD_TO with wait trigger and ticks."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b",
            trigger="wait",
            wait_ticks=5
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("wait_ticks") == 5

    def test_add_can_lead_to_consumes_origin_false(self, mock_graph_ops):
        """Test CAN_LEAD_TO with consumes_origin=false."""
        mock_graph_ops.add_can_lead_to(
            from_moment_id="moment_a",
            to_moment_id="moment_b",
            consumes_origin=False
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("consumes_origin") == False


# =============================================================================
# VIEW QUERY TESTS - Phase 2: View Queries
# =============================================================================

class TestGetCurrentView:
    """Test get_current_view() main query method."""

    def test_get_current_view_returns_structure(self, mock_graph_queries):
        """Test that get_current_view returns expected structure."""
        # Mock the sub-methods
        mock_graph_queries.get_characters_at = MagicMock(return_value=[
            {"id": "char_aldric", "name": "Aldric"}
        ])
        mock_graph_queries.get_place = MagicMock(return_value={
            "id": "place_camp", "name": "Camp"
        })
        mock_graph_queries.get_live_moments = MagicMock(return_value=[])
        mock_graph_queries.get_available_transitions = MagicMock(return_value=[])

        result = mock_graph_queries.get_current_view(
            player_id="char_player",
            location_id="place_camp"
        )

        assert "location" in result
        assert "characters" in result
        assert "active_moments" in result
        assert "possible_moments" in result
        assert "transitions" in result

    def test_get_current_view_queries_present_characters(self, mock_graph_queries):
        """Test that view query fetches present characters."""
        mock_graph_queries.get_characters_at = MagicMock(return_value=[
            {"id": "char_aldric", "name": "Aldric"},
            {"id": "char_player", "name": "Player"}
        ])
        mock_graph_queries.get_place = MagicMock(return_value={"id": "place_camp"})
        mock_graph_queries.get_live_moments = MagicMock(return_value=[])
        mock_graph_queries.get_available_transitions = MagicMock(return_value=[])

        result = mock_graph_queries.get_current_view(
            player_id="char_player",
            location_id="place_camp"
        )

        mock_graph_queries.get_characters_at.assert_called_once_with("place_camp")
        assert len(result["characters"]) == 2


class TestGetLiveMoments:
    """Test get_live_moments() presence gating query."""

    def test_get_live_moments_builds_correct_query(self, mock_graph_queries):
        """Test that get_live_moments constructs proper Cypher."""
        mock_graph_queries._query = MagicMock(return_value=[])

        mock_graph_queries.get_live_moments(
            location_id="place_camp",
            present_character_ids=["char_aldric", "char_player"],
            status_filter=["possible", "active"]
        )

        # Verify query was called
        mock_graph_queries._query.assert_called_once()
        cypher = mock_graph_queries._query.call_args[0][0]

        # Check key parts of the query
        assert "MATCH (m:Moment)" in cypher
        assert "status IN" in cypher
        assert "ATTACHED_TO" in cypher
        assert "CAN_SPEAK" in cypher


class TestResolveSpeaker:
    """Test resolve_speaker() for finding who speaks a moment."""

    def test_resolve_speaker_returns_highest_weight(self, mock_graph_queries):
        """Test speaker resolution returns highest-weight present character."""
        # Mock query result: Aldric (0.9) beats Wulfric (0.7)
        mock_graph_queries._query = MagicMock(return_value=[
            ("char_aldric", "Aldric", 0.9)
        ])
        mock_graph_queries._parse_node = MagicMock(return_value={
            "id": "char_aldric",
            "name": "Aldric",
            "weight": 0.9
        })

        result = mock_graph_queries.resolve_speaker(
            moment_id="test_moment",
            present_character_ids=["char_aldric", "char_wulfric"]
        )

        assert result is not None
        assert result["id"] == "char_aldric"

    def test_resolve_speaker_none_when_no_speakers(self, mock_graph_queries):
        """Test speaker resolution returns None when no one can speak."""
        mock_graph_queries._query = MagicMock(return_value=[])

        result = mock_graph_queries.resolve_speaker(
            moment_id="test_moment",
            present_character_ids=["char_player"]
        )

        assert result is None


class TestGetAvailableTransitions:
    """Test get_available_transitions() for CAN_LEAD_TO queries."""

    def test_get_available_transitions_from_active(self, mock_graph_queries):
        """Test getting transitions from active moments."""
        mock_graph_queries._query = MagicMock(return_value=[
            ("moment_a", "moment_b", "player", '["fire"]', 0.3, False, True)
        ])
        mock_graph_queries._parse_node = MagicMock(return_value={
            "from_id": "moment_a",
            "to_id": "moment_b",
            "trigger": "player",
            "require_words": '["fire"]',
            "weight_transfer": 0.3,
            "bidirectional": False,
            "consumes_origin": True
        })

        result = mock_graph_queries.get_available_transitions(
            active_moment_ids=["moment_a"]
        )

        assert len(result) == 1
        assert result[0]["from_id"] == "moment_a"
        assert result[0]["to_id"] == "moment_b"

    def test_get_available_transitions_empty_for_no_active(self, mock_graph_queries):
        """Test transitions returns empty for empty active list."""
        result = mock_graph_queries.get_available_transitions(
            active_moment_ids=[]
        )

        assert result == []


class TestGetClickableWords:
    """Test get_clickable_words() for extracting clickables."""

    def test_get_clickable_words_extracts_from_transitions(self, mock_graph_queries):
        """Test clickable words are extracted from CAN_LEAD_TO links."""
        mock_graph_queries._query = MagicMock(return_value=[
            ('["fire", "looks"]', "moment_b", 0.3)
        ])

        result = mock_graph_queries.get_clickable_words(
            moment_id="moment_a"
        )

        assert len(result) == 2
        words = [r["word"] for r in result]
        assert "fire" in words
        assert "looks" in words


# =============================================================================
# CLICK HANDLER TESTS - Phase 3: Click Handling
# =============================================================================

class TestHandleClick:
    """Test handle_click() instant response mechanism."""

    def test_handle_click_no_transitions_queues_narrator(self, mock_graph_ops):
        """Test click with no matching transitions queues narrator."""
        mock_graph_ops._query = MagicMock(return_value=[])

        result = mock_graph_ops.handle_click(
            moment_id="test_moment",
            clicked_word="random",
            player_id="char_player"
        )

        assert result["flipped"] == False
        assert result["flipped_moments"] == []
        assert result["queue_narrator"] == True

    def test_handle_click_word_not_in_require_words(self, mock_graph_ops):
        """Test click with word not matching require_words."""
        # Return a transition but word won't match
        mock_graph_ops._query = MagicMock(return_value=[
            ("moment_b", "Target text", "dialogue", "possible", 0.5, '["fire"]', 0.3, True)
        ])

        result = mock_graph_ops.handle_click(
            moment_id="test_moment",
            clicked_word="random",  # Not "fire"
            player_id="char_player"
        )

        # Word doesn't match, so should queue narrator
        assert result["queue_narrator"] == True

    def test_handle_click_applies_weight_transfer(self, mock_graph_ops):
        """Test click applies weight transfer to target."""
        # Track query calls
        query_calls = []

        def tracking_query(cypher, params=None):
            query_calls.append({"cypher": cypher, "params": params})
            # First call: find transitions
            if "CAN_LEAD_TO" in cypher and "RETURN" in cypher:
                return [
                    ("moment_b", "Target text", "dialogue", "possible", 0.5, '["fire"]', 0.3, True)
                ]
            return []

        mock_graph_ops._query = tracking_query

        result = mock_graph_ops.handle_click(
            moment_id="test_moment",
            clicked_word="fire",
            player_id="char_player"
        )

        # Should have weight updates
        assert len(result["weight_updates"]) > 0
        # New weight should be 0.5 + 0.3 = 0.8
        assert result["weight_updates"][0]["new_weight"] == 0.8

    def test_handle_click_flip_threshold(self, mock_graph_ops):
        """Test click flips moment when weight >= 0.8."""
        def tracking_query(cypher, params=None):
            if "CAN_LEAD_TO" in cypher and "RETURN" in cypher:
                # Target starts at 0.5, transfer 0.3 = 0.8 = flip
                return [
                    ("moment_b", "Target text", "dialogue", "possible", 0.5, '["fire"]', 0.3, True)
                ]
            return []

        mock_graph_ops._query = tracking_query

        result = mock_graph_ops.handle_click(
            moment_id="test_moment",
            clicked_word="fire",
            player_id="char_player"
        )

        assert result["flipped"] == True
        assert len(result["flipped_moments"]) == 1
        assert result["flipped_moments"][0]["id"] == "moment_b"

    def test_handle_click_no_flip_below_threshold(self, mock_graph_ops):
        """Test click doesn't flip when weight < 0.8."""
        def tracking_query(cypher, params=None):
            if "CAN_LEAD_TO" in cypher and "RETURN" in cypher:
                # Target starts at 0.3, transfer 0.3 = 0.6 < 0.8 = no flip
                return [
                    ("moment_b", "Target text", "dialogue", "possible", 0.3, '["fire"]', 0.3, True)
                ]
            return []

        mock_graph_ops._query = tracking_query

        result = mock_graph_ops.handle_click(
            moment_id="test_moment",
            clicked_word="fire",
            player_id="char_player"
        )

        assert result["flipped"] == False
        assert result["queue_narrator"] == True


class TestUpdateMomentWeight:
    """Test update_moment_weight() manual weight updates."""

    def test_update_weight_clamps_to_bounds(self, mock_graph_ops):
        """Test weight is clamped between 0 and 1."""
        def tracking_query(cypher, params=None):
            if "RETURN m.weight" in cypher:
                return [(0.9, "possible")]  # Current weight 0.9
            return []

        mock_graph_ops._query = tracking_query

        # Try to add 0.5 (would be 1.4, should clamp to 1.0)
        result = mock_graph_ops.update_moment_weight(
            moment_id="test_moment",
            weight_delta=0.5
        )

        assert result["new_weight"] == 1.0

    def test_update_weight_triggers_flip(self, mock_graph_ops):
        """Test weight update that crosses threshold triggers flip."""
        query_calls = []

        def tracking_query(cypher, params=None):
            query_calls.append({"cypher": cypher, "params": params})
            if "RETURN m.weight" in cypher:
                return [(0.7, "possible")]
            return []

        mock_graph_ops._query = tracking_query

        result = mock_graph_ops.update_moment_weight(
            moment_id="test_moment",
            weight_delta=0.2  # 0.7 + 0.2 = 0.9 >= 0.8
        )

        assert result["flipped"] == True

    def test_update_weight_no_flip_already_active(self, mock_graph_ops):
        """Test weight update doesn't flip already active moments."""
        def tracking_query(cypher, params=None):
            if "RETURN m.weight" in cypher:
                return [(0.5, "active")]  # Already active
            return []

        mock_graph_ops._query = tracking_query

        result = mock_graph_ops.update_moment_weight(
            moment_id="test_moment",
            weight_delta=0.5  # Would exceed threshold
        )

        assert result["flipped"] == False  # Already active, no flip


# =============================================================================
# SCENE TREE COMPATIBILITY TESTS
# =============================================================================

class TestViewToSceneTree:
    """Test view_to_scene_tree() backward compatibility conversion."""

    def test_view_to_scene_tree_basic_structure(self):
        """Test SceneTree conversion produces expected structure."""
        from engine.physics.graph.graph_queries import view_to_scene_tree

        view_result = {
            "location": {"id": "place_camp", "name": "Camp", "type": "wilderness"},
            "characters": [{"id": "char_aldric"}, {"id": "char_player"}],
            "active_moments": [
                {
                    "id": "moment_1",
                    "text": "The fire crackles.",
                    "speaker": None
                }
            ],
            "possible_moments": [],
            "transitions": []
        }

        scene_tree = view_to_scene_tree(view_result)

        assert "id" in scene_tree
        assert "location" in scene_tree
        assert "characters" in scene_tree
        assert "narration" in scene_tree
        assert scene_tree["location"]["place"] == "place_camp"

    def test_view_to_scene_tree_with_clickables(self):
        """Test SceneTree includes clickables from transitions."""
        from engine.physics.graph.graph_queries import view_to_scene_tree

        view_result = {
            "location": {"id": "place_camp", "name": "Camp"},
            "characters": [],
            "active_moments": [
                {"id": "moment_1", "text": "He looks at the fire.", "speaker": None}
            ],
            "possible_moments": [],
            "transitions": [
                {
                    "from_id": "moment_1",
                    "to_id": "moment_2",
                    "trigger": "player",
                    "require_words": '["fire"]',
                    "weight_transfer": 0.3
                }
            ]
        }

        scene_tree = view_to_scene_tree(view_result)

        # First narration should have clickable
        assert len(scene_tree["narration"]) == 1
        assert "clickable" in scene_tree["narration"][0]
        assert "fire" in scene_tree["narration"][0]["clickable"]


# =============================================================================
# INVARIANT TESTS - From VALIDATION_Moments.md
# =============================================================================

class TestInvariants:
    """Test system invariants that must always hold."""

    def test_weight_bounds_invariant(self, mock_graph_ops):
        """Weight must always be 0-1."""
        # Test that add_moment with invalid weight would be caught
        # (Currently no validation in add_moment, this tests behavior)
        mock_graph_ops.add_moment(
            id="test",
            text="test",
            weight=0.5
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        weight = props.get("weight")
        assert 0 <= weight <= 1

    def test_status_consistency_invariant(self, mock_graph_ops):
        """Spoken moments should have tick_spoken set."""
        # When creating a spoken moment, tick_spoken should be provided
        mock_graph_ops.add_moment(
            id="spoken_moment",
            text="Past dialogue",
            status="spoken",
            tick=1440,
            tick_spoken=1440
        )

        params = mock_graph_ops._queries[0]["params"]
        props = params.get("props", {})
        assert props.get("tick_spoken") is not None


# =============================================================================
# BEHAVIORAL TESTS - From VALIDATION_Moments.md
# =============================================================================

class TestBehavioralVisibility:
    """Test visibility by attachment behavior."""

    def test_presence_required_filters_correctly(self, mock_graph_queries):
        """Moments with presence_required should only show when target present."""
        # This is tested via the query structure
        mock_graph_queries._query = MagicMock(return_value=[])

        mock_graph_queries.get_live_moments(
            location_id="place_camp",
            present_character_ids=["char_player"],  # Aldric NOT present
            status_filter=["possible"]
        )

        cypher = mock_graph_queries._query.call_args[0][0]

        # Query should check presence_required attachments
        assert "presence_required" in cypher
        # Query should filter by present characters
        assert "char_player" in cypher


class TestBehavioralSpeakerResolution:
    """Test speaker resolution behavior."""

    def test_speaker_resolution_by_weight(self, mock_graph_queries):
        """Highest-weight present character should speak."""
        # Return ordered by weight DESC
        mock_graph_queries._query = MagicMock(return_value=[
            ("char_aldric", "Aldric", 0.9)
        ])
        mock_graph_queries._parse_node = MagicMock(return_value={
            "id": "char_aldric", "name": "Aldric", "weight": 0.9
        })

        result = mock_graph_queries.resolve_speaker(
            moment_id="test",
            present_character_ids=["char_aldric", "char_wulfric"]
        )

        # Query should ORDER BY weight DESC
        cypher = mock_graph_queries._query.call_args[0][0]
        assert "ORDER BY r.weight DESC" in cypher


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegrationConversationFlow:
    """Integration tests for complete conversation flows."""

    def test_moment_creation_and_linking_flow(self, mock_graph_ops):
        """Test creating a conversation with moments and transitions."""
        # Create moment 1 (opening)
        mock_graph_ops.add_moment(
            id="m1",
            text="Aldric looks at the fire.",
            type="narration",
            status="active",
            tick=1440
        )

        # Create moment 2 (response)
        mock_graph_ops.add_moment(
            id="m2",
            text="Three days now.",
            type="dialogue",
            status="possible",
            weight=0.5,
            tick=1440
        )

        # Link them
        mock_graph_ops.add_can_lead_to(
            from_moment_id="m1",
            to_moment_id="m2",
            trigger="player",
            require_words=["fire", "looks"]
        )

        # Add speaker
        mock_graph_ops.add_can_speak(
            character_id="char_aldric",
            moment_id="m2"
        )

        # Add attachment
        mock_graph_ops.add_attached_to(
            moment_id="m2",
            target_id="char_aldric",
            presence_required=True
        )

        # Verify all queries were issued
        assert len(mock_graph_ops._queries) >= 5  # 2 moments + 1 transition + 1 speaker + 1 attachment

    def test_click_to_flip_flow(self, mock_graph_ops):
        """Test clicking a word to flip a moment to active."""
        # Setup: click returns a matching transition
        def flow_query(cypher, params=None):
            if "CAN_LEAD_TO" in cypher and "WHERE r.trigger" in cypher:
                # Return target at weight 0.5, will flip to 0.8+
                return [
                    ("m2", "Three days now.", "dialogue", "possible", 0.5, '["fire"]', 0.3, True)
                ]
            return []

        mock_graph_ops._query = flow_query

        result = mock_graph_ops.handle_click(
            moment_id="m1",
            clicked_word="fire",
            player_id="char_player"
        )

        assert result["flipped"] == True
        assert result["flipped_moments"][0]["text"] == "Three days now."


# =============================================================================
# EXTRACT MOMENT ARGS TEST (from test_moment.py pattern)
# =============================================================================

class TestExtractMomentArgs:
    """Test _extract_moment_args helper method."""

    def test_extract_moment_args_basic(self):
        """Test extracting moment arguments from query result."""
        from engine.physics.graph.graph_ops import GraphOps

        # Create instance without connecting
        ops = GraphOps.__new__(GraphOps)

        node = {
            'id': 'camp_d1_night_dialogue_001',
            'text': 'I swore an oath.',
            'moment_type': 'dialogue',
            'tick': 1440,
            'speaker': 'char_aldric',
            'place_id': 'place_camp',
            'line': 42,
            'status': 'spoken',
            'weight': 0.7,
            'tone': 'defiant'
        }

        args = ops._extract_moment_args(node)

        assert args['id'] == 'camp_d1_night_dialogue_001'
        assert args['text'] == 'I swore an oath.'
        assert args['type'] == 'dialogue'
        assert args['tick'] == 1440
        assert args['speaker'] == 'char_aldric'


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
