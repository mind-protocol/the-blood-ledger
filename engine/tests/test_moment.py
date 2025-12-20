"""
Tests for the Moment system.

Specs: docs/engine/moments/VALIDATION_Moments.md and docs/engine/moments/ALGORITHM_*.md

Tests:
1. Moment creation via GraphOps
2. Moment queries via GraphQueries
3. MomentProcessor end-to-end
4. Transcript management
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.models.base import MomentType
from engine.models.nodes import Moment


class TestMomentModel:
    """Test the Moment Pydantic model."""

    def test_moment_creation(self):
        """Test creating a Moment model."""
        moment = Moment(
            id="camp_d1_night_dialogue_001",
            text="I swore an oath.",
            type=MomentType.DIALOGUE,
            tick=1440,
            speaker="char_aldric"
        )

        assert moment.id == "camp_d1_night_dialogue_001"
        assert moment.text == "I swore an oath."
        assert moment.type == MomentType.DIALOGUE
        assert moment.tick == 1440
        assert moment.speaker == "char_aldric"

    def test_embeddable_text_dialogue(self):
        """Test embeddable text for dialogue includes speaker."""
        moment = Moment(
            id="test",
            text="Hello there.",
            type=MomentType.DIALOGUE,
            tick=0,
            speaker="char_aldric"
        )

        assert moment.embeddable_text() == "char_aldric: Hello there."

    def test_embeddable_text_narration(self):
        """Test embeddable text for narration is just text."""
        moment = Moment(
            id="test",
            text="The fire crackles.",
            type=MomentType.NARRATION,
            tick=0
        )

        assert moment.embeddable_text() == "The fire crackles."

    def test_should_embed_long_text(self):
        """Test should_embed is True for text > 20 chars."""
        moment = Moment(
            id="test",
            text="This is a longer piece of text that should be embedded.",
            type=MomentType.NARRATION,
            tick=0
        )

        assert moment.should_embed is True

    def test_should_embed_short_text(self):
        """Test should_embed is False for short text."""
        moment = Moment(
            id="test",
            text="Short.",
            type=MomentType.NARRATION,
            tick=0
        )

        assert moment.should_embed is False


class TestMomentGraphOps:
    """Test GraphOps moment methods (mocked)."""

    def test_extract_moment_args(self):
        """Test _extract_moment_args extracts correct fields."""
        # Import here to avoid connection issues
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
            'line': 42
        }

        args = ops._extract_moment_args(node)

        assert args['id'] == 'camp_d1_night_dialogue_001'
        assert args['text'] == 'I swore an oath.'
        assert args['type'] == 'dialogue'
        assert args['tick'] == 1440
        assert args['speaker'] == 'char_aldric'
        assert args['place_id'] == 'place_camp'
        assert args['line'] == 42


class TestMomentProcessor:
    """Test MomentProcessor."""

    def test_generate_id(self):
        """Test moment ID generation."""
        from engine.infrastructure.memory.moment_processor import MomentProcessor

        # Create processor with mocked dependencies
        mock_ops = MagicMock()
        mock_embed = MagicMock(return_value=[0.1] * 768)

        with tempfile.TemporaryDirectory() as tmpdir:
            processor = MomentProcessor(
                graph_ops=mock_ops,
                embed_fn=mock_embed,
                playthrough_id="test",
                playthroughs_dir=Path(tmpdir)
            )

            # Set context: tick 7200 = Day 5, afternoon (7200 / 1440 = 5, 7200 % 1440 = 0 = night... wait)
            # Actually: day = (7200 // 1440) + 1 = 5 + 1 = 6
            # time = 7200 % 1440 = 0 = night
            # Let's use tick 1500 instead: day = 2, time = 60/60 = 1 hour = night
            # Let's use tick 2160: day = 2, time = 720 = 12 hours = midday

            processor.set_context(tick=2160, place_id="place_camp")

            moment_id = processor._generate_id("dialogue", "aldric_oath")

            assert "camp_d2_midday_dialogue_aldric_oath" == moment_id

    def test_tick_to_time_of_day(self):
        """Test tick to time of day conversion."""
        from engine.infrastructure.memory.moment_processor import MomentProcessor

        mock_ops = MagicMock()
        mock_embed = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            processor = MomentProcessor(
                graph_ops=mock_ops,
                embed_fn=mock_embed,
                playthrough_id="test",
                playthroughs_dir=Path(tmpdir)
            )

            # Test various times (ticks within a day, 0-1439)
            assert processor._tick_to_time_of_day(0) == "night"      # midnight
            assert processor._tick_to_time_of_day(300) == "night"    # 5am
            assert processor._tick_to_time_of_day(360) == "dawn"     # 6am
            assert processor._tick_to_time_of_day(540) == "morning"  # 9am
            assert processor._tick_to_time_of_day(720) == "midday"   # 12pm
            assert processor._tick_to_time_of_day(900) == "afternoon"  # 3pm
            assert processor._tick_to_time_of_day(1200) == "evening"    # 8pm
        
    def test_process_dialogue(self):
        """Test processing dialogue creates moment and updates transcript."""
        from engine.infrastructure.memory.moment_processor import MomentProcessor

        mock_ops = MagicMock()
        mock_embed = MagicMock(return_value=[0.1] * 768)

        with tempfile.TemporaryDirectory() as tmpdir:
            processor = MomentProcessor(
                graph_ops=mock_ops,
                embed_fn=mock_embed,
                playthrough_id="test",
                playthroughs_dir=Path(tmpdir)
            )

            processor.set_context(tick=2160, place_id="place_camp")

            moment_id = processor.process_dialogue(
                text="I swore an oath. That hasn't changed.",
                speaker="char_aldric",
                name="aldric_oath"
            )

            # Check moment was created
            mock_ops.add_moment.assert_called_once()
            call_args = mock_ops.add_moment.call_args

            assert call_args.kwargs['id'] == moment_id
            assert call_args.kwargs['text'] == "I swore an oath. That hasn't changed."
            assert call_args.kwargs['type'] == "dialogue"
            assert call_args.kwargs['speaker'] == "char_aldric"
            assert call_args.kwargs['line'] == 0  # First entry

            # Check transcript was updated
            transcript_path = Path(tmpdir) / "test" / "transcript.json"
            assert transcript_path.exists()

            with open(transcript_path) as f:
                transcript = json.load(f)

            assert len(transcript) == 1
            assert transcript[0]['type'] == 'dialogue'
            assert transcript[0]['speaker'] == 'char_aldric'
            assert transcript[0]['text'] == "I swore an oath. That hasn't changed."

    def test_process_narration(self):
        """Test processing narration creates moment."""
        from engine.infrastructure.memory.moment_processor import MomentProcessor

        mock_ops = MagicMock()
        mock_embed = MagicMock(return_value=[0.1] * 768)

        with tempfile.TemporaryDirectory() as tmpdir:
            processor = MomentProcessor(
                graph_ops=mock_ops,
                embed_fn=mock_embed,
                playthrough_id="test",
                playthroughs_dir=Path(tmpdir)
            )

            processor.set_context(tick=2160, place_id="place_crossing")

            moment_id = processor.process_narration(
                text="The blade lies in two pieces at his feet.",
                name="blade_broken"
            )

            # Check moment was created
            mock_ops.add_moment.assert_called_once()
            call_args = mock_ops.add_moment.call_args

            assert call_args.kwargs['type'] == "narration"
            assert call_args.kwargs.get('speaker') is None
            assert call_args.kwargs['tick'] == 2160

    def test_sequence_linking(self):
        """Test that moments are linked in sequence."""
        from engine.infrastructure.memory.moment_processor import MomentProcessor

        mock_ops = MagicMock()
        mock_embed = MagicMock(return_value=[0.1] * 768)

        with tempfile.TemporaryDirectory() as tmpdir:
            processor = MomentProcessor(
                graph_ops=mock_ops,
                embed_fn=mock_embed,
                playthrough_id="test",
                playthroughs_dir=Path(tmpdir)
            )

            processor.set_context(tick=2160, place_id="place_camp")

            # First moment - no after_moment_id
            moment1_id = processor.process_narration("First line.", name="first")
            first_call = mock_ops.add_moment.call_args_list[0]
            assert first_call.kwargs['after_moment_id'] is None

            # Second moment - should link to first
            moment2_id = processor.process_narration("Second line.", name="second")
            second_call = mock_ops.add_moment.call_args_list[1]
            assert second_call.kwargs['after_moment_id'] == moment1_id

    def test_link_narrative_to_moments(self):
        """Test linking a narrative to source moments."""
        from engine.infrastructure.memory.moment_processor import MomentProcessor

        mock_ops = MagicMock()
        mock_embed = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            processor = MomentProcessor(
                graph_ops=mock_ops,
                embed_fn=mock_embed,
                playthrough_id="test",
                playthroughs_dir=Path(tmpdir)
            )

            processor.link_narrative_to_moments(
                narrative_id="narr_sword_broken",
                moment_ids=["moment_1", "moment_2", "moment_3"]
            )

            # Check add_narrative_from_moment was called 3 times
            assert mock_ops.add_narrative_from_moment.call_count == 3


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
