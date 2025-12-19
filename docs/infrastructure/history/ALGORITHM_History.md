# History — Algorithm: Retrieval and Recording Procedures

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_History.md
BEHAVIORS:   ./BEHAVIORS_History.md
THIS:        ALGORITHM_History.md (you are here)
VALIDATION:  ./VALIDATION_History.md
IMPLEMENTATION: ./IMPLEMENTATION_History_Service_Architecture.md
TEST:        ./TEST_History.md
SYNC:        ./SYNC_History.md
```

---

## OVERVIEW

The History system has two primary operations:

1. **Retrieval** — Querying the graph for what a character knows about the past
2. **Recording** — Creating narratives and beliefs when events occur

Both operations are graph-native. History isn't a separate data structure — it's narrative nodes with BELIEVES edges, queryable through Cypher.

---

## DATA STRUCTURES

### Narrative Node (History-Relevant Fields)

```
Narrative {
    id: string              // narr_{description}
    type: string            // "memory", "event", "secret", etc.
    content: string         // Summary: "Aldric told me about his brother"

    // Temporal
    occurred_at: string     // "Day 4, night"
    // occurred_where is OCCURRED_AT link to Place, not attribute
    created_at: string      // When narrative entered graph

    // Content (one of these)
    source: {               // For player-experienced
        file: string        // "conversations/char_aldric.md"
        section: string     // "Day 4, Night — The Camp"
    }
    detail: string          // For world-generated (full description)

    // Connections
    about: {
        characters: [string]
        places: [string]
        things: [string]
    }
}
```

### BELIEVES Edge

```
BELIEVES {
    believes: float         // 0.0-1.0 confidence
    source: string          // "witnessed" | "told" | "rumor" | "deduced" | "participated"
    when: string            // "Day 5, dusk"
    where: string           // place_id where learned
    heard: float?           // 0.0-1.0 how directly (1.0 = witnessed, 0.5 = secondhand)
}
```

### Conversation Thread (Markdown File)

```markdown
# Conversations with {Character}

## Day 4, Night — The Camp

{Full dialogue and narration}

## Day 7, Morning — The Road

{Full dialogue and narration}
```

---

## ALGORITHM: query_history()

Retrieves what a character knows about the past.

### Step 1: Build Base Query

Start with the character's beliefs:

```cypher
MATCH (c:Character {id: $character_id})-[b:BELIEVES]->(n:Narrative)
```

### Step 2: Apply Filters

Add filters based on parameters:

```cypher
// If about_person specified
WHERE n.about_characters CONTAINS $about_person

// If about_place specified
WHERE n.about_places CONTAINS $about_place
   OR EXISTS((n)-[:OCCURRED_AT]->(:Place {id: $about_place}))

// If time_range specified
WHERE n.occurred_at >= $time_start
  AND n.occurred_at <= $time_end

// If topic specified (semantic - may need full-text or LLM)
WHERE n.content CONTAINS $topic
```

### Step 3: Order and Return

```cypher
OPTIONAL MATCH (n)-[:OCCURRED_AT]->(place:Place)
RETURN n.id, n.content, n.source, n.detail, n.occurred_at, place.id AS occurred_where, b.believes, b.source
ORDER BY n.occurred_at DESC
```

### Step 4: Enrich with Conversations

For each narrative with `source.file`:

```python
def enrich_with_conversation(narrative):
    if narrative.source:
        file_path = narrative.source.file
        section = narrative.source.section
        conversation_text = read_markdown_section(file_path, section)
        narrative.conversation = conversation_text
    return narrative
```

---

## ALGORITHM: record_player_history()

Records an event that happened in a scene.

### Step 1: Append to Conversation Thread

```python
def append_conversation(character_id, day, time, location, dialogue):
    file_path = f"conversations/char_{character_id}.md"
    section_header = f"## {day}, {time} — {location}"

    with open(file_path, 'a') as f:
        f.write(f"\n{section_header}\n\n")
        f.write(dialogue)
        f.write("\n")

    return {
        "file": file_path,
        "section": section_header
    }
```

### Step 2: Create Narrative Node with OCCURRED_AT Link

```cypher
CREATE (n:Narrative {
    id: $narrative_id,
    type: 'memory',
    content: $content,
    occurred_at: $occurred_at,
    created_at: $now,
    source: $source_ref,
    about: $about
})
WITH n
MATCH (p:Place {id: $occurred_where})
CREATE (n)-[:OCCURRED_AT]->(p)
RETURN n.id
```

### Step 3: Create BELIEVES Links

For each witness:

```cypher
MATCH (c:Character {id: $witness_id})
MATCH (n:Narrative {id: $narrative_id})
CREATE (c)-[b:BELIEVES {
    believes: $confidence,
    source: $witness_type,  // "participated" or "witnessed"
    when: $occurred_at,
    where: $occurred_where,
    heard: 1.0
}]->(n)
```

---

## ALGORITHM: record_world_history()

Records an event that happened off-screen.

### Step 1: Create Narrative with Detail and OCCURRED_AT Link

```cypher
CREATE (n:Narrative {
    id: $narrative_id,
    type: 'event',
    content: $content,
    occurred_at: $occurred_at,
    created_at: $now,
    detail: $detail,
    about: $about
})
WITH n
MATCH (p:Place {id: $occurred_where})
CREATE (n)-[:OCCURRED_AT]->(p)
RETURN n.id
```

No conversation thread — the `detail` field IS the content.

### Step 2: Create Initial BELIEVES Links

For characters directly involved:

```cypher
// Direct participants
MATCH (c:Character {id: $participant_id})
MATCH (n:Narrative {id: $narrative_id})
CREATE (c)-[b:BELIEVES {
    believes: 1.0,
    source: 'participated',
    when: $occurred_at,
    where: $occurred_where,
    heard: 1.0
}]->(n)
```

### Step 3: Propagate Beliefs

News spreads based on proximity and time:

```python
def propagate_belief(narrative_id, origin_place, origin_time):
    # Characters at origin place learn immediately
    nearby = get_characters_at_place(origin_place, origin_time)
    for char in nearby:
        create_belief(char, narrative_id,
            believes=0.9, source='witnessed', heard=0.9)

    # Characters in connected places learn over time
    for place, distance in get_connected_places(origin_place):
        delay = distance  # days to travel
        affected = get_characters_at_place(place, origin_time + delay)
        for char in affected:
            confidence = 0.7 - (distance * 0.1)  # degrades with distance
            create_belief(char, narrative_id,
                believes=confidence, source='rumor', heard=0.5)
```

---

## KEY DECISIONS

### D1: Source vs Detail

```
IF narrative has source.file:
    // Player-experienced — read conversation
    content = read_markdown_section(source.file, source.section)
    // Full dialogue available
ELSE IF narrative has detail:
    // World-generated — use inline description
    content = narrative.detail
    // No dialogue, but complete description
ELSE:
    // Minimal — only summary available
    content = narrative.content
```

### D2: Confidence Calculation for Rumors

```
heard_directly = 1.0
told_by_witness = 0.8
secondhand = 0.6
rumor = 0.4

confidence = base_confidence * heard_factor * time_decay
```

---

## DATA FLOW

```
Event Occurs
    ↓
[Player present?]
    ↓ Yes                    ↓ No
Append Conversation      Create detail field
    ↓                        ↓
Create Narrative         Create Narrative
    ↓                        ↓
Create BELIEVES          Propagate BELIEVES
    ↓                        ↓
Graph Updated            Graph Updated
```

---

## COMPLEXITY

**query_history():**

Time: O(B) where B = number of beliefs for character
Space: O(N) where N = matching narratives
Bottleneck: Full-text search on topic, if used

**record_player_history():**

Time: O(W) where W = number of witnesses
Space: O(1) — creates fixed number of nodes/edges
Bottleneck: File append for conversation thread

**record_world_history() with propagation:**

Time: O(P * C) where P = connected places, C = characters per place
Space: O(P * C) — creates belief per affected character
Bottleneck: Propagation can create many beliefs

---

## HELPER FUNCTIONS

### `read_markdown_section(file, section_header)`

**Purpose:** Extract a specific section from a conversation file

**Logic:**
- Read file
- Find section header
- Return content until next ## header or EOF

### `get_characters_at_place(place_id, time)`

**Purpose:** Find who was at a location at a given time

**Logic:**
```cypher
MATCH (c:Character)-[p:PRESENT]->(place:Place {id: $place_id})
WHERE p.arrived_at <= $time
  AND (p.left_at IS NULL OR p.left_at > $time)
RETURN c.id
```

### `create_belief(char_id, narrative_id, believes, source, heard)`

**Purpose:** Create a BELIEVES edge with proper attributes

**Logic:** Single Cypher CREATE statement

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Graph | Cypher queries | Narrative nodes, BELIEVES edges |
| File System | read_markdown_section() | Conversation text |
| Narrator | query_history() results | Context for scene |
| Runner | record_world_history() | Narrative ID |

---

## COMMON QUERIES

### What happened at this place?

```cypher
MATCH (n:Narrative)
OPTIONAL MATCH (n)-[:OCCURRED_AT]->(place:Place)
WHERE n.about_places CONTAINS $place_id
   OR place.id = $place_id
RETURN n.content, n.detail, n.source, n.occurred_at
ORDER BY n.occurred_at
```

### What do I know about this person?

```cypher
MATCH (p:Character {id: 'player'})-[b:BELIEVES]->(n:Narrative)
WHERE n.about_characters CONTAINS $character_id
RETURN n.content, n.source, n.detail, b.when
ORDER BY b.when
```

### Have we met before?

```cypher
MATCH (p:Character {id: 'player'})-[:BELIEVES]->(n:Narrative)<-[:BELIEVES]-(character:Character {id: $npc_id})
OPTIONAL MATCH (n)-[:OCCURRED_AT]->(place:Place)
RETURN n.content, n.occurred_at, place.id AS occurred_where
```

### Where was I three days ago?

```cypher
MATCH (p:Character {id: 'player'})-[at:PRESENT]->(place:Place)
WHERE at.arrived_at <= 'Day 3'
  AND (at.left_at IS NULL OR at.left_at >= 'Day 3')
RETURN place.name
```

### Who knows I killed the guard?

```cypher
MATCH (c:Character)-[b:BELIEVES]->(n:Narrative {id: 'narr_guard_killed'})
WHERE b.heard > 0.5
RETURN c.name, b.source, b.when
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Full-text search on narrative content — FalkorDB capability?
- [ ] Timestamp comparison as strings vs. parsed
- [ ] Batch propagation for efficiency
- IDEA: Index narratives by about_characters for faster lookup
- IDEA: Cache frequently-accessed conversation sections
- QUESTION: How to handle very long games with thousands of narratives?
