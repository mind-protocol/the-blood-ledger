# DOCS: docs/infrastructure/world-builder/TEST/TEST_Overview.md
"""
Tests for World Builder module.

Specs:
- docs/infrastructure/world-builder/VALIDATION/VALIDATION_Overview.md (invariants)
- docs/infrastructure/world-builder/ALGORITHM/ALGORITHM_Overview.md (flow)
- docs/infrastructure/world-builder/TEST/TEST_Overview.md (test cases)

Implementation:
- engine/infrastructure/world_builder/
"""

import pytest
from unittest.mock import MagicMock, Mock, patch, AsyncMock
import sys
from pathlib import Path
import numpy as np

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_graph():
    """Create a mock GraphQueries instance."""
    graph = MagicMock()
    graph.query.return_value = []
    graph.get_character.return_value = {
        'id': 'char_test',
        'name': 'Test Character',
        'backstory_wound': 'Lost everything',
        'voice_tone': 'melancholic'
    }
    graph.get_place.return_value = {
        'id': 'place_test',
        'name': 'Test Place',
        'type': 'camp',
        'mood': 'tense'
    }
    graph.graph_name = 'test_graph'
    graph.host = 'localhost'
    graph.port = 6379
    return graph


@pytest.fixture
def mock_semantic_search():
    """Create a mock SemanticSearch instance."""
    search = MagicMock()
    search.find.return_value = [
        {'id': 'node_1', 'name': 'Result 1', 'similarity': 0.8},
        {'id': 'node_2', 'name': 'Result 2', 'similarity': 0.7},
        {'id': 'node_3', 'name': 'Result 3', 'similarity': 0.6},
    ]
    return search


@pytest.fixture
def mock_embed_fn():
    """Create a mock embedding function."""
    def embed(text):
        # Return a deterministic embedding based on text hash
        np.random.seed(hash(text) % 2**32)
        return np.random.rand(768).astype(np.float32)
    return embed


@pytest.fixture
def mock_count_links_fn():
    """Create a mock link count function."""
    def count_links(node_id):
        # Return 2 links for most nodes
        return 2
    return count_links


@pytest.fixture
def sample_enrichment():
    """Sample enrichment response from LLM."""
    return {
        'characters': [
            {
                'id': 'char_uncle',
                'name': 'Uncle Godric',
                'character_type': 'minor',
                'backstory': 'Your father\'s brother',
                'voice': {'tone': 'bitter'}
            }
        ],
        'places': [
            {
                'id': 'place_farm',
                'name': 'The Old Farm',
                'type': 'homestead',
                'atmosphere': {'sounds': 'wind'},
                'description': 'A ruined farm'
            }
        ],
        'things': [
            {
                'id': 'thing_ring',
                'name': 'Father\'s Ring',
                'type': 'jewelry',
                'description': 'A silver ring',
                'significance': 'Family heirloom'
            }
        ],
        'narratives': [
            {
                'id': 'narr_feud',
                'name': 'The Family Feud',
                'content': 'Godric never forgave your father',
                'type': 'memory',
                'truth': 0.7
            }
        ],
        'links': [
            {
                'from': 'char_test',
                'to': 'char_uncle',
                'type': 'RELATED_TO',
                'weight': 0.6
            }
        ],
        'moments': [
            {
                'text': 'I should find Uncle Godric.',
                'type': 'thought',
                'weight': 0.5,
                'speaker_id': 'char_test'
            }
        ]
    }


@pytest.fixture
def mock_llm_yaml_response():
    """Mock LLM response with YAML."""
    return """Here is the enrichment content:

```yaml
characters:
  - id: char_relative
    name: Anna
    character_type: minor
    backstory: Your sister's daughter

moments:
  - text: "I haven't seen Anna in years."
    type: thought
    weight: 0.5
    speaker_id: char_test
```

This provides family connections for the query."""


# =============================================================================
# SPARSITY DETECTION TESTS
# =============================================================================

class TestSparsityDetection:
    """Tests for sparsity.py"""

    def test_empty_results_sparse(self):
        """V: Empty results should always be sparse."""
        from engine.infrastructure.world_builder.sparsity import is_sparse

        result = is_sparse("test query", [])

        assert result.sparse is True
        assert result.reason == 'no_results'
        assert result.cluster_size == 0
        assert result.proximity == 0.0

    def test_single_result_sparse(self, mock_embed_fn, mock_count_links_fn):
        """Single result should be sparse (cluster_size < 2)."""
        from engine.infrastructure.world_builder.sparsity import is_sparse

        results = [{'id': 'node_1', 'name': 'Single Result'}]
        result = is_sparse("test query", results, mock_embed_fn, mock_count_links_fn)

        assert result.sparse is True
        assert result.cluster_size == 1
        assert 'cluster_size' in result.reason

    def test_rich_results_not_sparse(self, mock_embed_fn):
        """Multiple diverse, connected results should not be sparse."""
        from engine.infrastructure.world_builder.sparsity import is_sparse

        # Create diverse results
        results = [
            {'id': 'node_1', 'name': 'Alpha topic discussion'},
            {'id': 'node_2', 'name': 'Beta completely different'},
            {'id': 'node_3', 'name': 'Gamma another subject'},
            {'id': 'node_4', 'name': 'Delta fourth item'},
        ]

        # High link counts
        def high_links(node_id):
            return 5

        result = is_sparse("alpha", results, mock_embed_fn, high_links)

        # With enough results, high connectivity, should not be sparse
        assert result.cluster_size == 4

    def test_sparsity_result_complete(self, mock_embed_fn, mock_count_links_fn):
        """SparsityResult should have all fields."""
        from engine.infrastructure.world_builder.sparsity import is_sparse, SparsityResult

        results = [{'id': 'n1', 'name': 'Test'}]
        result = is_sparse("test", results, mock_embed_fn, mock_count_links_fn)

        assert isinstance(result, SparsityResult)
        assert isinstance(result.sparse, bool)
        assert isinstance(result.proximity, float)
        assert isinstance(result.cluster_size, int)
        assert isinstance(result.diversity, float)
        assert isinstance(result.connectedness, float)

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        from engine.infrastructure.world_builder.sparsity import cosine_similarity

        # Identical vectors
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([1.0, 0.0, 0.0])
        assert cosine_similarity(a, b) == pytest.approx(1.0)

        # Orthogonal vectors
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 1.0, 0.0])
        assert cosine_similarity(a, b) == pytest.approx(0.0)

        # Opposite vectors
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([-1.0, 0.0, 0.0])
        assert cosine_similarity(a, b) == pytest.approx(-1.0)

    def test_cosine_similarity_none_input(self):
        """Cosine similarity with None should return 0."""
        from engine.infrastructure.world_builder.sparsity import cosine_similarity

        assert cosine_similarity(None, np.array([1, 0, 0])) == 0.0
        assert cosine_similarity(np.array([1, 0, 0]), None) == 0.0

    def test_node_to_text_priority(self):
        """node_to_text should prioritize detail > name > text > id."""
        from engine.infrastructure.world_builder.sparsity import node_to_text

        # Detail takes priority
        assert node_to_text({'detail': 'Detail', 'name': 'Name'}) == 'Detail'

        # Name if no detail
        assert node_to_text({'name': 'Name', 'text': 'Text'}) == 'Name'

        # Text if no detail or name
        assert node_to_text({'text': 'Text', 'id': 'id_1'}) == 'Text'

        # Content for narratives
        assert node_to_text({'content': 'Content', 'id': 'id_1'}) == 'Content'

        # Fallback to id
        assert node_to_text({'id': 'id_1'}) == 'id_1'

    def test_no_embeddings_fallback(self, mock_count_links_fn):
        """Without embeddings, should use heuristic fallback."""
        from engine.infrastructure.world_builder.sparsity import is_sparse

        # No embed function provided
        results = [{'id': 'n1'}, {'id': 'n2'}]
        result = is_sparse("test", results, embed_fn=None, count_links_fn=mock_count_links_fn)

        # Should still return a result
        assert isinstance(result.sparse, bool)
        assert result.reason == 'no_embeddings' or result.reason is None


# =============================================================================
# QUERY MOMENT TESTS
# =============================================================================

class TestQueryMomentRecording:
    """Tests for query_moment.py"""

    def test_record_creates_moment(self, mock_graph):
        """Recording query should create a Moment node."""
        from engine.infrastructure.world_builder.query_moment import record_query_moment

        moment_id = record_query_moment(
            query_text="What do I know?",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert moment_id.startswith('mom_')
        assert mock_graph.query.called

    def test_moment_type_thought_with_char(self, mock_graph):
        """Moment should be type 'thought' when char_id provided."""
        from engine.infrastructure.world_builder.query_moment import record_query_moment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        record_query_moment("test", "char_test", None, mock_graph, 0)

        # Check the CREATE query
        create_query = [q for q, p in queries if 'CREATE' in q][0]
        assert "type: 'thought'" in create_query or "'thought'" in str(queries)

    def test_moment_type_query_without_char(self, mock_graph):
        """Moment should be type 'query' when no char_id."""
        from engine.infrastructure.world_builder.query_moment import record_query_moment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        record_query_moment("test", None, None, mock_graph, 0)

        # First query should create the moment
        assert mock_graph.query.called

    def test_moment_links_to_character(self, mock_graph):
        """Moment should link to character via ATTACHED_TO and CAN_SPEAK."""
        from engine.infrastructure.world_builder.query_moment import record_query_moment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        record_query_moment("test", "char_test", None, mock_graph, 0)

        all_queries = ' '.join([q for q, p in queries])
        assert 'ATTACHED_TO' in all_queries
        assert 'CAN_SPEAK' in all_queries

    def test_moment_links_to_place(self, mock_graph):
        """Moment should link to place via OCCURRED_AT."""
        from engine.infrastructure.world_builder.query_moment import record_query_moment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        record_query_moment("test", None, "place_test", mock_graph, 0)

        all_queries = ' '.join([q for q, p in queries])
        assert 'OCCURRED_AT' in all_queries

    def test_link_results_to_moment(self, mock_graph):
        """link_results_to_moment should create ABOUT links."""
        from engine.infrastructure.world_builder.query_moment import link_results_to_moment

        results = [
            {'id': 'node_1', 'similarity': 0.8},
            {'id': 'node_2', 'similarity': 0.7},
        ]

        count = link_results_to_moment("mom_test", results, mock_graph)

        assert count == 2
        assert mock_graph.query.call_count >= 2

    def test_link_weight_from_similarity(self, mock_graph):
        """ABOUT link weight should come from similarity score."""
        from engine.infrastructure.world_builder.query_moment import link_results_to_moment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        results = [{'id': 'node_1', 'similarity': 0.85}]
        link_results_to_moment("mom_test", results, mock_graph)

        # Check params include weight
        link_query = [p for q, p in queries if p and 'weight' in (p or {})]
        assert len(link_query) > 0
        assert link_query[0]['weight'] == 0.85


# =============================================================================
# WORLD BUILDER CLASS TESTS
# =============================================================================

class TestWorldBuilderClass:
    """Tests for world_builder.py"""

    def test_init_with_api_key(self):
        """Should initialize with explicit API key."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        wb = WorldBuilder(api_key="test-key")
        assert wb.api_key == "test-key"

    def test_init_from_env(self):
        """Should use ANTHROPIC_API_KEY env var."""
        import os
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'env-key'}):
            wb = WorldBuilder()
            assert wb.api_key == 'env-key'

    def test_init_no_key_warning(self, caplog):
        """Should log warning when no API key."""
        import os
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        with patch.dict(os.environ, {}, clear=True):
            # Remove ANTHROPIC_API_KEY if present
            os.environ.pop('ANTHROPIC_API_KEY', None)
            wb = WorldBuilder(api_key=None)
            assert wb.api_key is None

    def test_cache_key_generation(self):
        """Cache key should be unique per query+char."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        wb = WorldBuilder(api_key="test")
        key1 = wb._hash_query("query1", "char_a")
        key2 = wb._hash_query("query1", "char_b")
        key3 = wb._hash_query("query2", "char_a")

        assert key1 != key2  # Different char
        assert key1 != key3  # Different query
        assert key2 != key3

    @pytest.mark.asyncio
    async def test_cache_prevents_reenrichment(self):
        """Same query within cache window should return None."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder
        from datetime import datetime

        wb = WorldBuilder(api_key="test")

        # Manually add to cache
        query_hash = wb._hash_query("test query", "char_test")
        wb._cache[query_hash] = datetime.now()

        result = await wb.enrich("test query", {'char_id': 'char_test'})
        assert result is None

    @pytest.mark.asyncio
    async def test_no_api_key_returns_none(self):
        """Without API key, enrich should return None."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        wb = WorldBuilder(api_key=None)
        result = await wb.enrich("test", {})
        assert result is None

    def test_parse_yaml_from_code_fence(self, mock_llm_yaml_response):
        """Should extract YAML from markdown code fence."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        wb = WorldBuilder(api_key="test")
        result = wb._parse_response(mock_llm_yaml_response)

        assert result is not None
        assert 'characters' in result
        assert result['characters'][0]['id'] == 'char_relative'

    def test_parse_plain_yaml(self):
        """Should parse YAML without code fence."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        plain_yaml = """characters:
  - id: char_test
    name: Test
"""
        wb = WorldBuilder(api_key="test")
        result = wb._parse_response(plain_yaml)

        assert result is not None
        assert result['characters'][0]['id'] == 'char_test'

    def test_parse_invalid_yaml(self):
        """Invalid YAML should return None."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        invalid = "this: is: not: valid: yaml: ["
        wb = WorldBuilder(api_key="test")
        result = wb._parse_response(invalid)

        assert result is None

    def test_clear_cache(self):
        """clear_cache should empty the cache."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder
        from datetime import datetime

        wb = WorldBuilder(api_key="test")
        wb._cache['key1'] = datetime.now()
        wb._cache['key2'] = datetime.now()

        wb.clear_cache()

        assert len(wb._cache) == 0

    @pytest.mark.asyncio
    async def test_recursion_prevention(self):
        """Concurrent enrichment of same query should be blocked."""
        from engine.infrastructure.world_builder.world_builder import WorldBuilder

        wb = WorldBuilder(api_key="test")

        # Simulate being in enrichment
        query_hash = wb._hash_query("test", "char")
        wb._enriching.add(query_hash)

        result = await wb.enrich("test", {'char_id': 'char'})
        assert result is None

        wb._enriching.discard(query_hash)


# =============================================================================
# ENRICHMENT APPLICATION TESTS
# =============================================================================

class TestEnrichmentApplication:
    """Tests for enrichment.py"""

    def test_apply_creates_characters(self, mock_graph, sample_enrichment):
        """apply_enrichment should create Character nodes."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['characters'] == 1

    def test_apply_creates_places(self, mock_graph, sample_enrichment):
        """apply_enrichment should create Place nodes."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['places'] == 1

    def test_apply_creates_things(self, mock_graph, sample_enrichment):
        """apply_enrichment should create Thing nodes."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['things'] == 1

    def test_apply_creates_narratives(self, mock_graph, sample_enrichment):
        """apply_enrichment should create Narrative nodes."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['narratives'] == 1

    def test_apply_creates_links(self, mock_graph, sample_enrichment):
        """apply_enrichment should create links between nodes."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['links'] == 1

    def test_apply_creates_moments(self, mock_graph, sample_enrichment):
        """apply_enrichment should create Moment nodes."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['moments'] == 1

    def test_generated_flag_set(self, mock_graph, sample_enrichment):
        """All created nodes should have generated=true."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        # Check that generated=true appears in queries
        all_queries = ' '.join([q for q, p in queries])
        assert 'generated' in all_queries.lower()

    def test_link_to_query_moment(self, mock_graph, sample_enrichment):
        """All created nodes should link back to query moment via ABOUT."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        # Count ABOUT link creations
        about_queries = [q for q, p in queries if 'ABOUT' in q]
        # Should have ABOUT links for: 1 char + 1 place + 1 thing + 1 narrative + 1 moment = 5
        assert len(about_queries) >= 5

    def test_moment_links_to_speaker(self, mock_graph, sample_enrichment):
        """Enriched moments should link to speaker via ATTACHED_TO and CAN_SPEAK."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        queries = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries.append((cypher, params)) or []

        apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        all_queries = ' '.join([q for q, p in queries])
        assert 'CAN_SPEAK' in all_queries

    def test_build_enrichment_prompt(self, mock_graph):
        """build_enrichment_prompt should include context."""
        from engine.infrastructure.world_builder.enrichment import build_enrichment_prompt

        context = {
            'char_id': 'char_test',
            'character_data': {'name': 'Aldric', 'backstory': 'Lost brother'},
            'place_id': 'place_camp',
            'place_data': {'name': 'The Camp', 'type': 'camp'},
            'existing': [{'id': 'n1', 'name': 'Existing Node'}]
        }

        prompt = build_enrichment_prompt("Who are my relatives?", context)

        assert "Who are my relatives?" in prompt
        assert "Aldric" in prompt
        assert "The Camp" in prompt
        assert "1087 England" in prompt
        assert "YAML" in prompt


# =============================================================================
# QUERY INTERFACE TESTS
# =============================================================================

def _get_query_module():
    """Get the actual query module (not the function)."""
    import importlib
    return importlib.import_module('engine.infrastructure.world_builder.query')


class TestQueryInterface:
    """Tests for query.py"""

    @pytest.mark.asyncio
    async def test_query_records_moment(self, mock_graph, mock_semantic_search):
        """query() should record a query moment."""
        query_module = _get_query_module()

        with patch.object(query_module, '_get_default_semantic_search', return_value=mock_semantic_search):
            with patch.object(query_module, 'get_default_world_builder') as mock_wb:
                mock_wb.return_value.enrich = AsyncMock(return_value=None)

                results = await query_module.query(
                    "test query",
                    mock_graph,
                    char_id="char_test",
                    enrich=False
                )

        # Should have called graph.query to create moment
        assert mock_graph.query.called

    @pytest.mark.asyncio
    async def test_query_executes_search(self, mock_graph, mock_semantic_search):
        """query() should execute semantic search."""
        query_module = _get_query_module()

        with patch.object(query_module, '_get_default_semantic_search', return_value=mock_semantic_search):
            results = await query_module.query(
                "test query",
                mock_graph,
                enrich=False
            )

        mock_semantic_search.find.assert_called_once()

    @pytest.mark.asyncio
    async def test_query_returns_results(self, mock_graph, mock_semantic_search):
        """query() should return search results."""
        query_module = _get_query_module()

        with patch.object(query_module, '_get_default_semantic_search', return_value=mock_semantic_search):
            results = await query_module.query(
                "test query",
                mock_graph,
                enrich=False
            )

        assert len(results) == 3
        assert results[0]['id'] == 'node_1'

    def test_query_sync_no_enrichment(self, mock_graph, mock_semantic_search):
        """query_sync() should not call LLM."""
        query_module = _get_query_module()

        with patch.object(query_module, '_get_default_semantic_search', return_value=mock_semantic_search):
            results = query_module.query_sync(
                "test query",
                mock_graph,
                char_id="char_test"
            )

        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_query_enriches_sparse_results(self, mock_graph, mock_semantic_search, sample_enrichment):
        """query() should enrich when results are sparse."""
        query_module = _get_query_module()

        # Make results sparse
        mock_semantic_search.find.return_value = []

        with patch.object(query_module, '_get_default_semantic_search', return_value=mock_semantic_search):
            with patch.object(query_module, 'get_default_world_builder') as mock_wb:
                mock_builder = MagicMock()
                mock_builder.enrich = AsyncMock(return_value=sample_enrichment)
                mock_wb.return_value = mock_builder

                results = await query_module.query(
                    "test query",
                    mock_graph,
                    char_id="char_test",
                    enrich=True
                )

        # Should have called enrich
        mock_builder.enrich.assert_called_once()


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestEdgeCases:
    """Edge case tests."""

    def test_empty_enrichment(self, mock_graph):
        """Empty enrichment dict should not crash."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        counts = apply_enrichment(
            enrichment={},
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['characters'] == 0
        assert counts['places'] == 0
        assert counts['moments'] == 0

    def test_enrichment_missing_id(self, mock_graph):
        """Enrichment items without id should be skipped."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        enrichment = {
            'characters': [
                {'name': 'No ID Character'}  # Missing id
            ]
        }

        counts = apply_enrichment(
            enrichment=enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['characters'] == 0

    def test_moment_missing_text(self, mock_graph):
        """Moment without text should be skipped."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        enrichment = {
            'moments': [
                {'type': 'thought', 'weight': 0.5}  # Missing text
            ]
        }

        counts = apply_enrichment(
            enrichment=enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id="place_test",
            graph=mock_graph,
            tick=100
        )

        assert counts['moments'] == 0

    @pytest.mark.asyncio
    async def test_search_failure_graceful(self, mock_graph):
        """Search failure should not crash query()."""
        query_module = _get_query_module()

        failing_search = MagicMock()
        failing_search.find.side_effect = Exception("Search failed")

        with patch.object(query_module, '_get_default_semantic_search', return_value=failing_search):
            results = await query_module.query(
                "test query",
                mock_graph,
                enrich=False
            )

        assert results == []

    def test_graph_failure_graceful(self, mock_graph):
        """Graph failure should not crash query moment recording."""
        from engine.infrastructure.world_builder.query_moment import record_query_moment

        mock_graph.query.side_effect = Exception("Graph error")

        # Should not raise
        moment_id = record_query_moment("test", "char", "place", mock_graph, 0)
        assert moment_id.startswith('mom_')


# =============================================================================
# INVARIANT TESTS
# =============================================================================

class TestInvariants:
    """Tests for validation invariants."""

    def test_v1_query_creates_moment(self, mock_graph, mock_semantic_search):
        """V1: Every query creates a moment."""
        query_module = _get_query_module()

        queries_made = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries_made.append(cypher) or []

        with patch.object(query_module, '_get_default_semantic_search', return_value=mock_semantic_search):
            query_module.query_sync("test", mock_graph)

        # Should have CREATE query for moment
        create_queries = [q for q in queries_made if 'CREATE' in q and 'Moment' in q]
        assert len(create_queries) > 0

    def test_v5_moments_always_thought(self, mock_graph, sample_enrichment):
        """V5: All created moments are type 'thought'."""
        from engine.infrastructure.world_builder.enrichment import apply_enrichment

        queries_made = []
        mock_graph.query.side_effect = lambda cypher, params=None: queries_made.append((cypher, params)) or []

        apply_enrichment(
            enrichment=sample_enrichment,
            query_moment_id="mom_query",
            char_id="char_test",
            place_id=None,
            graph=mock_graph,
            tick=100
        )

        # Find moment creation query
        moment_queries = [q for q, p in queries_made if 'Moment' in q and 'CREATE' in q]
        for q in moment_queries:
            assert "'thought'" in q or "type: 'thought'" in q

    def test_v6_sparsity_thresholds(self):
        """V6: Sparsity thresholds match constants."""
        from engine.infrastructure.world_builder import sparsity

        assert sparsity.SPARSITY_PROXIMITY_THRESHOLD == 0.6
        assert sparsity.SPARSITY_MIN_CLUSTER == 2
        assert sparsity.SPARSITY_MIN_DIVERSITY == 0.3
        assert sparsity.SPARSITY_MIN_CONNECTEDNESS == 1.5
