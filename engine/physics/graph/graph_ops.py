"""
Blood Ledger — Graph Operations

Write mutations to FalkorDB via YAML/JSON files.

Usage:
    from engine.physics.graph.graph_ops import GraphOps

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
from engine.physics.graph.graph_ops_moments import MomentOperationsMixin
from engine.physics.graph.graph_ops_apply import ApplyOperationsMixin

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


class GraphOps(MomentOperationsMixin, ApplyOperationsMixin):
    """
    Simple interface for FalkorDB graph operations.

    All functions use MERGE (upsert) - safe to call multiple times.

    Inherits moment lifecycle methods from MomentOperationsMixin:
    - handle_click(): Handle player word clicks
    - update_moment_weight(): Update moment weights
    - propagate_embedding_energy(): Propagate energy through graph
    - decay_moments(): Apply weight decay
    - on_player_leaves_location(): Handle player departure
    - on_player_arrives_location(): Handle player arrival
    - garbage_collect_moments(): Remove old decayed moments
    - boost_moment_weight(): Boost moment weights
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

    # NOTE: apply() method and extraction helpers are in graph_ops_apply.py
    # Inherited from ApplyOperationsMixin

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

    # NOTE: Moment lifecycle methods (handle_click, update_moment_weight,
    # propagate_embedding_energy, decay_moments, etc.) are inherited from
    # MomentOperationsMixin in graph_ops_moments.py

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
