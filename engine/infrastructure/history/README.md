# History Module

**History is distributed, not centralized.**

There is no event log. There is no timeline table. There is no master record of "what happened."

Instead, the past exists as:
- **Narratives** — stories about what happened
- **Beliefs** — who knows those stories, and how they learned them
- **Conversation threads** — the actual words exchanged (for player-experienced history)

Every query about the past is a query about what characters *know* and *remember*. There is no omniscient view.

## Core Principle

The player's history is what the player believes. Aldric's history is what Aldric believes. **They may differ.**

## Two Sources of History

| Source | Storage | When Used |
|--------|---------|-----------|
| **Player-experienced** | Conversation thread file + narrative with `source` reference | Events in scenes |
| **World-generated** | Narrative with `detail` field | Off-screen events |

### Player-Experienced History

When something happens in a scene, the conversation IS the history:

```python
history.record_player_history(
    content="Aldric told me about his brother's death",
    conversation_text='''
Aldric stares into the fire.

You: "You fought at Stamford Bridge."
Aldric: "Aye."
You: "What happened?"
Aldric: *long pause* "My brother held the bridge."
''',
    character_id="char_aldric",
    witnesses=["player", "char_aldric"],
    occurred_at="Day 4, night",
    occurred_where="place_camp",
    place_name="The Camp"
)
```

This creates:
1. A section in `conversations/aldric.md`
2. A narrative pointing to that section
3. BELIEVES edges for player and Aldric

### World-Generated History

When something happens off-screen, the narrative carries its own detail:

```python
history.record_world_history(
    content="Saxon thegns seized York",
    detail='''
The rebellion began at dawn. Saxon thegns overwhelmed
the garrison before the Normans could arm. Robert Cumin
died in the bishop's house, trapped by flames.
''',
    occurred_at="Day 12, dawn",
    occurred_where="place_york",
    witnesses=["char_malet"],
    propagate=True  # Spread news to nearby characters
)
```

## Usage

### Initialize

```python
from engine.history import HistoryService
from engine.db.graph_queries import GraphQueries
from engine.db.graph_ops import GraphOps

history = HistoryService(
    graph_queries=GraphQueries(),
    graph_ops=GraphOps(),
    conversations_dir="playthroughs/abc123/conversations"
)
```

### Query History

```python
# What does the player know about Aldric?
memories = history.query_history(
    character_id="player",
    about_person="char_aldric"
)

# What does the player know happened at York?
york_history = history.query_history(
    character_id="player",
    about_place="place_york"
)

# What happened between Day 5 and Day 10?
recent = history.query_history(
    character_id="player",
    time_start="Day 5, dawn",
    time_end="Day 10, night"
)

# Search by topic
oaths = history.query_history(
    character_id="player",
    topic="oath"
)
```

### Find Who Knows

```python
# Who knows about the guard's death?
witnesses = history.who_knows("narr_guard_killed", min_confidence=0.5)

# What history do player and Aldric share?
shared = history.get_shared_history("player", "char_aldric")
```

## Conversation Files

Conversation threads are markdown files:

```
playthroughs/{id}/conversations/
├── aldric.md
├── edmund.md
└── mildred.md
```

Each file contains sections:

```markdown
# Conversations with Aldric

## Day 4, Night — The Camp

Aldric stares into the fire...

## Day 7, Morning — The Road

The morning is cold...
```

### Reading Sections

```python
from engine.history import ConversationThread

threads = ConversationThread("playthroughs/abc123/conversations")

# Read a specific section
content = threads.read_section(
    file_path="conversations/aldric.md",
    section_header="Day 4, Night — The Camp"
)

# List all sections
sections = threads.list_sections("char_aldric")

# Search for sections containing a keyword
results = threads.search_sections("char_aldric", "brother")
```

## Timestamps

Format: `Day {n}, {time_of_day}`

Valid times: `dawn`, `morning`, `midday`, `afternoon`, `dusk`, `evening`, `night`, `midnight`

```python
from engine.models.base import GameTimestamp, TimeOfDay

# Parse
ts = GameTimestamp.parse("Day 4, night")

# Create
ts = GameTimestamp(day=4, time=TimeOfDay.NIGHT)

# Compare
ts1 < ts2  # Earlier
ts1 > ts2  # Later

# String
str(ts)  # "Day 4, night"
```

## API Reference

### HistoryService

| Method | Description |
|--------|-------------|
| `query_history(character_id, ...)` | Query what a character knows about the past |
| `record_player_history(...)` | Record an event from a scene |
| `record_world_history(...)` | Record an off-screen event |
| `who_knows(narrative_id)` | Find all characters who know about something |
| `get_shared_history(char_a, char_b)` | Find narratives both characters believe |

### ConversationThread

| Method | Description |
|--------|-------------|
| `append_section(...)` | Add a new conversation section |
| `read_section(file, header)` | Read a specific section |
| `list_sections(character_id)` | List all section headers |
| `get_full_thread(character_id)` | Get complete conversation file |
| `search_sections(character_id, keyword)` | Find sections containing keyword |

## Data Model

### Narrative (extended fields)

```python
# When did this happen?
occurred_at: str      # "Day 4, night"

# Where did this happen? (OCCURRED_AT link to Place, not attribute)
# (Narrative)-[:OCCURRED_AT]->(Place)

# Content source (ONE of these)
source: NarrativeSource  # {file, section} for player-experienced
detail: str              # Full text for world-generated
```

### BELIEVES Edge (extended)

```python
where: str  # Place ID where they learned this
```

## Design Rationale

See `docs/history/PATTERNS_History.md` for the full design philosophy.

Key insights:
- **Beliefs over facts** — No character has direct access to "what happened"
- **Two sources, two formats** — Player-experienced has conversations; world-generated has detail
- **Timestamps as structure** — Enable queries like "where was I three days ago?"

## Testing

```bash
# Run history tests
cd engine
pytest tests/test_history.py -v

# Run with coverage
pytest tests/test_history.py --cov=history
```

## Files

```
engine/history/
├── __init__.py         # Exports
├── README.md           # This file
├── service.py          # HistoryService
└── conversations.py    # ConversationThread

engine/tests/
└── test_history.py     # Tests
```
