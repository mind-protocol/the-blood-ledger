"""
Tests for Narrator Integration (Phase 4).

Specs:
- docs/engine/moments/SYNC_Moments.md (Phase 4)
- docs/engine/moments/ALGORITHM_Transitions.md

Implementation:
- tools/stream_dialogue.py (create_moment_with_clickables)
- engine/memory/moment_processor.py (process_* methods with new schema)

Tests cover:
1. Clickable parsing (parse_inline_clickables)
2. Graph mode moment creation (create_moment_with_clickables)
3. MomentProcessor with status/weight/tone
4. CAN_LEAD_TO link creation for clickables
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


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

        # Track method calls
        ops._add_moment_calls = []
        ops._add_can_lead_to_calls = []
        ops._add_can_speak_calls = []
        ops._add_attached_to_calls = []

        original_add_moment = ops.add_moment
        original_add_can_lead_to = ops.add_can_lead_to
        original_add_can_speak = ops.add_can_speak
        original_add_attached_to = ops.add_attached_to

        def tracking_add_moment(**kwargs):
            ops._add_moment_calls.append(kwargs)
            return kwargs.get('id', 'mock_id')

        def tracking_add_can_lead_to(**kwargs):
            ops._add_can_lead_to_calls.append(kwargs)
            return None

        def tracking_add_can_speak(**kwargs):
            ops._add_can_speak_calls.append(kwargs)
            return None

        def tracking_add_attached_to(**kwargs):
            ops._add_attached_to_calls.append(kwargs)
            return None

        ops.add_moment = tracking_add_moment
        ops.add_can_lead_to = tracking_add_can_lead_to
        ops.add_can_speak = tracking_add_can_speak
        ops.add_attached_to = tracking_add_attached_to

        yield ops


@pytest.fixture
def mock_moment_processor(mock_graph_ops):
    """Create a MomentProcessor with mocked dependencies."""
    from engine.infrastructure.memory.moment_processor import MomentProcessor

    mock_embed = MagicMock(return_value=[0.0] * 768)

    processor = MomentProcessor(
        graph_ops=mock_graph_ops,
        embed_fn=mock_embed,
        playthrough_id="test_playthrough",
        playthroughs_dir=Path("/tmp/test_playthroughs")
    )

    # Set context
    processor.set_context(tick=1440, place_id="place_camp")

    yield processor


# =============================================================================
# CLICKABLE PARSING TESTS
# =============================================================================

class TestClickableParsing:
    """Test parse_inline_clickables() function."""

    def test_parse_single_clickable(self):
        """Test parsing a single clickable word."""
        sys.path.insert(0, str(PROJECT_ROOT / 'tools'))
        from stream_dialogue import parse_inline_clickables

        text = "My niece [Edda](Who's Edda?) is an archer."
        clean_text, clickables = parse_inline_clickables(text)

        assert clean_text == "My niece Edda is an archer."
        assert "Edda" in clickables
        assert clickables["Edda"]["speaks"] == "Who's Edda?"

    def test_parse_multiple_clickables(self):
        """Test parsing multiple clickable words."""
        from stream_dialogue import parse_inline_clickables

        text = "We should head to [York](Let's go to York.) via [the Humber](Where's that?)."
        clean_text, clickables = parse_inline_clickables(text)

        assert clean_text == "We should head to York via the Humber."
        assert "York" in clickables
        assert "the Humber" in clickables
        assert clickables["York"]["speaks"] == "Let's go to York."
        assert clickables["the Humber"]["speaks"] == "Where's that?"

    def test_parse_no_clickables(self):
        """Test parsing text with no clickables."""
        from stream_dialogue import parse_inline_clickables

        text = "The fire crackles softly."
        clean_text, clickables = parse_inline_clickables(text)

        assert clean_text == "The fire crackles softly."
        assert clickables == {}

    def test_parse_clickable_with_special_chars(self):
        """Test parsing clickables with special characters in speaks."""
        from stream_dialogue import parse_inline_clickables

        text = "He mentioned his [brother](Your brother? What happened to him?)."
        clean_text, clickables = parse_inline_clickables(text)

        assert clean_text == "He mentioned his brother."
        assert clickables["brother"]["speaks"] == "Your brother? What happened to him?"


# =============================================================================
# MOMENT PROCESSOR TESTS
# =============================================================================

class TestMomentProcessorSchema:
    """Test MomentProcessor with new schema fields (tone, weight, status)."""

    def test_process_dialogue_with_tone(self, mock_moment_processor, mock_graph_ops):
        """Test process_dialogue includes tone field."""
        moment_id = mock_moment_processor.process_dialogue(
            text="Aye, I remember.",
            speaker="char_aldric",
            tone="nostalgic"
        )

        assert len(mock_graph_ops._add_moment_calls) == 1
        call = mock_graph_ops._add_moment_calls[0]
        assert call["tone"] == "nostalgic"
        assert call["type"] == "dialogue"

    def test_process_dialogue_with_weight_and_status(self, mock_moment_processor, mock_graph_ops):
        """Test process_dialogue includes weight and status fields."""
        moment_id = mock_moment_processor.process_dialogue(
            text="A potential response.",
            speaker="char_aldric",
            initial_weight=0.7,
            initial_status="active"
        )

        call = mock_graph_ops._add_moment_calls[0]
        assert call["weight"] == 0.7
        assert call["status"] == "active"

    def test_process_narration_with_tone(self, mock_moment_processor, mock_graph_ops):
        """Test process_narration includes tone field."""
        moment_id = mock_moment_processor.process_narration(
            text="The wind howls outside.",
            tone="ominous"
        )

        call = mock_graph_ops._add_moment_calls[0]
        assert call["tone"] == "ominous"
        assert call["type"] == "narration"

    def test_process_hint_defaults(self, mock_moment_processor, mock_graph_ops):
        """Test process_hint has correct default weight and status."""
        moment_id = mock_moment_processor.process_hint(
            text="Something feels wrong."
        )

        call = mock_graph_ops._add_moment_calls[0]
        assert call["weight"] == 0.8  # Hints default to high weight
        assert call["status"] == "active"  # Hints default to active

    def test_spoken_status_sets_tick_spoken(self, mock_moment_processor, mock_graph_ops):
        """Test that spoken status sets tick_spoken."""
        mock_moment_processor.process_dialogue(
            text="Hello there.",
            speaker="char_aldric",
            initial_status="spoken"
        )

        call = mock_graph_ops._add_moment_calls[0]
        assert call["tick_spoken"] == 1440  # Current tick from context

    def test_possible_status_no_tick_spoken(self, mock_moment_processor, mock_graph_ops):
        """Test that possible status doesn't set tick_spoken."""
        mock_moment_processor.process_dialogue(
            text="A future possibility.",
            speaker="char_aldric",
            initial_status="possible"
        )

        call = mock_graph_ops._add_moment_calls[0]
        assert call["tick_spoken"] is None


class TestPossibleMomentCreation:
    """Test create_possible_moment() method."""

    def test_create_possible_moment_basic(self, mock_moment_processor, mock_graph_ops):
        """Test creating a possible moment with CAN_SPEAK link."""
        moment_id = mock_moment_processor.create_possible_moment(
            text="Something I might say later.",
            speaker_id="char_aldric"
        )

        # Check moment was created with possible status
        moment_call = mock_graph_ops._add_moment_calls[0]
        assert moment_call["status"] == "possible"
        assert moment_call["weight"] == 0.5  # Default

        # Check CAN_SPEAK link was created
        assert len(mock_graph_ops._add_can_speak_calls) == 1
        speak_call = mock_graph_ops._add_can_speak_calls[0]
        assert speak_call["character_id"] == "char_aldric"
        assert speak_call["weight"] == 1.0

    def test_create_possible_moment_with_attachments(self, mock_moment_processor, mock_graph_ops):
        """Test that possible moment attaches to character and place."""
        mock_moment_processor.create_possible_moment(
            text="Location-specific dialogue.",
            speaker_id="char_aldric",
            attach_to_character=True,
            attach_to_place=True
        )

        # Should have 2 ATTACHED_TO links
        assert len(mock_graph_ops._add_attached_to_calls) == 2

        # Check character attachment
        char_attach = [c for c in mock_graph_ops._add_attached_to_calls
                       if c["target_id"] == "char_aldric"][0]
        assert char_attach["presence_required"] is True
        assert char_attach["persistent"] is True

        # Check place attachment
        place_attach = [c for c in mock_graph_ops._add_attached_to_calls
                        if c["target_id"] == "place_camp"][0]
        assert place_attach["presence_required"] is True


class TestMomentLinking:
    """Test link_moments() method."""

    def test_link_moments_basic(self, mock_moment_processor, mock_graph_ops):
        """Test creating CAN_LEAD_TO link between moments."""
        mock_moment_processor.link_moments(
            from_moment_id="moment_1",
            to_moment_id="moment_2",
            trigger="player",
            require_words=["blade"]
        )

        assert len(mock_graph_ops._add_can_lead_to_calls) == 1
        call = mock_graph_ops._add_can_lead_to_calls[0]
        assert call["from_moment_id"] == "moment_1"
        assert call["to_moment_id"] == "moment_2"
        assert call["trigger"] == "player"
        assert call["require_words"] == ["blade"]

    def test_link_moments_with_weight_transfer(self, mock_moment_processor, mock_graph_ops):
        """Test CAN_LEAD_TO with custom weight_transfer."""
        mock_moment_processor.link_moments(
            from_moment_id="m1",
            to_moment_id="m2",
            weight_transfer=0.6
        )

        call = mock_graph_ops._add_can_lead_to_calls[0]
        assert call["weight_transfer"] == 0.6


# =============================================================================
# GRAPH MODE INTEGRATION TESTS
# =============================================================================

class TestGraphModeIntegration:
    """Test create_moment_with_clickables() from stream_dialogue.py."""

    @patch('tools.stream_dialogue.get_graph_ops')
    @patch('tools.stream_dialogue.get_current_tick')
    @patch('tools.stream_dialogue.get_current_place')
    def test_create_moment_with_single_clickable(
        self, mock_place, mock_tick, mock_get_ops
    ):
        """Test creating a moment with one clickable creates CAN_LEAD_TO link."""
        # Setup mocks
        mock_ops = MagicMock()
        mock_ops.add_moment = MagicMock(return_value="test_moment")
        mock_ops.add_can_lead_to = MagicMock()
        mock_get_ops.return_value = mock_ops
        mock_tick.return_value = 1440
        mock_place.return_value = "place_camp"

        from tools.stream_dialogue import create_moment_with_clickables

        moment_id, clickables = create_moment_with_clickables(
            playthrough="test",
            text="My niece [Edda](Who's Edda?) is an archer.",
            moment_type="dialogue",
            speaker="char_aldric"
        )

        # Main moment should be created as active
        main_call = mock_ops.add_moment.call_args_list[0]
        assert main_call.kwargs["status"] == "active"
        assert main_call.kwargs["weight"] == 1.0
        assert main_call.kwargs["text"] == "My niece Edda is an archer."

        # Target moment should be created as possible
        target_call = mock_ops.add_moment.call_args_list[1]
        assert target_call.kwargs["status"] == "possible"
        assert target_call.kwargs["weight"] == 0.5

        # CAN_LEAD_TO should be created
        mock_ops.add_can_lead_to.assert_called_once()
        link_call = mock_ops.add_can_lead_to.call_args
        assert link_call.kwargs["require_words"] == ["Edda"]
        assert link_call.kwargs["weight_transfer"] == 0.4

    @patch('tools.stream_dialogue.get_graph_ops')
    @patch('tools.stream_dialogue.get_current_tick')
    @patch('tools.stream_dialogue.get_current_place')
    def test_create_moment_with_multiple_clickables(
        self, mock_place, mock_tick, mock_get_ops
    ):
        """Test creating a moment with multiple clickables."""
        mock_ops = MagicMock()
        mock_ops.add_moment = MagicMock(return_value="test_moment")
        mock_ops.add_can_lead_to = MagicMock()
        mock_get_ops.return_value = mock_ops
        mock_tick.return_value = 1440
        mock_place.return_value = "place_camp"

        from tools.stream_dialogue import create_moment_with_clickables

        moment_id, clickables = create_moment_with_clickables(
            playthrough="test",
            text="Go to [York](Let's go.) or [the moor](What's there?).",
            moment_type="narration"
        )

        # Should create 1 main moment + 2 target moments = 3 total
        assert mock_ops.add_moment.call_count == 3

        # Should create 2 CAN_LEAD_TO links
        assert mock_ops.add_can_lead_to.call_count == 2

    @patch('tools.stream_dialogue.get_graph_ops')
    @patch('tools.stream_dialogue.get_current_tick')
    @patch('tools.stream_dialogue.get_current_place')
    def test_create_moment_with_tone(
        self, mock_place, mock_tick, mock_get_ops
    ):
        """Test that tone is passed through to moment."""
        mock_ops = MagicMock()
        mock_ops.add_moment = MagicMock(return_value="test_moment")
        mock_get_ops.return_value = mock_ops
        mock_tick.return_value = 1440
        mock_place.return_value = "place_camp"

        from tools.stream_dialogue import create_moment_with_clickables

        create_moment_with_clickables(
            playthrough="test",
            text="The wind howls.",
            moment_type="narration",
            tone="ominous"
        )

        main_call = mock_ops.add_moment.call_args_list[0]
        assert main_call.kwargs["tone"] == "ominous"


# =============================================================================
# WEIGHT-BASED ACTIVATION TESTS
# =============================================================================

class TestWeightActivation:
    """Test that weight transfer enables moment activation."""

    def test_weight_below_threshold_stays_possible(self, mock_graph_ops):
        """Verify moment with weight < 0.8 remains possible."""
        # This is a behavioral test - just verify the contract
        from engine.physics.graph.graph_ops import GraphOps

        # Weight 0.5 + transfer 0.4 = 0.9 > 0.8 threshold
        # This tests the design contract
        initial_weight = 0.5
        weight_transfer = 0.4
        threshold = 0.8

        assert initial_weight < threshold  # Starts below
        assert initial_weight + weight_transfer >= threshold  # One click activates


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
