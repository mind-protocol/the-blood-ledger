# History — Behaviors: Observable Memory Effects

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_History.md
THIS:        BEHAVIORS_History.md (you are here)
ALGORITHM:   ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:  ./VALIDATION_History.md
IMPLEMENTATION: ./IMPLEMENTATION_History_Service_Architecture.md
TEST:        ./TEST/TEST_Overview.md
SYNC:        ./SYNC_History.md
```

---

## BEHAVIORS

### B1: Player Queries Past — Character Context

```
GIVEN:  Player asks "What did Aldric tell me about his brother?"
WHEN:   Narrator processes the query
THEN:   System queries player's BELIEVES links for narratives about Aldric and "brother"
AND:    Returns narrative with source pointing to conversation section
AND:    Narrator reads that conversation section for full dialogue
AND:    Response includes Aldric's exact words from that conversation
```

### B2: Player Queries Past — World Events

```
GIVEN:  Player asks "What happened at York while I was gone?"
WHEN:   Narrator processes the query
THEN:   System queries narratives with OCCURRED_AT link to place_york
AND:    Filters by player's BELIEVES links (only what player knows)
AND:    Returns narratives with detail field (world-generated history)
AND:    Response uses the narrative detail, not conversation (none exists)
```

### B3: Creating Player-Experienced History

```
GIVEN:  Scene where significant event occurs (player kills guard)
WHEN:   Narrator processes the scene outcome
THEN:   Appends full exchange to conversation thread file
AND:    Creates narrative with source.file and source.section pointing to that exchange
AND:    Creates BELIEVES links for all characters present
AND:    Each BELIEVES link has source: "participated" or "witnessed"
```

### B4: Creating World-Generated History

```
GIVEN:  Runner processes a tension break off-screen (York uprising)
WHEN:   No player is present
THEN:   Creates narrative with detail field containing full description
AND:    Creates BELIEVES links for characters who would know
AND:    Propagates beliefs based on proximity and communication patterns
AND:    Player does NOT automatically receive the belief
```

### B5: Character Memory Surfaces in Scene

```
GIVEN:  Player interacts with Aldric
AND:    High-weight narrative exists where Aldric BELIEVES something about player
WHEN:   Narrator constructs scene context
THEN:   That narrative enters context
AND:    Aldric's dialogue can reference the memory
AND:    Reference is organic, not forced ("Remember when you..." feels natural)
```

### B6: Chronicle View Assembly

```
GIVEN:  Player opens Chronicle view
WHEN:   System assembles history display
THEN:   Queries all narratives player BELIEVES
AND:    Orders by occurred_at timestamp
AND:    Displays as chronological record of player's memories
AND:    Does NOT show events player doesn't know about
```

---

## INPUTS / OUTPUTS

### Primary Function: `query_history()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| character_id | string | Who is asking (determines belief filter) |
| about_person | string? | Character the query is about |
| about_place | string? | Place the query is about |
| time_range | tuple? | (Day start, Day end) to filter by |
| topic | string? | Free text for semantic matching |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| narratives | List[Narrative] | Matching narratives with source/detail |
| conversations | List[ConversationSection]? | Full text if source exists |

**Side Effects:**

- None (read-only query)

### Primary Function: `record_history()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| event_type | enum | "player_experienced" or "world_generated" |
| narrative_content | string | Summary of what happened |
| detail | string? | Full description (world-generated only) |
| conversation_ref | dict? | {file, section} (player-experienced only) |
| occurred_at | string | "Day N, time" |
| occurred_where | string | place_id (creates OCCURRED_AT link) |
| about | dict | {characters: [], places: [], things: []} |
| witnesses | List[string] | Character IDs present |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| narrative_id | string | Created narrative node ID |
| belief_ids | List[string] | Created BELIEVES link IDs |

**Side Effects:**

- Creates narrative node in graph
- Creates BELIEVES links for witnesses
- Appends to conversation thread file (if player_experienced)

---

## EDGE CASES

### E1: Empty History

```
GIVEN:  Player queries about something they never learned
THEN:   Returns empty result
AND:    Narrator can truthfully say "You don't know anything about that"
```

### E2: Conflicting Memories

```
GIVEN:  Player BELIEVES narr_betrayal (Edmund stole inheritance)
AND:    Edmund BELIEVES narr_salvation (he saved the family)
THEN:   Both beliefs exist separately
AND:    No automatic resolution
AND:    Conflict surfaces when they meet (tension system handles this)
```

### E3: Rumor Chain

```
GIVEN:  Character A witnesses event
AND:    Tells Character B
AND:    B tells C
THEN:   A BELIEVES with source: "witnessed", believes: 1.0
AND:    B BELIEVES with source: "told", believes: 0.9
AND:    C BELIEVES with source: "rumor", believes: 0.6
AND:    Each has correct when/where for when they learned
```

### E4: Learning You Were Wrong

```
GIVEN:  Player BELIEVES narr_betrayal with truth: 0.3
AND:    Player discovers evidence contradicting this
THEN:   New narrative created (narr_salvation_learned)
AND:    Old belief may remain but weight decreases
AND:    Or: Old BELIEVES link modified with lower confidence
```

---

## ANTI-BEHAVIORS

### A1: Omniscient Queries

```
GIVEN:   Player
WHEN:    Queries "What happened at York?" (without having learned)
MUST NOT: Return events player hasn't heard about
INSTEAD:  Return only narratives player BELIEVES about York
```

### A2: Lost Conversations

```
GIVEN:   Player-experienced event with full dialogue
WHEN:    System retrieves this history later
MUST NOT: Return only the summary narrative content
INSTEAD:  Retrieve and return the actual conversation section
```

### A3: Automatic Belief Synchronization

```
GIVEN:   Two characters with conflicting beliefs meet
WHEN:    No explicit confrontation occurs
MUST NOT: Automatically align their beliefs
INSTEAD:  Keep beliefs separate until tension system triggers break
```

### A4: Mixing History Sources

```
GIVEN:   World-generated narrative (has detail, no source)
WHEN:    Retrieving history
MUST NOT: Try to find conversation that doesn't exist
INSTEAD:  Use detail field for world-generated, source for player-experienced
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] How does confidence decay over time?
- [ ] Should player be able to write journal entries that become narratives?
- IDEA: Visual indicator in Chronicle for confidence level
- IDEA: "Heard from" chain visualization for rumors
- QUESTION: Can player actively try to remember something (boost weight)?
