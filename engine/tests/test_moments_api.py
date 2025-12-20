"""
Tests for Moment Graph API Endpoints.

Tests the FastAPI endpoints in engine/infrastructure/api/moments.py:
- GET /api/moments/current/{playthrough_id}
- POST /api/moments/click
- GET /api/moments/{moment_id}
- POST /api/moments/surface
- GET /api/moments/stats
- GET /api/moments/stream/{playthrough_id} (SSE)

Uses TestClient for synchronous tests, httpx for async SSE tests.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi.testclient import TestClient


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_moment_queries():
    """Create mocked MomentQueries."""
    with patch('engine.infrastructure.api.moments.MomentQueries') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance

        # Default return values
        mock_instance.get_current_view.return_value = {
            "moments": [
                {
                    "id": "moment_test_1",
                    "text": "The fire crackles.",
                    "type": "narration",
                    "status": "active",
                    "weight": 0.8,
                    "tone": None
                }
            ],
            "transitions": [
                {
                    "from_id": "moment_test_1",
                    "to_id": "moment_test_2",
                    "trigger": "click",
                    "require_words": ["fire"],
                    "weight_transfer": 0.3,
                    "consumes_origin": True
                }
            ],
            "active_count": 1
        }

        mock_instance.get_moment_by_id.return_value = {
            "id": "moment_test_1",
            "text": "The fire crackles.",
            "type": "narration",
            "status": "active",
            "weight": 0.8
        }

        yield mock_instance


@pytest.fixture
def mock_moment_traversal():
    """Create mocked MomentTraversal."""
    with patch('engine.infrastructure.api.moments.MomentTraversal') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance

        # Default return values
        mock_instance.handle_click.return_value = {
            "id": "moment_test_2",
            "text": "He speaks.",
            "type": "dialogue",
            "weight": 0.8,
            "consumes_origin": True,
            "require_words": ["fire"]
        }

        mock_instance.activate_moment.return_value = None

        yield mock_instance


@pytest.fixture
def mock_moment_surface():
    """Create mocked MomentSurface."""
    with patch('engine.infrastructure.api.moments.MomentSurface') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance

        mock_instance.get_surface_stats.return_value = {
            "possible": 10,
            "active": 3,
            "spoken": 50,
            "dormant": 5,
            "decayed": 20
        }

        mock_instance.set_moment_weight.return_value = None

        yield mock_instance


@pytest.fixture
def mock_graph_queries():
    """Create mocked GraphQueries."""
    with patch('engine.infrastructure.api.moments.GraphQueries') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance

        # Default: player at camp
        mock_instance.query.return_value = [["place_camp"]]

        yield mock_instance


@pytest.fixture
def test_client(mock_moment_queries, mock_moment_traversal, mock_moment_surface, mock_graph_queries):
    """Create TestClient with mocked dependencies."""
    from engine.infrastructure.api.moments import create_moments_router
    from fastapi import FastAPI

    app = FastAPI()
    router = create_moments_router(
        host="localhost",
        port=6379,
        playthroughs_dir="playthroughs"
    )
    app.include_router(router, prefix="/api")

    return TestClient(app)


# =============================================================================
# GET CURRENT MOMENTS TESTS
# =============================================================================

class TestGetCurrentMoments:
    """Test GET /api/moments/current/{playthrough_id}."""

    def test_get_current_moments_basic(self, test_client, mock_moment_queries):
        """Test getting current moments returns expected structure."""
        response = test_client.get(
            "/api/moments/current/pt_test123",
            params={"location": "place_camp"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "moments" in data
        assert "transitions" in data
        assert "active_count" in data

        # Should have one moment
        assert len(data["moments"]) == 1
        assert data["moments"][0]["id"] == "moment_test_1"

    def test_get_current_moments_with_clickable_words(self, test_client, mock_moment_queries):
        """Test clickable words are derived from transitions."""
        response = test_client.get(
            "/api/moments/current/pt_test123",
            params={"location": "place_camp"}
        )

        data = response.json()

        # First moment should have "fire" as clickable
        assert "clickable_words" in data["moments"][0]
        assert "fire" in data["moments"][0]["clickable_words"]

    def test_get_current_moments_auto_location(self, test_client, mock_moment_queries, mock_graph_queries):
        """Test auto-resolving location from player AT link."""
        # Don't pass location, should auto-resolve
        response = test_client.get(
            "/api/moments/current/pt_test123",
            params={"player_id": "char_player"}
        )

        assert response.status_code == 200
        # GraphQueries should have been called to get location
        mock_graph_queries.query.assert_called()

    def test_get_current_moments_with_present_chars(self, test_client, mock_moment_queries):
        """Test passing present characters as comma-separated list."""
        response = test_client.get(
            "/api/moments/current/pt_test123",
            params={
                "location": "place_camp",
                "present_chars": "char_aldric,char_wulfric"
            }
        )

        assert response.status_code == 200
        # Verify the query was called with parsed chars
        call_args = mock_moment_queries.get_current_view.call_args
        assert "char_aldric" in call_args.kwargs["present_chars"]


# =============================================================================
# CLICK TESTS
# =============================================================================

class TestClickWord:
    """Test POST /api/moments/click."""

    def test_click_word_success(self, test_client, mock_moment_traversal):
        """Test successful click traversal."""
        response = test_client.post(
            "/api/moments/click",
            json={
                "playthrough_id": "pt_test123",
                "moment_id": "moment_test_1",
                "word": "fire",
                "tick": 1440
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ok"
        assert data["traversed"] == True
        assert data["target_moment"]["id"] == "moment_test_2"

    def test_click_word_no_match(self, test_client, mock_moment_traversal):
        """Test click with no matching transition."""
        mock_moment_traversal.handle_click.return_value = None

        response = test_client.post(
            "/api/moments/click",
            json={
                "playthrough_id": "pt_test123",
                "moment_id": "moment_test_1",
                "word": "random",
                "tick": 1440
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "no_match"
        assert data["traversed"] == False

    def test_click_word_error_handling(self, test_client, mock_moment_traversal):
        """Test click error returns error status."""
        mock_moment_traversal.handle_click.side_effect = Exception("DB error")

        response = test_client.post(
            "/api/moments/click",
            json={
                "playthrough_id": "pt_test123",
                "moment_id": "moment_test_1",
                "word": "fire",
                "tick": 1440
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "error"
        assert data["traversed"] == False


# =============================================================================
# GET SINGLE MOMENT TESTS
# =============================================================================

class TestGetMoment:
    """Test GET /api/moments/{moment_id}."""

    def test_get_moment_exists(self, test_client, mock_moment_queries):
        """Test getting an existing moment."""
        response = test_client.get("/api/moments/pt_test123/moment_test_1")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == "moment_test_1"
        assert data["text"] == "The fire crackles."

    def test_get_moment_not_found(self, test_client, mock_moment_queries):
        """Test getting a non-existent moment."""
        mock_moment_queries.get_moment_by_id.return_value = None

        response = test_client.get("/api/moments/pt_test123/nonexistent")

        assert response.status_code == 404


# =============================================================================
# SURFACE TESTS
# =============================================================================

class TestSurfaceMoment:
    """Test POST /api/moments/surface."""

    def test_surface_moment(self, test_client, mock_moment_surface, mock_moment_traversal):
        """Test manually surfacing a moment."""
        response = test_client.post(
            "/api/moments/surface",
            json={
                "moment_id": "moment_test_1",
                "playthrough_id": "pt_test123"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ok"
        assert data["moment_id"] == "moment_test_1"

        # Verify weight was set and moment activated
        mock_moment_surface.set_moment_weight.assert_called_with("moment_test_1", 1.0)
        mock_moment_traversal.activate_moment.assert_called()


# =============================================================================
# STATS TESTS
# =============================================================================

class TestMomentStats:
    """Test GET /api/moments/stats."""

    def test_get_stats(self, test_client, mock_moment_surface):
        """Test getting moment statistics."""
        response = test_client.get("/api/moments/stats/pt_test123")

        assert response.status_code == 200
        data = response.json()

        assert "stats" in data
        assert data["stats"]["possible"] == 10
        assert data["stats"]["active"] == 3
        assert data["stats"]["spoken"] == 50


# =============================================================================
# SSE STREAM TESTS
# =============================================================================

class TestMomentStream:
    """Test GET /api/moments/stream/{playthrough_id}."""

    def test_stream_connection(self, test_client):
        """Test SSE stream sends connected event."""
        with test_client.stream(
            "GET",
            "/api/moments/stream/pt_test123"
        ) as response:
            # Read first event
            for line in response.iter_lines():
                if line:
                    line_str = line.decode() if isinstance(line, bytes) else line
                    if line_str.startswith("event:"):
                        assert "connected" in line_str
                        break


# =============================================================================
# REQUEST VALIDATION TESTS
# =============================================================================

class TestRequestValidation:
    """Test request validation for endpoints."""

    def test_click_requires_playthrough_id(self, test_client):
        """Test click endpoint requires playthrough_id."""
        response = test_client.post(
            "/api/moments/click",
            json={
                "moment_id": "moment_test_1",
                "word": "fire",
                "tick": 1440
            }
        )

        assert response.status_code == 422  # Validation error

    def test_click_requires_moment_id(self, test_client):
        """Test click endpoint requires moment_id."""
        response = test_client.post(
            "/api/moments/click",
            json={
                "playthrough_id": "pt_test123",
                "word": "fire",
                "tick": 1440
            }
        )

        assert response.status_code == 422

    def test_surface_requires_both_ids(self, test_client):
        """Test surface endpoint requires both IDs."""
        response = test_client.post(
            "/api/moments/surface",
            json={
                "moment_id": "moment_test_1"
            }
        )

        assert response.status_code == 422


# =============================================================================
# RESPONSE MODEL TESTS
# =============================================================================

class TestResponseModels:
    """Test response models conform to spec."""

    def test_current_moments_response_shape(self, test_client):
        """Test CurrentMomentsResponse shape matches spec."""
        response = test_client.get(
            "/api/moments/current/pt_test123",
            params={"location": "place_camp"}
        )

        data = response.json()

        # Required fields
        assert "moments" in data
        assert "transitions" in data
        assert "active_count" in data

        # Moment shape
        moment = data["moments"][0]
        assert "id" in moment
        assert "text" in moment
        assert "type" in moment
        assert "status" in moment
        assert "weight" in moment
        assert "clickable_words" in moment

        # Transition shape
        if data["transitions"]:
            transition = data["transitions"][0]
            assert "from_id" in transition
            assert "to_id" in transition
            assert "trigger" in transition
            assert "require_words" in transition

    def test_click_response_shape(self, test_client, mock_moment_traversal):
        """Test ClickResponse shape matches spec."""
        response = test_client.post(
            "/api/moments/click",
            json={
                "playthrough_id": "pt_test123",
                "moment_id": "moment_test_1",
                "word": "fire",
                "tick": 1440
            }
        )

        data = response.json()

        assert "status" in data
        assert "traversed" in data
        assert "consumed_origin" in data
        assert "new_active_moments" in data


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
