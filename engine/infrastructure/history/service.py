"""
Blood Ledger — History Service

Core service for querying and recording distributed history.
History exists as narratives + beliefs, not as a central event log.

Every query filters through what the querying character BELIEVES.
The player's history is what the player believes. Aldric's history is what Aldric believes.
They may differ.

DOCS: docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from .conversations import ConversationThread

logger = logging.getLogger(__name__)


class HistoryService:
    """
    Service for querying and recording game history.

    History is distributed:
    - Player-experienced events point to conversation files
    - World-generated events carry their own detail
    - All access is filtered by character beliefs
    """

    def __init__(
        self,
        graph_queries,  # GraphQueries instance
        graph_ops,      # GraphOps instance (for writes)
        conversations_dir: str
    ):
        """
        Initialize history service.

        Args:
            graph_queries: GraphQueries instance for reading
            graph_ops: GraphOps instance for writing
            conversations_dir: Directory for conversation thread files
        """
        self.graph = graph_queries
        self.ops = graph_ops
        self.conversations = ConversationThread(conversations_dir)

    # =========================================================================
    # QUERY OPERATIONS
    # =========================================================================

    def query_history(
        self,
        character_id: str,
        about_person: Optional[str] = None,
        about_place: Optional[str] = None,
        time_start: Optional[str] = None,
        time_end: Optional[str] = None,
        topic: Optional[str] = None,
        min_confidence: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Query what a character knows about the past.

        Only returns narratives the character BELIEVES. No omniscient access.

        Args:
            character_id: Who is asking (e.g., "player", "char_aldric")
            about_person: Filter to narratives about this character
            about_place: Filter to narratives about/at this place
            time_start: Filter to events after this time (e.g., "Day 3, morning")
            time_end: Filter to events before this time
            topic: Text search in narrative content
            min_confidence: Minimum belief level (0-1)

        Returns:
            List of narrative dicts with belief info and conversation text (if available)
        """
        # Build Cypher query
        where_clauses = [f"r.heard > 0"]

        if min_confidence > 0:
            where_clauses.append(f"r.believes >= {min_confidence}")

        if about_person:
            where_clauses.append(f"'{about_person}' IN n.about_characters")

        if about_place:
            where_clauses.append(
                f"('{about_place}' IN n.about_places OR EXISTS((n)-[:OCCURRED_AT]->(:Place {{id: '{about_place}'}})))"
            )

        if topic:
            # Simple text search (could be enhanced with semantic search)
            where_clauses.append(f"toLower(n.content) CONTAINS toLower('{topic}')")

        where_clause = " AND ".join(where_clauses)

        cypher = f"""
        MATCH (c:Character {{id: '{character_id}'}})-[r:BELIEVES]->(n:Narrative)
        OPTIONAL MATCH (n)-[:OCCURRED_AT]->(place:Place)
        WHERE {where_clause}
        RETURN n.id, n.name, n.content, n.type, n.weight,
               n.occurred_at, place.id AS occurred_where,
               n.source_file, n.source_section, n.detail,
               n.about_characters, n.about_places,
               r.heard, r.believes, r.doubts, r.source, r.from_whom, r.when
        ORDER BY n.occurred_at DESC, n.weight DESC
        """

        rows = self.graph._query(cypher)

        # Parse results and enrich with conversation text
        results = []
        fields = [
            "id", "name", "content", "type", "weight",
            "occurred_at", "occurred_where",
            "source_file", "source_section", "detail",
            "about_characters", "about_places",
            "heard", "believes", "doubts", "source", "from_whom", "when"
        ]

        for row in rows:
            narrative = dict(zip(fields, row))

            # Filter by time range if specified
            if time_start and narrative.get("occurred_at"):
                if not self._timestamp_gte(narrative["occurred_at"], time_start):
                    continue
            if time_end and narrative.get("occurred_at"):
                if not self._timestamp_lte(narrative["occurred_at"], time_end):
                    continue

            # Enrich with conversation text if source exists
            if narrative.get("source_file") and narrative.get("source_section"):
                conversation_text = self.conversations.read_section(
                    narrative["source_file"],
                    narrative["source_section"]
                )
                narrative["conversation"] = conversation_text

            results.append(narrative)

        return results

    def get_shared_history(
        self,
        character_a: str,
        character_b: str
    ) -> List[Dict[str, Any]]:
        """
        Get narratives that both characters believe — their shared history.

        Args:
            character_a: First character ID
            character_b: Second character ID

        Returns:
            List of narratives both characters believe
        """
        cypher = f"""
        MATCH (a:Character {{id: '{character_a}'}})-[ra:BELIEVES]->(n:Narrative)<-[rb:BELIEVES]-(b:Character {{id: '{character_b}'}})
        OPTIONAL MATCH (n)-[:OCCURRED_AT]->(place:Place)
        WHERE ra.heard > 0 AND rb.heard > 0
        RETURN n.id, n.name, n.content, n.type, n.occurred_at, place.id AS occurred_where,
               ra.believes as a_believes, rb.believes as b_believes
        ORDER BY n.occurred_at DESC
        """

        rows = self.graph._query(cypher)
        fields = ["id", "name", "content", "type", "occurred_at", "occurred_where",
                  "a_believes", "b_believes"]
        return [dict(zip(fields, row)) for row in rows]

    def who_knows(
        self,
        narrative_id: str,
        min_confidence: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Find all characters who know about a specific event.

        Args:
            narrative_id: The narrative to check
            min_confidence: Minimum belief level

        Returns:
            List of characters with their belief info
        """
        cypher = f"""
        MATCH (c:Character)-[r:BELIEVES]->(n:Narrative {{id: '{narrative_id}'}})
        WHERE r.heard > 0 AND r.believes >= {min_confidence}
        RETURN c.id, c.name, c.type,
               r.believes, r.source, r.from_whom, r.when, r.where
        ORDER BY r.believes DESC
        """

        rows = self.graph._query(cypher)
        fields = ["id", "name", "type", "believes", "source", "from_whom", "when", "where"]
        return [dict(zip(fields, row)) for row in rows]

    # =========================================================================
    # RECORD OPERATIONS
    # =========================================================================

    def record_player_history(
        self,
        content: str,
        conversation_text: str,
        character_id: str,
        witnesses: List[str],
        occurred_at: str,
        occurred_where: str,
        place_name: str,
        narrative_type: str = "memory",
        about_characters: Optional[List[str]] = None,
        about_places: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Record an event that happened in a scene (player was present).

        Creates:
        1. Conversation section in thread file
        2. Narrative node with source reference
        3. BELIEVES edges for all witnesses

        Args:
            content: Summary of what happened
            conversation_text: Full dialogue and narration
            character_id: Primary character in the conversation
            witnesses: List of character IDs who were present
            occurred_at: When it happened (e.g., "Day 5, dusk")
            occurred_where: Place ID where it happened
            place_name: Human-readable place name for conversation header
            narrative_type: Type of narrative (default: "memory")
            about_characters: Characters this narrative is about
            about_places: Places this narrative is about

        Returns:
            Dict with narrative_id and created belief_ids
        """
        # Parse timestamp for day/time
        day, time_of_day = self._parse_timestamp(occurred_at)

        # 1. Append to conversation thread
        source_ref = self.conversations.append_section(
            character_id=character_id,
            day=day,
            time_of_day=time_of_day,
            location_name=place_name,
            content=conversation_text
        )

        # 2. Create narrative node
        narrative_id = f"narr_{uuid.uuid4().hex[:8]}"

        # Build about
        about_chars = about_characters or []
        if character_id not in about_chars:
            about_chars.append(character_id)

        about_plcs = about_places or []
        if occurred_where not in about_plcs:
            about_plcs.append(occurred_where)

        narrative_data = {
            "type": "narrative",
            "id": narrative_id,
            "name": content[:50],  # Short name from content
            "content": content,
            "narrative_type": narrative_type,
            "occurred_at": occurred_at,
            "occurred_where": occurred_where,
            "source_file": source_ref["file"],
            "source_section": source_ref["section"],
            "about_characters": about_chars,
            "about_places": about_plcs,
            "weight": 0.5,  # Start with moderate weight
        }

        # Create via graph ops (using direct Cypher for now)
        self._create_narrative_node(narrative_data)

        # 3. Create BELIEVES edges for witnesses
        belief_ids = []
        for witness_id in witnesses:
            belief_source = "participated" if witness_id in about_chars else "witnessed"
            belief_id = self._create_belief_edge(
                character_id=witness_id,
                narrative_id=narrative_id,
                believes=1.0,
                heard=1.0,
                source=belief_source,
                when=occurred_at,
                where=occurred_where
            )
            belief_ids.append(belief_id)

        logger.info(
            f"[History] Recorded player history: {narrative_id} "
            f"with {len(belief_ids)} witnesses"
        )

        return {
            "narrative_id": narrative_id,
            "belief_ids": belief_ids,
            "source": source_ref
        }

    def record_world_history(
        self,
        content: str,
        detail: str,
        occurred_at: str,
        occurred_where: str,
        witnesses: List[str],
        narrative_type: str = "memory",
        about_characters: Optional[List[str]] = None,
        about_places: Optional[List[str]] = None,
        propagate: bool = False
    ) -> Dict[str, Any]:
        """
        Record an event that happened off-screen (world-generated).

        Creates:
        1. Narrative node with detail field (no conversation exists)
        2. BELIEVES edges for direct witnesses
        3. Optionally propagates beliefs based on proximity

        Args:
            content: Summary of what happened
            detail: Full description of the event
            occurred_at: When it happened
            occurred_where: Place ID where it happened
            witnesses: Character IDs who directly witnessed/participated
            narrative_type: Type of narrative
            about_characters: Characters this narrative is about
            about_places: Places this narrative is about
            propagate: Whether to spread news to nearby characters

        Returns:
            Dict with narrative_id and created belief_ids
        """
        # 1. Create narrative node
        narrative_id = f"narr_{uuid.uuid4().hex[:8]}"

        about_chars = about_characters or []
        about_plcs = about_places or []
        if occurred_where not in about_plcs:
            about_plcs.append(occurred_where)

        narrative_data = {
            "type": "narrative",
            "id": narrative_id,
            "name": content[:50],
            "content": content,
            "narrative_type": narrative_type,
            "occurred_at": occurred_at,
            "occurred_where": occurred_where,
            "detail": detail,
            "about_characters": about_chars,
            "about_places": about_plcs,
            "weight": 0.5,
        }

        self._create_narrative_node(narrative_data)

        # 2. Create BELIEVES edges for direct witnesses
        belief_ids = []
        for witness_id in witnesses:
            belief_id = self._create_belief_edge(
                character_id=witness_id,
                narrative_id=narrative_id,
                believes=1.0,
                heard=1.0,
                source="witnessed",
                when=occurred_at,
                where=occurred_where
            )
            belief_ids.append(belief_id)

        # 3. Optionally propagate to nearby characters
        if propagate:
            propagated = self._propagate_beliefs(
                narrative_id=narrative_id,
                origin_place=occurred_where,
                origin_time=occurred_at
            )
            belief_ids.extend(propagated)

        logger.info(
            f"[History] Recorded world history: {narrative_id} "
            f"with {len(belief_ids)} total beliefs"
        )

        return {
            "narrative_id": narrative_id,
            "belief_ids": belief_ids
        }

    # =========================================================================
    # HELPERS
    # =========================================================================

    def _parse_timestamp(self, timestamp: str) -> tuple:
        """Parse 'Day N, time' into (day: int, time: str)."""
        import re
        match = re.match(r"Day\s+(\d+),?\s*(\w+)", timestamp, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid timestamp: {timestamp}")
        return int(match.group(1)), match.group(2).lower()

    def _timestamp_gte(self, ts1: str, ts2: str) -> bool:
        """Check if ts1 >= ts2."""
        try:
            day1, time1 = self._parse_timestamp(ts1)
            day2, time2 = self._parse_timestamp(ts2)
            if day1 != day2:
                return day1 >= day2
            time_order = ["dawn", "morning", "midday", "afternoon", "dusk", "evening", "night", "midnight"]
            return time_order.index(time1) >= time_order.index(time2)
        except:
            return True

    def _timestamp_lte(self, ts1: str, ts2: str) -> bool:
        """Check if ts1 <= ts2."""
        try:
            day1, time1 = self._parse_timestamp(ts1)
            day2, time2 = self._parse_timestamp(ts2)
            if day1 != day2:
                return day1 <= day2
            time_order = ["dawn", "morning", "midday", "afternoon", "dusk", "evening", "night", "midnight"]
            return time_order.index(time1) <= time_order.index(time2)
        except:
            return True

    def _create_narrative_node(self, data: dict):
        """Create a narrative node in the graph with OCCURRED_AT link."""
        # Extract occurred_where for link creation
        occurred_where = data.pop("occurred_where", None)

        props = []
        for key, value in data.items():
            if key == "type":
                continue
            if isinstance(value, str):
                # Escape single quotes
                escaped = value.replace("'", "\\'")
                props.append(f"{key}: '{escaped}'")
            elif isinstance(value, list):
                items = [f"'{v}'" for v in value]
                props.append(f"{key}: [{', '.join(items)}]")
            elif isinstance(value, (int, float)):
                props.append(f"{key}: {value}")

        props_str = ", ".join(props)
        cypher = f"CREATE (n:Narrative {{{props_str}}})"
        self.graph._query(cypher)

        # Create OCCURRED_AT link to Place
        if occurred_where:
            link_cypher = f"""
            MATCH (n:Narrative {{id: '{data['id']}'}})
            MATCH (p:Place {{id: '{occurred_where}'}})
            CREATE (n)-[:OCCURRED_AT]->(p)
            """
            self.graph._query(link_cypher)

    def _create_belief_edge(
        self,
        character_id: str,
        narrative_id: str,
        believes: float,
        heard: float,
        source: str,
        when: str,
        where: str
    ) -> str:
        """Create a BELIEVES edge between character and narrative."""
        cypher = f"""
        MATCH (c:Character {{id: '{character_id}'}})
        MATCH (n:Narrative {{id: '{narrative_id}'}})
        CREATE (c)-[r:BELIEVES {{
            believes: {believes},
            heard: {heard},
            source: '{source}',
            when: '{when}',
            where: '{where}'
        }}]->(n)
        RETURN id(r)
        """
        result = self.graph._query(cypher)
        return f"belief_{character_id}_{narrative_id}"

    def _propagate_beliefs(
        self,
        narrative_id: str,
        origin_place: str,
        origin_time: str
    ) -> List[str]:
        """
        Propagate beliefs about an event to nearby characters.

        Characters at the origin place get high confidence.
        Characters at connected places get lower confidence (rumor).

        Returns list of created belief IDs.
        """
        belief_ids = []

        # Get characters at origin place (who didn't already get belief)
        cypher = f"""
        MATCH (c:Character)-[at:AT]->(p:Place {{id: '{origin_place}'}})
        WHERE at.present > 0.5
        AND NOT EXISTS {{
            MATCH (c)-[:BELIEVES]->(n:Narrative {{id: '{narrative_id}'}})
        }}
        RETURN c.id
        """
        nearby = self.graph._query(cypher)

        for row in nearby:
            char_id = row[0]
            belief_id = self._create_belief_edge(
                character_id=char_id,
                narrative_id=narrative_id,
                believes=0.9,
                heard=0.9,
                source="witnessed",
                when=origin_time,
                where=origin_place
            )
            belief_ids.append(belief_id)

        # Get characters at connected places (lower confidence)
        cypher = f"""
        MATCH (origin:Place {{id: '{origin_place}'}})-[conn:CONNECTS]-(nearby:Place)
        WHERE conn.path > 0
        MATCH (c:Character)-[at:AT]->(nearby)
        WHERE at.present > 0.5
        AND NOT EXISTS {{
            MATCH (c)-[:BELIEVES]->(n:Narrative {{id: '{narrative_id}'}})
        }}
        RETURN c.id, nearby.id
        """
        distant = self.graph._query(cypher)

        for row in distant:
            char_id, place_id = row[0], row[1]
            belief_id = self._create_belief_edge(
                character_id=char_id,
                narrative_id=narrative_id,
                believes=0.5,
                heard=0.7,
                source="rumor",
                when=origin_time,
                where=place_id
            )
            belief_ids.append(belief_id)

        return belief_ids
