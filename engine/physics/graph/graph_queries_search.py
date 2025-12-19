"""
Blood Ledger — Search Query Methods

Mixin class providing semantic search methods for GraphQueries.
Extracted from graph_queries.py to reduce file size.

DOCS: docs/physics/IMPLEMENTATION_Physics.md

Usage:
    This module is automatically mixed into GraphQueries.
    Use it via the main GraphQueries class:

    from engine.physics.graph.graph_queries import GraphQueries

    graph = GraphQueries()

    # Semantic search
    results = graph.search("Tell me about the oath", embed_fn=get_embedding)
"""

import json
import logging
from typing import Dict, Any, List, Callable

import numpy as np

from engine.physics.graph.graph_query_utils import (
    SYSTEM_FIELDS,
    extract_node_props,
    extract_link_props,
)

logger = logging.getLogger(__name__)

# Max nodes per cluster
MAX_CLUSTER_SIZE = 40

# Output formats
FORMAT_JSON = 'json'
FORMAT_MARKDOWN = 'md'


class SearchQueryMixin:
    """
    Mixin class providing semantic search methods.

    These methods are mixed into GraphQueries to provide search-related
    functionality while keeping the main file smaller.

    Prerequisites:
        - self._query(cypher, params) method
    """

    # =========================================================================
    # NATURAL LANGUAGE SEARCH
    # =========================================================================

    def search(
        self,
        query: str,
        embed_fn: Callable[[str], List[float]],
        top_k: int = 10,
        expand_connections: bool = True,
        format: str = FORMAT_MARKDOWN
    ) -> Any:
        """
        Search the graph using natural language.

        IMPORTANT: This method returns ALL fields for every node. NEVER filter
        output fields - the LLM needs complete context to make decisions.

        Args:
            query: Natural language query (e.g., "Who betrayed Edmund?")
            embed_fn: Function to convert text to embedding
            top_k: Number of top matches to return
            expand_connections: If True, expand to include connected nodes
            format: Output format - 'md' (default, for LLM) or 'json'

        Returns:
            If format='md': Markdown string ready for LLM prompt
            If format='json': Dict with matches and clusters

        Example:
            # Markdown (default)
            context = read.search("Tell me about the oath", embed_fn=get_embedding)

            # JSON (for programmatic use)
            results = read.search("Tell me about the oath", embed_fn=get_embedding, format='json')
        """
        # Get embedding for the query
        query_embedding = embed_fn(query)

        # Search all node types with embeddings
        matches = []

        for label in ['Character', 'Place', 'Thing', 'Narrative']:
            similar = self._find_similar_by_embedding(label, query_embedding, top_k)
            matches.extend(similar)

        # Sort by similarity and take top_k
        matches.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        matches = matches[:top_k]

        result = {
            'query': query,
            'matches': matches
        }

        # Expand to connected nodes if requested
        if expand_connections and matches:
            clusters = []
            for match in matches[:5]:  # Expand top 5 matches
                cluster = self._get_connected_cluster(
                    match['id'],
                    match['type'],
                    max_nodes=MAX_CLUSTER_SIZE
                )
                if cluster['nodes']:
                    clusters.append(cluster)

            result['clusters'] = clusters

        # Convert to markdown if requested
        if format == FORMAT_MARKDOWN:
            return self._to_markdown(result)

        return result

    def _to_markdown(self, search_result: Dict[str, Any]) -> str:
        """
        Convert search results to markdown format for LLM consumption.

        IMPORTANT: Include ALL fields. NEVER filter or summarize.
        The LLM needs complete information to make decisions.
        """
        lines = []
        query = search_result.get('query', '')
        matches = search_result.get('matches', [])
        clusters = search_result.get('clusters', [])

        lines.append(f"# Search: \"{query}\"\n")

        # Matches section
        lines.append("## Matches\n")
        for i, match in enumerate(matches, 1):
            node_type = match.get('type', 'unknown')
            name = match.get('name', match.get('id', 'Unknown'))
            similarity = match.get('similarity', 0)

            lines.append(f"### {i}. {name} ({node_type}) — {similarity:.2f}\n")

            # Include ALL fields (except similarity which is in header)
            for key, value in match.items():
                if key in ('type', 'name', 'similarity'):
                    continue
                if value is None:
                    continue

                # Format the value
                if isinstance(value, list):
                    value_str = ', '.join(str(v) for v in value)
                elif isinstance(value, dict):
                    value_str = json.dumps(value)
                else:
                    value_str = str(value)

                lines.append(f"- **{key}:** {value_str}")

            lines.append("")  # Blank line between matches

        # Clusters section
        if clusters:
            lines.append("## Clusters\n")
            for cluster in clusters:
                root_id = cluster.get('root', 'unknown')
                root_type = cluster.get('root_type', 'unknown')
                nodes = cluster.get('nodes', [])

                lines.append(f"### Cluster: {root_id} ({root_type})\n")

                for node in nodes:
                    node_name = node.get('name', node.get('id', 'Unknown'))
                    node_type = node.get('type', 'unknown')
                    distance = node.get('distance', 0)
                    is_root = node.get('is_root', False)

                    if is_root:
                        lines.append(f"**[ROOT] {node_name}** ({node_type})")
                    else:
                        lines.append(f"- {node_name} ({node_type}, distance={distance})")

                    # Include ALL fields for each node
                    for key, value in node.items():
                        if key in ('type', 'name', 'id', 'distance', 'is_root'):
                            continue
                        if value is None:
                            continue

                        if isinstance(value, list):
                            value_str = ', '.join(str(v) for v in value)
                        elif isinstance(value, dict):
                            value_str = json.dumps(value)
                        else:
                            value_str = str(value)

                        lines.append(f"  - {key}: {value_str}")

                lines.append("")  # Blank line between clusters

        return '\n'.join(lines)

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _find_similar_by_embedding(
        self,
        label: str,
        embedding: List[float],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Find nodes similar to the given embedding."""
        cypher = f"""
        MATCH (n:{label})
        WHERE n.embedding IS NOT NULL
        RETURN n
        """

        try:
            rows = self._query(cypher)
            if not rows:
                return []

            results = []
            for row in rows:
                if row:
                    node = row[0] if isinstance(row, list) else row
                    # Parse node properties - handle FalkorDB Node objects
                    if hasattr(node, 'properties'):
                        props = node.properties
                    elif isinstance(node, list) and len(node) >= 2:
                        props = node[1] if isinstance(node[1], dict) else {}
                    elif isinstance(node, dict):
                        props = node
                    else:
                        continue

                    node_embedding = props.get('embedding')
                    if node_embedding:
                        if isinstance(node_embedding, str):
                            node_embedding = json.loads(node_embedding)

                        sim = self._cosine_similarity(embedding, node_embedding)

                        # Clean props - remove system fields
                        clean_props = {
                            k: v for k, v in props.items()
                            if k not in SYSTEM_FIELDS
                        }
                        clean_props['type'] = label.lower()
                        clean_props['similarity'] = sim

                        results.append(clean_props)

            # Sort by similarity
            results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
            return results[:top_k]

        except Exception as e:
            logger.warning(f"Error searching {label}: {e}")
            return []

    def _get_connected_cluster(
        self,
        node_id: str,
        node_type: str,
        max_nodes: int = MAX_CLUSTER_SIZE
    ) -> Dict[str, Any]:
        """
        Get a cluster of connected nodes around a starting node.

        Returns nodes and their links, sorted by connection strength.
        """
        # Get the starting node and its connections (2 hops)
        cypher = f"""
        MATCH (start {{id: '{node_id}'}})
        OPTIONAL MATCH (start)-[r1]-(n1)
        OPTIONAL MATCH (n1)-[r2]-(n2)
        WHERE n2.id <> start.id
        RETURN start, collect(DISTINCT n1), collect(DISTINCT n2),
               collect(DISTINCT r1), collect(DISTINCT r2)
        LIMIT 1
        """

        try:
            rows = self._query(cypher)
            if not rows or not rows[0]:
                return {'root': node_id, 'nodes': [], 'links': []}

            row = rows[0]
            nodes = []
            links = []
            seen_ids = set()

            # Handle both dict and list results from FalkorDB
            if isinstance(row, dict):
                start_data = row.get('start')
                n1_data = row.get('collect(DISTINCT n1)') or []
                n2_data = row.get('collect(DISTINCT n2)') or []
                r1_data = row.get('collect(DISTINCT r1)') or []
                r2_data = row.get('collect(DISTINCT r2)') or []
            else:
                start_data = row[0] if len(row) > 0 else None
                n1_data = row[1] if len(row) > 1 else []
                n2_data = row[2] if len(row) > 2 else []
                r1_data = row[3] if len(row) > 3 else []
                r2_data = row[4] if len(row) > 4 else []

            # Parse start node
            if start_data:
                start_node = extract_node_props(start_data)
                if start_node and start_node.get('id'):
                    start_node['is_root'] = True
                    nodes.append(start_node)
                    seen_ids.add(start_node['id'])

            # Parse 1-hop neighbors
            if n1_data:
                for n in n1_data:
                    props = extract_node_props(n)
                    if props and props.get('id') and props['id'] not in seen_ids:
                        props['distance'] = 1
                        nodes.append(props)
                        seen_ids.add(props['id'])

            # Parse 2-hop neighbors (only if we have room)
            if n2_data and len(nodes) < max_nodes:
                for n in n2_data:
                    if len(nodes) >= max_nodes:
                        break
                    props = extract_node_props(n)
                    if props and props.get('id') and props['id'] not in seen_ids:
                        props['distance'] = 2
                        nodes.append(props)
                        seen_ids.add(props['id'])

            # Parse relationships
            for rel_list in [r1_data, r2_data]:
                if rel_list:
                    for r in rel_list:
                        link = extract_link_props(r)
                        if link:
                            links.append(link)

            return {
                'root': node_id,
                'root_type': node_type,
                'nodes': nodes[:max_nodes],
                'links': links
            }

        except Exception as e:
            logger.warning(f"Error getting cluster for {node_id}: {e}")
            return {'root': node_id, 'nodes': [], 'links': []}
