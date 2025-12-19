# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md
"""
World Builder module.

JIT compiler for narrative content. Graph is sparse by default.
Content materializes on demand when queries return unsatisfying results.

Key principles:
1. Every query is a moment - queries leave traces in the graph
2. Sparse triggers enrichment - World Builder invents content when needed

Usage:
    from engine.infrastructure.world_builder import query

    # Async query with enrichment
    results = await query(
        "What do I know about Edmund?",
        graph,
        char_id="char_aldric",
        place_id="place_camp"
    )

    # Sync query without enrichment
    from engine.infrastructure.world_builder import query_sync
    results = query_sync("memories of home", graph, char_id="char_player")
"""

from .query import query, query_sync
from .world_builder import WorldBuilder, get_default_world_builder
from .sparsity import is_sparse, SparsityResult
from .query_moment import record_query_moment, link_results_to_moment
from .enrichment import apply_enrichment, build_enrichment_prompt

__all__ = [
    # Main query interface
    'query',
    'query_sync',
    # World Builder
    'WorldBuilder',
    'get_default_world_builder',
    # Sparsity detection
    'is_sparse',
    'SparsityResult',
    # Query moment recording
    'record_query_moment',
    'link_results_to_moment',
    # Enrichment
    'apply_enrichment',
    'build_enrichment_prompt',
]
