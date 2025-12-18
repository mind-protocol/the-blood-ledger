"""
Blood Ledger — Graph Operations

Write mutations to FalkorDB via YAML/JSON files.

Usage:
    from engine.db.graph_ops import GraphOps

    write = GraphOps()

    # Apply a mutation file
    result = write.apply(path="mutations/scene_001.yaml")

    if result.errors:
        for error in result.errors:
            print(f"{error['item']}: {error['message']}")
            print(f"  Fix: {error['fix']}")

Docs:
- docs/engine/moments/SCHEMA_Moments.md — node/link schema for the moment graph
- docs/engine/moments/ALGORITHM_Transitions.md — how mutations should behave
- docs/engine/GRAPH_OPERATIONS_GUIDE.md — mutation file format
"""

import json
import yaml
import logging
import numpy as np
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple, Callable
from datetime import datetime
from dataclasses import dataclass, field
from falkordb import FalkorDB

# Add tools directory to path for image generation
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "image_generation"))

try:
    from generate_image import generate_image as _generate_image
    IMAGE_GENERATION_AVAILABLE = True
except ImportError:
    IMAGE_GENERATION_AVAILABLE = False
    _generate_image = None

logger = logging.getLogger(__name__)


import threading

# Queue for async image generation
_image_generation_queue: list = []
_image_generation_lock = threading.Lock()


def _get_image_path(node_type: str, node_id: str, playthrough: str) -> str:
    """Get the expected path for a node's image."""
    type_config = {
        'character': 'characters',
        'place': 'places',
        'thing': 'things',
    }
    subdir = type_config.get(node_type, 'other')
    return f"frontend/public/playthroughs/{playthrough}/images/{subdir}/{node_id}.png"


def _generate_node_image_async(
    node_type: str,
    node_id: str,
    image_prompt: str,
    playthrough: str = "default"
) -> None:
    """Generate image in background thread."""
    if not IMAGE_GENERATION_AVAILABLE or not _generate_image:
        return

    type_config = {
        'character': {'image_type': 'character_portrait', 'subdir': 'characters'},
        'place': {'image_type': 'setting_strip', 'subdir': 'places'},
        'thing': {'image_type': 'object_icon', 'subdir': 'things'},
    }

    config = type_config.get(node_type)
    if not config:
        return

    try:
        logger.info(f"[GraphOps] Generating {config['image_type']} for {node_id} (async)...")
        result = _generate_image(
            prompt=image_prompt,
            image_type=config['image_type'],
            playthrough=playthrough,
            name=f"{config['subdir']}/{node_id}",
            save=True
        )
        if result and result.get('local_path'):
            logger.info(f"[GraphOps] Image saved: {result['local_path']}")
    except Exception as e:
        logger.warning(f"[GraphOps] Image generation failed for {node_id}: {e}")


import shutil

def _generate_node_image(
    node_type: str,
    node_id: str,
    image_prompt: str,
    playthrough: str = "default"
) -> Optional[str]:
    """
    Get or generate image for a node (character, place, or thing).

    Priority:
    1. Check if image exists in playthrough folder
    2. Copy from default/seed folder if available
    3. Generate async if not found anywhere

    Args:
        node_type: 'character', 'place', or 'thing'
        node_id: The node ID (used as filename)
        image_prompt: The prompt for image generation
        playthrough: Playthrough folder name

    Returns:
        Path to image (may not exist yet if generating async)
    """
    if not image_prompt:
        return None

    # Check if image already exists in playthrough folder
    expected_path = _get_image_path(node_type, node_id, playthrough)
    if Path(expected_path).exists():
        logger.debug(f"[GraphOps] Image already exists: {expected_path}")
        return expected_path

    # Check if image exists in default/seed folder - copy if found
    if playthrough != "default":
        seed_path = _get_image_path(node_type, node_id, "default")
        if Path(seed_path).exists():
            # Copy from seed to playthrough
            dest_path = Path(expected_path)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(seed_path, dest_path)
            logger.info(f"[GraphOps] Copied seed image: {seed_path} -> {expected_path}")
            return expected_path

    # Generate async if no existing image found
    if not IMAGE_GENERATION_AVAILABLE or not _generate_image:
        return None

    thread = threading.Thread(
        target=_generate_node_image_async,
        args=(node_type, node_id, image_prompt, playthrough),
        daemon=True
    )
    thread.start()

    return expected_path


# =============================================================================
# GLOBAL EVENT EMITTER
# =============================================================================

# Callbacks registered for mutation events
_mutation_listeners: List[Callable[[Dict[str, Any]], None]] = []


def add_mutation_listener(callback: Callable[[Dict[str, Any]], None]) -> None:
    """
    Register a callback to receive mutation events.

    The callback receives a dict with:
        - type: 'node_created', 'node_updated', 'link_created', 'link_updated',
                'movement', 'tension_update', 'apply_start', 'apply_complete', 'apply_error'
        - timestamp: ISO timestamp
        - data: Event-specific data
    """
    if callback not in _mutation_listeners:
        _mutation_listeners.append(callback)


def remove_mutation_listener(callback: Callable[[Dict[str, Any]], None]) -> None:
    """Remove a mutation listener."""
    if callback in _mutation_listeners:
        _mutation_listeners.remove(callback)


def _emit_event(event_type: str, data: Dict[str, Any]) -> None:
    """Emit an event to all registered listeners."""
    event = {
        "type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    for listener in _mutation_listeners:
        try:
            listener(event)
        except Exception as e:
            logger.warning(f"Mutation listener error: {e}")

# Similarity threshold for duplicate detection
SIMILARITY_THRESHOLD = 0.85


class WriteError(Exception):
    """Error with helpful fix instructions."""

    def __init__(self, message: str, fix: str):
        self.message = message
        self.fix = fix
        super().__init__(f"{message}\n\nHOW TO FIX:\n{fix}")


@dataclass
class SimilarNode:
    """A node that is similar to one being created."""
    id: str
    name: str
    node_type: str
    similarity: float

    def __str__(self):
        return f"{self.name} ({self.id}) - {self.similarity:.0%} similar"


@dataclass
class ApplyResult:
    """Result of applying a mutation file."""
    persisted: List[str] = field(default_factory=list)
    rejected: List[str] = field(default_factory=list)
    errors: List[Dict[str, str]] = field(default_factory=list)
    duplicates: List[Dict[str, Any]] = field(default_factory=list)  # Similar nodes found

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    @property
    def has_duplicates(self) -> bool:
        return len(self.duplicates) > 0


class GraphOps:
    """
    Simple interface for FalkorDB graph operations.

    All functions use MERGE (upsert) - safe to call multiple times.
    """

    def __init__(
        self,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379
    ):
        self.graph_name = graph_name

        # Connect using FalkorDB client
        try:
            self.db = FalkorDB(host=host, port=port)
            self.graph = self.db.select_graph(graph_name)
            logger.info(f"[GraphOps] Connected to {graph_name}")
        except Exception as e:
            raise WriteError(
                f"Cannot connect to FalkorDB at {host}:{port}",
                f"""1. Start FalkorDB server (pip install falkordb)

2. Or use FalkorDB Cloud: https://app.falkordb.cloud

3. Check connection settings:
   GraphOps(host="your-host", port=6379)

Error: {e}"""
            )

    def _query(self, cypher: str, params: Dict[str, Any] = None) -> List:
        """Execute a Cypher query."""
        try:
            result = self.graph.query(cypher, params or {})
            return result.result_set if result.result_set else []
        except Exception as e:
            error_str = str(e)
            if "already exists" in error_str.lower():
                raise WriteError(
                    f"Node or link already exists",
                    "This is usually fine - MERGE updates existing nodes.\n"
                    "If you want to update, just call the same function again with new values."
                )
            elif "property" in error_str.lower() and "not found" in error_str.lower():
                raise WriteError(
                    f"Invalid property: {error_str}",
                    "Check that you're using valid property names from the schema.\n"
                    "See: docs/engine/SCHEMA.md"
                )
            elif "syntax" in error_str.lower():
                raise WriteError(
                    f"Cypher syntax error: {error_str}",
                    f"This is likely a bug in graph_ops.py. Query was:\n{cypher}"
                )
            else:
                raise WriteError(
                    f"Write failed: {error_str}",
                    f"Query: {cypher}\nParams: {params}"
                )

    # =========================================================================
    # DUPLICATE DETECTION
    # =========================================================================

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _find_similar_nodes(
        self,
        label: str,
        embedding: List[float],
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[SimilarNode]:
        """
        Find nodes with embeddings similar to the given embedding.

        Args:
            label: Node label (Character, Place, Thing, Narrative)
            embedding: The embedding to compare against
            threshold: Minimum similarity to return (default 0.85)

        Returns:
            List of SimilarNode objects above threshold, sorted by similarity
        """
        if not embedding:
            return []

        # Get all nodes of this type with embeddings
        cypher = f"""
        MATCH (n:{label})
        WHERE n.embedding IS NOT NULL
        RETURN n.id, n.name, n.embedding
        """

        try:
            rows = self._query(cypher)
            if not rows:
                return []

            similar = []
            for row in rows:
                if len(row) >= 3 and row[2]:
                    node_id = row[0]
                    node_name = row[1]
                    node_embedding = json.loads(row[2]) if isinstance(row[2], str) else row[2]

                    sim = self._cosine_similarity(embedding, node_embedding)
                    if sim >= threshold:
                        similar.append(SimilarNode(
                            id=node_id,
                            name=node_name,
                            node_type=label.lower(),
                            similarity=sim
                        ))

            # Sort by similarity descending
            similar.sort(key=lambda x: x.similarity, reverse=True)
            return similar

        except Exception as e:
            logger.warning(f"Error finding similar nodes: {e}")
            return []

    def check_duplicate(
        self,
        label: str,
        embedding: List[float],
        threshold: float = SIMILARITY_THRESHOLD
    ) -> Optional[SimilarNode]:
        """
        Check if a similar node already exists.

        Args:
            label: Node type (Character, Place, Thing, Narrative)
            embedding: Embedding of the new node
            threshold: Similarity threshold

        Returns:
            Most similar node if above threshold, None otherwise
        """
        similar = self._find_similar_nodes(label, embedding, threshold)
        return similar[0] if similar else None

    # =========================================================================
    # APPLY METHOD (Main API)
    # =========================================================================

    def apply(self, path: str = None, data: Dict = None, playthrough: str = "default") -> ApplyResult:
        """
        Apply mutations from a YAML/JSON file or dict.

        Args:
            path: Path to mutation file (YAML or JSON)
            data: Dict with mutations (alternative to file)
            playthrough: Playthrough folder name (for image generation)

        Returns:
            ApplyResult with persisted, rejected, and errors

        File format:
            nodes:
              - type: character
                id: char_aldric
                name: Aldric
                image_prompt: "A cinematic portrait of..."
                ...
            links:
              - type: belief
                character: char_aldric
                narrative: narr_oath
                ...
            updates:
              - node: char_aldric
                modifier_add: {...}
            movements:
              - character: char_edmund
                to: place_castle
        """
        self._current_playthrough = playthrough  # Store for use in add_* methods
        result = ApplyResult()

        # Load data
        if path:
            try:
                file_path = Path(path)
                if not file_path.exists():
                    raise WriteError(
                        f"File not found: {path}",
                        f"Create the file at: {file_path.absolute()}"
                    )

                with open(file_path) as f:
                    if path.endswith('.yaml') or path.endswith('.yml'):
                        data = yaml.safe_load(f)
                    else:
                        data = json.load(f)
            except yaml.YAMLError as e:
                raise WriteError(
                    f"Invalid YAML: {e}",
                    "Check your YAML syntax. Common issues:\n"
                    "- Missing colons after keys\n"
                    "- Inconsistent indentation\n"
                    "- Unquoted special characters"
                )
            except json.JSONDecodeError as e:
                raise WriteError(
                    f"Invalid JSON: {e}",
                    "Check your JSON syntax. Common issues:\n"
                    "- Missing commas between items\n"
                    "- Trailing commas\n"
                    "- Unquoted keys"
                )

        if not data:
            raise WriteError(
                "No data provided",
                "Either provide a path to a mutation file:\n"
                "  write.apply(path='mutations/scene.yaml')\n\n"
                "Or provide data directly:\n"
                "  write.apply(data={'nodes': [...], 'links': [...]})"
            )

        # Emit apply_start event
        _emit_event("apply_start", {
            "source": path or "direct",
            "node_count": len(data.get('nodes', [])),
            "link_count": len(data.get('links', [])),
            "update_count": len(data.get('updates', [])),
            "movement_count": len(data.get('movements', [])),
            "event_summary": data.get('event', {}).get('summary', '')
        })

        # Get existing node IDs for connectivity check
        existing_ids = self._get_existing_node_ids()
        new_node_ids: Set[str] = set()
        linked_ids: Set[str] = set()

        # 1. Process nodes
        for node in data.get('nodes', []):
            node_type = node.get('type')
            node_id = node.get('id')
            embedding = node.get('embedding')

            if not node_type or not node_id:
                result.errors.append({
                    'item': str(node),
                    'message': 'Node missing type or id',
                    'fix': 'Every node needs: type (character/place/thing/narrative/tension/moment) and id'
                })
                result.rejected.append(str(node))
                continue

            # Check for duplicates if embedding provided
            if embedding:
                label = node_type.capitalize()
                similar = self.check_duplicate(label, embedding)
                if similar:
                    result.duplicates.append({
                        'new_node': node_id,
                        'new_name': node.get('name', node_id),
                        'similar_to': similar.id,
                        'similar_name': similar.name,
                        'similarity': similar.similarity,
                        'action': 'skipped',
                        'fix': f"Update existing node '{similar.id}' or use force=True to create anyway"
                    })
                    result.rejected.append(node_id)
                    continue

            new_node_ids.add(node_id)

            try:
                if node_type == 'character':
                    self.add_character(**self._extract_character_args(node))
                elif node_type == 'place':
                    self.add_place(**self._extract_place_args(node))
                elif node_type == 'thing':
                    self.add_thing(**self._extract_thing_args(node))
                elif node_type == 'narrative':
                    self.add_narrative(**self._extract_narrative_args(node))
                elif node_type == 'tension':
                    self.add_tension(**self._extract_tension_args(node))
                elif node_type == 'moment':
                    self.add_moment(**self._extract_moment_args(node))
                else:
                    result.errors.append({
                        'item': node_id,
                        'message': f'Invalid node type: {node_type}',
                        'fix': 'Valid types: character, place, thing, narrative, tension, moment'
                    })
                    result.rejected.append(node_id)
                    continue

                result.persisted.append(node_id)

                # Emit node_created event with ALL fields
                _emit_event("node_created", node)

            except WriteError as e:
                result.errors.append({
                    'item': node_id,
                    'message': e.message,
                    'fix': e.fix
                })
                result.rejected.append(node_id)

                # Emit error event
                _emit_event("node_error", {
                    "id": node_id,
                    "type": node_type,
                    "error": e.message
                })

        # 2. Process links
        for link in data.get('links', []):
            link_type = link.get('type')
            link_id = self._link_id(link)

            try:
                if link_type == 'belief':
                    char_id = link.get('character')
                    narr_id = link.get('narrative')
                    self._validate_link_targets(char_id, narr_id, existing_ids, new_node_ids)
                    linked_ids.add(char_id)
                    linked_ids.add(narr_id)
                    self.add_belief(**self._extract_belief_args(link))

                elif link_type == 'present':
                    char_id = link.get('from')
                    place_id = link.get('to')
                    self._validate_link_targets(char_id, place_id, existing_ids, new_node_ids)
                    linked_ids.add(char_id)
                    linked_ids.add(place_id)
                    self.add_presence(**self._extract_presence_args(link))

                elif link_type in ('carries', 'carries_hidden'):
                    char_id = link.get('from')
                    thing_id = link.get('to')
                    self._validate_link_targets(char_id, thing_id, existing_ids, new_node_ids)
                    linked_ids.add(char_id)
                    linked_ids.add(thing_id)
                    self.add_possession(**self._extract_possession_args(link))

                elif link_type == 'geography':
                    from_id = link.get('from')
                    to_id = link.get('to')
                    self._validate_link_targets(from_id, to_id, existing_ids, new_node_ids)
                    linked_ids.add(from_id)
                    linked_ids.add(to_id)
                    self.add_geography(**self._extract_geography_args(link))

                elif link_type == 'narrative_link':
                    from_id = link.get('from')
                    to_id = link.get('to')
                    self._validate_link_targets(from_id, to_id, existing_ids, new_node_ids)
                    linked_ids.add(from_id)
                    linked_ids.add(to_id)
                    self.add_narrative_link(**self._extract_narrative_link_args(link))

                elif link_type == 'located':
                    thing_id = link.get('from')
                    place_id = link.get('to')
                    self._validate_link_targets(thing_id, place_id, existing_ids, new_node_ids)
                    linked_ids.add(thing_id)
                    linked_ids.add(place_id)
                    self.add_thing_location(**self._extract_thing_location_args(link))

                elif link_type == 'said':
                    char_id = link.get('character')
                    moment_id = link.get('moment')
                    self._validate_link_targets(char_id, moment_id, existing_ids, new_node_ids)
                    linked_ids.add(char_id)
                    linked_ids.add(moment_id)
                    self.add_said(char_id, moment_id)

                elif link_type == 'moment_at':
                    moment_id = link.get('moment')
                    place_id = link.get('place')
                    self._validate_link_targets(moment_id, place_id, existing_ids, new_node_ids)
                    linked_ids.add(moment_id)
                    linked_ids.add(place_id)
                    self.add_moment_at(moment_id, place_id)

                elif link_type == 'moment_then':
                    from_id = link.get('from')
                    to_id = link.get('to')
                    self._validate_link_targets(from_id, to_id, existing_ids, new_node_ids)
                    linked_ids.add(from_id)
                    linked_ids.add(to_id)
                    self.add_moment_then(from_id, to_id)

                elif link_type == 'narrative_from':
                    narr_id = link.get('narrative')
                    moment_id = link.get('moment')
                    self._validate_link_targets(narr_id, moment_id, existing_ids, new_node_ids)
                    linked_ids.add(narr_id)
                    linked_ids.add(moment_id)
                    self.add_narrative_from_moment(narr_id, moment_id)

                elif link_type == 'can_speak':
                    char_id = link.get('character')
                    moment_id = link.get('moment')
                    self._validate_link_targets(char_id, moment_id, existing_ids, new_node_ids)
                    linked_ids.add(char_id)
                    linked_ids.add(moment_id)
                    self.add_can_speak(
                        char_id,
                        moment_id,
                        weight=link.get('weight', 1.0)
                    )

                elif link_type == 'attached_to':
                    moment_id = link.get('moment')
                    target_id = link.get('target')
                    self._validate_link_targets(moment_id, target_id, existing_ids, new_node_ids)
                    linked_ids.add(moment_id)
                    linked_ids.add(target_id)
                    self.add_attached_to(
                        moment_id,
                        target_id,
                        presence_required=link.get('presence_required', False),
                        persistent=link.get('persistent', True),
                        dies_with_target=link.get('dies_with_target', False)
                    )

                elif link_type == 'can_lead_to':
                    from_id = link.get('from')
                    to_id = link.get('to')
                    self._validate_link_targets(from_id, to_id, existing_ids, new_node_ids)
                    linked_ids.add(from_id)
                    linked_ids.add(to_id)
                    self.add_can_lead_to(
                        from_id,
                        to_id,
                        trigger=link.get('trigger', 'player'),
                        weight_transfer=link.get('weight_transfer', 0.3),
                        require_words=link.get('require_words'),
                        bidirectional=link.get('bidirectional', False),
                        wait_ticks=link.get('wait_ticks'),
                        consumes_origin=link.get('consumes_origin', True)
                    )

                else:
                    result.errors.append({
                        'item': link_id,
                        'message': f'Invalid link type: {link_type}',
                        'fix': 'Valid types: belief, present, carries, carries_hidden, located, geography, narrative_link, said, moment_at, moment_then, narrative_from, can_speak, attached_to, can_lead_to'
                    })
                    result.rejected.append(link_id)
                    continue

                result.persisted.append(link_id)

                # Emit link_created event with ALL fields
                _emit_event("link_created", {**link, "_link_id": link_id})

            except WriteError as e:
                result.errors.append({
                    'item': link_id,
                    'message': e.message,
                    'fix': e.fix
                })
                result.rejected.append(link_id)

                # Emit error event
                _emit_event("link_error", {
                    "id": link_id,
                    "type": link_type,
                    "error": e.message
                })

        # 3. Check for orphaned new nodes
        orphaned = new_node_ids - linked_ids - existing_ids
        for node_id in orphaned:
            # Check if it links to existing nodes (not captured above)
            if not self._node_has_links(node_id):
                result.errors.append({
                    'item': node_id,
                    'message': f'{node_id} has no links (orphaned)',
                    'fix': 'Add at least one link connecting this node to the graph'
                })

        # 4. Process updates
        for update in data.get('updates', []):
            try:
                if 'node' in update:
                    self._apply_node_update(update)
                    result.persisted.append(f"update:{update.get('node')}")
                elif 'tension' in update:
                    self._apply_tension_update(update)
                    result.persisted.append(f"update:{update.get('tension')}")
            except WriteError as e:
                result.errors.append({
                    'item': str(update),
                    'message': e.message,
                    'fix': e.fix
                })

        # 5. Process movements
        for move in data.get('movements', []):
            try:
                char_id = move.get('character')
                to_place = move.get('to')
                visible = move.get('visible', True)
                self.move_character(char_id, to_place, 1.0 if visible else 0.0)
                result.persisted.append(f"move:{char_id}->{to_place}")

                # Emit movement event with ALL fields
                _emit_event("movement", move)

            except WriteError as e:
                result.errors.append({
                    'item': f"move:{move.get('character')}",
                    'message': e.message,
                    'fix': e.fix
                })

        # Emit apply_complete event
        _emit_event("apply_complete", {
            "source": path or "direct",
            "persisted_count": len(result.persisted),
            "rejected_count": len(result.rejected),
            "error_count": len(result.errors),
            "duplicate_count": len(result.duplicates),
            "success": result.success
        })

        logger.info(f"[GraphOps] Applied: {len(result.persisted)} persisted, {len(result.rejected)} rejected")
        return result

    def _get_existing_node_ids(self) -> Set[str]:
        """Get all existing node IDs in the graph."""
        try:
            cypher = """
            MATCH (n)
            WHERE n.id IS NOT NULL
            RETURN n.id
            """
            rows = self._query(cypher)
            return {row[0] for row in rows if rows}
        except:
            return set()

    def _node_has_links(self, node_id: str) -> bool:
        """Check if a node has any links."""
        cypher = f"""
        MATCH (n {{id: '{node_id}'}})-[r]-()
        RETURN count(r) > 0
        """
        try:
            rows = self._query(cypher)
            return rows and rows[0][0]
        except:
            return False

    def _validate_link_targets(self, id1: str, id2: str, existing: Set[str], new: Set[str]):
        """Validate that link targets exist."""
        all_ids = existing | new
        if id1 and id1 not in all_ids:
            raise WriteError(
                f"Link references non-existent node: {id1}",
                f"Create the node first, or check the ID spelling.\n"
                f"Existing nodes: {', '.join(sorted(existing)[:10])}..."
            )
        if id2 and id2 not in all_ids:
            raise WriteError(
                f"Link references non-existent node: {id2}",
                f"Create the node first, or check the ID spelling.\n"
                f"Existing nodes: {', '.join(sorted(existing)[:10])}..."
            )

    def _link_id(self, link: Dict) -> str:
        """Generate a readable ID for a link."""
        link_type = link.get('type', 'unknown')
        if link_type == 'belief':
            return f"belief:{link.get('character')}->{link.get('narrative')}"
        elif link_type == 'present':
            return f"present:{link.get('from')}@{link.get('to')}"
        elif link_type in ('carries', 'carries_hidden'):
            return f"{link_type}:{link.get('from')}->{link.get('to')}"
        elif link_type == 'located':
            return f"located:{link.get('from')}@{link.get('to')}"
        elif link_type == 'geography':
            return f"geography:{link.get('from')}->{link.get('to')}"
        elif link_type == 'narrative_link':
            return f"narr_link:{link.get('from')}->{link.get('to')}"
        elif link_type == 'can_speak':
            return f"can_speak:{link.get('character')}->{link.get('moment')}"
        elif link_type == 'attached_to':
            return f"attached:{link.get('moment')}->{link.get('target')}"
        elif link_type == 'can_lead_to':
            return f"can_lead:{link.get('from')}->{link.get('to')}"
        else:
            return f"link:{link_type}"

    # Extraction helpers
    def _extract_character_args(self, node: Dict) -> Dict:
        return {
            'id': node['id'],
            'name': node.get('name', node['id']),
            'type': node.get('character_type', 'minor'),
            'alive': node.get('alive', True),
            'face': node.get('face'),
            'skills': node.get('skills'),
            'voice_tone': node.get('voice_tone') or node.get('voice', {}).get('tone'),
            'voice_style': node.get('voice_style') or node.get('voice', {}).get('style'),
            'approach': node.get('approach') or node.get('personality', {}).get('approach'),
            'values': node.get('values') or node.get('personality', {}).get('values'),
            'flaw': node.get('flaw') or node.get('personality', {}).get('flaw'),
            'backstory_family': node.get('backstory_family') or node.get('backstory', {}).get('family'),
            'backstory_wound': node.get('backstory_wound') or node.get('backstory', {}).get('wound'),
            'backstory_why_here': node.get('backstory_why_here') or node.get('backstory', {}).get('why_here'),
            'image_prompt': node.get('image_prompt'),
        }

    def _extract_place_args(self, node: Dict) -> Dict:
        return {
            'id': node['id'],
            'name': node.get('name', node['id']),
            'type': node.get('place_type', 'village'),
            'mood': node.get('mood') or node.get('atmosphere', {}).get('mood'),
            'weather': node.get('weather') or node.get('atmosphere', {}).get('weather'),
            'details': node.get('details') or node.get('atmosphere', {}).get('details'),
            'image_prompt': node.get('image_prompt'),
        }

    def _extract_thing_args(self, node: Dict) -> Dict:
        return {
            'id': node['id'],
            'name': node.get('name', node['id']),
            'type': node.get('thing_type', 'tool'),
            'portable': node.get('portable', True),
            'significance': node.get('significance', 'mundane'),
            'description': node.get('description'),
            'quantity': node.get('quantity', 1),
            'image_prompt': node.get('image_prompt'),
        }

    def _extract_narrative_args(self, node: Dict) -> Dict:
        about = node.get('about', {})
        return {
            'id': node['id'],
            'name': node.get('name', node['id']),
            'content': node.get('content', ''),
            'type': node.get('narrative_type', node.get('type', 'memory')),
            'interpretation': node.get('interpretation'),
            'about_characters': about.get('characters') or node.get('about_characters'),
            'about_places': about.get('places') or node.get('about_places'),
            'about_things': about.get('things') or node.get('about_things'),
            'about_relationship': about.get('relationship') or node.get('about_relationship'),
            'tone': node.get('tone'),
            'voice_style': node.get('voice_style') or node.get('voice', {}).get('style'),
            'voice_phrases': node.get('voice_phrases') or node.get('voice', {}).get('phrases'),
            'weight': node.get('weight', 0.5),
            'focus': node.get('focus', 1.0),
            'truth': node.get('truth', 1.0),
            'narrator_notes': node.get('narrator_notes'),
        }

    def _extract_tension_args(self, node: Dict) -> Dict:
        return {
            'id': node['id'],
            'narratives': node.get('narratives', []),
            'description': node.get('description', ''),
            'pressure': node.get('pressure', 0.0),
            'pressure_type': node.get('pressure_type', 'gradual'),
            'breaking_point': node.get('breaking_point', 0.9),
            'base_rate': node.get('base_rate', 0.001),
            'trigger_at': node.get('trigger_at'),
            'progression': node.get('progression'),
            'narrator_notes': node.get('narrator_notes'),
        }

    def _extract_moment_args(self, node: Dict) -> Dict:
        return {
            'id': node['id'],
            'text': node.get('text', ''),
            'type': node.get('moment_type', 'narration'),
            'tick': node.get('tick', 0),
            'status': node.get('status', 'spoken'),
            'weight': node.get('weight', 0.5),
            'tone': node.get('tone'),
            'tick_spoken': node.get('tick_spoken'),
            'tick_decayed': node.get('tick_decayed'),
            'speaker': node.get('speaker'),  # Used for SAID link, not stored as attribute
            'place_id': node.get('place_id'),
            'after_moment_id': node.get('after_moment_id'),
            'embedding': node.get('embedding'),
            'line': node.get('line'),
        }

    def _extract_belief_args(self, link: Dict) -> Dict:
        return {
            'character_id': link['character'],
            'narrative_id': link['narrative'],
            'heard': link.get('heard', 0.0),
            'believes': link.get('believes', 0.0),
            'doubts': link.get('doubts', 0.0),
            'denies': link.get('denies', 0.0),
            'hides': link.get('hides', 0.0),
            'spreads': link.get('spreads', 0.0),
            'originated': link.get('originated', 0.0),
            'source': link.get('source', 'none'),
            'from_whom': link.get('from_whom'),
        }

    def _extract_presence_args(self, link: Dict) -> Dict:
        return {
            'character_id': link['from'],
            'place_id': link['to'],
            'present': link.get('present', 1.0),
            'visible': link.get('visible', 1.0),
        }

    def _extract_possession_args(self, link: Dict) -> Dict:
        # carries_hidden as link type sets carries_hidden=1.0
        is_hidden = link.get('type') == 'carries_hidden'
        return {
            'character_id': link['from'],
            'thing_id': link['to'],
            'carries': link.get('carries', 1.0),
            'carries_hidden': 1.0 if is_hidden else link.get('carries_hidden', 0.0),
        }

    def _extract_geography_args(self, link: Dict) -> Dict:
        return {
            'from_place_id': link['from'],
            'to_place_id': link['to'],
            'contains': link.get('contains', 0.0),
            'path': link.get('path', 0.0),
            'path_distance': link.get('path_distance'),
            'path_difficulty': link.get('path_difficulty', 'moderate'),
            'borders': link.get('borders', 0.0),
        }

    def _extract_narrative_link_args(self, link: Dict) -> Dict:
        return {
            'source_id': link['from'],
            'target_id': link['to'],
            'contradicts': link.get('contradicts', 0.0),
            'supports': link.get('supports', 0.0),
            'elaborates': link.get('elaborates', 0.0),
            'subsumes': link.get('subsumes', 0.0),
            'supersedes': link.get('supersedes', 0.0),
        }

    def _extract_thing_location_args(self, link: Dict) -> Dict:
        return {
            'thing_id': link['from'],
            'place_id': link['to'],
            'located': link.get('located', 1.0),
            'hidden': link.get('hidden', 0.0),
            'specific_location': link.get('specific_location'),
        }

    def _apply_node_update(self, update: Dict):
        """Apply an update to a node."""
        node_id = update['node']

        if 'modifier_add' in update:
            mod = update['modifier_add']
            cypher = f"""
            MATCH (n {{id: '{node_id}'}})
            SET n.modifiers = COALESCE(n.modifiers, '[]')
            """
            self._query(cypher)
            # TODO: Proper modifier handling

        # Add other update types as needed

    def _apply_tension_update(self, update: Dict):
        """Apply an update to a tension."""
        tension_id = update['tension']
        props = {}

        if 'pressure' in update:
            props['pressure'] = update['pressure']
        if 'resolved' in update:
            props['resolved'] = update['resolved']

        if props:
            props_str = ', '.join(f"t.{k} = {repr(v)}" for k, v in props.items())
            cypher = f"""
            MATCH (t:Tension {{id: '{tension_id}'}})
            SET {props_str}
            """
            self._query(cypher)

    # =========================================================================
    # NODES
    # =========================================================================

    def add_character(
        self,
        id: str,
        name: str,
        type: str = "minor",
        alive: bool = True,
        gender: str = None,
        face: str = None,
        skills: Dict[str, str] = None,
        voice_tone: str = None,
        voice_style: str = None,
        approach: str = None,
        values: List[str] = None,
        flaw: str = None,
        backstory_family: str = None,
        backstory_wound: str = None,
        backstory_why_here: str = None,
        embedding: List[float] = None,
        image_prompt: str = None,
        playthrough: str = None,
        detail: str = None
    ) -> None:
        """
        Add or update a CHARACTER node.

        Args:
            id: Unique identifier (e.g., "char_aldric")
            name: Display name (e.g., "Aldric")
            type: player, companion, major, minor, background
            alive: Is the character alive?
            face: young, scarred, weathered, gaunt, hard, noble
            skills: Dict of skill -> level (untrained, capable, skilled, master)
            voice_tone: quiet, sharp, warm, bitter, measured, fierce
            voice_style: direct, questioning, sardonic, gentle, blunt
            approach: direct, cunning, cautious, impulsive, deliberate
            values: List of values (loyalty, survival, honor, etc.)
            flaw: pride, fear, greed, wrath, doubt, rigidity, softness, envy, sloth
            backstory_*: Backstory fields
            embedding: 768-dim vector for semantic search
            image_prompt: Prompt for generating character portrait (1:1 aspect ratio)
            playthrough: Playthrough folder name for image storage
        """
        # Determine playthrough from parameter or stored value
        pt = playthrough or getattr(self, '_current_playthrough', 'default')

        props = {
            "id": id,
            "name": name,
            "type": type,
            "alive": alive,
            "created_at": datetime.utcnow().isoformat()
        }

        if gender:
            props["gender"] = gender
        if face:
            props["face"] = face
        if skills:
            props["skills"] = json.dumps(skills)
        if voice_tone:
            props["voice_tone"] = voice_tone
        if voice_style:
            props["voice_style"] = voice_style
        if approach:
            props["approach"] = approach
        if values:
            props["values"] = json.dumps(values)
        if flaw:
            props["flaw"] = flaw
        if backstory_family:
            props["backstory_family"] = backstory_family
        if backstory_wound:
            props["backstory_wound"] = backstory_wound
        if backstory_why_here:
            props["backstory_why_here"] = backstory_why_here
        if embedding:
            props["embedding"] = embedding
        if image_prompt:
            props["image_prompt"] = image_prompt
        if detail:
            props["detail"] = detail

        # Generate image if prompt provided
        if image_prompt:
            image_path = _generate_node_image('character', id, image_prompt, pt)
            if image_path:
                props["image_path"] = image_path

        cypher = """
        MERGE (n:Character {id: $id})
        SET n += $props
        """
        self._query(cypher, {"id": id, "props": props})
        logger.info(f"[GraphOps] Added character: {name} ({id})")

    def add_place(
        self,
        id: str,
        name: str,
        type: str = "village",
        mood: str = None,
        weather: List[str] = None,
        details: List[str] = None,
        embedding: List[float] = None,
        image_prompt: str = None,
        playthrough: str = None,
        detail: str = None
    ) -> None:
        """
        Add or update a PLACE node.

        Args:
            id: Unique identifier (e.g., "place_york")
            name: Display name (e.g., "York")
            type: region, city, hold, village, monastery, camp, road, room, wilderness, ruin
            mood: welcoming, hostile, indifferent, fearful, watchful, desperate, peaceful, tense
            weather: List of weather conditions
            details: List of atmospheric details
            embedding: 768-dim vector for semantic search
            image_prompt: Prompt for generating place illustration (1:3 aspect ratio)
            playthrough: Playthrough folder name for image storage
        """
        # Determine playthrough from parameter or stored value
        pt = playthrough or getattr(self, '_current_playthrough', 'default')

        props = {
            "id": id,
            "name": name,
            "type": type,
            "created_at": datetime.utcnow().isoformat()
        }

        if mood:
            props["mood"] = mood
        if weather:
            props["weather"] = json.dumps(weather)
        if details:
            props["details"] = json.dumps(details)
        if embedding:
            props["embedding"] = embedding
        if image_prompt:
            props["image_prompt"] = image_prompt
        if detail:
            props["detail"] = detail

        # Generate image if prompt provided
        if image_prompt:
            image_path = _generate_node_image('place', id, image_prompt, pt)
            if image_path:
                props["image_path"] = image_path

        cypher = """
        MERGE (n:Place {id: $id})
        SET n += $props
        """
        self._query(cypher, {"id": id, "props": props})
        logger.info(f"[GraphOps] Added place: {name} ({id})")

    def add_thing(
        self,
        id: str,
        name: str,
        type: str = "tool",
        portable: bool = True,
        significance: str = "mundane",
        description: str = None,
        quantity: int = 1,
        embedding: List[float] = None,
        image_prompt: str = None,
        playthrough: str = None,
        detail: str = None
    ) -> None:
        """
        Add or update a THING node.

        Args:
            id: Unique identifier (e.g., "thing_sword")
            name: Display name (e.g., "Wulfric's Sword")
            type: weapon, armor, document, letter, relic, treasure, title, land, token, provisions, coin_purse, horse, ship, tool
            portable: Can it be carried?
            significance: mundane, personal, political, sacred, legendary
            description: What it is
            quantity: How many
            embedding: 768-dim vector for semantic search
            image_prompt: Prompt for generating thing illustration (1:1 aspect ratio)
            playthrough: Playthrough folder name for image storage
        """
        # Determine playthrough from parameter or stored value
        pt = playthrough or getattr(self, '_current_playthrough', 'default')

        props = {
            "id": id,
            "name": name,
            "type": type,
            "portable": portable,
            "significance": significance,
            "quantity": quantity,
            "created_at": datetime.utcnow().isoformat()
        }

        if description:
            props["description"] = description
        if embedding:
            props["embedding"] = embedding
        if image_prompt:
            props["image_prompt"] = image_prompt
        if detail:
            props["detail"] = detail

        # Generate image if prompt provided
        if image_prompt:
            image_path = _generate_node_image('thing', id, image_prompt, pt)
            if image_path:
                props["image_path"] = image_path

        cypher = """
        MERGE (n:Thing {id: $id})
        SET n += $props
        """
        self._query(cypher, {"id": id, "props": props})
        logger.info(f"[GraphOps] Added thing: {name} ({id})")

    def add_narrative(
        self,
        id: str,
        name: str,
        content: str,
        type: str,
        interpretation: str = None,
        about_characters: List[str] = None,
        about_places: List[str] = None,
        about_things: List[str] = None,
        about_relationship: List[str] = None,
        tone: str = None,
        voice_style: str = None,
        voice_phrases: List[str] = None,
        weight: float = 0.5,
        focus: float = 1.0,
        truth: float = 1.0,
        narrator_notes: str = None,
        embedding: List[float] = None,
        occurred_at: str = None,
        occurred_where: str = None,
        detail: str = None
    ) -> None:
        """
        Add or update a NARRATIVE node.

        Args:
            id: Unique identifier (e.g., "narr_oath")
            name: Short label (e.g., "Aldric's Oath")
            content: The story itself
            type: memory, account, rumor, reputation, identity, bond, oath, debt, blood, enmity, love, service, ownership, claim, control, origin, belief, prophecy, lie, secret
            interpretation: What it means (emotional/thematic weight)
            about_characters: Character IDs this is about
            about_places: Place IDs this is about
            about_things: Thing IDs this is about
            about_relationship: Pair of character IDs (for bond/enmity types)
            tone: bitter, proud, shameful, defiant, mournful, cold, righteous, hopeful, fearful, warm, dark, sacred
            voice_style: whisper, demand, remind, accuse, plead, warn, inspire, mock, question
            voice_phrases: Example lines this narrative might say
            weight: 0-1, computed importance (usually set by graph engine)
            focus: 0.1-3.0, pacing multiplier
            truth: 0-1, how true (director only)
            narrator_notes: Continuity notes
            embedding: 768-dim vector for semantic search
        """
        props = {
            "id": id,
            "name": name,
            "content": content,
            "type": type,
            "weight": weight,
            "focus": focus,
            "truth": truth,
            "created_at": datetime.utcnow().isoformat()
        }

        if interpretation:
            props["interpretation"] = interpretation
        if about_characters:
            props["about_characters"] = json.dumps(about_characters)
        if about_places:
            props["about_places"] = json.dumps(about_places)
        if about_things:
            props["about_things"] = json.dumps(about_things)
        if about_relationship:
            props["about_relationship"] = json.dumps(about_relationship)
        if tone:
            props["tone"] = tone
        if voice_style:
            props["voice_style"] = voice_style
        if voice_phrases:
            props["voice_phrases"] = json.dumps(voice_phrases)
        if narrator_notes:
            props["narrator_notes"] = narrator_notes
        if embedding:
            props["embedding"] = embedding
        if occurred_at:
            props["occurred_at"] = occurred_at
        if detail:
            props["detail"] = detail

        cypher = """
        MERGE (n:Narrative {id: $id})
        SET n += $props
        """
        self._query(cypher, {"id": id, "props": props})

        # Create OCCURRED_AT link to Place if specified
        if occurred_where:
            link_cypher = """
            MATCH (n:Narrative {id: $narr_id})
            MATCH (p:Place {id: $place_id})
            MERGE (n)-[:OCCURRED_AT]->(p)
            """
            self._query(link_cypher, {"narr_id": id, "place_id": occurred_where})

        logger.info(f"[GraphOps] Added narrative: {name} ({id})")

    def add_tension(
        self,
        id: str,
        narratives: List[str],
        description: str,
        pressure: float = 0.0,
        pressure_type: str = "gradual",
        breaking_point: float = 0.9,
        base_rate: float = 0.001,
        trigger_at: str = None,
        progression: List[Dict] = None,
        narrator_notes: str = None,
        detail: str = None
    ) -> None:
        """
        Add or update a TENSION node.

        Args:
            id: Unique identifier (e.g., "tension_confrontation")
            narratives: List of narrative IDs in tension
            description: What this tension is about
            pressure: Current pressure level (0-1)
            pressure_type: gradual, scheduled, hybrid
            breaking_point: When it breaks (usually 0.9)
            base_rate: Pressure increase per minute (for gradual)
            trigger_at: When it must break (for scheduled)
            progression: Timeline steps (for scheduled/hybrid)
            narrator_notes: How to handle the break
        """
        props = {
            "id": id,
            "narratives": json.dumps(narratives),
            "description": description,
            "pressure": pressure,
            "pressure_type": pressure_type,
            "breaking_point": breaking_point,
            "base_rate": base_rate,
            "created_at": datetime.utcnow().isoformat()
        }

        if trigger_at:
            props["trigger_at"] = trigger_at
        if progression:
            props["progression"] = json.dumps(progression)
        if narrator_notes:
            props["narrator_notes"] = narrator_notes
        if detail:
            props["detail"] = detail

        cypher = """
        MERGE (n:Tension {id: $id})
        SET n += $props
        """
        self._query(cypher, {"id": id, "props": props})
        logger.info(f"[GraphOps] Added tension: {id}")

    def add_moment(
        self,
        id: str,
        text: str,
        type: str = "narration",
        tick: int = 0,
        status: str = "spoken",
        weight: float = 0.5,
        tone: str = None,
        tick_spoken: int = None,
        tick_decayed: int = None,
        speaker: str = None,
        place_id: str = None,
        after_moment_id: str = None,
        embedding: List[float] = None,
        line: int = None
    ) -> str:
        """
        Add or update a MOMENT node.

        A Moment is a single unit of narrated content - dialogue, narration,
        hint, or player action. Every piece of text shown to the player
        becomes a Moment for traceability and semantic search.

        Moments follow a lifecycle:
        - possible: Could surface but hasn't yet (weight determines priority)
        - active: Currently being shown/spoken
        - spoken: Has been shown, part of history
        - dormant: Old, but can reactivate (e.g., return to location)
        - decayed: Archived, no longer in active graph

        Args:
            id: Unique identifier (e.g., "crossing_d5_dusk_dialogue_143521")
            text: The actual text content
            type: narration, dialogue, hint, player_click, player_freeform, player_choice
            tick: World tick when this was created
            status: possible, active, spoken, dormant, decayed
            weight: 0-1, determines surfacing priority for possible moments
            tone: curious, defiant, vulnerable, warm, cold, bitter, etc.
            tick_spoken: World tick when moment was spoken (null if not yet)
            tick_decayed: World tick when moment decayed (null if not yet)
            speaker: Character ID - creates SAID link (not stored as attribute)
            place_id: Where it occurred (creates AT link)
            after_moment_id: Previous moment (creates THEN link for sequence)
            embedding: 768-dim vector for semantic search
            line: Starting line number in transcript.json

        Returns:
            The moment ID
        """
        props = {
            "id": id,
            "text": text,
            "type": type,
            "tick": tick,
            "status": status,
            "weight": weight,
            "created_at": datetime.utcnow().isoformat()
        }

        if tone:
            props["tone"] = tone
        if tick_spoken is not None:
            props["tick_spoken"] = tick_spoken
        if tick_decayed is not None:
            props["tick_decayed"] = tick_decayed
        if embedding:
            props["embedding"] = embedding
        if line is not None:
            props["line"] = line

        cypher = """
        MERGE (n:Moment {id: $id})
        SET n += $props
        """
        self._query(cypher, {"id": id, "props": props})

        # Create SAID link if speaker (dialogue or player action)
        if speaker:
            self.add_said(speaker, id)

        # Create AT link if place specified
        if place_id:
            self.add_moment_at(id, place_id)

        # Create THEN link if after_moment specified (sequence)
        if after_moment_id:
            self.add_moment_then(after_moment_id, id)

        logger.info(f"[GraphOps] Added moment: {id} ({type}, status={status})")
        return id

    # =========================================================================
    # LINKS
    # =========================================================================

    def add_said(
        self,
        character_id: str,
        moment_id: str
    ) -> None:
        """
        Add SAID link from Character to Moment.

        Used for dialogue and player actions to track who said/did what.
        """
        cypher = """
        MATCH (c:Character {id: $char_id})
        MATCH (m:Moment {id: $moment_id})
        MERGE (c)-[r:SAID]->(m)
        """
        self._query(cypher, {
            "char_id": character_id,
            "moment_id": moment_id
        })
        logger.debug(f"[GraphOps] Added said: {character_id} -> {moment_id}")

    def add_moment_at(
        self,
        moment_id: str,
        place_id: str
    ) -> None:
        """
        Add AT link from Moment to Place.

        Records where a moment occurred.
        """
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        MATCH (p:Place {id: $place_id})
        MERGE (m)-[r:AT]->(p)
        """
        self._query(cypher, {
            "moment_id": moment_id,
            "place_id": place_id
        })
        logger.debug(f"[GraphOps] Added moment at: {moment_id} @ {place_id}")

    def add_moment_then(
        self,
        from_moment_id: str,
        to_moment_id: str
    ) -> None:
        """
        Add THEN link between Moments.

        Records sequence within a scene.
        """
        cypher = """
        MATCH (m1:Moment {id: $from_id})
        MATCH (m2:Moment {id: $to_id})
        MERGE (m1)-[r:THEN]->(m2)
        """
        self._query(cypher, {
            "from_id": from_moment_id,
            "to_id": to_moment_id
        })
        logger.debug(f"[GraphOps] Added sequence: {from_moment_id} -> {to_moment_id}")

    def add_narrative_from_moment(
        self,
        narrative_id: str,
        moment_id: str
    ) -> None:
        """
        Add FROM link from Narrative to Moment.

        Source attribution - which moments created this narrative.
        """
        cypher = """
        MATCH (n:Narrative {id: $narr_id})
        MATCH (m:Moment {id: $moment_id})
        MERGE (n)-[r:FROM]->(m)
        """
        self._query(cypher, {
            "narr_id": narrative_id,
            "moment_id": moment_id
        })
        logger.debug(f"[GraphOps] Added narrative source: {narrative_id} <- {moment_id}")

    def add_can_speak(
        self,
        character_id: str,
        moment_id: str,
        weight: float = 1.0
    ) -> None:
        """
        Add CAN_SPEAK link from Character to Moment.

        Indicates which characters can speak a potential moment.
        Used for dialogue routing - when a moment surfaces, find who CAN_SPEAK it.

        Args:
            character_id: Character who can speak this moment
            moment_id: The potential moment
            weight: How likely this character would speak it (default 1.0)
        """
        cypher = """
        MATCH (c:Character {id: $char_id})
        MATCH (m:Moment {id: $moment_id})
        MERGE (c)-[r:CAN_SPEAK]->(m)
        SET r.weight = $weight
        """
        self._query(cypher, {
            "char_id": character_id,
            "moment_id": moment_id,
            "weight": weight
        })
        logger.debug(f"[GraphOps] Added can_speak: {character_id} -> {moment_id}")

    def add_attached_to(
        self,
        moment_id: str,
        target_id: str,
        presence_required: bool = False,
        persistent: bool = True,
        dies_with_target: bool = False
    ) -> None:
        """
        Add ATTACHED_TO link from Moment to any target node.

        Moments are attached to places, characters, narratives, things.
        This determines when moments surface based on context.

        Args:
            moment_id: The moment being attached
            target_id: What it's attached to (character, place, narrative, thing)
            presence_required: If true, moment only surfaces when target is present
            persistent: If true, goes dormant when target leaves, reactivates on return
                        If false, deleted when target leaves
            dies_with_target: If true, moment deleted if target is destroyed
        """
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        MATCH (t {id: $target_id})
        MERGE (m)-[r:ATTACHED_TO]->(t)
        SET r.presence_required = $presence_required,
            r.persistent = $persistent,
            r.dies_with_target = $dies_with_target
        """
        self._query(cypher, {
            "moment_id": moment_id,
            "target_id": target_id,
            "presence_required": presence_required,
            "persistent": persistent,
            "dies_with_target": dies_with_target
        })
        logger.debug(f"[GraphOps] Added attached_to: {moment_id} -> {target_id}")

    def add_can_lead_to(
        self,
        from_moment_id: str,
        to_moment_id: str,
        trigger: str = "player",
        weight_transfer: float = 0.3,
        require_words: List[str] = None,
        bidirectional: bool = False,
        wait_ticks: int = None,
        consumes_origin: bool = True
    ) -> None:
        """
        Add CAN_LEAD_TO link between Moments.

        The core of dialogue flow. When from_moment is active/spoken,
        to_moment becomes possible based on trigger conditions.

        Args:
            from_moment_id: The source moment
            to_moment_id: The target moment that can follow
            trigger: How the transition happens:
                - "player": Player click/input activates (default)
                - "auto": Automatic when from_moment spoken
                - "wait": Auto-fires after wait_ticks of silence
            weight_transfer: How much weight flows from source to target
            require_words: Words that must appear in player input to trigger
            bidirectional: If true, create link in both directions
            wait_ticks: For trigger="wait", how many ticks of silence before firing
            consumes_origin: If true, origin status → spoken after traversal
                             If false, origin stays active
        """
        props = {
            "trigger": trigger,
            "weight_transfer": weight_transfer,
            "consumes_origin": consumes_origin
        }

        if require_words:
            props["require_words"] = json.dumps(require_words)
        if wait_ticks is not None:
            props["wait_ticks"] = wait_ticks

        cypher = """
        MATCH (m1:Moment {id: $from_id})
        MATCH (m2:Moment {id: $to_id})
        MERGE (m1)-[r:CAN_LEAD_TO]->(m2)
        SET r += $props
        """
        self._query(cypher, {
            "from_id": from_moment_id,
            "to_id": to_moment_id,
            "props": props
        })
        logger.debug(f"[GraphOps] Added can_lead_to: {from_moment_id} -> {to_moment_id}")

        # Create reverse link if bidirectional
        if bidirectional:
            cypher_reverse = """
            MATCH (m1:Moment {id: $from_id})
            MATCH (m2:Moment {id: $to_id})
            MERGE (m2)-[r:CAN_LEAD_TO]->(m1)
            SET r += $props
            """
            self._query(cypher_reverse, {
                "from_id": from_moment_id,
                "to_id": to_moment_id,
                "props": props
            })
            logger.debug(f"[GraphOps] Added bidirectional: {to_moment_id} -> {from_moment_id}")

    # =========================================================================
    # CLICK HANDLER (Moment Graph Architecture)
    # =========================================================================

    def handle_click(
        self,
        moment_id: str,
        clicked_word: str,
        player_id: str
    ) -> Dict[str, Any]:
        """
        Handle a player click on a word in a moment.

        This is the core instant-response mechanism. Target: <50ms.
        No LLM calls in this path.

        Args:
            moment_id: The moment containing the clicked word
            clicked_word: The word that was clicked
            player_id: The player character ID

        Returns:
            Dict with:
                - flipped: bool - whether any moments crossed threshold
                - flipped_moments: List of moment dicts that flipped to active
                - weight_updates: List of moments that had weight increased
                - queue_narrator: bool - whether to fall back to narrator

        Mechanism:
            1. Find CAN_LEAD_TO links from moment where clicked_word is in require_words
            2. Apply weight_transfer to target moments
            3. Check for flips (weight > 0.8)
            4. Return flipped moments (or empty + queue_narrator if none flip)
        """
        # Find matching transitions
        cypher_find = """
        MATCH (m:Moment {id: $moment_id})-[r:CAN_LEAD_TO]->(target:Moment)
        WHERE r.trigger = 'player'
          AND r.require_words IS NOT NULL
        RETURN target.id, target.text, target.type, target.status, target.weight,
               r.require_words, r.weight_transfer, r.consumes_origin
        """

        rows = self._query(cypher_find, {"moment_id": moment_id})

        if not rows:
            return {
                "flipped": False,
                "flipped_moments": [],
                "weight_updates": [],
                "queue_narrator": True
            }

        # Check which transitions match the clicked word
        matching_targets = []
        for row in rows:
            target_id, target_text, target_type, target_status, target_weight, \
                require_words, weight_transfer, consumes_origin = row

            # Parse require_words if it's a JSON string
            if isinstance(require_words, str):
                require_words = json.loads(require_words)

            # Check if clicked word matches any require_words
            clicked_lower = clicked_word.lower()
            if any(word.lower() == clicked_lower for word in (require_words or [])):
                matching_targets.append({
                    "id": target_id,
                    "text": target_text,
                    "type": target_type,
                    "status": target_status,
                    "weight": target_weight or 0.5,
                    "weight_transfer": weight_transfer or 0.3,
                    "consumes_origin": consumes_origin if consumes_origin is not None else True
                })

        if not matching_targets:
            return {
                "flipped": False,
                "flipped_moments": [],
                "weight_updates": [],
                "queue_narrator": True
            }

        # Apply weight transfers
        weight_updates = []
        flipped_moments = []

        for target in matching_targets:
            new_weight = target["weight"] + target["weight_transfer"]
            new_weight = min(new_weight, 1.0)  # Cap at 1.0

            # Update the weight
            cypher_update = """
            MATCH (m:Moment {id: $target_id})
            SET m.weight = $new_weight
            """
            self._query(cypher_update, {
                "target_id": target["id"],
                "new_weight": new_weight
            })

            weight_updates.append({
                "id": target["id"],
                "old_weight": target["weight"],
                "new_weight": new_weight
            })

            # Check for flip (threshold: 0.8)
            if new_weight >= 0.8:
                # Flip to active
                current_tick = self._get_current_tick()
                cypher_flip = """
                MATCH (m:Moment {id: $target_id})
                SET m.status = 'active',
                    m.tick_spoken = $tick
                """
                self._query(cypher_flip, {
                    "target_id": target["id"],
                    "tick": current_tick
                })

                flipped_moments.append({
                    "id": target["id"],
                    "text": target["text"],
                    "type": target["type"],
                    "weight": new_weight
                })

                logger.info(f"[GraphOps] Moment flipped: {target['id']} (weight={new_weight})")

        # If consumes_origin and we had flips, mark source as spoken
        if flipped_moments and matching_targets[0].get("consumes_origin"):
            current_tick = self._get_current_tick()
            cypher_consume = """
            MATCH (m:Moment {id: $moment_id})
            SET m.status = 'spoken',
                m.tick_spoken = $tick
            """
            self._query(cypher_consume, {
                "moment_id": moment_id,
                "tick": current_tick
            })

        return {
            "flipped": len(flipped_moments) > 0,
            "flipped_moments": flipped_moments,
            "weight_updates": weight_updates,
            "queue_narrator": len(flipped_moments) == 0
        }

    def update_moment_weight(
        self,
        moment_id: str,
        weight_delta: float,
        reason: str = "manual"
    ) -> Dict[str, Any]:
        """
        Update a moment's weight by a delta amount.

        Args:
            moment_id: The moment to update
            weight_delta: Amount to add (positive) or subtract (negative)
            reason: Why the update is happening (for logging)

        Returns:
            Dict with old_weight, new_weight, and flipped status
        """
        # Get current weight
        cypher_get = """
        MATCH (m:Moment {id: $moment_id})
        RETURN m.weight, m.status
        """
        rows = self._query(cypher_get, {"moment_id": moment_id})

        if not rows:
            return {"error": f"Moment not found: {moment_id}"}

        old_weight = rows[0][0] or 0.5
        old_status = rows[0][1] or "possible"
        new_weight = max(0.0, min(1.0, old_weight + weight_delta))

        # Update weight
        cypher_update = """
        MATCH (m:Moment {id: $moment_id})
        SET m.weight = $new_weight
        """
        self._query(cypher_update, {
            "moment_id": moment_id,
            "new_weight": new_weight
        })

        # Check for flip
        flipped = False
        if old_status == "possible" and new_weight >= 0.8:
            current_tick = self._get_current_tick()
            cypher_flip = """
            MATCH (m:Moment {id: $moment_id})
            SET m.status = 'active',
                m.tick_spoken = $tick
            """
            self._query(cypher_flip, {
                "moment_id": moment_id,
                "tick": current_tick
            })
            flipped = True
            logger.info(f"[GraphOps] Moment flipped by {reason}: {moment_id}")

        return {
            "moment_id": moment_id,
            "old_weight": old_weight,
            "new_weight": new_weight,
            "flipped": flipped,
            "reason": reason
        }

    def propagate_embedding_energy(
        self,
        moment_id: str,
        base_boost: float = 0.1
    ) -> List[Dict[str, Any]]:
        """
        Propagate energy to semantically similar moments.

        When a moment is activated, nearby moments in embedding space
        also get a small boost. This creates associative conversation flow.

        Args:
            moment_id: The activated moment
            base_boost: Base amount to boost similar moments

        Returns:
            List of moments that received boosts
        """
        # Get the moment's embedding
        cypher_get = """
        MATCH (m:Moment {id: $moment_id})
        RETURN m.embedding
        """
        rows = self._query(cypher_get, {"moment_id": moment_id})

        if not rows or not rows[0][0]:
            return []

        source_embedding = rows[0][0]
        if isinstance(source_embedding, str):
            source_embedding = json.loads(source_embedding)

        # Find neighbors with embeddings (via CAN_LEAD_TO links first)
        cypher_neighbors = """
        MATCH (m:Moment {id: $moment_id})-[:CAN_LEAD_TO]-(neighbor:Moment)
        WHERE neighbor.status IN ['possible', 'dormant']
          AND neighbor.embedding IS NOT NULL
        RETURN neighbor.id, neighbor.weight, neighbor.embedding
        """
        rows = self._query(cypher_neighbors, {"moment_id": moment_id})

        import numpy as np
        source_vec = np.array(source_embedding)
        source_norm = np.linalg.norm(source_vec)

        boosted = []
        for row in rows:
            neighbor_id, neighbor_weight, neighbor_embedding = row

            if isinstance(neighbor_embedding, str):
                neighbor_embedding = json.loads(neighbor_embedding)

            neighbor_vec = np.array(neighbor_embedding)
            neighbor_norm = np.linalg.norm(neighbor_vec)

            if source_norm > 0 and neighbor_norm > 0:
                similarity = float(np.dot(source_vec, neighbor_vec) / (source_norm * neighbor_norm))

                if similarity > 0.7:  # Only boost if fairly similar
                    boost = base_boost * similarity
                    new_weight = min(1.0, (neighbor_weight or 0.5) + boost)

                    cypher_boost = """
                    MATCH (m:Moment {id: $neighbor_id})
                    SET m.weight = $new_weight
                    """
                    self._query(cypher_boost, {
                        "neighbor_id": neighbor_id,
                        "new_weight": new_weight
                    })

                    boosted.append({
                        "id": neighbor_id,
                        "similarity": similarity,
                        "boost": boost,
                        "new_weight": new_weight
                    })

        return boosted

    def _get_current_tick(self) -> int:
        """Get the current world tick (placeholder - should come from game state)."""
        # In production, this would query the playthrough state
        # For now, return a timestamp-based value
        from datetime import datetime
        return int(datetime.utcnow().timestamp())

    # =========================================================================
    # MOMENT LIFECYCLE METHODS (Phase 5)
    # Ref: docs/engine/moments/ALGORITHM_Lifecycle.md
    # =========================================================================

    def decay_moments(
        self,
        decay_rate: float = 0.99,
        decay_threshold: float = 0.1,
        current_tick: int = None
    ) -> Dict[str, Any]:
        """
        Apply weight decay to possible moments, mark as decayed below threshold.

        Called every world tick (5 minutes). Possible moments gradually lose
        weight. When weight drops below threshold, they become decayed and
        are no longer candidates for activation.

        Args:
            decay_rate: Multiplier per tick (0.99 = 1% decay)
            decay_threshold: Weight below which moment decays (default 0.1)
            current_tick: Current world tick (for tick_decayed)

        Returns:
            Dict with counts: {decayed_count, updated_count}

        Ref: ALGORITHM_Lifecycle.md § Weight Decay
        """
        if current_tick is None:
            current_tick = self._get_current_tick()

        # Apply decay to all possible moments
        decay_cypher = """
        MATCH (m:Moment)
        WHERE m.status = 'possible'
        SET m.weight = m.weight * $decay_rate
        RETURN count(m)
        """
        result = self._query(decay_cypher, {"decay_rate": decay_rate})
        updated_count = result[0][0] if result and result[0] else 0

        # Mark below-threshold moments as decayed
        decayed_cypher = """
        MATCH (m:Moment)
        WHERE m.status = 'possible' AND m.weight < $threshold
        SET m.status = 'decayed', m.tick_decayed = $tick
        RETURN count(m)
        """
        result = self._query(decayed_cypher, {
            "threshold": decay_threshold,
            "tick": current_tick
        })
        decayed_count = result[0][0] if result and result[0] else 0

        if decayed_count > 0:
            logger.info(f"[GraphOps] Decay: {updated_count} updated, {decayed_count} decayed")

        return {
            "updated_count": updated_count,
            "decayed_count": decayed_count
        }

    def on_player_leaves_location(
        self,
        location_id: str,
        player_id: str = "char_player"
    ) -> Dict[str, Any]:
        """
        Handle moment state when player leaves a location.

        - Persistent moments → dormant (can reactivate on return)
        - Non-persistent moments → deleted

        Called when player moves to a new location.

        Args:
            location_id: The place ID being left
            player_id: Player character ID

        Returns:
            Dict with counts: {dormant_count, deleted_count}

        Ref: ALGORITHM_Lifecycle.md § Dormancy
        """
        # Mark persistent moments as dormant
        dormant_cypher = """
        MATCH (m:Moment)-[a:ATTACHED_TO]->(p:Place {id: $location_id})
        WHERE a.persistent = true AND m.status IN ['possible', 'active']
        SET m.status = 'dormant'
        RETURN count(m)
        """
        result = self._query(dormant_cypher, {"location_id": location_id})
        dormant_count = result[0][0] if result and result[0] else 0

        # Delete non-persistent moments attached to this location
        delete_cypher = """
        MATCH (m:Moment)-[a:ATTACHED_TO]->(p:Place {id: $location_id})
        WHERE a.persistent = false AND m.status IN ['possible', 'active']
        DETACH DELETE m
        RETURN count(m)
        """
        result = self._query(delete_cypher, {"location_id": location_id})
        deleted_count = result[0][0] if result and result[0] else 0

        logger.info(f"[GraphOps] Player left {location_id}: {dormant_count} dormant, {deleted_count} deleted")

        return {
            "dormant_count": dormant_count,
            "deleted_count": deleted_count
        }

    def on_player_arrives_location(
        self,
        location_id: str,
        player_id: str = "char_player"
    ) -> Dict[str, Any]:
        """
        Handle moment reactivation when player arrives at a location.

        Dormant moments attached to this location become possible again.

        Args:
            location_id: The place ID being entered
            player_id: Player character ID

        Returns:
            Dict with counts: {reactivated_count}

        Ref: ALGORITHM_Lifecycle.md § Reactivation
        """
        reactivate_cypher = """
        MATCH (m:Moment)-[a:ATTACHED_TO]->(p:Place {id: $location_id})
        WHERE m.status = 'dormant'
        SET m.status = 'possible'
        RETURN count(m)
        """
        result = self._query(reactivate_cypher, {"location_id": location_id})
        reactivated_count = result[0][0] if result and result[0] else 0

        if reactivated_count > 0:
            logger.info(f"[GraphOps] Player arrived {location_id}: {reactivated_count} reactivated")

        return {
            "reactivated_count": reactivated_count
        }

    def garbage_collect_moments(
        self,
        current_tick: int,
        retention_ticks: int = 100
    ) -> Dict[str, Any]:
        """
        Remove old decayed moments to prevent graph bloat.

        Called periodically (e.g., every 10 ticks or on game save).

        Args:
            current_tick: Current world tick
            retention_ticks: How long to keep decayed moments (default 100)

        Returns:
            Dict with counts: {deleted_count}

        Ref: ALGORITHM_Lifecycle.md § Garbage Collection
        """
        threshold_tick = current_tick - retention_ticks

        gc_cypher = """
        MATCH (m:Moment)
        WHERE m.status = 'decayed' AND m.tick_decayed < $threshold
        DETACH DELETE m
        RETURN count(m)
        """
        result = self._query(gc_cypher, {"threshold": threshold_tick})
        deleted_count = result[0][0] if result and result[0] else 0

        if deleted_count > 0:
            logger.info(f"[GraphOps] GC: {deleted_count} old decayed moments removed")

        return {
            "deleted_count": deleted_count
        }

    def boost_moment_weight(
        self,
        moment_id: str,
        boost: float,
        current_tick: int = None
    ) -> Dict[str, Any]:
        """
        Add weight to a moment, checking for flip to active.

        Used for external events that should surface moments
        (e.g., NPC initiates conversation).

        Args:
            moment_id: The moment to boost
            boost: Weight to add (0-1)
            current_tick: Current tick for tick_spoken if flipped

        Returns:
            Dict with {new_weight, flipped, status}

        Ref: ALGORITHM_Transitions.md § External Activation
        """
        if current_tick is None:
            current_tick = self._get_current_tick()

        flip_threshold = 0.8

        # Get current weight
        get_cypher = """
        MATCH (m:Moment {id: $id})
        RETURN m.weight, m.status
        """
        result = self._query(get_cypher, {"id": moment_id})
        if not result or not result[0]:
            return {"error": f"Moment {moment_id} not found"}

        current_weight = result[0][0] or 0.5
        current_status = result[0][1]

        # Calculate new weight (capped at 1.0)
        new_weight = min(1.0, current_weight + boost)
        flipped = False
        new_status = current_status

        # Check for flip
        if current_status == "possible" and new_weight >= flip_threshold:
            flipped = True
            new_status = "active"

        # Update moment
        if flipped:
            update_cypher = """
            MATCH (m:Moment {id: $id})
            SET m.weight = $weight, m.status = 'active', m.tick_spoken = $tick
            """
            self._query(update_cypher, {
                "id": moment_id,
                "weight": new_weight,
                "tick": current_tick
            })
        else:
            update_cypher = """
            MATCH (m:Moment {id: $id})
            SET m.weight = $weight
            """
            self._query(update_cypher, {"id": moment_id, "weight": new_weight})

        logger.info(f"[GraphOps] Boosted {moment_id}: {current_weight:.2f} → {new_weight:.2f}" +
                    (f" (FLIPPED to active)" if flipped else ""))

        return {
            "new_weight": new_weight,
            "flipped": flipped,
            "status": new_status
        }

    def add_belief(
        self,
        character_id: str,
        narrative_id: str,
        heard: float = 0.0,
        believes: float = 0.0,
        doubts: float = 0.0,
        denies: float = 0.0,
        hides: float = 0.0,
        spreads: float = 0.0,
        originated: float = 0.0,
        source: str = "none",
        from_whom: str = None,
        where: str = None
    ) -> None:
        """
        Add or update a CHARACTER_NARRATIVE link (belief).

        This is how characters know things. There is no "knowledge" stat.

        Args:
            character_id: Who believes
            narrative_id: What they believe
            heard: 0-1, how much they know
            believes: 0-1, how certain
            doubts: 0-1, active uncertainty
            denies: 0-1, rejects as false
            hides: 0-1, conceals knowledge
            spreads: 0-1, actively promotes
            originated: 0-1, they created this narrative
            source: none, witnessed, told, inferred, assumed, taught
            from_whom: Who told them (if told)
        """
        props = {
            "heard": heard,
            "believes": believes,
            "doubts": doubts,
            "denies": denies,
            "hides": hides,
            "spreads": spreads,
            "originated": originated,
            "source": source,
            "when": datetime.utcnow().isoformat()
        }

        if from_whom:
            props["from_whom"] = from_whom
        if where:
            props["where"] = where

        cypher = """
        MATCH (c:Character {id: $char_id})
        MATCH (n:Narrative {id: $narr_id})
        MERGE (c)-[r:BELIEVES]->(n)
        SET r += $props
        """
        self._query(cypher, {
            "char_id": character_id,
            "narr_id": narrative_id,
            "props": props
        })
        logger.info(f"[GraphOps] Added belief: {character_id} -> {narrative_id}")

    def add_narrative_link(
        self,
        source_id: str,
        target_id: str,
        contradicts: float = 0.0,
        supports: float = 0.0,
        elaborates: float = 0.0,
        subsumes: float = 0.0,
        supersedes: float = 0.0
    ) -> None:
        """
        Add or update a NARRATIVE_NARRATIVE link.

        How stories relate to each other.

        Args:
            source_id: Source narrative
            target_id: Target narrative
            contradicts: 0-1, cannot both be true
            supports: 0-1, reinforce each other
            elaborates: 0-1, adds detail
            subsumes: 0-1, specific case of
            supersedes: 0-1, replaces (old fades)
        """
        props = {
            "contradicts": contradicts,
            "supports": supports,
            "elaborates": elaborates,
            "subsumes": subsumes,
            "supersedes": supersedes
        }

        cypher = """
        MATCH (s:Narrative {id: $source_id})
        MATCH (t:Narrative {id: $target_id})
        MERGE (s)-[r:RELATES_TO]->(t)
        SET r += $props
        """
        self._query(cypher, {
            "source_id": source_id,
            "target_id": target_id,
            "props": props
        })
        logger.info(f"[GraphOps] Added narrative link: {source_id} -> {target_id}")

    def add_presence(
        self,
        character_id: str,
        place_id: str,
        present: float = 1.0,
        visible: float = 1.0
    ) -> None:
        """
        Add or update a CHARACTER_PLACE link (physical presence).

        Ground truth - where character IS.

        Args:
            character_id: Who
            place_id: Where
            present: 0-1 (usually 1.0 = here, 0.0 = not here)
            visible: 0-1 (0 = hiding, 1 = visible)
        """
        props = {
            "present": present,
            "visible": visible
        }

        cypher = """
        MATCH (c:Character {id: $char_id})
        MATCH (p:Place {id: $place_id})
        MERGE (c)-[r:AT]->(p)
        SET r += $props
        """
        self._query(cypher, {
            "char_id": character_id,
            "place_id": place_id,
            "props": props
        })
        logger.info(f"[GraphOps] Added presence: {character_id} at {place_id}")

    def move_character(
        self,
        character_id: str,
        to_place_id: str,
        visible: float = 1.0
    ) -> None:
        """
        Move a character to a new location.

        Removes all previous AT links and creates new one.

        Args:
            character_id: Who to move
            to_place_id: Where to move them
            visible: 0-1 visibility at new location
        """
        # Remove all existing AT links
        cypher_remove = """
        MATCH (c:Character {id: $char_id})-[r:AT]->()
        DELETE r
        """
        self._query(cypher_remove, {"char_id": character_id})

        # Add new presence
        self.add_presence(character_id, to_place_id, present=1.0, visible=visible)
        logger.info(f"[GraphOps] Moved {character_id} to {to_place_id}")

    def add_possession(
        self,
        character_id: str,
        thing_id: str,
        carries: float = 1.0,
        carries_hidden: float = 0.0
    ) -> None:
        """
        Add or update a CHARACTER_THING link (physical possession).

        Ground truth - what character HAS.

        Args:
            character_id: Who has it
            thing_id: What they have
            carries: 0-1 (1 = has it)
            carries_hidden: 0-1 (1 = secretly)
        """
        props = {
            "carries": carries,
            "carries_hidden": carries_hidden
        }

        cypher = """
        MATCH (c:Character {id: $char_id})
        MATCH (t:Thing {id: $thing_id})
        MERGE (c)-[r:CARRIES]->(t)
        SET r += $props
        """
        self._query(cypher, {
            "char_id": character_id,
            "thing_id": thing_id,
            "props": props
        })
        logger.info(f"[GraphOps] Added possession: {character_id} carries {thing_id}")

    def add_thing_location(
        self,
        thing_id: str,
        place_id: str,
        located: float = 1.0,
        hidden: float = 0.0,
        specific_location: str = None
    ) -> None:
        """
        Add or update a THING_PLACE link (where uncarried thing is).

        Ground truth - where thing IS (when not carried).

        Args:
            thing_id: What
            place_id: Where
            located: 0-1 (1 = here)
            hidden: 0-1 (1 = concealed)
            specific_location: "under the altar", "in the chest"
        """
        props = {
            "located": located,
            "hidden": hidden
        }

        if specific_location:
            props["specific_location"] = specific_location

        cypher = """
        MATCH (t:Thing {id: $thing_id})
        MATCH (p:Place {id: $place_id})
        MERGE (t)-[r:LOCATED_AT]->(p)
        SET r += $props
        """
        self._query(cypher, {
            "thing_id": thing_id,
            "place_id": place_id,
            "props": props
        })
        logger.info(f"[GraphOps] Added thing location: {thing_id} at {place_id}")

    def add_geography(
        self,
        from_place_id: str,
        to_place_id: str,
        contains: float = 0.0,
        path: float = 0.0,
        path_distance: str = None,
        path_difficulty: str = "moderate",
        borders: float = 0.0
    ) -> None:
        """
        Add or update a PLACE_PLACE link (geography).

        Ground truth - how places connect.

        Args:
            from_place_id: Source place
            to_place_id: Target place
            contains: 0-1 (from contains to)
            path: 0-1 (can travel between)
            path_distance: "2 days", "4 hours", "adjacent"
            path_difficulty: easy, moderate, hard, dangerous, impassable
            borders: 0-1 (share a border)
        """
        props = {
            "contains": contains,
            "path": path,
            "path_difficulty": path_difficulty,
            "borders": borders
        }

        if path_distance:
            props["path_distance"] = path_distance

        cypher = """
        MATCH (f:Place {id: $from_id})
        MATCH (t:Place {id: $to_id})
        MERGE (f)-[r:CONNECTS]->(t)
        SET r += $props
        """
        self._query(cypher, {
            "from_id": from_place_id,
            "to_id": to_place_id,
            "props": props
        })
        logger.info(f"[GraphOps] Added geography: {from_place_id} -> {to_place_id}")

    # =========================================================================
    # BULK OPERATIONS
    # =========================================================================

    def apply_mutations(self, mutations: Dict[str, Any]) -> None:
        """
        Apply a batch of mutations from Narrator or World Runner output.

        Args:
            mutations: Dict with keys:
                - new_narratives: List of narrative dicts
                - new_beliefs: List of belief dicts
                - tension_updates: List of tension update dicts
                - new_tensions: List of new tension dicts
                - character_movements: List of movement dicts
        """
        # 1. New narratives first
        for narr in mutations.get("new_narratives", []):
            self.add_narrative(
                id=narr["id"],
                name=narr["name"],
                content=narr["content"],
                type=narr["type"],
                interpretation=narr.get("interpretation"),
                about_characters=narr.get("about", {}).get("characters"),
                about_places=narr.get("about", {}).get("places"),
                about_things=narr.get("about", {}).get("things"),
                about_relationship=narr.get("about", {}).get("relationship"),
                tone=narr.get("tone"),
                truth=narr.get("truth", 1.0),
                focus=narr.get("focus", 1.0)
            )

        # 2. New beliefs
        for belief in mutations.get("new_beliefs", []):
            self.add_belief(
                character_id=belief["character"],
                narrative_id=belief["narrative"],
                heard=belief.get("heard", 0.0),
                believes=belief.get("believes", 0.0),
                doubts=belief.get("doubts", 0.0),
                denies=belief.get("denies", 0.0),
                source=belief.get("source", "none"),
                from_whom=belief.get("from_whom")
            )

        # 3. Tension updates
        for update in mutations.get("tension_updates", []):
            props = {}
            if "pressure" in update:
                props["pressure"] = update["pressure"]
            if update.get("resolved"):
                props["resolved"] = True

            if props:
                cypher = """
                MATCH (t:Tension {id: $id})
                SET t += $props
                """
                self._query(cypher, {"id": update["id"], "props": props})
                logger.info(f"[GraphOps] Updated tension: {update['id']}")

        # 4. New tensions
        for tension in mutations.get("new_tensions", []):
            self.add_tension(
                id=tension["id"],
                narratives=tension["narratives"],
                description=tension["description"],
                pressure=tension.get("pressure", 0.0),
                pressure_type=tension.get("pressure_type", "gradual"),
                breaking_point=tension.get("breaking_point", 0.9),
                base_rate=tension.get("base_rate", 0.001),
                trigger_at=tension.get("trigger_at"),
                progression=tension.get("progression"),
                narrator_notes=tension.get("narrator_notes")
            )

        # 5. Character movements
        for move in mutations.get("character_movements", []):
            self.move_character(
                character_id=move["character"],
                to_place_id=move["to"],
                visible=1.0 if move.get("visible", True) else 0.0
            )

        logger.info(f"[GraphOps] Applied {len(mutations)} mutation types")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_graph(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379
) -> GraphOps:
    """Get a GraphOps instance."""
    return GraphOps(graph_name=graph_name, host=host, port=port)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Create initial game state
    graph = get_graph("blood_ledger_test")

    # Add characters
    graph.add_character(
        id="char_rolf",
        name="Rolf",
        type="player",
        backstory_wound="Thornwick burned. Edmund took everything."
    )

    graph.add_character(
        id="char_aldric",
        name="Aldric",
        type="companion",
        voice_tone="quiet",
        voice_style="blunt",
        values=["loyalty", "survival"],
        flaw="doubt"
    )

    # Add places
    graph.add_place(
        id="place_camp",
        name="The Camp",
        type="camp",
        mood="watchful",
        weather=["cold", "clear"]
    )

    graph.add_place(
        id="place_york",
        name="York",
        type="city",
        mood="tense"
    )

    # Add geography
    graph.add_geography(
        from_place_id="place_camp",
        to_place_id="place_york",
        path=1.0,
        path_distance="2 days",
        path_difficulty="moderate"
    )

    # Add narratives
    graph.add_narrative(
        id="narr_oath",
        name="Rolf's Oath",
        content="I swore to find Edmund and reclaim what he stole.",
        type="oath",
        tone="cold",
        about_characters=["char_rolf", "char_edmund"]
    )

    graph.add_narrative(
        id="narr_aldric_loyalty",
        name="Aldric's Loyalty",
        content="Aldric follows by choice, not obligation.",
        type="bond",
        tone="warm",
        about_characters=["char_aldric", "char_rolf"]
    )

    # Add beliefs
    graph.add_belief(
        character_id="char_rolf",
        narrative_id="narr_oath",
        heard=1.0,
        believes=1.0,
        originated=1.0,
        source="witnessed"
    )

    graph.add_belief(
        character_id="char_aldric",
        narrative_id="narr_oath",
        heard=1.0,
        believes=1.0,
        source="witnessed"
    )

    # Add presence
    graph.add_presence("char_rolf", "place_camp")
    graph.add_presence("char_aldric", "place_camp")

    # Add tension
    graph.add_tension(
        id="tension_confrontation",
        narratives=["narr_oath"],
        description="Edmund draws closer. The reckoning approaches.",
        pressure=0.3,
        pressure_type="hybrid"
    )

    print("Initial game state created!")
