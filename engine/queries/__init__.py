"""
Blood Ledger — Semantic Query Layer

Natural language queries using embeddings + graph.

Usage:
    from engine.queries import SemanticSearch

    search = SemanticSearch()

    # Search by natural language
    results = search.find("oaths and promises")

    # Find similar narratives
    similar = search.find_similar("narr_oath")
"""

from .semantic import SemanticSearch, get_semantic_search

__all__ = ['SemanticSearch', 'get_semantic_search']
