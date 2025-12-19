# History — Algorithm: Query and Record

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:    ../PATTERNS_History.md
BEHAVIORS:   ../BEHAVIORS_History.md
THIS:        ALGORITHM_Query_and_Record.md
OVERVIEW:    ./ALGORITHM_Overview.md
PROPAGATION: ./ALGORITHM_Propagation_and_Beliefs.md
VALIDATION:  ../VALIDATION_History.md
IMPLEMENTATION: ../IMPLEMENTATION_History_Service_Architecture.md
TEST:        ../TEST/TEST_Overview.md
SYNC:        ../SYNC_History.md
```

---

## DATA STRUCTURES

### Narrative Node (History-Relevant Fields)

```
Narrative {
    id: string              // narr_{description}
    type: string            // "memory", "event", "secret", etc.
    content: string         // Summary

    // Temporal
    occurred_at: string     // "Day 4, night"
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
```

---

## ALGORITHM: query_history()

Retrieves what a character knows about the past.

### Step 1: Base Query

Start with the character's beliefs:

```cypher
MATCH (c:Character {id: $character_id})-[b:BELIEVES]->(n:Narrative)
```

### Step 2: Filters

Apply filters for person/place/time/topic as provided.

### Step 3: Order + Return

Return narrative fields plus belief metadata, ordered by `occurred_at`.

### Step 4: Conversation Enrichment

If narrative has `source.file`, read the referenced markdown section and attach the conversation text.

---

## ALGORITHM: record_player_history()

Records an event that happened in a scene.

### Step 1: Append to Conversation Thread

Append dialogue to a character-specific markdown thread and return `{file, section}`.

### Step 2: Create Narrative Node + OCCURRED_AT

Create a narrative with `source` reference and link it to the place via `OCCURRED_AT`.

### Step 3: Create BELIEVES Links

Create BELIEVES edges for all witnesses, with `source` set to `participated` or `witnessed`.

---

## ALGORITHM: record_world_history()

Records an event that happened off-screen.

### Step 1: Create Narrative with Detail + OCCURRED_AT

Create a narrative with `detail` and link it to the place via `OCCURRED_AT`.

### Step 2: Create BELIEVES Links

Create BELIEVES edges for direct witnesses, then hand off to propagation.

---

## KEY DECISIONS

### D1: Source vs Detail

```
IF narrative has source.file:
    // Player-experienced — read conversation
    content = read_markdown_section(source.file, source.section)
ELSE IF narrative has detail:
    // World-generated — use inline description
    content = narrative.detail
ELSE:
    // Minimal — only summary available
    content = narrative.content
```
