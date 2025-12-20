"""
Tests for the Blood Ledger History Module

Tests cover:
- Conversation thread handling (read/write sections)
- GameTimestamp parsing and comparison
- History query filtering (unit tests with mocked graph)
- Integration tests (require FalkorDB)
"""

import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime

from engine.models.base import GameTimestamp, TimeOfDay, NarrativeSource
from engine.infrastructure.history.conversations import ConversationThread, ConversationSection


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def temp_conversations_dir():
    """Create a temporary directory for conversation files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def conversation_thread(temp_conversations_dir):
    """Create a ConversationThread instance with temp directory."""
    conv_dir = Path(temp_conversations_dir) / "conversations"
    conv_dir.mkdir(exist_ok=True)
    return ConversationThread(str(conv_dir))


@pytest.fixture
def sample_conversation_file(temp_conversations_dir):
    """Create a sample conversation file with content."""
    content = """# Conversations with Aldric

## Day 4, Night — The Camp

Aldric stares into the fire. He hasn't spoken in an hour.

You: "You fought at Stamford Bridge."
Aldric: "Aye."
You: "What happened?"
Aldric: *long pause* "My brother held the bridge. Alone, for a time. They got him from below. A spear, through the planks."

He doesn't look at you.

Aldric: "I was fifty yards away. Couldn't reach him."

## Day 7, Morning — The Road

The morning is cold. Frost on the grass.

You: "We should reach York by nightfall."
Aldric: "Aye. If the road holds."
"""
    conv_dir = Path(temp_conversations_dir) / "conversations"
    conv_dir.mkdir(exist_ok=True)
    file_path = conv_dir / "aldric.md"
    file_path.write_text(content)
    return file_path


# =============================================================================
# GAME TIMESTAMP TESTS
# =============================================================================

class TestGameTimestamp:
    """Tests for GameTimestamp parsing and comparison."""

    def test_parse_basic(self):
        """Parse a basic timestamp string."""
        ts = GameTimestamp.parse("Day 4, night")
        assert ts.day == 4
        assert ts.time == TimeOfDay.NIGHT

    def test_parse_different_formats(self):
        """Parse various timestamp formats."""
        ts1 = GameTimestamp.parse("Day 1, dawn")
        assert ts1.day == 1
        assert ts1.time == TimeOfDay.DAWN

        ts2 = GameTimestamp.parse("Day 12, midday")
        assert ts2.day == 12
        assert ts2.time == TimeOfDay.MIDDAY

        ts3 = GameTimestamp.parse("Day 100, midnight")
        assert ts3.day == 100
        assert ts3.time == TimeOfDay.MIDNIGHT

    def test_parse_case_insensitive(self):
        """Parsing should be case insensitive."""
        ts = GameTimestamp.parse("DAY 5, MORNING")
        assert ts.day == 5
        assert ts.time == TimeOfDay.MORNING

    def test_parse_invalid_raises(self):
        """Invalid format should raise ValueError."""
        with pytest.raises(ValueError):
            GameTimestamp.parse("invalid timestamp")

        with pytest.raises(ValueError):
            GameTimestamp.parse("5, morning")

    def test_str_format(self):
        """String representation should match expected format."""
        ts = GameTimestamp(day=4, time=TimeOfDay.NIGHT)
        assert str(ts) == "Day 4, night"

    def test_comparison_same_day(self):
        """Compare timestamps on the same day."""
        ts_dawn = GameTimestamp(day=1, time=TimeOfDay.DAWN)
        ts_night = GameTimestamp(day=1, time=TimeOfDay.NIGHT)

        assert ts_dawn < ts_night
        assert ts_night > ts_dawn
        assert ts_dawn <= ts_night
        assert ts_night >= ts_dawn
        assert not ts_dawn > ts_night

    def test_comparison_different_days(self):
        """Compare timestamps on different days."""
        ts_day1 = GameTimestamp(day=1, time=TimeOfDay.NIGHT)
        ts_day2 = GameTimestamp(day=2, time=TimeOfDay.DAWN)

        assert ts_day1 < ts_day2
        assert ts_day2 > ts_day1

    def test_comparison_equal(self):
        """Test equality comparison."""
        ts1 = GameTimestamp(day=5, time=TimeOfDay.DUSK)
        ts2 = GameTimestamp(day=5, time=TimeOfDay.DUSK)

        assert ts1 == ts2
        assert ts1 <= ts2
        assert ts1 >= ts2


# =============================================================================
# CONVERSATION THREAD TESTS
# =============================================================================

class TestConversationThread:
    """Tests for ConversationThread file handling."""

    def test_append_section_creates_file(self, conversation_thread, temp_conversations_dir):
        """Appending a section should create the file if it doesn't exist."""
        result = conversation_thread.append_section(
            character_id="char_aldric",
            day=1,
            time_of_day="morning",
            location_name="The Camp",
            content="Aldric nods.\n\nYou: 'Ready?'\nAldric: 'Always.'"
        )

        assert result["file"] == "conversations/aldric.md"
        assert result["section"] == "Day 1, Morning — The Camp"

        # File should exist
        file_path = Path(temp_conversations_dir) / "conversations" / "aldric.md"
        assert file_path.exists()

        # Content should include header and section
        content = file_path.read_text()
        assert "# Conversations with Aldric" in content
        assert "## Day 1, Morning — The Camp" in content
        assert "Aldric nods." in content

    def test_append_multiple_sections(self, conversation_thread, temp_conversations_dir):
        """Multiple sections can be appended to the same file."""
        conversation_thread.append_section(
            character_id="char_aldric",
            day=1,
            time_of_day="morning",
            location_name="The Camp",
            content="First conversation."
        )

        conversation_thread.append_section(
            character_id="char_aldric",
            day=2,
            time_of_day="night",
            location_name="York",
            content="Second conversation."
        )

        file_path = Path(temp_conversations_dir) / "conversations" / "aldric.md"
        content = file_path.read_text()

        assert "## Day 1, Morning — The Camp" in content
        assert "## Day 2, Night — York" in content
        assert "First conversation." in content
        assert "Second conversation." in content
        assert "Second conversation." in content

    def test_read_section(self, conversation_thread, sample_conversation_file, temp_conversations_dir):
        """Reading a specific section should return its content."""
        content = conversation_thread.read_section(
            file_path="conversations/aldric.md",
            section_header="Day 4, Night — The Camp"
        )

        assert content is not None
        assert "Aldric stares into the fire" in content
        assert "My brother held the bridge" in content

    def test_read_section_not_found(self, conversation_thread, sample_conversation_file):
        """Reading a non-existent section should return None."""
        content = conversation_thread.read_section(
            file_path="conversations/aldric.md",
            section_header="Day 99, Night — Nowhere"
        )

        assert content is None

    def test_read_section_file_not_found(self, conversation_thread):
        """Reading from non-existent file should return None."""
        content = conversation_thread.read_section(
            file_path="conversations/nonexistent.md",
            section_header="Any Section"
        )

        assert content is None

    def test_list_sections(self, conversation_thread, sample_conversation_file):
        """List all section headers in a file."""
        sections = conversation_thread.list_sections("char_aldric")

        assert len(sections) == 2
        assert "Day 4, Night — The Camp" in sections
        assert "Day 7, Morning — The Road" in sections

    def test_list_sections_empty_file(self, conversation_thread):
        """List sections for non-existent file returns empty list."""
        sections = conversation_thread.list_sections("char_nobody")
        assert sections == []

    def test_get_full_thread(self, conversation_thread, sample_conversation_file):
        """Get complete conversation thread content."""
        content = conversation_thread.get_full_thread("char_aldric")

        assert content is not None
        assert "# Conversations with Aldric" in content
        assert "Day 4, Night" in content
        assert "Day 7, Morning" in content

    def test_search_sections(self, conversation_thread, sample_conversation_file):
        """Search for sections containing keyword."""
        results = conversation_thread.search_sections("char_aldric", "brother")

        assert len(results) == 1
        assert results[0].header == "Day 4, Night — The Camp"
        assert "brother" in results[0].content.lower()

    def test_search_sections_multiple_matches(self, conversation_thread, sample_conversation_file):
        """Search can return multiple matching sections."""
        results = conversation_thread.search_sections("char_aldric", "Aldric")

        assert len(results) == 2  # Both sections mention Aldric


# =============================================================================
# NARRATIVE SOURCE TESTS
# =============================================================================

class TestNarrativeSource:
    """Tests for NarrativeSource model."""

    def test_create_source(self):
        """Create a narrative source reference."""
        source = NarrativeSource(
            file="conversations/aldric.md",
            section="Day 4, Night — The Camp"
        )

        assert source.file == "conversations/aldric.md"
        assert source.section == "Day 4, Night — The Camp"

    def test_source_from_dict(self):
        """Create source from dictionary."""
        data = {
            "file": "conversations/edmund.md",
            "section": "Day 10, Dusk — The Hall"
        }
        source = NarrativeSource(**data)

        assert source.file == data["file"]
        assert source.section == data["section"]


# =============================================================================
# HISTORY SERVICE TESTS (Unit - Mocked Graph)
# =============================================================================

class MockGraphQueries:
    """Mock GraphQueries for unit testing."""

    def __init__(self, query_results=None):
        self.query_results = query_results or []
        self.queries_executed = []

    def _query(self, cypher, params=None):
        self.queries_executed.append((cypher, params))
        return self.query_results


class MockGraphOps:
    """Mock GraphOps for unit testing."""

    def __init__(self):
        self.operations = []

    def apply(self, data):
        self.operations.append(data)


class TestHistoryServiceUnit:
    """Unit tests for HistoryService with mocked dependencies."""

    def test_query_history_builds_correct_cypher(self, temp_conversations_dir):
        """query_history should build appropriate Cypher query."""
        from engine.infrastructure.history.service import HistoryService

        mock_graph = MockGraphQueries()
        mock_ops = MockGraphOps()

        service = HistoryService(
            graph_queries=mock_graph,
            graph_ops=mock_ops,
            conversations_dir=temp_conversations_dir
        )

        # Execute query
        service.query_history("player", about_person="char_aldric")

        # Check query was executed
        assert len(mock_graph.queries_executed) == 1
        cypher, _ = mock_graph.queries_executed[0]

        assert "player" in cypher
        assert "char_aldric" in cypher
        assert "BELIEVES" in cypher

    def test_query_history_filters_by_place(self, temp_conversations_dir):
        """query_history should filter by place when specified."""
        from engine.infrastructure.history.service import HistoryService

        mock_graph = MockGraphQueries()
        mock_ops = MockGraphOps()

        service = HistoryService(
            graph_queries=mock_graph,
            graph_ops=mock_ops,
            conversations_dir=temp_conversations_dir
        )

        service.query_history("player", about_place="place_york")

        cypher, _ = mock_graph.queries_executed[0]
        assert "place_york" in cypher


# =============================================================================
# INTEGRATION TESTS (Require FalkorDB)
# =============================================================================

@pytest.mark.integration
class TestHistoryServiceIntegration:
    """Integration tests requiring actual FalkorDB connection."""

    @pytest.fixture
    def live_service(self, temp_conversations_dir):
        """Create HistoryService with real graph connections."""
        try:
            from engine.physics.graph.graph_queries import GraphQueries
            from engine.physics.graph.graph_ops import GraphOps
            from engine.infrastructure.history.service import HistoryService

            graph = GraphQueries()
            ops = GraphOps()

            return HistoryService(
                graph_queries=graph,
                graph_ops=ops,
                conversations_dir=temp_conversations_dir
            )
        except Exception as e:
            pytest.skip(f"FalkorDB not available: {e}")

    def test_record_and_query_player_history(self, live_service, temp_conversations_dir):
        """Record player history and query it back."""
        # Setup: Ensure characters exist
        live_service.ops.add_character(id="player", name="Player")
        live_service.ops.add_character(id="char_aldric", name="Aldric")
        live_service.ops.add_place(id="place_camp", name="The Camp")

        # Record
        result = live_service.record_player_history(
            content="Aldric told me about his brother",
            conversation_text="Aldric: My brother held the bridge...",
            character_id="char_aldric",
            witnesses=["player", "char_aldric"],
            occurred_at="Day 4, night",
            occurred_where="place_camp",
            place_name="The Camp"
        )

        assert "narrative_id" in result
        assert len(result["belief_ids"]) == 2

        # Query
        memories = live_service.query_history("player", about_person="char_aldric")
        assert len(memories) > 0

    def test_record_world_history(self, live_service):
        """Record world-generated history."""
        result = live_service.record_world_history(
            content="Saxon thegns seized York",
            detail="The rebellion began at dawn...",
            occurred_at="Day 12, dawn",
            occurred_where="place_york",
            witnesses=["char_malet"],
            about_places=["place_york"]
        )

        assert "narrative_id" in result
        assert len(result["belief_ids"]) >= 1


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
