# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md
"""
Universal query interface for World Builder.

The main entry point for all graph queries with:
- Query moment recording (attention as energy)
- Semantic search execution
- Sparsity detection and enrichment
- Result linking

Every query leaves a trace. Sparse results trigger content generation.

Specs:
- docs/infrastructure/world-builder/ALGORITHM_World_Builder.md
"""

import logging
from typing import List, Dict, Any, Optional

from .sparsity import is_sparse, SparsityResult
from .query_moment import record_query_moment, link_results_to_moment
from .enrichment import apply_enrichment
from .world_builder import get_default_world_builder

logger = logging.getLogger(__name__)


async def query(
    query_text: str,
    graph,
    char_id: Optional[str] = None,
    place_id: Optional[str] = None,
    enrich: bool = True,
    tick: int = 0,
    semantic_search=None,
    embed_fn=None,
    count_links_fn=None
) -> List[Dict[str, Any]]:
    """
    The universal graph query function.

    - Records query as moment (energy=0.3)
    - Executes semantic search
    - Links results to moment via ABOUT (physics flows energy)
    - Enriches if sparse
    - Returns results

    Args:
        query_text: Natural language query
        graph: GraphQueries instance
        char_id: Character perspective (query becomes their thought)
        place_id: Location context
        enrich: Whether to enrich if sparse (default True)
        tick: Current world tick
        semantic_search: SemanticSearch instance (optional, uses default)
        embed_fn: Embedding function for sparsity check
        count_links_fn: Link count function for sparsity check

    Returns:
        List of result nodes

    Example:
        results = await query(
            "What do I know about Edmund?",
            graph,
            char_id="char_aldric",
            place_id="place_camp"
        )
    """
    # 1. Record query as moment (this IS the energy source)
    moment_id = record_query_moment(
        query_text=query_text,
        char_id=char_id,
        place_id=place_id,
        graph=graph,
        tick=tick
    )

    logger.debug(f"[Query] Recorded query moment: {moment_id}")

    # 2. Execute semantic search
    if semantic_search is None:
        semantic_search = _get_default_semantic_search(graph)

    results = []
    if semantic_search:
        try:
            results = semantic_search.find(query_text, limit=10)
        except Exception as e:
            logger.warning(f"[Query] Semantic search failed: {e}")
            results = []

    logger.debug(f"[Query] Found {len(results)} results")

    # 3. Link results to moment (weight=similarity, physics flows energy)
    link_results_to_moment(moment_id, results, graph, max_links=5)

    # 4. Check sparsity and enrich if needed
    if enrich and results is not None:
        # Create link count function if not provided
        if count_links_fn is None:
            count_links_fn = _create_count_links_fn(graph)

        sparsity = is_sparse(
            query_text=query_text,
            results=results,
            embed_fn=embed_fn,
            count_links_fn=count_links_fn
        )

        if sparsity.sparse:
            logger.info(f"[Query] Sparse results ({sparsity.reason}), triggering enrichment")

            # Build enrichment context
            context = _build_enrichment_context(
                char_id=char_id,
                place_id=place_id,
                existing=results,
                sparsity=sparsity,
                graph=graph
            )

            # Get enrichment from World Builder
            world_builder = get_default_world_builder()
            enrichment = await world_builder.enrich(query_text, context)

            if enrichment:
                # Apply enrichment - creates nodes, links back to query moment
                counts = apply_enrichment(
                    enrichment=enrichment,
                    query_moment_id=moment_id,
                    char_id=char_id,
                    place_id=place_id,
                    graph=graph,
                    tick=tick
                )

                logger.info(f"[Query] Applied enrichment: {counts}")

                # Re-query to get enriched results
                if semantic_search:
                    try:
                        new_results = semantic_search.find(query_text, limit=10)
                        # Link new results
                        link_results_to_moment(moment_id, new_results[5:], graph, max_links=5)
                        results = new_results
                    except Exception as e:
                        logger.warning(f"[Query] Re-query after enrichment failed: {e}")

    return results


def query_sync(
    query_text: str,
    graph,
    char_id: Optional[str] = None,
    place_id: Optional[str] = None,
    tick: int = 0,
    semantic_search=None
) -> List[Dict[str, Any]]:
    """
    Synchronous query without enrichment.

    Use this when you just need to search without LLM enrichment.

    Args:
        query_text: Natural language query
        graph: GraphQueries instance
        char_id: Character perspective
        place_id: Location context
        tick: Current world tick
        semantic_search: SemanticSearch instance

    Returns:
        List of result nodes
    """
    # Record query as moment
    moment_id = record_query_moment(
        query_text=query_text,
        char_id=char_id,
        place_id=place_id,
        graph=graph,
        tick=tick
    )

    # Execute semantic search
    if semantic_search is None:
        semantic_search = _get_default_semantic_search(graph)

    results = []
    if semantic_search:
        try:
            results = semantic_search.find(query_text, limit=10)
        except Exception as e:
            logger.warning(f"[Query] Semantic search failed: {e}")
            results = []

    # Link results to moment
    link_results_to_moment(moment_id, results, graph, max_links=5)

    return results


def _get_default_semantic_search(graph):
    """Get or create default semantic search instance."""
    try:
        from engine.world.map.semantic import get_semantic_search
        return get_semantic_search(
            graph_name=graph.graph_name if hasattr(graph, 'graph_name') else "blood_ledger",
            host=graph.host if hasattr(graph, 'host') else "localhost",
            port=graph.port if hasattr(graph, 'port') else 6379
        )
    except ImportError:
        logger.warning("[Query] SemanticSearch not available")
        return None


def _create_count_links_fn(graph):
    """Create a function to count links for a node."""
    def count_links(node_id: str) -> int:
        if not node_id:
            return 0
        try:
            cypher = """
            MATCH (n {id: $node_id})-[r]-()
            RETURN count(r) AS link_count
            """
            result = graph.query(cypher, {'node_id': node_id})
            if result and len(result) > 0:
                return result[0].get('link_count', 0)
            return 0
        except Exception:
            return 0

    return count_links


def _build_enrichment_context(
    char_id: Optional[str],
    place_id: Optional[str],
    existing: List[Dict[str, Any]],
    sparsity: SparsityResult,
    graph
) -> Dict[str, Any]:
    """Build context dict for enrichment prompt."""
    context = {
        'char_id': char_id,
        'place_id': place_id,
        'existing': existing,
        'sparsity': sparsity
    }

    # Get character data if available
    if char_id:
        try:
            char_data = graph.get_character(char_id)
            if char_data:
                context['character_data'] = char_data
        except Exception:
            pass

    # Get place data if available
    if place_id:
        try:
            place_data = graph.get_place(place_id)
            if place_data:
                context['place_data'] = place_data
        except Exception:
            pass

    return context
