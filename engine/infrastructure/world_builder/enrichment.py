# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md
"""
Enrichment prompts and application for World Builder.

Builds prompts for LLM enrichment and applies the results to the graph.
All created content links back to the query moment via ABOUT.

Specs:
- docs/infrastructure/world-builder/ALGORITHM_World_Builder.md
"""

import logging
from typing import Dict, Any, List, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


def build_enrichment_prompt(
    query: str,
    context: Dict[str, Any]
) -> str:
    """
    Build the LLM prompt for world enrichment.

    Args:
        query: The sparse query that needs enrichment
        context: Dict with char_id, place_id, existing results, sparsity info

    Returns:
        Prompt string for LLM
    """
    char_context = ""
    if context.get('char_id'):
        char = context.get('character_data', {})
        char_context = f"""
FROM PERSPECTIVE OF: {char.get('name', context['char_id'])}
  Backstory: {char.get('backstory', 'Unknown')}
  Location: {char.get('location', 'Unknown')}
  Voice: {char.get('voice', 'Unknown')}
"""

    place_context = ""
    if context.get('place_id'):
        place = context.get('place_data', {})
        place_context = f"""
LOCATION: {place.get('name', context['place_id'])} ({place.get('type', 'place')})
  Region: {place.get('region', 'Unknown')}
"""

    existing = ""
    if context.get('existing'):
        existing = f"""
EXISTING (sparse, needs enrichment):
{_format_results(context['existing'])}
"""

    sparsity_info = ""
    if context.get('sparsity'):
        s = context['sparsity']
        sparsity_info = f"""
SPARSITY ANALYSIS:
  Proximity: {s.proximity:.2f} (results match query?)
  Cluster size: {s.cluster_size} (how many results?)
  Diversity: {s.diversity:.2f} (results varied?)
  Connectedness: {s.connectedness:.2f} (results linked?)
  Reason: {s.reason or 'multiple factors'}
"""

    return f"""You are the World Builder for a story set in 1087 England, after the Norman Conquest.

QUERY: "{query}"

{char_context}
{place_context}
{existing}
{sparsity_info}

Generate content to answer this query richly. You may create:

1. CHARACTERS - New people with names, backstories, relationships
2. PLACES - Locations with atmosphere, details
3. THINGS - Objects with significance
4. NARRATIVES - Events, memories, rumors, beliefs
5. LINKS - Relationships between any nodes (just weight, physics handles energy)
6. MOMENTS - Thoughts as potential dialogue (type=thought, status=possible)

For moments, these are things the querying character might think or say.
They should feel personal, emotional, connected to the query.

Output as YAML:

```yaml
characters:
  - id: char_{{slug}}
    name: string
    character_type: minor | significant
    backstory: string
    voice: {{tone, patterns}}

places:
  - id: place_{{slug}}
    name: string
    type: string
    atmosphere: {{sights, sounds, smells}}
    description: string

things:
  - id: thing_{{slug}}
    name: string
    type: string
    description: string
    significance: string

narratives:
  - id: narr_{{slug}}
    name: string
    content: string
    type: memory | rumor | event | legend
    truth: float

links:
  - from: node_id
    to: node_id
    type: LINK_TYPE
    weight: float  # 0.0-1.0

moments:
  - text: string
    type: thought  # Always "thought"
    weight: float  # 0.3-0.7
    speaker_id: char_id  # Who would say/think this
```

Be specific. Use concrete details. Create 2-5 items per category (not all categories needed).
Moments should be emotional, personal - things the character might actually think or say.
"""


def apply_enrichment(
    enrichment: Dict[str, Any],
    query_moment_id: str,
    char_id: Optional[str],
    place_id: Optional[str],
    graph,
    tick: int = 0
) -> Dict[str, int]:
    """
    Create all nodes, links, and moments from enrichment.

    Links ALL created content back to the query moment via ABOUT.
    Physics handles energy flow - we just set weights.

    Args:
        enrichment: Parsed YAML from LLM
        query_moment_id: The query moment to link back to
        char_id: Default character context
        place_id: Default place context
        graph: Graph interface
        tick: Current world tick

    Returns:
        Dict with counts of created items
    """
    counts = {
        'characters': 0,
        'places': 0,
        'things': 0,
        'narratives': 0,
        'links': 0,
        'moments': 0
    }

    created_ids = []

    # Characters
    for char in enrichment.get('characters', []):
        if _create_character(char, graph):
            created_ids.append(char['id'])
            counts['characters'] += 1

    # Places
    for place in enrichment.get('places', []):
        if _create_place(place, graph):
            created_ids.append(place['id'])
            counts['places'] += 1

    # Things
    for thing in enrichment.get('things', []):
        if _create_thing(thing, graph):
            created_ids.append(thing['id'])
            counts['things'] += 1

    # Narratives
    for narr in enrichment.get('narratives', []):
        if _create_narrative(narr, graph):
            created_ids.append(narr['id'])
            counts['narratives'] += 1

    # Links between nodes
    for link in enrichment.get('links', []):
        if _create_link(link, graph):
            counts['links'] += 1

    # Link ALL created nodes back to query moment
    for node_id in created_ids:
        _link_to_query_moment(query_moment_id, node_id, graph)

    # Moments - potential thoughts
    for moment in enrichment.get('moments', []):
        moment_id = _create_moment(moment, char_id, place_id, graph, tick)
        if moment_id:
            # Link enriched moment back to query moment
            _link_to_query_moment(query_moment_id, moment_id, graph, weight=0.6)
            counts['moments'] += 1

    logger.info(
        f"[Enrichment] Applied: {counts['characters']} chars, "
        f"{counts['places']} places, {counts['things']} things, "
        f"{counts['narratives']} narrs, {counts['links']} links, "
        f"{counts['moments']} moments"
    )

    return counts


def _format_results(results: List[Dict]) -> str:
    """Format existing results for prompt."""
    lines = []
    for r in results[:5]:
        name = r.get('name', r.get('text', r.get('id', 'unknown')))
        node_type = r.get('label', r.get('type', 'node'))
        lines.append(f"  - [{node_type}] {name}")
    return '\n'.join(lines) if lines else '  (none)'


def _create_character(char: Dict, graph) -> bool:
    """Create a Character node."""
    if 'id' not in char:
        return False

    cypher = """
    MERGE (c:Character {id: $id})
    SET c.name = $name,
        c.character_type = $character_type,
        c.backstory = $backstory,
        c.voice = $voice,
        c.generated = true
    """

    try:
        graph.query(cypher, {
            'id': char['id'],
            'name': char.get('name', char['id']),
            'character_type': char.get('character_type', 'minor'),
            'backstory': char.get('backstory', ''),
            'voice': str(char.get('voice', {}))
        })
        logger.debug(f"[Enrichment] Created character: {char['id']}")
        return True
    except Exception as e:
        logger.warning(f"[Enrichment] Failed to create character {char.get('id')}: {e}")
        return False


def _create_place(place: Dict, graph) -> bool:
    """Create a Place node."""
    if 'id' not in place:
        return False

    cypher = """
    MERGE (p:Place {id: $id})
    SET p.name = $name,
        p.type = $type,
        p.atmosphere = $atmosphere,
        p.description = $description,
        p.generated = true
    """

    try:
        graph.query(cypher, {
            'id': place['id'],
            'name': place.get('name', place['id']),
            'type': place.get('type', 'location'),
            'atmosphere': str(place.get('atmosphere', {})),
            'description': place.get('description', '')
        })
        logger.debug(f"[Enrichment] Created place: {place['id']}")
        return True
    except Exception as e:
        logger.warning(f"[Enrichment] Failed to create place {place.get('id')}: {e}")
        return False


def _create_thing(thing: Dict, graph) -> bool:
    """Create a Thing node."""
    if 'id' not in thing:
        return False

    cypher = """
    MERGE (t:Thing {id: $id})
    SET t.name = $name,
        t.type = $type,
        t.description = $description,
        t.significance = $significance,
        t.generated = true
    """

    try:
        graph.query(cypher, {
            'id': thing['id'],
            'name': thing.get('name', thing['id']),
            'type': thing.get('type', 'object'),
            'description': thing.get('description', ''),
            'significance': thing.get('significance', '')
        })
        logger.debug(f"[Enrichment] Created thing: {thing['id']}")
        return True
    except Exception as e:
        logger.warning(f"[Enrichment] Failed to create thing {thing.get('id')}: {e}")
        return False


def _create_narrative(narr: Dict, graph) -> bool:
    """Create a Narrative node."""
    if 'id' not in narr:
        return False

    cypher = """
    MERGE (n:Narrative {id: $id})
    SET n.name = $name,
        n.content = $content,
        n.type = $type,
        n.truth = $truth,
        n.generated = true
    """

    try:
        graph.query(cypher, {
            'id': narr['id'],
            'name': narr.get('name', narr['id']),
            'content': narr.get('content', ''),
            'type': narr.get('type', 'event'),
            'truth': narr.get('truth', 0.5)
        })
        logger.debug(f"[Enrichment] Created narrative: {narr['id']}")
        return True
    except Exception as e:
        logger.warning(f"[Enrichment] Failed to create narrative {narr.get('id')}: {e}")
        return False


def _create_link(link: Dict, graph) -> bool:
    """Create a link between nodes."""
    if not all(k in link for k in ['from', 'to', 'type']):
        return False

    # Build dynamic link type
    link_type = link['type'].upper().replace(' ', '_')
    weight = link.get('weight', 0.5)

    cypher = f"""
    MATCH (a {{id: $from_id}})
    MATCH (b {{id: $to_id}})
    MERGE (a)-[r:{link_type}]->(b)
    SET r.weight = $weight
    """

    try:
        graph.query(cypher, {
            'from_id': link['from'],
            'to_id': link['to'],
            'weight': weight
        })
        logger.debug(f"[Enrichment] Created link: {link['from']}-[{link_type}]->{link['to']}")
        return True
    except Exception as e:
        logger.debug(f"[Enrichment] Failed to create link: {e}")
        return False


def _create_moment(
    moment: Dict,
    char_id: Optional[str],
    place_id: Optional[str],
    graph,
    tick: int
) -> Optional[str]:
    """Create a Moment node (thought)."""
    if 'text' not in moment:
        return None

    moment_id = f"mom_{uuid4().hex[:8]}"
    weight = moment.get('weight', 0.4)
    speaker_id = moment.get('speaker_id', char_id)

    cypher = """
    CREATE (m:Moment {
        id: $moment_id,
        text: $text,
        type: 'thought',
        status: 'possible',
        weight: $weight,
        energy: 0.5,
        tick_created: $tick,
        generated: true
    })
    """

    try:
        graph.query(cypher, {
            'moment_id': moment_id,
            'text': moment['text'],
            'weight': weight,
            'tick': tick
        })

        # Link to speaker
        if speaker_id:
            _link_moment_to_speaker(moment_id, speaker_id, graph)

        # Link to place
        if place_id:
            _link_moment_to_place(moment_id, place_id, graph)

        logger.debug(f"[Enrichment] Created moment: {moment_id}")
        return moment_id

    except Exception as e:
        logger.warning(f"[Enrichment] Failed to create moment: {e}")
        return None


def _link_moment_to_speaker(moment_id: str, speaker_id: str, graph):
    """Link moment to its speaker."""
    cypher = """
    MATCH (m:Moment {id: $moment_id})
    MATCH (c:Character {id: $speaker_id})
    MERGE (m)-[:ATTACHED_TO]->(c)
    MERGE (c)-[r:CAN_SPEAK]->(m)
    SET r.strength = 0.8
    """
    try:
        graph.query(cypher, {'moment_id': moment_id, 'speaker_id': speaker_id})
    except Exception as e:
        logger.debug(f"[Enrichment] Failed to link moment to speaker: {e}")


def _link_moment_to_place(moment_id: str, place_id: str, graph):
    """Link moment to location."""
    cypher = """
    MATCH (m:Moment {id: $moment_id})
    MATCH (p:Place {id: $place_id})
    MERGE (m)-[:ATTACHED_TO]->(p)
    """
    try:
        graph.query(cypher, {'moment_id': moment_id, 'place_id': place_id})
    except Exception as e:
        logger.debug(f"[Enrichment] Failed to link moment to place: {e}")


def _link_to_query_moment(query_moment_id: str, node_id: str, graph, weight: float = 0.5):
    """Link created node back to the query moment via ABOUT."""
    cypher = """
    MATCH (q:Moment {id: $query_moment_id})
    MATCH (n {id: $node_id})
    MERGE (q)-[r:ABOUT]->(n)
    SET r.weight = $weight
    """
    try:
        graph.query(cypher, {
            'query_moment_id': query_moment_id,
            'node_id': node_id,
            'weight': weight
        })
    except Exception as e:
        logger.debug(f"[Enrichment] Failed to link to query moment: {e}")
