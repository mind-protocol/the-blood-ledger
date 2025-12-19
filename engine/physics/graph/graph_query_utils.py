"""
Blood Ledger — Graph Query Utilities

Standalone helper functions for graph query operations.
Extracted from graph_queries.py to reduce file size.

DOCS: None yet (extracted during monolith split)
"""

import json
import logging
import numpy as np
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Fields to exclude from output (internal/technical only)
SYSTEM_FIELDS = {'embedding', 'created_at', 'updated_at'}


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def extract_node_props(node, system_fields: set = None) -> Optional[Dict[str, Any]]:
    """
    Extract properties from a FalkorDB node.

    Args:
        node: FalkorDB node object or dict
        system_fields: Fields to exclude (defaults to SYSTEM_FIELDS)

    Returns:
        Dict of cleaned properties or None if invalid
    """
    if system_fields is None:
        system_fields = SYSTEM_FIELDS

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
        clean = {k: v for k, v in props.items() if k not in system_fields}

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


def extract_link_props(rel, system_fields: set = None) -> Optional[Dict[str, Any]]:
    """
    Extract properties from a FalkorDB relationship.

    Args:
        rel: FalkorDB relationship object or dict
        system_fields: Fields to exclude (defaults to SYSTEM_FIELDS)

    Returns:
        Dict of cleaned properties or None if invalid
    """
    if system_fields is None:
        system_fields = SYSTEM_FIELDS

    if not rel:
        return None

    try:
        # FalkorDB relationship format varies
        if isinstance(rel, list) and len(rel) >= 3:
            rel_type = rel[0]
            props = rel[1] if isinstance(rel[1], dict) else {}
            link = {
                'type': rel_type,
                **{k: v for k, v in props.items() if k not in system_fields}
            }
            return link

        elif isinstance(rel, dict):
            return {k: v for k, v in rel.items() if k not in system_fields}

        return None

    except Exception as e:
        logger.warning(f"Error extracting link props: {e}")
        return None


def to_markdown(search_result: Dict[str, Any]) -> str:
    """
    Convert search results to markdown format for LLM consumption.

    IMPORTANT: Include ALL fields. NEVER filter or summarize.
    The LLM needs complete information to make decisions.

    Args:
        search_result: Dict with 'query', 'matches', and optional 'clusters'

    Returns:
        Markdown-formatted string
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
