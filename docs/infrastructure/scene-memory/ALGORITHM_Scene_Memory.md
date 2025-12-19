# Scene Memory System — Algorithm

```
STATUS: DRAFT
CREATED: 2024-12-16
```

===============================================================================
## CHAIN
===============================================================================

```
PATTERNS:    ./PATTERNS_Scene_Memory.md
BEHAVIORS:   ./BEHAVIORS_Scene_Memory.md
THIS:        ALGORITHM_Scene_Memory.md (you are here)
VALIDATION:  ./VALIDATION_Scene_Memory.md
SYNC:        ./SYNC_Scene_Memory.md
```

===============================================================================
## OVERVIEW
===============================================================================

This document specifies **how** the system accomplishes the behaviors defined
in BEHAVIOR.md.

===============================================================================
## NAME EXPANSION
===============================================================================

### Algorithm

```python
def expand_names(scene: dict, narration: list, player_inputs: list) -> tuple:
    """
    Expand short names to globally unique names using scene context.

    Pattern: {place}_{day}_{time}_{short_name}
    Example: crossing_d5_dusk_blade_broken
    """
    # Build prefix from scene context
    place = scene["where"].replace("place_", "")

    # Parse "Day 5, dusk" → "d5", "dusk"
    when_parts = scene["when"].split(", ")
    day = when_parts[0].replace("Day ", "d")
    time = when_parts[1].lower() if len(when_parts) > 1 else "unknown"

    prefix = f"{place}_{day}_{time}"
    # → "crossing_d5_dusk"

    # Track used names for collision detection
    used_names = set()

    def make_unique(short_name: str) -> str:
        """Ensure name is unique, append suffix if needed."""
        full_name = f"{prefix}_{short_name}"
        if full_name not in used_names:
            used_names.add(full_name)
            return full_name

        # Collision: append incrementing suffix
        counter = 2
        while f"{full_name}_{counter}" in used_names:
            counter += 1
        unique_name = f"{full_name}_{counter}"
        used_names.add(unique_name)
        return unique_name

    # Expand narration element names
    for elem in narration:
        elem["name"] = make_unique(elem["name"])

        # Expand clickable hint names
        if "clickable" in elem:
            for word, data in elem["clickable"].items():
                data["name"] = make_unique(data["name"])

    # Expand player input names
    for inp in player_inputs:
        inp["name"] = make_unique(inp["name"])

    return narration, player_inputs
```

### Examples

| Input | Output |
|-------|--------|
| Scene: `{when: "Day 5, dusk", where: "place_crossing"}` | Prefix: `crossing_d5_dusk` |
| Name: `blade_broken` | `crossing_d5_dusk_blade_broken` |
| Name: `aldric_speaks` (first) | `crossing_d5_dusk_aldric_speaks` |
| Name: `aldric_speaks` (second) | `crossing_d5_dusk_aldric_speaks_2` |

===============================================================================
## SCENE PROCESSING
===============================================================================

### Main Flow

```python
def process_narrator_output(output: NarratorOutput, tick: int) -> None:
    """
    Process narrator output: create moments, store scene, create beliefs.
    """
    scene = output["scene"]
    narration = output["narration"]
    mutations = output["mutations"]
    present = scene["present"]

    # 1. Store scene node
    scene_node = store_scene(scene, tick)

    # 2. Create Moment nodes for each narration element
    moment_map = {}  # short_name -> moment_id
    prev_moment = None

    for elem in narration:
        moment = create_moment(scene, elem, tick)
        moment_map[elem["name"]] = moment["id"]

        # Link scene to moment
        graph.create_link(scene_node["id"], "CONTAINS", moment["id"])

        # Link moment to place
        graph.create_link(moment["id"], "AT", scene["where"])

        # Link dialogue to speaker
        if "speaker" in elem:
            graph.create_link(elem["speaker"], "SAID", moment["id"])

        # Link to previous moment (sequence)
        if prev_moment:
            graph.create_link(prev_moment["id"], "THEN", moment["id"])
        prev_moment = moment

        # Create moments for clickable hints
        if "clickable" in elem:
            for word, hint_data in elem["clickable"].items():
                hint_moment = create_hint_moment(scene, hint_data, tick)
                moment_map[hint_data["name"]] = hint_moment["id"]
                graph.create_link(scene_node["id"], "CONTAINS", hint_moment["id"])
                graph.create_link(hint_moment["id"], "AT", scene["where"])

    # 3. Process mutations - create narratives with FROM links
    for mutation in mutations:
        if mutation["type"] == "new_narrative":
            narr_node = create_narrative(mutation, tick)

            # Link scene to narrative
            graph.create_link(scene_node["id"], "CREATES", narr_node["id"])

            # Create FROM links to source moments
            for source_name in mutation["sources"]:
                moment_id = moment_map.get(source_name) or expand_name(scene, source_name)
                graph.create_link(narr_node["id"], "FROM", moment_id)

            # Auto-create beliefs for all present
            for char_id in present:
                create_witnessed_belief(
                    character=char_id,
                    narrative=narr_node["id"],
                    when=scene["when"],
                    where=scene["where"]
                )
```

### Store Scene

```python
def store_scene(scene: dict, tick: int) -> dict:
    """
    Store scene as graph node. Moments are separate nodes.
    """
    scene_id = generate_scene_id(scene)
    # → "scene_d5_dusk_crossing"

    scene_node = {
        "id": scene_id,
        "when": scene["when"],
        "tick": tick
    }

    graph.create_node("Scene", scene_node)

    # Link to place
    graph.create_link(scene_id, "AT", scene["where"])

    # Link to present characters
    for char_id in scene["present"]:
        graph.create_link(scene_id, "INVOLVES", char_id)

    return scene_node
```

### Create Moment

```python
def create_moment(scene: dict, elem: dict, tick: int) -> dict:
    """
    Create a Moment node from a narration element.
    """
    moment_id = expand_name(scene, elem["name"])

    moment_type = "dialogue" if "speaker" in elem else "narration"

    moment = {
        "id": moment_id,
        "text": elem["text"],
        "type": moment_type,
        "tick": tick
    }

    # Embed if sufficient text
    if len(elem["text"]) > 20:
        moment["embedding"] = embed(elem["text"])

    graph.create_node("Moment", moment)

    return moment


def create_hint_moment(scene: dict, hint_data: dict, tick: int) -> dict:
    """
    Create a Moment node from a clickable hint.
    """
    moment_id = expand_name(scene, hint_data["name"])

    moment = {
        "id": moment_id,
        "text": hint_data["speaks"],
        "type": "hint",
        "tick": tick
    }

    if len(hint_data["speaks"]) > 20:
        moment["embedding"] = embed(hint_data["speaks"])

    graph.create_node("Moment", moment)

    return moment
```

===============================================================================
## PLAYER INPUT PROCESSING
===============================================================================

### Flow

```python
def process_player_input(scene: dict, player_input: dict, tick: int) -> dict:
    """
    Process player input: create Moment node, return for narrator.
    """
    moment_id = expand_name(scene, player_input["name"])

    # Determine moment type from input type
    type_map = {
        "click": "player_click",
        "freeform": "player_freeform",
        "choice": "player_choice"
    }
    moment_type = type_map.get(player_input["type"], "player_action")

    # Build moment text
    if player_input["type"] == "freeform":
        text = player_input["text"]
    elif player_input["type"] == "click":
        text = f"[Clicked: {player_input['clicked']}]"
    elif player_input["type"] == "choice":
        text = f"[Selected: {player_input['selected']}]"
    else:
        text = str(player_input)

    moment = {
        "id": moment_id,
        "text": text,
        "type": moment_type,
        "tick": tick
    }

    if len(text) > 20:
        moment["embedding"] = embed(text)

    graph.create_node("Moment", moment)

    # Link to place
    graph.create_link(moment_id, "AT", scene["where"])

    # Link to player character
    graph.create_link("char_player", "SAID", moment_id)

    return moment
```

===============================================================================
## NARRATIVE CREATION
===============================================================================

### Flow

```python
def create_narrative(mutation: dict, tick: int) -> dict:
    """
    Create narrative node. FROM links to moments created separately.
    """
    narr_node = {
        "id": mutation["id"],
        "content": mutation["content"],
        "occurred_at": mutation.get("occurred_at"),
        "tick": tick
    }

    # Add detail and embedding if provided
    if "detail" in mutation:
        narr_node["detail"] = mutation["detail"]
        if len(mutation["detail"]) > 20:
            narr_node["embedding"] = embed(mutation["detail"])

    graph.create_node("Narrative", narr_node)

    # Create ABOUT links if specified (for key things)
    if "about_things" in mutation:
        for thing_id in mutation["about_things"]:
            graph.create_link(narr_node["id"], "ABOUT", thing_id)

    # Note: FROM links to moments are created in process_narrator_output()
    return narr_node
```

===============================================================================
## BELIEF CREATION
===============================================================================

### Witnessed Belief

```python
def create_witnessed_belief(
    character: str,
    narrative: str,
    when: str,
    where: str
) -> None:
    """
    Create belief link for character who witnessed narrative.
    """
    belief = {
        "witnessed": 1.0,
        "believes": 1.0,  # Witnessing implies believing (initially)
        "source": "witnessed",
        "when": when,
        "where": where
    }

    graph.create_link(
        from_node=character,
        link_type="BELIEVES",
        to_node=narrative,
        properties=belief
    )
```

### Heard Belief (for later propagation)

```python
def create_heard_belief(
    character: str,
    narrative: str,
    from_whom: str,
    when: str,
    where: str,
    detail: str = None
) -> None:
    """
    Create belief link for character who was told about narrative.
    """
    belief = {
        "heard": 1.0,
        "believes": 0.7,  # Default partial belief for hearsay
        "source": "told",
        "from_whom": from_whom,
        "when": when,
        "where": where
    }

    if detail:
        belief["detail"] = detail
        if len(detail) > 20:
            belief["embedding"] = embed(detail)

    graph.create_link(
        from_node=character,
        link_type="BELIEVES",
        to_node=narrative,
        properties=belief
    )
```

===============================================================================
## EMBEDDING
===============================================================================

### What Gets Embedded

```python
EMBEDDABLE_FIELDS = {
    "Narrative": "detail",
    "Scene": "narration_text",
    "Character": "detail",
    "Place": "detail",
}

EMBEDDABLE_LINKS = {
    "BELIEVES": "detail",
}

MIN_TEXT_LENGTH = 20


def should_embed(text: str) -> bool:
    return text is not None and len(text) > MIN_TEXT_LENGTH


def embed(text: str) -> list[float]:
    """
    Generate embedding vector for text.
    Uses configured embedding model.
    """
    return embedding_model.encode(text)
```

### Vector Indices

```cypher
-- Create vector indices for semantic search
CREATE VECTOR INDEX narrative_emb FOR (n:Narrative) ON n.embedding
CREATE VECTOR INDEX scene_emb FOR (s:Scene) ON s.embedding
CREATE VECTOR INDEX character_emb FOR (c:Character) ON c.embedding
CREATE VECTOR INDEX place_emb FOR (p:Place) ON p.embedding
```

===============================================================================
## QUERIES
===============================================================================

### Narratives From Moment

```python
def narratives_from_moment(moment_id: str) -> list:
    """
    Find all narratives sourced from this moment.
    """
    return graph.query("""
        MATCH (n:Narrative)-[:FROM]->(m:Moment {id: $moment_id})
        RETURN n.id, n.content
    """, {"moment_id": moment_id})
```

### Moments Of Narrative

```python
def moments_of_narrative(narrative_id: str) -> list:
    """
    Get the source moments for a narrative.
    """
    return graph.query("""
        MATCH (n:Narrative {id: $id})-[:FROM]->(m:Moment)
        RETURN m.id, m.text, m.type, m.tick
    """, {"id": narrative_id})
```

### What Character Said

```python
def character_said(character_id: str) -> list:
    """
    Get all moments where this character spoke.
    """
    return graph.query("""
        MATCH (c:Character {id: $char_id})-[:SAID]->(m:Moment)
        RETURN m.id, m.text, m.tick
        ORDER BY m.tick
    """, {"char_id": character_id})
```

### Who Knows

```python
def who_knows(narrative_id: str) -> list:
    """
    Find all characters who believe a narrative and how they learned.
    """
    return graph.query("""
        MATCH (c:Character)-[b:BELIEVES]->(n:Narrative {id: $id})
        RETURN c.id, c.name, b.source, b.from_whom, b.when, b.where
    """, {"id": narrative_id})
```

### Scene History For Place

```python
def scene_history(place_id: str) -> list:
    """
    Get all scenes at a place, chronologically.
    """
    return graph.query("""
        MATCH (s:Scene)-[:AT]->(p:Place {id: $place_id})
        RETURN s.id, s.when, s.narration_text
        ORDER BY s.when
    """, {"place_id": place_id})
```

### Semantic Scene Search

```python
def search_scenes(query_text: str, limit: int = 5) -> list:
    """
    Semantic search over scene content.
    """
    query_vector = embed(query_text)
    return graph.query("""
        CALL db.idx.vector.queryNodes('scene_emb', $limit, $vector)
        YIELD node, score
        RETURN node.id, node.when, node.narration_text, score
    """, {"limit": limit, "vector": query_vector})
```

### Character Witnessed On Day

```python
def witnessed_on_day(character_id: str, day: str) -> list:
    """
    What narratives did this character witness on a given day?
    """
    return graph.query("""
        MATCH (s:Scene)-[:INVOLVES]->(c:Character {id: $char_id})
        WHERE s.when STARTS WITH $day
        MATCH (s)-[:CREATES]->(n:Narrative)
        RETURN s.when, n.id, n.content
        ORDER BY s.when
    """, {"char_id": character_id, "day": day})
```

===============================================================================
## THE FULL CHAIN
===============================================================================

### Step-by-Step Example

**1. Narrator outputs scene:**

```json
{
  "scene": {
    "when": "Day 5, dusk",
    "where": "place_crossing",
    "present": ["char_player", "char_aldric"]
  },
  "narration": [
    {
      "name": "blade_broken",
      "text": "The blade lies in two pieces at his feet.",
      "clickable": {
        "blade": {
          "speaks": "That was his father's sword.",
          "name": "blade_hint"
        }
      }
    },
    {
      "name": "aldric_done",
      "speaker": "char_aldric",
      "text": "It's done. He's done."
    }
  ],
  "mutations": [
    {
      "type": "new_narrative",
      "id": "narr_sword_broken",
      "content": "Aldric's sword broke killing the Dane",
      "sources": ["blade_broken", "aldric_done"]
    }
  ]
}
```

**2. System creates Scene node:**

```yaml
Scene:
  id: scene_d5_dusk_crossing
  when: "Day 5, dusk"
  tick: 142
```

**3. System creates Moment nodes:**

```yaml
Moment:
  id: crossing_d5_dusk_blade_broken
  text: "The blade lies in two pieces at his feet."
  type: narration
  tick: 142
  embedding: [0.123, -0.456, ...]

Moment:
  id: crossing_d5_dusk_blade_hint
  text: "That was his father's sword."
  type: hint
  tick: 142

Moment:
  id: crossing_d5_dusk_aldric_done
  text: "It's done. He's done."
  type: dialogue
  tick: 142
```

**4. System creates Moment links:**

```
scene_d5_dusk_crossing -[CONTAINS]-> crossing_d5_dusk_blade_broken
scene_d5_dusk_crossing -[CONTAINS]-> crossing_d5_dusk_blade_hint
scene_d5_dusk_crossing -[CONTAINS]-> crossing_d5_dusk_aldric_done

crossing_d5_dusk_blade_broken -[AT]-> place_crossing
crossing_d5_dusk_aldric_done -[AT]-> place_crossing

char_aldric -[SAID]-> crossing_d5_dusk_aldric_done

crossing_d5_dusk_blade_broken -[THEN]-> crossing_d5_dusk_aldric_done
```

**5. System creates Narrative with FROM links:**

```yaml
Narrative:
  id: narr_sword_broken
  content: "Aldric's sword broke killing the Dane"
  occurred_at: "Day 5, dusk"
  tick: 142
```

```
narr_sword_broken -[FROM]-> crossing_d5_dusk_blade_broken
narr_sword_broken -[FROM]-> crossing_d5_dusk_aldric_done
scene_d5_dusk_crossing -[CREATES]-> narr_sword_broken
```

**6. System creates beliefs:**

```yaml
char_player -[BELIEVES]-> narr_sword_broken:
  witnessed: 1.0
  believes: 1.0
  source: witnessed
  when: "Day 5, dusk"
  where: place_crossing

char_aldric -[BELIEVES]-> narr_sword_broken:
  witnessed: 1.0
  believes: 1.0
  source: witnessed
  when: "Day 5, dusk"
  where: place_crossing
```

**7. System links Scene:**

```
scene_d5_dusk_crossing -[AT]-> place_crossing
scene_d5_dusk_crossing -[INVOLVES]-> char_player
scene_d5_dusk_crossing -[INVOLVES]-> char_aldric
```

**8. Player clicks "blade":**

```json
{
  "type": "click",
  "name": "rolf_asks_blade",
  "clicked": "blade",
  "from": "crossing_d5_dusk_blade_hint"
}
```

System creates player Moment:

```yaml
Moment:
  id: crossing_d5_dusk_rolf_asks_blade
  text: "[Clicked: blade]"
  type: player_click
  tick: 143
```

```
char_player -[SAID]-> crossing_d5_dusk_rolf_asks_blade
crossing_d5_dusk_rolf_asks_blade -[AT]-> place_crossing
```

**9. Narrator responds, creates more narratives with FROM links:**

```
narr_oathblade_history -[FROM]-> crossing_d5_dusk_rolf_asks_blade
narr_oathblade_history -[FROM]-> crossing_d5_dusk_aldric_explains
narr_oathblade_history -[FROM]-> crossing_d5_dusk_blade_broken
```

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **VALIDATION.md** — How do we verify this works correctly?
