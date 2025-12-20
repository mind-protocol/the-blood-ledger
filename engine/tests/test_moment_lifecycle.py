"""
Tests for Moment Lifecycle (Phase 5).

Specs:
- docs/engine/moments/ALGORITHM_Lifecycle.md
- docs/engine/moments/SYNC_Moments.md (Phase 5)

Implementation:
- engine/physics/graph/graph_ops.py (decay_moments, on_player_leaves_location, etc.)
- engine/physics/tick.py (_process_moment_tick)

Tests cover:
1. Weight decay (decay_moments)
2. Dormancy (on_player_leaves_location)
3. Reactivation (on_player_arrives_location)
4. Garbage collection (garbage_collect_moments)
5. World tick integration
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

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

        # Track queries for verification
        ops._queries = []

        def tracking_query(cypher, params=None):
            ops._queries.append({"cypher": cypher, "params": params})
            # Return mock result structure (list-based like real FalkorDB)
            # FalkorDB returns lists, not dicts: [[value1, value2, ...]]
            # Different queries need different return structures
            if "RETURN m.weight, m.status" in cypher:
                # boost_moment_weight query: [weight, status]
                return [[0.5, "possible"]]
            elif "count(m)" in cypher.lower():
                # Count queries
                return [[5]]
            else:
                # Default: used for checking query structure
                return [[5, 2, 3, 1, 2, 0.5, "possible"]]

        ops._query = tracking_query
        yield ops


# =============================================================================
# DECAY TESTS
# =============================================================================

class TestDecayMoments:
    """Test decay_moments() method."""

    def test_decay_applies_rate_to_possible_moments(self, mock_graph_ops):
        """Test that decay multiplies weight of possible moments."""
        result = mock_graph_ops.decay_moments(decay_rate=0.99)

        # Should have executed decay query
        assert len(mock_graph_ops._queries) >= 1
        decay_query = mock_graph_ops._queries[0]
        assert "status = 'possible'" in decay_query["cypher"]
        assert decay_query["params"]["decay_rate"] == 0.99

    def test_decay_marks_below_threshold_as_decayed(self, mock_graph_ops):
        """Test that moments below threshold are marked decayed."""
        result = mock_graph_ops.decay_moments(decay_threshold=0.1)

        # Should have executed threshold check query
        decayed_query = mock_graph_ops._queries[1]
        assert "status = 'decayed'" in decayed_query["cypher"]
        assert decayed_query["params"]["threshold"] == 0.1

    def test_decay_returns_counts(self, mock_graph_ops):
        """Test that decay returns updated and decayed counts."""
        result = mock_graph_ops.decay_moments()

        assert "updated_count" in result
        assert "decayed_count" in result

    def test_decay_with_custom_tick(self, mock_graph_ops):
        """Test that tick_decayed is set correctly."""
        result = mock_graph_ops.decay_moments(current_tick=1500)

        decayed_query = mock_graph_ops._queries[1]
        assert decayed_query["params"]["tick"] == 1500


# =============================================================================
# DORMANCY TESTS
# =============================================================================

class TestDormancy:
    """Test on_player_leaves_location() and on_player_arrives_location()."""

    def test_leaves_marks_persistent_as_dormant(self, mock_graph_ops):
        """Test that persistent moments become dormant when player leaves."""
        result = mock_graph_ops.on_player_leaves_location("place_camp")

        # Should have executed dormant query
        dormant_query = mock_graph_ops._queries[0]
        assert "dormant" in dormant_query["cypher"]
        assert "persistent = true" in dormant_query["cypher"]
        assert dormant_query["params"]["location_id"] == "place_camp"

    def test_leaves_deletes_non_persistent(self, mock_graph_ops):
        """Test that non-persistent moments are deleted when player leaves."""
        result = mock_graph_ops.on_player_leaves_location("place_camp")

        # Should have executed delete query
        delete_query = mock_graph_ops._queries[1]
        assert "DELETE" in delete_query["cypher"]
        assert "persistent = false" in delete_query["cypher"]

    def test_leaves_returns_counts(self, mock_graph_ops):
        """Test that leaves returns dormant and deleted counts."""
        result = mock_graph_ops.on_player_leaves_location("place_camp")

        assert "dormant_count" in result
        assert "deleted_count" in result

    def test_arrives_reactivates_dormant(self, mock_graph_ops):
        """Test that dormant moments become possible when player arrives."""
        result = mock_graph_ops.on_player_arrives_location("place_camp")

        reactivate_query = mock_graph_ops._queries[0]
        assert "possible" in reactivate_query["cypher"]
        assert "dormant" in reactivate_query["cypher"]
        assert reactivate_query["params"]["location_id"] == "place_camp"

    def test_arrives_returns_count(self, mock_graph_ops):
        """Test that arrives returns reactivated count."""
        result = mock_graph_ops.on_player_arrives_location("place_camp")

        assert "reactivated_count" in result


# =============================================================================
# GARBAGE COLLECTION TESTS
# =============================================================================

class TestGarbageCollection:
    """Test garbage_collect_moments() method."""

    def test_gc_removes_old_decayed(self, mock_graph_ops):
        """Test that old decayed moments are removed."""
        result = mock_graph_ops.garbage_collect_moments(
            current_tick=200,
            retention_ticks=100
        )

        gc_query = mock_graph_ops._queries[0]
        assert "DELETE" in gc_query["cypher"]
        assert "decayed" in gc_query["cypher"]
        # threshold should be 200 - 100 = 100
        assert gc_query["params"]["threshold"] == 100

    def test_gc_returns_count(self, mock_graph_ops):
        """Test that GC returns deleted count."""
        result = mock_graph_ops.garbage_collect_moments(current_tick=200)

        assert "deleted_count" in result


# =============================================================================
# BOOST WEIGHT TESTS
# =============================================================================

class TestBoostMomentWeight:
    """Test boost_moment_weight() method."""

    def test_boost_adds_weight(self, mock_graph_ops):
        """Test that boost adds weight to moment."""
        result = mock_graph_ops.boost_moment_weight("moment_1", boost=0.3)

        # Should have gotten current weight then updated
        assert len(mock_graph_ops._queries) >= 2
        assert "new_weight" in result

    def test_boost_caps_at_one(self, mock_graph_ops):
        """Test that weight is capped at 1.0."""
        # Mock returns weight 0.5, boost 0.6 should cap at 1.0
        result = mock_graph_ops.boost_moment_weight("moment_1", boost=0.6)

        assert result["new_weight"] == 1.0

    def test_boost_flips_above_threshold(self, mock_graph_ops):
        """Test that boost above 0.8 flips to active."""
        # Mock returns weight 0.5, status possible
        # boost 0.35 = 0.85 >= 0.8 threshold
        result = mock_graph_ops.boost_moment_weight("moment_1", boost=0.35)

        assert result["flipped"] is True
        assert result["status"] == "active"


# =============================================================================
# WORLD TICK INTEGRATION TESTS
# =============================================================================

class TestWorldTickIntegration:
    """Test moment decay integration with world tick."""

    @patch('engine.physics.tick.GraphQueries')
    @patch('engine.physics.tick.GraphOps')
    def test_tick_calls_moment_decay(self, mock_ops_class, mock_queries_class):
        """Test that world tick calls moment decay."""
        from engine.physics.tick import GraphTick

        mock_ops = MagicMock()
        mock_ops.decay_moments.return_value = {"updated_count": 5, "decayed_count": 1}
        mock_ops_class.return_value = mock_ops

        mock_queries = MagicMock()
        mock_queries.get_all_characters.return_value = []
        mock_queries.get_all_tensions.return_value = []
        mock_queries_class.return_value = mock_queries

        tick = GraphTick(graph_name="test")
        result = tick.run(elapsed_minutes=10)

        # Should have called decay_moments
        mock_ops.decay_moments.assert_called()

    @patch('engine.physics.tick.GraphQueries')
    @patch('engine.physics.tick.GraphOps')
    def test_tick_result_includes_moments_decayed(self, mock_ops_class, mock_queries_class):
        """Test that tick result includes moments_decayed count."""
        from engine.physics.tick import GraphTick

        mock_ops = MagicMock()
        mock_ops.decay_moments.return_value = {"updated_count": 5, "decayed_count": 3}
        mock_ops_class.return_value = mock_ops

        mock_queries = MagicMock()
        mock_queries.get_all_characters.return_value = []
        mock_queries.get_all_tensions.return_value = []
        mock_queries_class.return_value = mock_queries

        tick = GraphTick(graph_name="test")
        result = tick.run(elapsed_minutes=10)

        assert hasattr(result, 'moments_decayed')
        assert result.moments_decayed >= 0

    @patch('engine.physics.tick.GraphQueries')
    @patch('engine.physics.tick.GraphOps')
    def test_tick_decay_iterations_scale_with_time(self, mock_ops_class, mock_queries_class):
        """Test that longer time = more decay iterations."""
        from engine.physics.tick import GraphTick

        mock_ops = MagicMock()
        mock_ops.decay_moments.return_value = {"updated_count": 5, "decayed_count": 1}
        mock_ops_class.return_value = mock_ops

        mock_queries = MagicMock()
        mock_queries.get_all_characters.return_value = []
        mock_queries.get_all_tensions.return_value = []
        mock_queries_class.return_value = mock_queries

        tick = GraphTick(graph_name="test")

        # 10 minutes = 2 iterations
        tick.run(elapsed_minutes=10)
        assert mock_ops.decay_moments.call_count == 2

        mock_ops.reset_mock()

        # 25 minutes = 5 iterations
        tick.run(elapsed_minutes=25)
        assert mock_ops.decay_moments.call_count == 5


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
