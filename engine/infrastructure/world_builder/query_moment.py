# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md
"""
Query moment recording for World Builder.

Every query leaves a trace in the graph as a moment.
This makes the graph self-documenting and enables energy flow
from attention (queries) to related content.

Specs:
- docs/infrastructure/world-builder/ALGORITHM/ALGORITHM_Overview.md
"""

import logging
from typing import List, Dict, Any, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)

# Configuration
QUERY_MOMENT_WEIGHT = 0.2  # Low weight - may not surface unless relevant
QUERY_MOMENT_ENERGY = 0.3


def record_query_moment(
    query_text: str,
    char_id: Optional[str],
    place_id: Optional[str],
    graph,  # GraphQueries or GraphOps
    tick: int = 0
) -> str:
    """
    Create a moment representing this query/thought.

    The query becomes a trace in the graph. If char_id is provided,
    it's recorded as a "thought" that character had. Otherwise,
    it's recorded as a generic "query".

    Args:
        query_text: The natural language query
        char_id: Character perspective (query becomes their thought)
        place_id: Location context
        graph: Graph interface for creating nodes/links
        tick: Current world tick

    Returns:
        moment_id of the created moment
    """
    moment_id = f"mom_{uuid4().hex[:8]}"

    # Determine type: thought if char-centered, query otherwise
    moment_type = 'thought' if char_id else 'query'

    # Create moment node
    cypher = """
    CREATE (m:Moment {
        id: $moment_id,
        text: $text,
        type: $moment_type,
        status: 'possible',
        weight: $weight,
        energy: $energy,
        tick_created: $tick
    })
    RETURN m.id
    """

    try:
        graph.query(cypher, {
            'moment_id': moment_id,
            'text': query_text,
            'moment_type': moment_type,
            'weight': QUERY_MOMENT_WEIGHT,
            'energy': QUERY_MOMENT_ENERGY,
            'tick': tick
        })

        logger.debug(f"[QueryMoment] Created {moment_type} moment: {moment_id}")

        # Link to character if provided
        if char_id:
            _link_to_character(moment_id, char_id, graph)

        # Link to place if provided
        if place_id:
            _link_to_place(moment_id, place_id, graph)

    except Exception as e:
        logger.warning(f"[QueryMoment] Failed to create moment: {e}")

    return moment_id


def link_results_to_moment(
    moment_id: str,
    results: List[Dict[str, Any]],
    graph,
    max_links: int = 10
) -> int:
    """
    Create ABOUT links from query moment to result nodes.

    Links are weighted by similarity score if available.
    This enables physics to flow energy from query attention
    to related content.

    Args:
        moment_id: The query moment to link from
        results: Result nodes with 'id' and optionally 'similarity'
        graph: Graph interface
        max_links: Maximum number of links to create

    Returns:
        Number of links created
    """
    links_created = 0

    for result in results[:max_links]:
        result_id = result.get('id')
        if not result_id:
            continue

        # Use similarity score as weight, default 0.5
        weight = result.get('similarity', 0.5)

        cypher = """
        MATCH (m:Moment {id: $moment_id})
        MATCH (n {id: $result_id})
        MERGE (m)-[r:ABOUT]->(n)
        SET r.weight = $weight
        """

        try:
            graph.query(cypher, {
                'moment_id': moment_id,
                'result_id': result_id,
                'weight': weight
            })
            links_created += 1
        except Exception as e:
            logger.debug(f"[QueryMoment] Failed to link to {result_id}: {e}")

    if links_created > 0:
        logger.debug(f"[QueryMoment] Linked {moment_id} to {links_created} results")

    return links_created


def _link_to_character(moment_id: str, char_id: str, graph):
    """Create bidirectional links between moment and character."""
    # Moment attached to character
    cypher_attached = """
    MATCH (m:Moment {id: $moment_id})
    MATCH (c:Character {id: $char_id})
    MERGE (m)-[:ATTACHED_TO]->(c)
    """

    # Character can speak this thought
    cypher_can_speak = """
    MATCH (m:Moment {id: $moment_id})
    MATCH (c:Character {id: $char_id})
    MERGE (c)-[r:CAN_SPEAK]->(m)
    SET r.strength = 0.5
    """

    try:
        graph.query(cypher_attached, {'moment_id': moment_id, 'char_id': char_id})
        graph.query(cypher_can_speak, {'moment_id': moment_id, 'char_id': char_id})
        logger.debug(f"[QueryMoment] Linked {moment_id} to character {char_id}")
    except Exception as e:
        logger.debug(f"[QueryMoment] Failed to link to character: {e}")


def _link_to_place(moment_id: str, place_id: str, graph):
    """Create link from moment to place where it occurred."""
    cypher = """
    MATCH (m:Moment {id: $moment_id})
    MATCH (p:Place {id: $place_id})
    MERGE (m)-[:OCCURRED_AT]->(p)
    """

    try:
        graph.query(cypher, {'moment_id': moment_id, 'place_id': place_id})
        logger.debug(f"[QueryMoment] Linked {moment_id} to place {place_id}")
    except Exception as e:
        logger.debug(f"[QueryMoment] Failed to link to place: {e}")
