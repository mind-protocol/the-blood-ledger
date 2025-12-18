# Schema Delta: Moment Graph Architecture

```
STATUS: Implementation Spec
CREATED: 2024-12-17
AFFECTS: engine/models/base.py, engine/models/nodes.py, engine/db/graph_ops.py
```

This document provides exact code changes needed to implement the Moment Graph spec.

---

## 1. New Enums (base.py)

Add to `engine/models/base.py`:

```python
# =============================================================================
# MOMENT GRAPH ENUMS (NEW)
# =============================================================================

class MomentStatus(str, Enum):
    """Lifecycle status of a Moment in the moment graph."""
    POSSIBLE = "possible"    # Created, not yet surfaced
    ACTIVE = "active"        # Visible to player, can be triggered
    SPOKEN = "spoken"        # In transcript, part of history
    DORMANT = "dormant"      # Waiting for return (persistent=True)
    DECAYED = "decayed"      # Pruned, no longer relevant


class MomentTrigger(str, Enum):
    """How a CAN_LEAD_TO link can be traversed."""
    CLICK = "click"          # Player clicks a word
    WAIT = "wait"            # Time passes without player input
    AUTO = "auto"            # Automatic when conditions met
    SEMANTIC = "semantic"    # Freeform input matches embedding


# Extend MomentType (already exists, add action/thought)
class MomentType(str, Enum):
    """Type of narrated moment."""
    NARRATION = "narration"
    DIALOGUE = "dialogue"
    ACTION = "action"              # NEW: Physical action
    THOUGHT = "thought"            # NEW: Internal thought
    HINT = "hint"
    PLAYER_CLICK = "player_click"
    PLAYER_FREEFORM = "player_freeform"
    PLAYER_CHOICE = "player_choice"
```

---

## 2. Moment Model Expansion (nodes.py)

Update `engine/models/nodes.py`:

```python
class Moment(BaseModel):
    """
    MOMENT - A single unit of narrated content OR a potential moment.

    In the Moment Graph architecture, moments exist in a possibility space.
    They can be:
    - possible: Created but not yet surfaced
    - active: Visible to player, can be triggered
    - spoken: Part of history
    - dormant: Waiting for player return
    - decayed: Pruned

    Links:
        Character -[CAN_SPEAK]-> Moment (who can say this)
        Character -[SAID]-> Moment (who said this - after spoken)
        Moment -[ATTACHED_TO]-> Character|Place|Thing|Narrative|Tension
        Moment -[CAN_LEAD_TO]-> Moment (traversal)
        Moment -[THEN]-> Moment (sequence after spoken)
        Moment -[AT]-> Place (where it occurred)
        Narrative -[FROM]-> Moment (source attribution)
    """
    id: str = Field(description="Unique ID: {place}_{day}_{time}_{type}_{timestamp}")
    text: str = Field(description="The actual text content")
    type: MomentType = MomentType.NARRATION

    # NEW: Moment Graph fields
    status: MomentStatus = Field(
        default=MomentStatus.SPOKEN,  # Default for backward compat
        description="Lifecycle status in moment graph"
    )
    weight: float = Field(
        default=0.5,
        ge=0.0, le=1.0,
        description="Salience/importance (computed from graph topology)"
    )
    tone: Optional[str] = Field(
        default=None,
        description="Emotional tone: bitter, hopeful, urgent, etc."
    )

    # Tick tracking (expanded from single tick)
    tick_created: int = Field(
        default=0, ge=0,
        description="World tick when moment was created"
    )
    tick_spoken: Optional[int] = Field(
        default=None,
        description="World tick when moment was spoken (if spoken)"
    )
    tick_decayed: Optional[int] = Field(
        default=None,
        description="World tick when moment decayed (if decayed)"
    )

    # Backward compat: keep tick as alias for tick_created
    @property
    def tick(self) -> int:
        return self.tick_created

    # Transcript reference
    line: Optional[int] = Field(default=None, description="Line in transcript.json")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    # Query fields (for backstory generation)
    query: Optional[str] = Field(
        default=None,
        description="Question this moment asks (triggers backstory generation)"
    )
    query_type: Optional[str] = Field(
        default=None,
        description="Type of query: backstory_gap, clarification, etc."
    )
    query_filled: bool = Field(
        default=False,
        description="Whether the query has been answered"
    )

    def embeddable_text(self) -> str:
        return self.text

    @property
    def should_embed(self) -> bool:
        return len(self.text) > 20

    @property
    def is_active(self) -> bool:
        return self.status == MomentStatus.ACTIVE

    @property
    def is_spoken(self) -> bool:
        return self.status == MomentStatus.SPOKEN

    @property
    def can_surface(self) -> bool:
        return self.status in [MomentStatus.POSSIBLE, MomentStatus.ACTIVE]
```

---

## 3. New Link Types (links.py)

Create new link models in `engine/models/links.py`:

```python
# =============================================================================
# MOMENT GRAPH LINKS (NEW)
# =============================================================================

class CanSpeak(BaseModel):
    """
    CAN_SPEAK: Character -> Moment

    Which characters can speak/trigger this moment.
    Multiple characters can CAN_SPEAK the same moment.
    Highest weight present character speaks.
    """
    character_id: str
    moment_id: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)


class AttachedTo(BaseModel):
    """
    ATTACHED_TO: Moment -> Character|Place|Thing|Narrative|Tension

    Binds moments to graph nodes. Controls when moment is visible.
    """
    moment_id: str
    target_id: str  # Any node ID
    target_type: str  # character, place, thing, narrative, tension

    presence_required: bool = Field(
        default=False,
        description="Moment only visible when target is present"
    )
    persistent: bool = Field(
        default=True,
        description="Survives scene change (goes dormant vs pruned)"
    )
    dies_with_target: bool = Field(
        default=False,
        description="Moment decays if target is destroyed/dies"
    )


class CanLeadTo(BaseModel):
    """
    CAN_LEAD_TO: Moment -> Moment

    Traversal link in the moment graph.
    This is the core mechanic for click-based dialogue.
    """
    from_moment_id: str
    to_moment_id: str

    # Trigger configuration
    trigger: MomentTrigger = MomentTrigger.CLICK
    require_words: List[str] = Field(
        default_factory=list,
        description="Words that trigger this link (for click)"
    )
    require_similarity: float = Field(
        default=0.65,
        description="Embedding similarity threshold (for semantic)"
    )
    wait_ticks: int = Field(
        default=3,
        description="Ticks to wait before auto-fire (for wait)"
    )

    # Link behavior
    bidirectional: bool = Field(
        default=False,
        description="Can traverse in both directions"
    )
    consumes_origin: bool = Field(
        default=True,
        description="Origin becomes 'spoken' after traversal"
    )
    weight_transfer: float = Field(
        default=0.3,
        description="Weight transferred to target on traversal"
    )


class Then(BaseModel):
    """
    THEN: Moment -> Moment (enhanced)

    Sequence link for spoken moments.
    Records temporal ordering after moments are spoken.
    """
    from_moment_id: str
    to_moment_id: str
    tick: int = Field(description="When this transition occurred")
    player_caused: bool = Field(
        default=False,
        description="Player action caused this transition (vs NPC/system)"
    )
```

---

## 4. GraphOps Additions (graph_ops.py)

Add these methods to `GraphOps` class:

```python
# =============================================================================
# MOMENT GRAPH OPERATIONS (NEW)
# =============================================================================

def add_can_speak(
    self,
    character_id: str,
    moment_id: str,
    weight: float = 1.0
) -> None:
    """
    Add CAN_SPEAK link: Character can speak this moment.

    Args:
        character_id: Who can speak it
        moment_id: The moment they can speak
        weight: Priority weight (highest present character speaks)
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
    target_type: str,
    presence_required: bool = False,
    persistent: bool = True,
    dies_with_target: bool = False
) -> None:
    """
    Add ATTACHED_TO link: Moment attached to graph node.

    Args:
        moment_id: The moment
        target_id: Node ID (character, place, thing, narrative, tension)
        target_type: Node type label
        presence_required: Only visible when target present
        persistent: Survives scene change
        dies_with_target: Decays if target dies/destroyed
    """
    # Map target_type to label
    label_map = {
        'character': 'Character',
        'place': 'Place',
        'thing': 'Thing',
        'narrative': 'Narrative',
        'tension': 'Tension'
    }
    label = label_map.get(target_type.lower(), target_type.capitalize())

    props = {
        "presence_required": presence_required,
        "persistent": persistent,
        "dies_with_target": dies_with_target
    }

    cypher = f"""
    MATCH (m:Moment {{id: $moment_id}})
    MATCH (t:{label} {{id: $target_id}})
    MERGE (m)-[r:ATTACHED_TO]->(t)
    SET r += $props
    """
    self._query(cypher, {
        "moment_id": moment_id,
        "target_id": target_id,
        "props": props
    })
    logger.debug(f"[GraphOps] Added attached_to: {moment_id} -> {target_id}")


def add_can_lead_to(
    self,
    from_moment_id: str,
    to_moment_id: str,
    trigger: str = "click",
    require_words: List[str] = None,
    require_similarity: float = 0.65,
    wait_ticks: int = 3,
    bidirectional: bool = False,
    consumes_origin: bool = True,
    weight_transfer: float = 0.3
) -> None:
    """
    Add CAN_LEAD_TO link: Traversal between moments.

    Args:
        from_moment_id: Origin moment
        to_moment_id: Target moment
        trigger: click, wait, auto, semantic
        require_words: Words that trigger (for click)
        require_similarity: Embedding threshold (for semantic)
        wait_ticks: Ticks to wait (for wait)
        bidirectional: Can traverse both ways
        consumes_origin: Origin becomes spoken
        weight_transfer: Weight transferred to target
    """
    props = {
        "trigger": trigger,
        "require_words": json.dumps(require_words or []),
        "require_similarity": require_similarity,
        "wait_ticks": wait_ticks,
        "bidirectional": bidirectional,
        "consumes_origin": consumes_origin,
        "weight_transfer": weight_transfer
    }

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

    # Create reverse link if bidirectional
    if bidirectional:
        reverse_props = dict(props)
        self._query(cypher, {
            "from_id": to_moment_id,
            "to_id": from_moment_id,
            "props": reverse_props
        })

    logger.debug(f"[GraphOps] Added can_lead_to: {from_moment_id} -> {to_moment_id}")


def update_moment_status(
    self,
    moment_id: str,
    status: str,
    tick: int = None
) -> None:
    """
    Update moment status and relevant tick.

    Args:
        moment_id: Which moment
        status: New status (possible, active, spoken, dormant, decayed)
        tick: Current tick (updates tick_spoken or tick_decayed)
    """
    props = {"status": status}

    if status == "spoken" and tick is not None:
        props["tick_spoken"] = tick
    elif status == "decayed" and tick is not None:
        props["tick_decayed"] = tick

    cypher = """
    MATCH (m:Moment {id: $moment_id})
    SET m += $props
    """
    self._query(cypher, {"moment_id": moment_id, "props": props})
    logger.debug(f"[GraphOps] Updated moment status: {moment_id} -> {status}")


def update_moment_weight(
    self,
    moment_id: str,
    weight: float
) -> None:
    """
    Update moment weight (salience).

    Args:
        moment_id: Which moment
        weight: New weight (0-1)
    """
    cypher = """
    MATCH (m:Moment {id: $moment_id})
    SET m.weight = $weight
    """
    self._query(cypher, {"moment_id": moment_id, "weight": max(0.0, min(1.0, weight))})


def boost_moment_weight(
    self,
    moment_id: str,
    boost: float
) -> None:
    """
    Add to moment weight (clamped to 0-1).

    Args:
        moment_id: Which moment
        boost: Amount to add (can be negative)
    """
    cypher = """
    MATCH (m:Moment {id: $moment_id})
    SET m.weight = CASE
        WHEN m.weight + $boost > 1.0 THEN 1.0
        WHEN m.weight + $boost < 0.0 THEN 0.0
        ELSE m.weight + $boost
    END
    """
    self._query(cypher, {"moment_id": moment_id, "boost": boost})
```

---

## 5. GraphOps Apply Extension

Extend the `apply()` method's link processing:

```python
# In apply() method, add to link processing:

elif link_type == 'can_speak':
    char_id = link.get('character')
    moment_id = link.get('moment')
    self._validate_link_targets(char_id, moment_id, existing_ids, new_node_ids)
    linked_ids.add(char_id)
    linked_ids.add(moment_id)
    self.add_can_speak(
        character_id=char_id,
        moment_id=moment_id,
        weight=link.get('weight', 1.0)
    )

elif link_type == 'attached_to':
    moment_id = link.get('moment')
    target_id = link.get('target')
    target_type = link.get('target_type')
    self._validate_link_targets(moment_id, target_id, existing_ids, new_node_ids)
    linked_ids.add(moment_id)
    linked_ids.add(target_id)
    self.add_attached_to(
        moment_id=moment_id,
        target_id=target_id,
        target_type=target_type,
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
        from_moment_id=from_id,
        to_moment_id=to_id,
        trigger=link.get('trigger', 'click'),
        require_words=link.get('require_words'),
        require_similarity=link.get('require_similarity', 0.65),
        wait_ticks=link.get('wait_ticks', 3),
        bidirectional=link.get('bidirectional', False),
        consumes_origin=link.get('consumes_origin', True),
        weight_transfer=link.get('weight_transfer', 0.3)
    )
```

---

## 6. Moment Extraction Helper

Add to `GraphOps`:

```python
def _extract_moment_args(self, node: Dict) -> Dict:
    """Extract moment arguments from mutation node."""
    return {
        'id': node['id'],
        'text': node.get('text', ''),
        'type': node.get('moment_type', node.get('type', 'narration')),
        'tick': node.get('tick', node.get('tick_created', 0)),
        'speaker': node.get('speaker'),
        'place_id': node.get('place_id'),
        'after_moment_id': node.get('after_moment_id'),
        'embedding': node.get('embedding'),
        'line': node.get('line'),
        # NEW fields
        'status': node.get('status', 'possible'),
        'weight': node.get('weight', 0.5),
        'tone': node.get('tone'),
        'query': node.get('query'),
        'query_type': node.get('query_type'),
    }
```

Update `add_moment()` to accept new fields:

```python
def add_moment(
    self,
    id: str,
    text: str,
    type: str = "narration",
    tick: int = 0,
    speaker: str = None,
    place_id: str = None,
    after_moment_id: str = None,
    embedding: List[float] = None,
    line: int = None,
    # NEW parameters
    status: str = "spoken",  # Default for backward compat
    weight: float = 0.5,
    tone: str = None,
    query: str = None,
    query_type: str = None
) -> None:
    """
    Add or update a MOMENT node (enhanced for Moment Graph).
    """
    props = {
        "id": id,
        "text": text,
        "type": type,
        "tick_created": tick,
        "status": status,
        "weight": weight,
        "created_at": datetime.utcnow().isoformat()
    }

    # Backward compat: also set tick
    props["tick"] = tick

    if status == "spoken":
        props["tick_spoken"] = tick

    if tone:
        props["tone"] = tone
    if embedding:
        props["embedding"] = embedding
    if line is not None:
        props["line"] = line
    if query:
        props["query"] = query
        props["query_type"] = query_type or "backstory_gap"
        props["query_filled"] = False

    cypher = """
    MERGE (n:Moment {id: $id})
    SET n += $props
    """
    self._query(cypher, {"id": id, "props": props})

    # Create links...
    if speaker:
        self.add_said(speaker, id)
    if place_id:
        self.add_moment_at(id, place_id)
    if after_moment_id:
        self.add_moment_then(after_moment_id, id)

    logger.info(f"[GraphOps] Added moment: {id} ({type}, {status})")
```

---

## 7. Migration Queries

For existing moments (all become `status: spoken`):

```cypher
-- Set status and weight for all existing moments
MATCH (m:Moment)
WHERE m.status IS NULL
SET m.status = 'spoken',
    m.weight = 0.5,
    m.tick_created = COALESCE(m.tick, 0),
    m.tick_spoken = COALESCE(m.tick, 0)

-- Verify migration
MATCH (m:Moment)
RETURN m.status, count(m)
```

---

## 8. Example Mutation File

`mutations/example_moment_graph.yaml`:

```yaml
# Example: Creating a conversation branch

nodes:
  # A moment Aldric can say
  - type: moment
    id: moment_aldric_about_brother
    text: "My brother... he's not the man you think he is."
    moment_type: dialogue
    status: possible
    weight: 0.6
    tone: bitter

  # A response if player asks about the brother
  - type: moment
    id: moment_aldric_brother_detail
    text: "He betrayed our father. Sold his secrets to the Normans for silver."
    moment_type: dialogue
    status: possible
    weight: 0.4
    tone: cold

  # A player query moment
  - type: moment
    id: moment_player_ask_brother
    text: "What happened with your brother?"
    moment_type: player_click
    status: possible
    weight: 0.0

links:
  # Who can speak what
  - type: can_speak
    character: char_aldric
    moment: moment_aldric_about_brother
    weight: 1.0

  - type: can_speak
    character: char_aldric
    moment: moment_aldric_brother_detail
    weight: 1.0

  # Attachments
  - type: attached_to
    moment: moment_aldric_about_brother
    target: char_aldric
    target_type: character
    presence_required: true
    persistent: true

  - type: attached_to
    moment: moment_aldric_about_brother
    target: narr_aldric_family_secret
    target_type: narrative
    presence_required: true  # Only surfaces when narrative is active

  # Traversal
  - type: can_lead_to
    from: moment_aldric_about_brother
    to: moment_player_ask_brother
    trigger: click
    require_words: ["brother", "man", "think"]
    consumes_origin: false  # Can revisit
    weight_transfer: 0.2

  - type: can_lead_to
    from: moment_player_ask_brother
    to: moment_aldric_brother_detail
    trigger: auto  # Player asked, Aldric answers
    consumes_origin: true
    weight_transfer: 0.4
```

---

## 9. Validation Checklist

After implementation:

- [ ] `MomentStatus` enum exists in base.py
- [ ] `MomentTrigger` enum exists in base.py
- [ ] Moment model has status, weight, tone, tick_created, tick_spoken, tick_decayed
- [ ] Moment model has query, query_type, query_filled
- [ ] GraphOps has `add_can_speak()`
- [ ] GraphOps has `add_attached_to()`
- [ ] GraphOps has `add_can_lead_to()`
- [ ] GraphOps has `update_moment_status()`
- [ ] GraphOps has `update_moment_weight()`, `boost_moment_weight()`
- [ ] GraphOps.apply() handles new link types
- [ ] GraphOps.add_moment() accepts new parameters
- [ ] Migration query runs on existing graph
- [ ] Example mutation file parses correctly

---

*"The schema is the contract. Everything else is implementation."*
