"""
Blood Ledger — Semantic Search

Natural language queries using embeddings + FalkorDB vector search.
"""

import logging
from typing import List, Dict, Any, Optional

from engine.infrastructure.embeddings import get_embedding_service
from engine.physics.graph import GraphQueries

logger = logging.getLogger(__name__)

_semantic_search: Optional['SemanticSearch'] = None


class SemanticSearch:
    """
    Semantic search combining embeddings with graph queries.
    """

    def __init__(
        self,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379
    ):
        self.graph = GraphQueries(graph_name=graph_name, host=host, port=port)
        self.embeddings = get_embedding_service()
        logger.info("[SemanticSearch] Initialized")

    def find(
        self,
        query: str,
        node_types: List[str] = None,
        limit: int = 10,
        min_similarity: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Find nodes matching a natural language query.

        Args:
            query: Natural language search query
            node_types: Filter by types (character, place, thing, narrative)
            limit: Max results
            min_similarity: Minimum similarity threshold

        Returns:
            List of matching nodes with similarity scores

        Example:
            results = search.find("oaths and loyalty")
            results = search.find("places near York", node_types=["place"])
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed(query)

        # Search using FalkorDB vector index
        results = self._vector_search(
            query_embedding,
            node_types=node_types,
            limit=limit * 2  # Get extra for filtering
        )

        # Filter by similarity and limit
        filtered = [
            r for r in results
            if r.get('similarity', 0) >= min_similarity
        ][:limit]

        return filtered

    def find_similar(
        self,
        node_id: str,
        node_types: List[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find nodes similar to a given node.

        Args:
            node_id: ID of node to find similar to
            node_types: Filter by types
            limit: Max results

        Returns:
            List of similar nodes
        """
        # Get the node's embedding
        node = self._get_node_with_embedding(node_id)
        if not node or not node.get('embedding'):
            return []

        # Search for similar
        results = self._vector_search(
            node['embedding'],
            node_types=node_types,
            limit=limit + 1  # +1 to exclude self
        )

        # Filter out the source node
        return [r for r in results if r.get('id') != node_id][:limit]

    def find_narratives_like(
        self,
        text: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find narratives similar to given text.

        Args:
            text: Text to match
            limit: Max results

        Returns:
            List of matching narratives
        """
        return self.find(text, node_types=['narrative'], limit=limit)

    def find_characters_like(
        self,
        description: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find characters matching a description.

        Args:
            description: Character description
            limit: Max results

        Returns:
            List of matching characters
        """
        return self.find(description, node_types=['character'], limit=limit)

    def answer_question(
        self,
        question: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find nodes that might answer a question.

        Args:
            question: Natural language question
            limit: Max results

        Returns:
            Relevant nodes sorted by relevance

        Example:
            results = search.answer_question("Who knows about the betrayal?")
            results = search.answer_question("What happened at Thornwick?")
        """
        # For questions, search narratives first (they contain stories)
        narrative_results = self.find(question, node_types=['narrative'], limit=limit)

        # Also search characters for "who" questions
        if any(w in question.lower() for w in ['who', 'whom', 'whose']):
            char_results = self.find(question, node_types=['character'], limit=3)
            # Interleave results
            combined = []
            for i in range(max(len(narrative_results), len(char_results))):
                if i < len(narrative_results):
                    combined.append(narrative_results[i])
                if i < len(char_results):
                    combined.append(char_results[i])
            return combined[:limit]

        return narrative_results

    def _vector_search(
        self,
        embedding: List[float],
        node_types: List[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search using FalkorDB vector index.
        """
        # Build type filter
        type_filter = ""
        if node_types:
            labels = ' OR '.join(f'n:{t.capitalize()}' for t in node_types)
            type_filter = f"WHERE ({labels})"

        # FalkorDB vector search
        # Note: Requires vector index to be created
        embedding_str = str(embedding)

        try:
            cypher = f"""
            CALL db.idx.vector.queryNodes('Node', 'embedding', {limit}, vecf32({embedding_str}))
            YIELD node, score
            {type_filter}
            RETURN node.id AS id, node.name AS name, node.type AS type,
                   node.content AS content,
                   node.description AS description,
                   node.backstory_wound AS wound,
                   node.backstory_why_here AS why_here,
                   node.mood AS mood,
                   node.tone AS tone,
                   score AS similarity
            ORDER BY score DESC
            LIMIT {limit}
            """
            return self.graph.query(cypher)
        except Exception as e:
            # Fallback to brute-force if vector index not available
            logger.warning(f"Vector search failed, using fallback: {e}")
            return self._fallback_search(embedding, node_types, limit)

    def _fallback_search(
        self,
        embedding: List[float],
        node_types: List[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fallback search without vector index (brute force).
        """
        # Get all nodes with embeddings
        type_filter = ""
        if node_types:
            labels = ' OR '.join(f'n:{t.capitalize()}' for t in node_types)
            type_filter = f"WHERE ({labels}) AND "
        else:
            type_filter = "WHERE "

        cypher = f"""
        MATCH (n)
        {type_filter}n.embedding IS NOT NULL
        RETURN n.id AS id, n.name AS name, n.type AS type,
               n.content AS content, n.description AS description,
               n.backstory_wound AS wound, n.backstory_why_here AS why_here,
               n.mood AS mood, n.tone AS tone, n.embedding AS embedding
        """

        try:
            nodes = self.graph.query(cypher)
        except:
            return []

        # Compute similarities
        results = []
        for node in nodes:
            node_emb = node.get('embedding')
            if node_emb:
                if isinstance(node_emb, str):
                    import json
                    node_emb = json.loads(node_emb)
                sim = self.embeddings.similarity(embedding, node_emb)
                results.append({
                    'id': node.get('id'),
                    'name': node.get('name'),
                    'type': node.get('type'),
                    'content': node.get('content'),
                    'description': node.get('description'),
                    'wound': node.get('wound'),
                    'why_here': node.get('why_here'),
                    'mood': node.get('mood'),
                    'tone': node.get('tone'),
                    'similarity': sim
                })

        # Sort by similarity
        results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        return results[:limit]

    def _get_node_with_embedding(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get a node with its embedding."""
        cypher = f"""
        MATCH (n {{id: '{node_id}'}})
        RETURN n.id AS id, n.embedding AS embedding
        """
        try:
            results = self.graph.query(cypher)
            return results[0] if results else None
        except:
            return None


def get_semantic_search(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379
) -> SemanticSearch:
    """Get singleton semantic search instance."""
    global _semantic_search
    if _semantic_search is None:
        _semantic_search = SemanticSearch(graph_name, host, port)
    return _semantic_search
