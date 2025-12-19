# DOCS: docs/infrastructure/canon/IMPLEMENTATION_Canon.md
"""
Speaker Resolution — Determines who speaks a moment.

Rules (from BEHAVIORS_Canon.md):
- Must be present (same location as player)
- Must be awake (state != sleeping, unconscious, dead)
- Highest CAN_SPEAK.strength wins
- Returns None for narration moments or if no valid speaker
"""

import logging
from typing import Optional

from engine.physics.graph import GraphQueries, get_playthrough_graph_name

logger = logging.getLogger(__name__)


def determine_speaker(
    playthrough_id: str,
    moment_id: str,
    player_id: str = "char_player",
    host: str = "localhost",
    port: int = 6379
) -> Optional[str]:
    """
    Find the best speaker for a moment.

    Queries for characters that:
    1. Have CAN_SPEAK link to the moment
    2. Are at same location as player
    3. Are awake (state = 'awake')

    Returns highest CAN_SPEAK.strength character, or None.

    Args:
        playthrough_id: The playthrough ID
        moment_id: The moment to find speaker for
        player_id: The player character ID (default: char_player)
        host: FalkorDB host
        port: FalkorDB port

    Returns:
        Character ID of best speaker, or None if no valid speaker
    """
    graph_name = get_playthrough_graph_name(playthrough_id)
    queries = GraphQueries(graph_name=graph_name, host=host, port=port)

    # Query for valid speakers (Q5 from ALGORITHM)
    # Must: have CAN_SPEAK to moment, be at player's location, be awake and alive
    cypher = """
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $moment_id})
        MATCH (c)-[:AT {present: 1.0}]->(loc:Place)<-[:AT {present: 1.0}]-(player:Character {id: $player_id})
        WHERE (c.state = 'awake' OR c.state IS NULL) AND (c.alive = true OR c.alive IS NULL)
        RETURN c.id AS speaker_id, r.strength AS strength
        ORDER BY r.strength DESC
        LIMIT 1
    """

    try:
        results = queries.query(cypher, {
            "moment_id": moment_id,
            "player_id": player_id
        })

        if results and len(results) > 0:
            speaker_id = results[0].get("speaker_id")
            strength = results[0].get("strength", 1.0)
            logger.debug(f"[Speaker] Found speaker {speaker_id} (strength={strength}) for {moment_id}")
            return speaker_id

        logger.debug(f"[Speaker] No valid speaker found for {moment_id}")
        return None

    except Exception as e:
        logger.warning(f"[Speaker] Error finding speaker for {moment_id}: {e}")
        return None


def get_moment_type(
    playthrough_id: str,
    moment_id: str,
    host: str = "localhost",
    port: int = 6379
) -> Optional[str]:
    """
    Get the type of a moment (narration, dialogue, action).

    Args:
        playthrough_id: The playthrough ID
        moment_id: The moment ID

    Returns:
        Moment type string, or None if not found
    """
    graph_name = get_playthrough_graph_name(playthrough_id)
    queries = GraphQueries(graph_name=graph_name, host=host, port=port)

    cypher = """
        MATCH (m:Moment {id: $moment_id})
        RETURN m.type AS type
    """

    try:
        results = queries.query(cypher, {"moment_id": moment_id})
        if results and len(results) > 0:
            return results[0].get("type", "narration")
        return None
    except Exception as e:
        logger.warning(f"[Speaker] Error getting moment type for {moment_id}: {e}")
        return None
