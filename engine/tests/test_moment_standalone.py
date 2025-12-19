#!/usr/bin/env python3
"""
Standalone tests for the Moment system (no pytest required).
"""

import json
import tempfile
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.models.base import MomentType
from engine.models.nodes import Moment


def test_moment_creation():
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
    print("  ✓ Moment creation works")


def test_embeddable_text():
    """Test embeddable text generation."""
    dialogue = Moment(
        id="test",
        text="Hello there.",
        type=MomentType.DIALOGUE,
        tick=0,
        speaker="char_aldric"
    )
    assert dialogue.embeddable_text() == "char_aldric: Hello there."

    narration = Moment(
        id="test",
        text="The fire crackles.",
        type=MomentType.NARRATION,
        tick=0
    )
    assert narration.embeddable_text() == "The fire crackles."
    print("  ✓ Embeddable text works")


def test_should_embed():
    """Test should_embed property."""
    long_text = Moment(
        id="test",
        text="This is a longer piece of text that should be embedded.",
        type=MomentType.NARRATION,
        tick=0
    )
    assert long_text.should_embed is True

    short_text = Moment(
        id="test",
        text="Short.",
        type=MomentType.NARRATION,
        tick=0
    )
    assert short_text.should_embed is False
    print("  ✓ should_embed works")


def test_extract_moment_args():
    """Test _extract_moment_args."""
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
    print("  ✓ _extract_moment_args works")


def test_moment_processor_id_generation():
    """Test moment ID generation."""
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
        moment_id = processor._generate_id("dialogue", "aldric_oath")

        assert moment_id == "camp_d2_midday_dialogue_aldric_oath"
    print("  ✓ ID generation works")


def test_moment_processor_time_conversion():
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

        assert processor._tick_to_time_of_day(0) == "night"       # midnight
        assert processor._tick_to_time_of_day(300) == "night"     # 5am
        assert processor._tick_to_time_of_day(360) == "dawn"      # 6am
        assert processor._tick_to_time_of_day(540) == "morning"   # 9am
        assert processor._tick_to_time_of_day(720) == "midday"    # 12pm
        assert processor._tick_to_time_of_day(900) == "afternoon" # 3pm
        assert processor._tick_to_time_of_day(1140) == "dusk"     # 7pm (1140/60=19)
        assert processor._tick_to_time_of_day(1260) == "evening"  # 9pm (1260/60=21)
    print("  ✓ Time conversion works")


def test_moment_processor_dialogue():
    """Test processing dialogue."""
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
        assert call_args.kwargs['line'] == 0

        # Check transcript was updated
        transcript_path = Path(tmpdir) / "test" / "transcript.json"
        assert transcript_path.exists()

        with open(transcript_path) as f:
            transcript = json.load(f)

        assert len(transcript) == 1
        assert transcript[0]['type'] == 'dialogue'
        assert transcript[0]['speaker'] == 'char_aldric'
    print("  ✓ Dialogue processing works")


def test_moment_processor_sequence():
    """Test moment sequence linking."""
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
    print("  ✓ Sequence linking works")


def test_moment_processor_narrative_linking():
    """Test linking narratives to moments."""
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

        assert mock_ops.add_narrative_from_moment.call_count == 3
    print("  ✓ Narrative linking works")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MOMENT SYSTEM TESTS")
    print("=" * 60)

    tests = [
        ("Moment Model", [
            test_moment_creation,
            test_embeddable_text,
            test_should_embed,
        ]),
        ("GraphOps", [
            test_extract_moment_args,
        ]),
        ("MomentProcessor", [
            test_moment_processor_id_generation,
            test_moment_processor_time_conversion,
            test_moment_processor_dialogue,
            test_moment_processor_sequence,
            test_moment_processor_narrative_linking,
        ]),
    ]

    total = 0
    passed = 0

    for category, test_funcs in tests:
        print(f"\n{category}:")
        for test_func in test_funcs:
            total += 1
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                print(f"  ✗ {test_func.__name__} FAILED: {e}")
            except Exception as e:
                print(f"  ✗ {test_func.__name__} ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
