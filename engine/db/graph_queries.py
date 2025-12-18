"""
Blood Ledger — Graph Queries

Easy-to-use functions for querying data from FalkorDB.
Narrator and World Runner use these to read game state.

Usage:
    from engine.db.graph_queries import GraphQueries

    graph = GraphQueries()

    # Get a character
    aldric = graph.get_character("char_aldric")

    # Get narratives a character believes
    beliefs = graph.get_character_beliefs("char_aldric")

    # Get characters at a location
    present = graph.get_characters_at("place_camp")

    # Search narratives by content
    oaths = graph.search_narratives("oath", type_filter="oath")

Docs:
- docs/engine/moments/ALGORITHM_View_Query.md — current view query contract
- docs/engine/moments/SCHEMA_Moments.md — node/link definitions
- docs/engine/moments/VALIDATION_Moments.md — invariants to maintain
"""

import json
import logging
import numpy as np
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime
from falkordb import FalkorDB

logger = logging.getLogger(__name__)

# Fields to exclude from output (internal/technical only)
# IMPORTANT: NEVER filter content fields. Only exclude embeddings and timestamps.
SYSTEM_FIELDS = {'embedding', 'created_at', 'updated_at'}

# Max nodes per cluster
MAX_CLUSTER_SIZE = 40

# Output formats
FORMAT_JSON = 'json'
FORMAT_MARKDOWN = 'md'


class QueryError(Exception):
    """Error with helpful fix instructions."""

    def __init__(self, message: str, fix: str):
        self.message = message
        self.fix = fix
        super().__init__(f"{message}\n\nHOW TO FIX:\n{fix}")


class GraphQueries:
    """
    Simple interface for querying FalkorDB graph.

    All functions return dictionaries, not raw Cypher results.
    """

    def __init__(
        self,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379
    ):
        self.graph_name = graph_name
        self.host = host
        self.port = port
        self._connect()

    def _connect(self):
        """Connect to FalkorDB."""
        try:
            self.db = FalkorDB(host=self.host, port=self.port)
            self.graph = self.db.select_graph(self.graph_name)
            logger.info(f"[GraphQueries] Connected to {self.graph_name}")
        except Exception as e:
            raise QueryError(
                f"Cannot connect to FalkorDB at {self.host}:{self.port}",
                f"""1. Start FalkorDB server (pip install falkordb)

2. Or use FalkorDB Cloud: https://app.falkordb.cloud

3. Check connection settings:
   GraphQueries(host="your-host", port=6379)

Error: {e}"""
            )

    def _query(self, cypher: str, params: Dict[str, Any] = None) -> List:
        """Execute a Cypher query and return raw results."""
        try:
            result = self.graph.query(cypher, params or {})
            return result.result_set if result.result_set else []
        except Exception as e:
            error_str = str(e)
            if "Unknown function" in error_str:
                raise QueryError(
                    f"Invalid Cypher function: {error_str}",
                    "Check the Cypher query for typos in function names."
                )
            elif "not defined" in error_str.lower():
                raise QueryError(
                    f"Variable not defined: {error_str}",
                    "Make sure all variables are defined in MATCH clauses before use."
                )
            else:
                raise QueryError(
                    f"Query failed: {error_str}",
                    f"Cypher query:\n{cypher}\n\nParams: {params}"
                )

    # =========================================================================
    # DIRECT CYPHER ACCESS
    # =========================================================================

    def query(self, cypher: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results as dicts.

        Full Cypher freedom - use this for any custom queries.

        Args:
            cypher: Cypher query string
            params: Optional parameters dict

        Returns:
            List of result dicts

        Examples:
            # Single node
            read.query("MATCH (c:Character {id: 'char_aldric'}) RETURN c")

            # Filtered
            read.query("MATCH (c:Character) WHERE c.type = 'companion' RETURN c")

            # With params
            read.query("MATCH (c:Character {id: $id}) RETURN c", {"id": "char_aldric"})

            # Complex
            read.query('''
                MATCH (c:Character)-[b:BELIEVES]->(n:Narrative)
                WHERE b.believes > 0.5
                RETURN c.name, n.content, b.believes
            ''')
        """
        try:
            result = self.graph.query(cypher, params or {})

            if not result.result_set:
                return []

            # Get headers from the result - format is [[type, name], [type, name], ...]
            raw_headers = result.header if hasattr(result, 'header') else []
            headers = []
            for h in raw_headers:
                if isinstance(h, list) and len(h) >= 2:
                    headers.append(h[1])  # Extract column name
                elif isinstance(h, str):
                    headers.append(h)
                else:
                    headers.append(str(h))

            rows = result.result_set

            # Convert to list of dicts
            results = []
            for row in rows:
                row_dict = {}
                for i, val in enumerate(row):
                    header = headers[i] if i < len(headers) else f"col{i}"
                    # Parse JSON strings
                    if isinstance(val, str) and (val.startswith('[') or val.startswith('{')):
                        try:
                            row_dict[header] = json.loads(val)
                        except:
                            row_dict[header] = val
                    else:
                        row_dict[header] = val
                results.append(row_dict)

            return results

        except Exception as e:
            error_str = str(e)
            raise QueryError(
                f"Query failed: {error_str}",
                f"Cypher:\n{cypher}\n\nParams: {params}"
            )

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
                start_node = self._extract_node_props(start_data)
                if start_node and start_node.get('id'):
                    start_node['is_root'] = True
                    nodes.append(start_node)
                    seen_ids.add(start_node['id'])

            # Parse 1-hop neighbors
            if n1_data:
                for n in n1_data:
                    props = self._extract_node_props(n)
                    if props and props.get('id') and props['id'] not in seen_ids:
                        props['distance'] = 1
                        nodes.append(props)
                        seen_ids.add(props['id'])

            # Parse 2-hop neighbors (only if we have room)
            if n2_data and len(nodes) < max_nodes:
                for n in n2_data:
                    if len(nodes) >= max_nodes:
                        break
                    props = self._extract_node_props(n)
                    if props and props.get('id') and props['id'] not in seen_ids:
                        props['distance'] = 2
                        nodes.append(props)
                        seen_ids.add(props['id'])

            # Parse relationships
            for rel_list in [r1_data, r2_data]:
                if rel_list:
                    for r in rel_list:
                        link = self._extract_link_props(r)
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

    def _extract_node_props(self, node) -> Optional[Dict[str, Any]]:
        """Extract properties from a FalkorDB node."""
        if not node:
            return None

        try:
            # Handle FalkorDB Node objects
            if hasattr(node, 'properties'):
                labels = list(node.labels) if hasattr(node, 'labels') else []
                props = node.properties
            elif isinstance(node, list) and len(node) >= 2:
                labels = node[0] if isinstance(node[0], list) else [node[0]]
                props = node[1] if isinstance(node[1], dict) else {}
            elif isinstance(node, dict):
                labels = []
                props = node
            else:
                return None

            # Clean props
            clean = {k: v for k, v in props.items() if k not in SYSTEM_FIELDS}

            # Add type from label
            if labels:
                label = labels[0] if isinstance(labels[0], str) else str(labels[0])
                clean['type'] = label.lower()

            # Parse JSON strings
            for key in ['values', 'skills', 'weather', 'details', 'about_characters',
                        'about_places', 'narratives', 'voice_phrases']:
                if key in clean and isinstance(clean[key], str):
                    try:
                        clean[key] = json.loads(clean[key])
                    except:
                        pass

            return clean

        except Exception as e:
            logger.warning(f"Error extracting node props: {e}")
            return None

    def _extract_link_props(self, rel) -> Optional[Dict[str, Any]]:
        """Extract properties from a FalkorDB relationship."""
        if not rel:
            return None

        try:
            # FalkorDB relationship format varies
            if isinstance(rel, list) and len(rel) >= 3:
                rel_type = rel[0]
                props = rel[1] if isinstance(rel[1], dict) else {}
                # source/target might be in different positions
                link = {
                    'type': rel_type,
                    **{k: v for k, v in props.items() if k not in SYSTEM_FIELDS}
                }
                return link

            elif isinstance(rel, dict):
                return {k: v for k, v in rel.items() if k not in SYSTEM_FIELDS}

            return None

        except Exception as e:
            logger.warning(f"Error extracting link props: {e}")
            return None

    def _parse_node(self, row, fields: List[str]) -> Dict[str, Any]:
        """Parse a row into a dict using field names."""
        if not row:
            return {}
        result = {}

        # Handle dict results from FalkorDB (newer versions return dicts)
        if isinstance(row, dict):
            for field in fields:
                # Try both 'field' and 'p.field' / 'c.field' style keys
                val = row.get(field) or row.get(f"p.{field}") or row.get(f"c.{field}") or row.get(f"n.{field}")
                if val is not None:
                    # Parse JSON strings back to dicts/lists
                    if isinstance(val, str) and val.startswith('['):
                        try:
                            result[field] = json.loads(val)
                        except:
                            result[field] = val
                    elif isinstance(val, str) and val.startswith('{'):
                        try:
                            result[field] = json.loads(val)
                        except:
                            result[field] = val
                    else:
                        result[field] = val
            return result

        # Handle list results (original format)
        for i, field in enumerate(fields):
            if i < len(row):
                val = row[i]
                # Parse JSON strings back to dicts/lists
                if isinstance(val, str) and val.startswith('['):
                    try:
                        result[field] = json.loads(val)
                    except:
                        result[field] = val
                elif isinstance(val, str) and val.startswith('{'):
                    try:
                        result[field] = json.loads(val)
                    except:
                        result[field] = val
                else:
                    result[field] = val
        return result

    # =========================================================================
    # CHARACTER QUERIES
    # =========================================================================

    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a character by ID.

        Args:
            character_id: e.g., "char_aldric"

        Returns:
            Character dict or None if not found

        Example:
            aldric = graph.get_character("char_aldric")
            print(aldric["name"])  # "Aldric"
        """
        if not character_id:
            raise QueryError(
                "character_id is required",
                "Provide a valid character ID:\n  graph.get_character('char_aldric')"
            )

        cypher = f"""
        MATCH (c:Character {{id: '{character_id}'}})
        RETURN c.id, c.name, c.type, c.alive, c.face,
               c.voice_tone, c.voice_style, c.approach, c.values, c.flaw,
               c.backstory_family, c.backstory_wound, c.backstory_why_here,
               c.skills
        """

        rows = self._query(cypher)
        if not rows:
            return None

        fields = [
            "id", "name", "type", "alive", "face",
            "voice_tone", "voice_style", "approach", "values", "flaw",
            "backstory_family", "backstory_wound", "backstory_why_here",
            "skills"
        ]
        return self._parse_node(rows[0], fields)

    def get_all_characters(self, type_filter: str = None) -> List[Dict[str, Any]]:
        """
        Get all characters, optionally filtered by type.

        Args:
            type_filter: "player", "companion", "major", "minor", "background"

        Returns:
            List of character dicts

        Example:
            companions = graph.get_all_characters(type_filter="companion")
        """
        if type_filter:
            cypher = f"""
            MATCH (c:Character {{type: '{type_filter}'}})
            RETURN c.id, c.name, c.type, c.alive
            ORDER BY c.name
            """
        else:
            cypher = """
            MATCH (c:Character)
            RETURN c.id, c.name, c.type, c.alive
            ORDER BY c.name
            """

        rows = self._query(cypher)
        return [
            self._parse_node(row, ["id", "name", "type", "alive"])
            for row in rows
        ]

    def get_characters_at(self, place_id: str) -> List[Dict[str, Any]]:
        """
        Get all characters present at a location.

        Args:
            place_id: e.g., "place_camp"

        Returns:
            List of character dicts with presence info

        Example:
            present = graph.get_characters_at("place_camp")
            for char in present:
                print(f"{char['name']} is here (visible: {char['visible']})")
        """
        if not place_id:
            raise QueryError(
                "place_id is required",
                "Provide a valid place ID:\n  graph.get_characters_at('place_camp')"
            )

        cypher = f"""
        MATCH (c:Character)-[r:AT]->(p:Place {{id: '{place_id}'}})
        WHERE r.present > 0.5
        RETURN c.id, c.name, c.type, r.visible
        ORDER BY c.name
        """

        rows = self._query(cypher)
        return [
            self._parse_node(row, ["id", "name", "type", "visible"])
            for row in rows
        ]

    # =========================================================================
    # PLACE QUERIES
    # =========================================================================

    def get_place(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a place by ID.

        Args:
            place_id: e.g., "place_york"

        Returns:
            Place dict or None if not found
        """
        if not place_id:
            raise QueryError(
                "place_id is required",
                "Provide a valid place ID:\n  graph.get_place('place_york')"
            )

        cypher = f"""
        MATCH (p:Place {{id: '{place_id}'}})
        RETURN p.id, p.name, p.type, p.mood, p.weather, p.details
        """

        rows = self._query(cypher)
        if not rows:
            return None

        return self._parse_node(rows[0], ["id", "name", "type", "mood", "weather", "details"])

    def get_path_between(self, from_place: str, to_place: str) -> Optional[Dict[str, Any]]:
        """
        Get travel info between two places.

        Args:
            from_place: Source place ID
            to_place: Destination place ID

        Returns:
            Dict with path_distance, path_difficulty, or None if no path
        """
        cypher = f"""
        MATCH (f:Place {{id: '{from_place}'}})-[r:CONNECTS]->(t:Place {{id: '{to_place}'}})
        WHERE r.path > 0.5
        RETURN r.path_distance, r.path_difficulty
        """

        rows = self._query(cypher)
        if not rows:
            return None

        return self._parse_node(rows[0], ["path_distance", "path_difficulty"])

    # =========================================================================
    # NARRATIVE QUERIES
    # =========================================================================

    def get_narrative(self, narrative_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a narrative by ID.

        Args:
            narrative_id: e.g., "narr_oath"

        Returns:
            Narrative dict or None if not found
        """
        if not narrative_id:
            raise QueryError(
                "narrative_id is required",
                "Provide a valid narrative ID:\n  graph.get_narrative('narr_oath')"
            )

        cypher = f"""
        MATCH (n:Narrative {{id: '{narrative_id}'}})
        RETURN n.id, n.name, n.content, n.type, n.interpretation,
               n.tone, n.weight, n.focus, n.truth,
               n.about_characters, n.about_places, n.about_things
        """

        rows = self._query(cypher)
        if not rows:
            return None

        fields = [
            "id", "name", "content", "type", "interpretation",
            "tone", "weight", "focus", "truth",
            "about_characters", "about_places", "about_things"
        ]
        return self._parse_node(rows[0], fields)

    def get_character_beliefs(
        self,
        character_id: str,
        min_heard: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Get all narratives a character believes.

        Args:
            character_id: e.g., "char_aldric"
            min_heard: Minimum heard threshold (0-1)

        Returns:
            List of narrative dicts with belief info

        Example:
            beliefs = graph.get_character_beliefs("char_aldric")
            for belief in beliefs:
                print(f"{belief['name']}: believes={belief['believes']}")
        """
        if not character_id:
            raise QueryError(
                "character_id is required",
                "Provide a valid character ID:\n  graph.get_character_beliefs('char_aldric')"
            )

        cypher = f"""
        MATCH (c:Character {{id: '{character_id}'}})-[r:BELIEVES]->(n:Narrative)
        WHERE r.heard >= {min_heard}
        RETURN n.id, n.name, n.content, n.type, n.weight,
               r.heard, r.believes, r.doubts, r.denies, r.source
        ORDER BY n.weight DESC
        """

        rows = self._query(cypher)
        fields = [
            "id", "name", "content", "type", "weight",
            "heard", "believes", "doubts", "denies", "source"
        ]
        return [self._parse_node(row, fields) for row in rows]

    def get_narrative_believers(self, narrative_id: str) -> List[Dict[str, Any]]:
        """
        Get all characters who believe a narrative.

        Args:
            narrative_id: e.g., "narr_oath"

        Returns:
            List of character dicts with belief info
        """
        if not narrative_id:
            raise QueryError(
                "narrative_id is required",
                "Provide a valid narrative ID:\n  graph.get_narrative_believers('narr_oath')"
            )

        cypher = f"""
        MATCH (c:Character)-[r:BELIEVES]->(n:Narrative {{id: '{narrative_id}'}})
        WHERE r.heard > 0
        RETURN c.id, c.name, c.type,
               r.heard, r.believes, r.doubts, r.denies
        ORDER BY r.believes DESC
        """

        rows = self._query(cypher)
        fields = ["id", "name", "type", "heard", "believes", "doubts", "denies"]
        return [self._parse_node(row, fields) for row in rows]

    def get_narratives_by_type(self, narrative_type: str) -> List[Dict[str, Any]]:
        """
        Get all narratives of a specific type.

        Args:
            narrative_type: oath, debt, blood, memory, rumor, etc.

        Returns:
            List of narrative dicts

        Example:
            oaths = read.get_narratives_by_type("oath")
        """
        cypher = f"""
        MATCH (n:Narrative {{type: '{narrative_type}'}})
        RETURN n.id, n.name, n.content, n.type, n.weight, n.tone
        ORDER BY n.weight DESC
        """

        rows = self._query(cypher)
        fields = ["id", "name", "content", "type", "weight", "tone"]
        return [self._parse_node(row, fields) for row in rows]

    def get_narratives_about(
        self,
        character_id: str = None,
        place_id: str = None,
        thing_id: str = None,
        type_filter: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get narratives about a specific node.

        Args:
            character_id: Filter by character
            place_id: Filter by place
            thing_id: Filter by thing
            type_filter: Filter by narrative type

        Returns:
            List of narrative dicts

        Example:
            about_aldric = graph.get_narratives_about(character_id="char_aldric")
            oaths = graph.get_narratives_about(type_filter="oath")
        """
        conditions = []

        # Note: about_* fields are stored as JSON strings, use CONTAINS
        if character_id:
            conditions.append(f"n.about_characters CONTAINS '{character_id}'")
        if place_id:
            conditions.append(f"n.about_places CONTAINS '{place_id}'")
        if thing_id:
            conditions.append(f"n.about_things CONTAINS '{thing_id}'")
        if type_filter:
            conditions.append(f"n.type = '{type_filter}'")

        where_clause = " AND ".join(conditions) if conditions else "true"

        cypher = f"""
        MATCH (n:Narrative)
        WHERE {where_clause}
        RETURN n.id, n.name, n.content, n.type, n.weight, n.tone
        ORDER BY n.weight DESC
        """

        rows = self._query(cypher)
        fields = ["id", "name", "content", "type", "weight", "tone"]
        return [self._parse_node(row, fields) for row in rows]

    def get_high_weight_narratives(
        self,
        min_weight: float = 0.5,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get narratives sorted by weight.

        Args:
            min_weight: Minimum weight threshold
            limit: Max number to return

        Returns:
            List of narrative dicts sorted by weight

        Example:
            important = graph.get_high_weight_narratives(min_weight=0.7)
        """
        cypher = f"""
        MATCH (n:Narrative)
        WHERE n.weight >= {min_weight}
        RETURN n.id, n.name, n.content, n.type, n.weight, n.tone
        ORDER BY n.weight DESC
        LIMIT {limit}
        """

        rows = self._query(cypher)
        fields = ["id", "name", "content", "type", "weight", "tone"]
        return [self._parse_node(row, fields) for row in rows]

    def get_contradicting_narratives(self, narrative_id: str) -> List[Dict[str, Any]]:
        """
        Get narratives that contradict a given narrative.

        Args:
            narrative_id: The narrative to check

        Returns:
            List of contradicting narrative dicts
        """
        cypher = f"""
        MATCH (n1:Narrative {{id: '{narrative_id}'}})-[r:RELATES_TO]-(n2:Narrative)
        WHERE r.contradicts > 0.5
        RETURN n2.id, n2.name, n2.content, n2.type, r.contradicts
        ORDER BY r.contradicts DESC
        """

        rows = self._query(cypher)
        fields = ["id", "name", "content", "type", "contradicts"]
        return [self._parse_node(row, fields) for row in rows]

    # =========================================================================
    # TENSION QUERIES
    # =========================================================================

    def get_tension(self, tension_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a tension by ID.

        Args:
            tension_id: e.g., "tension_confrontation"

        Returns:
            Tension dict or None if not found
        """
        if not tension_id:
            raise QueryError(
                "tension_id is required",
                "Provide a valid tension ID:\n  graph.get_tension('tension_confrontation')"
            )

        cypher = f"""
        MATCH (t:Tension {{id: '{tension_id}'}})
        RETURN t.id, t.description, t.narratives, t.pressure, t.pressure_type,
               t.breaking_point, t.base_rate, t.trigger_at, t.progression
        """

        rows = self._query(cypher)
        if not rows:
            return None

        fields = [
            "id", "description", "narratives", "pressure", "pressure_type",
            "breaking_point", "base_rate", "trigger_at", "progression"
        ]
        return self._parse_node(rows[0], fields)

    def get_all_tensions(self, min_pressure: float = 0.0) -> List[Dict[str, Any]]:
        """
        Get all tensions, optionally filtered by pressure.

        Args:
            min_pressure: Minimum pressure threshold

        Returns:
            List of tension dicts sorted by pressure

        Example:
            hot_tensions = graph.get_all_tensions(min_pressure=0.7)
        """
        cypher = f"""
        MATCH (t:Tension)
        WHERE t.pressure >= {min_pressure}
        RETURN t.id, t.description, t.pressure, t.breaking_point, t.pressure_type
        ORDER BY t.pressure DESC
        """

        rows = self._query(cypher)
        fields = ["id", "description", "pressure", "breaking_point", "pressure_type"]
        return [self._parse_node(row, fields) for row in rows]

    def get_flipped_tensions(self) -> List[Dict[str, Any]]:
        """
        Get tensions that have exceeded their breaking point.

        Returns:
            List of flipped tension dicts

        Example:
            flipped = graph.get_flipped_tensions()
            for t in flipped:
                print(f"FLIP: {t['id']} at pressure {t['pressure']}")
        """
        cypher = """
        MATCH (t:Tension)
        WHERE t.pressure >= t.breaking_point
        RETURN t.id, t.description, t.narratives, t.pressure, t.breaking_point
        ORDER BY t.pressure DESC
        """

        rows = self._query(cypher)
        fields = ["id", "description", "narratives", "pressure", "breaking_point"]
        return [self._parse_node(row, fields) for row in rows]

    # =========================================================================
    # MOMENT QUERIES
    # =========================================================================

    def get_moment(self, moment_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single moment by ID, including speaker via SAID link.

        Returns moment with all fields including lifecycle state (status, weight, tone).
        """
        cypher = """
        MATCH (m:Moment {id: $id})
        OPTIONAL MATCH (c:Character)-[:SAID]->(m)
        RETURN m.id, m.text, m.type, m.tick, m.line,
               m.status, m.weight, m.tone, m.tick_spoken, m.tick_decayed,
               c.id as speaker
        """
        rows = self._query(cypher, {"id": moment_id})
        if not rows:
            return None
        fields = ["id", "text", "type", "tick", "line",
                  "status", "weight", "tone", "tick_spoken", "tick_decayed",
                  "speaker"]
        return self._parse_node(rows[0], fields)

    def get_moments_at_place(
        self,
        place_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get moments that occurred at a specific place, including speaker via SAID link.
        """
        cypher = f"""
        MATCH (m:Moment)-[:AT]->(p:Place {{id: '{place_id}'}})
        OPTIONAL MATCH (c:Character)-[:SAID]->(m)
        RETURN m.id, m.text, m.type, m.tick, m.line, c.id as speaker
        ORDER BY m.tick DESC
        LIMIT {limit}
        """
        rows = self._query(cypher)
        fields = ["id", "text", "type", "tick", "line", "speaker"]
        return [self._parse_node(row, fields) for row in rows]

    def get_moments_by_character(
        self,
        character_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get moments where a character spoke or acted (via SAID link).
        """
        cypher = f"""
        MATCH (c:Character {{id: '{character_id}'}})-[:SAID]->(m:Moment)
        RETURN m.id, m.text, m.type, m.tick, m.line
        ORDER BY m.tick DESC
        LIMIT {limit}
        """
        rows = self._query(cypher)
        fields = ["id", "text", "type", "tick", "line"]
        return [self._parse_node(row, fields) for row in rows]

    def get_moments_in_tick_range(
        self,
        start_tick: int,
        end_tick: int,
        place_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get moments within a tick range, optionally filtered by place.
        """
        if place_id:
            cypher = f"""
            MATCH (m:Moment)-[:AT]->(p:Place {{id: '{place_id}'}})
            WHERE m.tick >= {start_tick} AND m.tick <= {end_tick}
            OPTIONAL MATCH (c:Character)-[:SAID]->(m)
            RETURN m.id, m.text, m.type, m.tick, m.line, c.id as speaker
            ORDER BY m.tick ASC
            """
        else:
            cypher = f"""
            MATCH (m:Moment)
            WHERE m.tick >= {start_tick} AND m.tick <= {end_tick}
            OPTIONAL MATCH (c:Character)-[:SAID]->(m)
            RETURN m.id, m.text, m.type, m.tick, m.line, c.id as speaker
            ORDER BY m.tick ASC
            """
        rows = self._query(cypher)
        fields = ["id", "text", "type", "tick", "line", "speaker"]
        return [self._parse_node(row, fields) for row in rows]

    def get_moment_sequence(
        self,
        start_moment_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get a sequence of moments starting from a given moment (following THEN links).
        """
        cypher = f"""
        MATCH path = (start:Moment {{id: '{start_moment_id}'}})-[:THEN*0..{limit}]->(m:Moment)
        OPTIONAL MATCH (c:Character)-[:SAID]->(m)
        RETURN m.id, m.text, m.type, m.tick, m.line, c.id as speaker, length(path) as depth
        ORDER BY depth ASC
        """
        rows = self._query(cypher)
        fields = ["id", "text", "type", "tick", "line", "speaker", "depth"]
        return [self._parse_node(row, fields) for row in rows]

    def get_narrative_moments(
        self,
        narrative_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all moments that are sources for a narrative (via FROM link).
        """
        cypher = f"""
        MATCH (n:Narrative {{id: '{narrative_id}'}})-[:FROM]->(m:Moment)
        OPTIONAL MATCH (c:Character)-[:SAID]->(m)
        RETURN m.id, m.text, m.type, m.tick, m.line, c.id as speaker
        ORDER BY m.tick ASC
        """
        rows = self._query(cypher)
        fields = ["id", "text", "type", "tick", "line", "speaker"]
        return [self._parse_node(row, fields) for row in rows]

    def get_narratives_from_moment(
        self,
        moment_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all narratives that cite this moment as a source.
        """
        cypher = f"""
        MATCH (n:Narrative)-[:FROM]->(m:Moment {{id: '{moment_id}'}})
        RETURN n.id, n.name, n.content, n.type
        """
        rows = self._query(cypher)
        fields = ["id", "name", "content", "type"]
        return [self._parse_node(row, fields) for row in rows]

    def search_moments(
        self,
        query: str,
        embed_fn: Callable[[str], List[float]],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Semantic search across moments.

        Args:
            query: Search query text
            embed_fn: Function to generate embedding from text
            top_k: Number of results to return
        """
        query_embedding = embed_fn(query)
        return self._find_similar_by_embedding('Moment', query_embedding, top_k)

    def _find_similar_by_embedding(
        self,
        label: str,
        embedding: List[float],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """
        Find similar nodes by embedding vector (brute force cosine similarity).
        """
        # Get all nodes with embeddings, speaker via SAID link
        cypher = f"""
        MATCH (n:{label})
        WHERE n.embedding IS NOT NULL
        OPTIONAL MATCH (c:Character)-[:SAID]->(n)
        RETURN n.id, n.text, n.type, n.tick, n.embedding, c.id as speaker
        """
        rows = self._query(cypher)

        if not rows:
            return []

        # Calculate similarities
        results = []
        query_vec = np.array(embedding)
        query_norm = np.linalg.norm(query_vec)

        for row in rows:
            node_embedding = row[4]  # embedding is 5th field (index 4)
            if node_embedding:
                if isinstance(node_embedding, str):
                    node_embedding = json.loads(node_embedding)
                node_vec = np.array(node_embedding)
                node_norm = np.linalg.norm(node_vec)
                if query_norm > 0 and node_norm > 0:
                    similarity = float(np.dot(query_vec, node_vec) / (query_norm * node_norm))
                    results.append({
                        "id": row[0],
                        "text": row[1],
                        "type": row[2],
                        "tick": row[3],
                        "speaker": row[5],  # speaker is 6th field (index 5)
                        "score": similarity
                    })

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    # =========================================================================
    # SCENE CONTEXT BUILDER
    # =========================================================================

    def build_scene_context(
        self,
        player_location: str,
        player_id: str = "char_player"
    ) -> Dict[str, Any]:
        """
        Build complete scene context for Narrator.

        Args:
            player_location: Where the player is
            player_id: Player character ID

        Returns:
            Dict ready for Narrator prompt with:
            - location info
            - present characters
            - active narratives (sorted by weight)
            - tensions

        Example:
            context = graph.build_scene_context("place_camp")
            # Use context in Narrator prompt
        """
        # Get location
        location = self.get_place(player_location)
        if not location:
            raise QueryError(
                f"Place not found: {player_location}",
                f"Add the place first:\n  graph.add_place(id='{player_location}', name='...', type='...')"
            )

        # Get present characters
        present = self.get_characters_at(player_location)

        # Get player's beliefs (active narratives)
        beliefs = self.get_character_beliefs(player_id, min_heard=0.5)
        active_narratives = [
            {
                "id": b["id"],
                "weight": b.get("weight", 0.5),
                "summary": b["content"][:100] + "..." if len(b.get("content", "")) > 100 else b.get("content", ""),
                "type": b["type"],
                "tone": b.get("tone")
            }
            for b in sorted(beliefs, key=lambda x: x.get("weight", 0), reverse=True)[:10]
        ]

        # Get relevant tensions
        tensions = self.get_all_tensions(min_pressure=0.2)
        tension_briefs = [
            {
                "id": t["id"],
                "description": t["description"],
                "pressure": t["pressure"],
                "breaking_point": t.get("breaking_point", 0.9)
            }
            for t in tensions[:5]
        ]

        return {
            "location": location,
            "present": present,
            "active_narratives": active_narratives,
            "tensions": tension_briefs
        }

    def get_player_location(self, player_id: str = "char_player") -> Optional[Dict[str, Any]]:
        """
        Resolve the current Place for a player character.

        Args:
            player_id: Character ID representing the player

        Returns:
            Place dict with optional presence metadata, or None if not found.
        """
        cypher = """
        MATCH (c:Character {id: $player_id})-[rel:AT]->(p:Place)
        RETURN p.id as place_id, rel.present as present, rel.visible as visible
        ORDER BY coalesce(rel.present, 1.0) DESC, coalesce(rel.visible, 1.0) DESC
        LIMIT 1
        """

        rows = self._query(cypher, {"player_id": player_id})
        if not rows:
            return None

        # Handle both dict and list results from FalkorDB
        row = rows[0]
        if isinstance(row, dict):
            place_id = row.get('place_id')
            present = row.get('present')
            visible = row.get('visible')
        else:
            place_id, present, visible = row
        place = self.get_place(place_id)
        if not place:
            return None

        if present is not None:
            place["present"] = present
        if visible is not None:
            place["visible"] = visible
        return place

    # =========================================================================
    # VIEW QUERIES (Moment Graph Architecture)
    # =========================================================================

    def get_current_view(
        self,
        player_id: str,
        location_id: str,
        present_character_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get the current view of moments visible to the player.

        This is the core query for the Moment Graph Architecture.
        Returns moments that pass presence gating, ordered by weight.

        Args:
            player_id: The player character ID
            location_id: Current location ID
            present_character_ids: IDs of characters currently present
                                   (if None, queries automatically)

        Returns:
            Dict with:
                - location: Place dict
                - characters: List of present character dicts
                - active_moments: Spoken/active moments (current conversation)
                - possible_moments: Moments that could surface (sorted by weight)
                - transitions: Available CAN_LEAD_TO transitions from active moments
        """
        # Get present characters if not provided
        if present_character_ids is None:
            present = self.get_characters_at(location_id)
            present_character_ids = [c['id'] for c in present]
        else:
            present = [self.get_character(cid) for cid in present_character_ids]
            present = [c for c in present if c]  # Filter None

        # Get location
        location = self.get_place(location_id)

        # Get active/spoken moments at this location
        active_moments = self.get_live_moments(
            location_id,
            present_character_ids,
            status_filter=['active', 'spoken']
        )

        # Get possible moments that could surface
        possible_moments = self.get_live_moments(
            location_id,
            present_character_ids,
            status_filter=['possible']
        )

        # Get transitions from active moments
        active_ids = [m['id'] for m in active_moments]
        transitions = self.get_available_transitions(active_ids)

        return {
            "location": location,
            "characters": present,
            "active_moments": active_moments,
            "possible_moments": possible_moments,
            "transitions": transitions
        }

    def get_live_moments(
        self,
        location_id: str,
        present_character_ids: List[str],
        status_filter: List[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get moments that pass presence gating for the current context.

        Implements the core visibility rule: a moment is visible when ALL
        attachments with presence_required=true have their targets present.

        Args:
            location_id: Current location ID
            present_character_ids: IDs of characters currently present
            status_filter: List of status values to include (default: possible, active)
            limit: Max number of moments to return

        Returns:
            List of moment dicts sorted by weight DESC
        """
        if status_filter is None:
            status_filter = ['possible', 'active']

        # Convert lists to Cypher format
        status_list = str(status_filter)
        char_list = str(present_character_ids)

        # Query moments that pass presence gating
        # A moment passes if ALL of its presence_required attachments are satisfied
        cypher = f"""
        MATCH (m:Moment)
        WHERE m.status IN {status_list}

        // Get all presence-required attachments
        OPTIONAL MATCH (m)-[r:ATTACHED_TO {{presence_required: true}}]->(target)

        // Collect targets and check if all are present
        WITH m, collect(target) as required_targets

        // For each required target, check if it's "present":
        // - Character: must be in present_character_ids
        // - Place: must be the current location
        // - Thing/Narrative/Tension: always considered present (no location check)
        WHERE ALL(t IN required_targets WHERE
            (t:Character AND t.id IN {char_list})
            OR (t:Place AND t.id = '{location_id}')
            OR (t:Thing)
            OR (t:Narrative)
            OR (t:Tension)
        )

        // Get speaker if any
        OPTIONAL MATCH (speaker:Character)-[:CAN_SPEAK]->(m)
        WHERE speaker.id IN {char_list}

        // Also check for SAID (for spoken moments)
        OPTIONAL MATCH (said_by:Character)-[:SAID]->(m)

        RETURN m.id, m.text, m.type, m.status, m.weight, m.tone,
               m.tick, m.tick_spoken,
               speaker.id as potential_speaker,
               said_by.id as actual_speaker
        ORDER BY m.weight DESC
        LIMIT {limit}
        """

        rows = self._query(cypher)
        fields = ["id", "text", "type", "status", "weight", "tone",
                  "tick", "tick_spoken",
                  "potential_speaker", "actual_speaker"]

        moments = []
        for row in rows:
            moment = self._parse_node(row, fields)
            # Use actual_speaker if available, otherwise potential_speaker
            moment['speaker'] = moment.pop('actual_speaker') or moment.pop('potential_speaker')
            moments.append(moment)

        return moments

    def resolve_speaker(
        self,
        moment_id: str,
        present_character_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Find which present character can speak a moment.

        For possible moments, returns the character with highest CAN_SPEAK weight
        among those currently present.

        Args:
            moment_id: The moment ID
            present_character_ids: IDs of characters currently present

        Returns:
            Dict with speaker info or None if no one can speak it
        """
        char_list = str(present_character_ids)

        cypher = f"""
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {{id: '{moment_id}'}})
        WHERE c.id IN {char_list}
        RETURN c.id, c.name, r.weight
        ORDER BY r.weight DESC
        LIMIT 1
        """

        rows = self._query(cypher)
        if not rows:
            return None

        return self._parse_node(rows[0], ["id", "name", "weight"])

    def get_available_transitions(
        self,
        active_moment_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get available CAN_LEAD_TO transitions from active moments.

        Args:
            active_moment_ids: IDs of currently active moments

        Returns:
            List of transition dicts with:
                - from_id: Source moment ID
                - to_id: Target moment ID
                - trigger: player | wait | auto
                - require_words: Words that trigger this transition
                - weight_transfer: How much weight flows
        """
        if not active_moment_ids:
            return []

        moment_list = str(active_moment_ids)

        cypher = f"""
        MATCH (from:Moment)-[r:CAN_LEAD_TO]->(to:Moment)
        WHERE from.id IN {moment_list}
          AND to.status IN ['possible', 'dormant']
        RETURN from.id as from_id, to.id as to_id,
               r.trigger, r.require_words, r.weight_transfer,
               r.bidirectional, r.consumes_origin
        """

        rows = self._query(cypher)
        fields = ["from_id", "to_id", "trigger", "require_words",
                  "weight_transfer", "bidirectional", "consumes_origin"]

        return [self._parse_node(row, fields) for row in rows]

    def get_clickable_words(
        self,
        moment_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all clickable words for a moment based on CAN_LEAD_TO links.

        Args:
            moment_id: The moment ID

        Returns:
            List of dicts with:
                - word: The clickable word
                - target_id: Where clicking leads
                - weight_transfer: How much weight flows
        """
        cypher = f"""
        MATCH (m:Moment {{id: '{moment_id}'}})-[r:CAN_LEAD_TO]->(target:Moment)
        WHERE r.trigger = 'player' AND r.require_words IS NOT NULL
        RETURN r.require_words, target.id, r.weight_transfer
        """

        rows = self._query(cypher)
        results = []

        for row in rows:
            words = row[0]
            if isinstance(words, str):
                words = json.loads(words)
            if words:
                for word in words:
                    results.append({
                        "word": word,
                        "target_id": row[1],
                        "weight_transfer": row[2]
                    })

        return results


def view_to_scene_tree(view_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a view query result to SceneTree format for backward compatibility.

    This allows the frontend to continue using SceneTree while we transition
    to the Moment Graph Architecture.

    Args:
        view_result: Result from get_current_view()

    Returns:
        SceneTree-compatible dict
    """
    location = view_result.get('location', {})
    characters = view_result.get('characters', [])
    active_moments = view_result.get('active_moments', [])
    transitions = view_result.get('transitions', [])

    # Build narration list from active moments
    narration = []
    for moment in active_moments:
        narration_item = {
            "text": moment.get('text', ''),
            "speaker": moment.get('speaker')
        }

        # Add clickables from transitions
        clickables = {}
        for trans in transitions:
            if trans.get('from_id') == moment.get('id'):
                words = trans.get('require_words', [])
                if isinstance(words, str):
                    words = json.loads(words)
                for word in (words or []):
                    clickables[word] = {
                        "speaks": f"Tell me about {word}",
                        "intent": "explore",
                        "waitingMessage": "..."
                    }

        if clickables:
            narration_item['clickable'] = clickables

        narration.append(narration_item)

    return {
        "id": f"scene_{location.get('id', 'unknown')}",
        "location": {
            "place": location.get('id', ''),
            "name": location.get('name', ''),
            "region": location.get('type', ''),
            "time": "present"
        },
        "characters": [c.get('id') for c in characters],
        "atmosphere": location.get('details', []) if isinstance(location.get('details'), list) else [],
        "narration": narration,
        "voices": []
    }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_queries(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379
) -> GraphQueries:
    """Get a GraphQueries instance."""
    return GraphQueries(graph_name=graph_name, host=host, port=port)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    try:
        graph = get_queries("blood_ledger_test")

        # Get a character
        print("\n=== Character ===")
        aldric = graph.get_character("char_aldric")
        if aldric:
            print(f"Name: {aldric['name']}")
            print(f"Type: {aldric['type']}")

        # Get characters at a location
        print("\n=== At Camp ===")
        at_camp = graph.get_characters_at("place_camp")
        for char in at_camp:
            print(f"  {char['name']}")

        # Get beliefs
        print("\n=== Aldric's Beliefs ===")
        beliefs = graph.get_character_beliefs("char_aldric")
        for b in beliefs:
            print(f"  {b['name']}: believes={b.get('believes', 0)}")

        # Get tensions
        print("\n=== Tensions ===")
        tensions = graph.get_all_tensions()
        for t in tensions:
            print(f"  {t['id']}: pressure={t['pressure']}")

        # Build scene context
        print("\n=== Scene Context ===")
        context = graph.build_scene_context("place_camp", "char_rolf")
        print(f"Location: {context['location']['name']}")
        print(f"Present: {[c['name'] for c in context['present']]}")
        print(f"Active narratives: {len(context['active_narratives'])}")

    except QueryError as e:
        print(f"\nERROR: {e.message}")
        print(f"\nHOW TO FIX:\n{e.fix}")
