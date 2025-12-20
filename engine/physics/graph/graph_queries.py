"""
Blood Ledger — Graph Queries

Easy-to-use functions for querying data from FalkorDB.
Narrator and World Runner use these to read game state.

Usage:
    from engine.physics.graph.graph_queries import GraphQueries

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
from typing import Dict, Any, List, Optional
from falkordb import FalkorDB

from engine.physics.graph.graph_query_utils import (
    SYSTEM_FIELDS,
    view_to_scene_tree,
)
from engine.physics.graph.graph_queries_moments import MomentQueryMixin
from engine.physics.graph.graph_queries_search import SearchQueryMixin

logger = logging.getLogger(__name__)


class QueryError(Exception):
    """Error with helpful fix instructions."""

    def __init__(self, message: str, fix: str):
        self.message = message
        self.fix = fix
        super().__init__(f"{message}\n\nHOW TO FIX:\n{fix}")


class GraphQueries(MomentQueryMixin, SearchQueryMixin):
    """
    Simple interface for querying FalkorDB graph.

    All functions return dictionaries, not raw Cypher results.

    Moment and view query methods are provided by MomentQueryMixin.
    Search and cluster methods are provided by SearchQueryMixin.
    See engine.physics.graph.graph_queries_moments for moment methods.
    See engine.physics.graph.graph_queries_search for search methods.
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

    ENERGY_BOOST_PER_READ = 0.05

    def _inject_energy_for_node(
        self,
        label: str,
        node_id: str,
        amount: float = None
    ) -> None:
        """Increment energy for a node when it is read via GraphQueries."""
        if not node_id:
            return
        boost = amount if amount is not None else self.ENERGY_BOOST_PER_READ
        cypher = f"""
        MATCH (n:{label} {{id: $id}})
        SET n.energy = coalesce(n.energy, 0) + $amount
        """
        try:
            self._query(cypher, {"id": node_id, "amount": boost})
        except QueryError as exc:
            logger.debug("[GraphQueries] Energy injection failed (%s:%s): %s", label, node_id, exc.message)

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

    # NOTE: Search methods (search, _to_markdown, _cosine_similarity,
    # _find_similar_by_embedding, _get_connected_cluster) are inherited
    # from SearchQueryMixin in graph_queries_search.py

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
        RETURN t.id, t.description, t.pressure, t.breaking_point, t.pressure_type, t.narratives
        ORDER BY t.pressure DESC
        """

        rows = self._query(cypher)
        fields = ["id", "description", "pressure", "breaking_point", "pressure_type", "narratives"]
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

    # NOTE: View/Moment query methods (get_current_view, get_live_moments,
    # resolve_speaker, get_available_transitions, get_clickable_words) are
    # inherited from MomentQueryMixin in graph_queries_moments.py


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
