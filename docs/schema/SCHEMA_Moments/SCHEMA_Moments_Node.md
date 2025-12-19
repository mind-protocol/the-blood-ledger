# Moment Node Schema

Purpose: A single unit of narrated content shown to the player.

When to create:
- Dialogue, narration, player input, or generated hints

Attributes:
```yaml
id: string
text: string
type: enum [narration, dialogue, thought, action, montage, hint, player_click, player_freeform, player_choice]
status: enum [possible, active, spoken, dormant, decayed]
weight: float
energy: float
tone: string
duration: integer
tick_created: integer
tick_spoken: integer
tick_decayed: integer
line: integer
embedding: float[]
```

Action fields (type=action):
```yaml
action: enum [travel, attack, take, give, use]
```

Query fields (handler -> Question Answerer):
```yaml
query: string
query_type: enum [backstory_gap, world_fact, relationship]
query_filled: boolean
```

Status flow:
```
possible -> active -> spoken
  |          |
  |          +-> dormant -> possible
  +-> decayed
```
