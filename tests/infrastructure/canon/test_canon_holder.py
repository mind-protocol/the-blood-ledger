# DOCS: docs/infrastructure/canon/TEST_Canon.md
"""
Tests for Canon Holder.

Specs:
- docs/infrastructure/canon/VALIDATION_Canon.md (invariants)
- docs/infrastructure/canon/ALGORITHM_Canon_Holder.md (queries)
- docs/infrastructure/canon/BEHAVIORS_Canon.md (behaviors)
- docs/infrastructure/canon/TEST_Canon.md (test cases)

Implementation:
- engine/infrastructure/canon/canon_holder.py
- engine/infrastructure/canon/speaker.py
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_graph_queries():
    """Create a GraphQueries instance with mocked database connection."""
    with patch('engine.physics.graph.graph_queries.FalkorDB') as mock_falkor:
        mock_graph = MagicMock()
        mock_falkor.return_value.select_graph.return_value = mock_graph

        from engine.physics.graph import GraphQueries
        queries = GraphQueries(graph_name="test_graph")
        queries._graph = mock_graph

        yield queries


@pytest.fixture
def mock_canon_holder():
    """Create a CanonHolder with mocked database."""
    with patch('engine.physics.graph.graph_queries.FalkorDB') as mock_falkor:
        mock_graph = MagicMock()
        mock_falkor.return_value.select_graph.return_value = mock_graph

        # Mock query results
        mock_graph.query.return_value = MagicMock(result_set=[])

        from engine.infrastructure.canon import CanonHolder
        holder = CanonHolder(playthrough_id="test_pt", host="localhost", port=6379)
        holder._mock_graph = mock_graph

        yield holder


@pytest.fixture
def mock_broadcast():
    """Mock SSE broadcast function."""
    with patch('engine.infrastructure.api.sse_broadcast.broadcast_moment_event') as mock:
        yield mock


# =============================================================================
# UNIT TESTS - Query Functions
# =============================================================================

class TestDetermineSpeaker:
    """Test Q5: determine_speaker()"""

    def test_q5_speaker_present_and_awake(self):
        """Speaker with CAN_SPEAK, present, awake should be returned."""
        with patch('engine.infrastructure.canon.speaker.get_playthrough_graph_name', return_value="test"):
            with patch('engine.infrastructure.canon.speaker.GraphQueries') as MockQueries:
                mock_instance = MagicMock()
                mock_instance.query.return_value = [{'speaker_id': 'char_aldric', 'strength': 0.9}]
                MockQueries.return_value = mock_instance

                from engine.infrastructure.canon import determine_speaker
                result = determine_speaker("test_pt", "mom_test")
                assert result == 'char_aldric'

    def test_q5_no_speaker_returns_none(self):
        """No valid speaker should return None."""
        with patch('engine.infrastructure.canon.speaker.get_playthrough_graph_name', return_value="test"):
            with patch('engine.infrastructure.canon.speaker.GraphQueries') as MockQueries:
                mock_instance = MagicMock()
                mock_instance.query.return_value = []
                MockQueries.return_value = mock_instance

                from engine.infrastructure.canon import determine_speaker
                result = determine_speaker("test_pt", "mom_test")
                assert result is None


class TestRecordToCanon:
    """Test Q6: record_to_canon()"""

    def test_q6_moment_not_found(self, mock_canon_holder):
        """Should return error if moment not found."""
        # Mock empty result for moment query
        mock_canon_holder._queries.query = MagicMock(return_value=[])

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_nonexistent",
            tick=100
        )

        assert result['status'] == 'error'
        assert result['error'] == 'moment_not_found'

    def test_q6_already_spoken(self, mock_canon_holder):
        """Should return early if moment already spoken."""
        # Mock moment query returning spoken moment
        mock_canon_holder._queries.query = MagicMock(return_value=[{
            'id': 'mom_test',
            'status': 'spoken',
            'type': 'narration',
            'weight': 0.5,
            'energy': 0.4,
            'text': 'Test moment'
        }])

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_test",
            tick=100
        )

        assert result['status'] == 'already_spoken'

    def test_q6_dialogue_no_speaker(self, mock_canon_holder):
        """Dialogue without speaker should return no_speaker."""
        # Mock moment as dialogue
        def mock_query(cypher, params=None):
            if 'RETURN m.id' in cypher:
                return [{
                    'id': 'mom_test',
                    'status': 'active',
                    'type': 'dialogue',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Test dialogue'
                }]
            return []

        mock_canon_holder._queries.query = mock_query

        with patch('engine.infrastructure.canon.canon_holder.determine_speaker', return_value=None):
            result = mock_canon_holder.record_to_canon(
                moment_id="mom_test",
                tick=100
            )

        assert result['status'] == 'no_speaker'

    def test_q6_narration_succeeds(self, mock_canon_holder, mock_broadcast):
        """Narration moment should be recorded without speaker."""
        call_count = [0]

        def mock_query(cypher, params=None):
            call_count[0] += 1
            if call_count[0] == 1:  # First call - get moment
                return [{
                    'id': 'mom_test',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Narration text'
                }]
            elif 'SET m.status' in cypher:  # Update query
                return [{'m.text': 'Narration text'}]
            return []

        mock_canon_holder._queries.query = mock_query

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_test",
            tick=100
        )

        assert result['status'] == 'ok'
        assert result['speaker'] is None


class TestGetLastSpokenMoment:
    """Test Q7: _get_last_spoken_moment_id()"""

    def test_q7_returns_latest(self, mock_canon_holder):
        """Should return moment with highest tick_spoken."""
        mock_canon_holder._queries.query = MagicMock(return_value=[{
            'm.id': 'mom_latest'
        }])

        result = mock_canon_holder._get_last_spoken_moment_id()

        assert result == 'mom_latest'

    def test_q7_no_spoken_returns_none(self, mock_canon_holder):
        """Should return None if no spoken moments."""
        mock_canon_holder._queries.query = MagicMock(return_value=[])

        result = mock_canon_holder._get_last_spoken_moment_id()

        assert result is None


# =============================================================================
# BEHAVIOR TESTS
# =============================================================================

class TestBehaviorB3EnergyConservation:
    """Test B3: Speaking costs 60% energy (keeps 40%)."""

    def test_energy_reduced_on_record(self, mock_canon_holder, mock_broadcast):
        """Energy should be multiplied by 0.4 when recorded."""
        queries_made = []

        def mock_query(cypher, params=None):
            queries_made.append({'cypher': cypher, 'params': params})
            if 'RETURN m.id' in cypher:
                return [{
                    'id': 'mom_test',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Test'
                }]
            elif 'SET m.status' in cypher:
                return [{'m.text': 'Test'}]
            return []

        mock_canon_holder._queries.query = mock_query

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_test",
            tick=100
        )

        # Verify energy update query was made
        update_query = [q for q in queries_made if 'energy = m.energy * 0.4' in q['cypher']]
        assert len(update_query) > 0, "Energy update query not found"


class TestBehaviorB4HighestSpeakerWins:
    """Test B4: Highest weight CAN_SPEAK character wins."""

    def test_highest_strength_selected(self):
        """Character with highest CAN_SPEAK.strength should be selected."""
        with patch('engine.infrastructure.canon.speaker.get_playthrough_graph_name', return_value="test"):
            with patch('engine.infrastructure.canon.speaker.GraphQueries') as MockQueries:
                mock_instance = MagicMock()
                # Query returns char_aldric (strength 0.9) over char_edmund (0.7)
                # due to ORDER BY strength DESC LIMIT 1
                mock_instance.query.return_value = [{'speaker_id': 'char_aldric', 'strength': 0.9}]
                MockQueries.return_value = mock_instance

                from engine.infrastructure.canon import determine_speaker
                result = determine_speaker("test_pt", "mom_test")
                assert result == 'char_aldric'


class TestBehaviorB9DialogueWithoutSpeakerWaits:
    """Test B9: Dialogue without valid speaker stays active."""

    def test_dialogue_stays_active_without_speaker(self, mock_canon_holder):
        """Dialogue moment should not become spoken if no speaker available."""
        def mock_query(cypher, params=None):
            if 'RETURN m.id' in cypher:
                return [{
                    'id': 'mom_dialogue',
                    'status': 'active',
                    'type': 'dialogue',
                    'weight': 0.8,
                    'energy': 1.0,
                    'text': 'Dialogue text'
                }]
            return []

        mock_canon_holder._queries.query = mock_query

        with patch('engine.infrastructure.canon.canon_holder.determine_speaker', return_value=None):
            result = mock_canon_holder.record_to_canon(
                moment_id="mom_dialogue",
                tick=100
            )

        assert result['status'] == 'no_speaker'


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestEdgeCaseE1FirstMoment:
    """Test E1: First moment has no THEN link."""

    def test_first_moment_no_then_link(self, mock_canon_holder, mock_broadcast):
        """First spoken moment should not create THEN link."""
        queries_made = []

        def mock_query(cypher, params=None):
            queries_made.append({'cypher': cypher, 'params': params})
            if 'RETURN m.id' in cypher and 'status' not in cypher:
                return [{
                    'id': 'mom_first',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'First moment'
                }]
            elif 'SET m.status' in cypher:
                return [{'m.text': 'First moment'}]
            return []

        mock_canon_holder._queries.query = mock_query

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_first",
            previous_moment_id=None,  # No previous
            tick=100
        )

        # Verify no THEN link query was made
        then_queries = [q for q in queries_made if 'THEN' in q['cypher']]
        assert len(then_queries) == 0, "THEN link should not be created for first moment"


class TestEdgeCaseE2NarrationMoment:
    """Test E2: Narration has no SAID link."""

    def test_narration_no_said_link(self, mock_canon_holder, mock_broadcast):
        """Narration moment should not create SAID link."""
        queries_made = []

        def mock_query(cypher, params=None):
            queries_made.append({'cypher': cypher, 'params': params})
            if 'RETURN m.id' in cypher:
                return [{
                    'id': 'mom_narration',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Narration'
                }]
            elif 'SET m.status' in cypher:
                return [{'m.text': 'Narration'}]
            return []

        mock_canon_holder._queries.query = mock_query

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_narration",
            speaker_id=None,
            tick=100
        )

        # Verify no SAID link query was made
        said_queries = [q for q in queries_made if 'SAID' in q['cypher']]
        assert len(said_queries) == 0, "SAID link should not be created for narration"


class TestEdgeCaseE4PlayerCaused:
    """Test E4: Player-caused THEN link."""

    def test_player_caused_flag_on_then_link(self, mock_canon_holder, mock_broadcast):
        """THEN link should have player_caused=true when set."""
        queries_made = []

        def mock_query(cypher, params=None):
            queries_made.append({'cypher': cypher, 'params': params})
            if 'RETURN m.id' in cypher and 'Moment {id:' in cypher:
                return [{
                    'id': 'mom_second',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Second moment'
                }]
            elif 'SET m.status' in cypher:
                return [{'m.text': 'Second moment'}]
            return []

        mock_canon_holder._queries.query = mock_query

        result = mock_canon_holder.record_to_canon(
            moment_id="mom_second",
            previous_moment_id="mom_first",
            tick=100,
            player_caused=True
        )

        # Verify THEN link query has player_caused=True
        then_queries = [q for q in queries_made if 'THEN' in q['cypher']]
        assert len(then_queries) > 0, "THEN link query should be made"
        assert then_queries[0]['params'].get('player_caused') == True


# =============================================================================
# SSE BROADCAST TESTS
# =============================================================================

class TestSSEBroadcast:
    """Test SSE event broadcasting."""

    def test_moment_spoken_event_sent(self, mock_canon_holder):
        """moment_spoken event should be broadcast after recording."""
        broadcast_calls = []

        def mock_query(cypher, params=None):
            if 'RETURN m.id' in cypher:
                return [{
                    'id': 'mom_test',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Test'
                }]
            elif 'SET m.status' in cypher:
                return [{'m.text': 'Test'}]
            return []

        mock_canon_holder._queries.query = mock_query

        with patch('engine.infrastructure.api.sse_broadcast.broadcast_moment_event') as mock_broadcast:
            mock_broadcast.side_effect = lambda *args: broadcast_calls.append(args)

            result = mock_canon_holder.record_to_canon(
                moment_id="mom_test",
                tick=100
            )

        assert len(broadcast_calls) == 1
        assert broadcast_calls[0][0] == "test_pt"  # playthrough_id
        assert broadcast_calls[0][1] == "moment_spoken"  # event type
        assert broadcast_calls[0][2]['moment_id'] == "mom_test"
        assert broadcast_calls[0][2]['tick'] == 100


# =============================================================================
# INVARIANT TESTS
# =============================================================================

class TestInvariantV4EnergyConservation:
    """Test V4: Energy multiplied by 0.4 on actualization."""

    def test_energy_formula(self, mock_canon_holder, mock_broadcast):
        """Verify energy = energy * 0.4 in query."""
        queries_made = []

        def mock_query(cypher, params=None):
            queries_made.append(cypher)
            if 'RETURN m.id' in cypher:
                return [{
                    'id': 'mom_test',
                    'status': 'active',
                    'type': 'narration',
                    'weight': 0.5,
                    'energy': 1.0,
                    'text': 'Test'
                }]
            elif 'SET m.status' in cypher:
                return [{'m.text': 'Test'}]
            return []

        mock_canon_holder._queries.query = mock_query
        mock_canon_holder.record_to_canon(moment_id="mom_test", tick=100)

        # Find the update query
        update_queries = [q for q in queries_made if 'SET m.status' in q]
        assert len(update_queries) > 0
        assert 'm.energy = m.energy * 0.4' in update_queries[0]
