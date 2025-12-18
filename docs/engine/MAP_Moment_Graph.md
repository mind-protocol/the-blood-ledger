# Moment Graph Architecture — System Map

```
STATUS: Reference Map
CREATED: 2024-12-17
```

---

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THREE AGENT LEVELS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                 │
│  │   WORLD     │      │   SCENE     │      │  CHARACTER  │                 │
│  │   RUNNER    │      │   NARRATOR  │      │   CITIZEN   │                 │
│  ├─────────────┤      ├─────────────┤      ├─────────────┤                 │
│  │ Tick-based  │      │ On-demand   │      │ Parallel    │                 │
│  │ Pressure    │      │ Moments     │      │ Background  │                 │
│  │ Time        │      │ Transitions │      │ Thoughts    │                 │
│  │ Consequences│      │ Fallback    │      │ Freeform    │                 │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                 │
│         │                    │                    │                         │
│         └────────────────────┴────────────────────┘                         │
│                              │                                              │
│                              ▼                                              │
│                    ┌─────────────────┐                                      │
│                    │   THE GRAPH     │                                      │
│                    │   (Neo4j/AGE)   │                                      │
│                    └─────────────────┘                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Moment Lifecycle

```
                    ┌──────────────┐
                    │   POSSIBLE   │ ◄─── Created by: Narrator, Citizen, World Runner
                    │  weight < 0.8│
                    └──────┬───────┘
                           │
              weight > 0.8 │ (flip detection)
                           ▼
                    ┌──────────────┐
                    │    ACTIVE    │ ◄─── Visible to player
                    │  can surface │      Can be clicked/triggered
                    └──────┬───────┘
                           │
              clicked or   │ triggered
                           ▼
                    ┌──────────────┐
                    │    SPOKEN    │ ◄─── In transcript
                    │  history     │      Creates THEN links
                    └──────┬───────┘
                           │
              player leaves│ location
                           ▼
                    ┌──────────────┐
                    │   DORMANT    │ ◄─── Waiting for return
                    │  persistent  │      (if persistent=true)
                    └──────┬───────┘
                           │
              weight < 0.1 │ or not persistent
                           ▼
                    ┌──────────────┐
                    │   DECAYED    │ ◄─── Pruned
                    │  garbage     │
                    └──────────────┘
```

---

## Link Types

```
CHARACTER ────[CAN_SPEAK]────► MOMENT
    │                            │
    │                            │
    └────[BELIEVES]────► NARRATIVE ◄────[ATTACHED_TO]────┘
                            │
                            │
                    [ATTACHED_TO]
                            │
                            ▼
                    ┌───────────────┐
                    │ PLACE | THING │
                    │   TENSION     │
                    └───────────────┘


MOMENT ────[CAN_LEAD_TO]────► MOMENT
  │                             │
  │  trigger: click|wait|auto   │
  │  require_words: [...]       │
  │  weight_transfer: 0.3       │
  │                             │
  └────────[THEN]───────────────┘
           tick: int
           player_caused: bool
```

---

## Phase Dependencies

```
                    ┌─────────────────┐
                    │    PHASE 1      │
                    │  Core Graph     │
                    │  MVP - No LLM   │
                    │  Rating: 8.8    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    PHASE 2      │
                    │  Energy Flow    │
                    │  Semantic Boost │
                    │  Rating: 8.8    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    PHASE 3      │
                    │  Citizens       │
                    │  Background LLM │
                    │  Rating: 9.0    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    PHASE 4      │
                    │  Social         │
                    │  Multi-Agent    │
                    │  Rating: 9.3    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    PHASE 5      │
                    │  Natural        │
                    │  Polish         │
                    │  Rating: 9.3    │
                    └─────────────────┘
```

---

## Critical 10/10 Patterns (Must Have)

| ID | Name | Phase | One-Line |
|----|------|-------|----------|
| P1.1 | Click Traversal | 1 | Instant response, no LLM |
| B1.1 | Instant Click | 1 | <50ms response |
| B1.3 | Conversation Persistence | 1 | NPCs remember mid-conversation |
| P2.1 | Semantic Boost | 2 | Free input matches moments |
| B2.1 | Freeform Without LLM | 2 | Semantic match, no wait |
| B2.2 | Characters Initiate | 2 | NPCs speak unprompted |
| P3.4 | Citizen Freeform | 3 | Character answers in voice |
| B3.2 | Proactive Dialogue | 3 | NPCs have things to say |
| B3.6 | Instant Freeform | 3 | Direct address works |
| P4.1 | Witness Reaction | 4 | Third parties notice |
| P4.2 | Char-to-Char | 4 | NPCs talk to each other |
| P4.7 | Party Memory | 4 | Shared experiences |
| B4.2 | Overhearing | 4 | Presence matters |
| B4.5 | NPCs Argue | 4 | Drama without player |
| B4.7 | Remember When | 4 | Location triggers memory |
| P5.2 | Autonomous | 5 | Characters erupt |
| P5.5 | Evolution | 5 | Repeated themes intensify |
| P5.7 | Heavy Reaction | 5 | Big events = big response |

---

## World Runner Integration

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CURRENT WORLD RUNNER FLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Tension Flip ──► World Runner ──► mutations/wr_{id}.yaml         │
│                         │                                           │
│                         └──────► injection_queue.json               │
│                                         │                           │
│                                         ▼                           │
│                                    Narrator                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    NEW WORLD RUNNER FLOW                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Tension Flip ──► World Runner ──► mutations/wr_{id}.yaml         │
│                         │               │                           │
│                         │               ├── nodes: [...moments]     │
│                         │               ├── links: [...moment links]│
│                         │               └── moment_activations: []  │
│                         │                                           │
│                         └──────► injection_queue.json               │
│                                         │                           │
│                                         ├── type: "event"           │
│                                         ├── type: "moment_activation"│
│                                         └── type: "moment_creation" │
│                                         │                           │
│                                         ▼                           │
│                                    Narrator                         │
│                                         │                           │
│                              ┌──────────┴──────────┐                │
│                              ▼                     ▼                │
│                     Surface Moments        LLM Fallback             │
│                     (from graph)           (if no match)            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Schema Delta Summary

```yaml
# ADDITIONS TO SCHEMA.md

moment:
  # NEW FIELDS
  status: enum [possible, active, spoken, dormant, decayed]
  weight: float
  tone: string
  tick_created: integer
  tick_spoken: integer
  tick_decayed: integer

# NEW LINK TYPES

CAN_SPEAK:
  from: character
  to: moment
  weight: float

ATTACHED_TO:
  from: moment
  to: [character, place, thing, narrative, tension]
  presence_required: boolean
  persistent: boolean
  dies_with_target: boolean

CAN_LEAD_TO:
  from: moment
  to: moment
  trigger: enum [click, wait, auto, semantic]
  require_words: array[string]
  require_similarity: float
  wait_ticks: integer
  bidirectional: boolean
  consumes_origin: boolean
  weight_transfer: float

# MODIFIED LINK

THEN:
  # ADD
  player_caused: boolean
```

---

## Key Queries

### Get Current View (Phase 1)
```cypher
MATCH (m:Moment)
WHERE m.status IN ['possible', 'active']
WITH m, [(m)-[r:ATTACHED_TO WHERE r.presence_required]->(t) | t] AS required
WHERE ALL(t IN required WHERE is_present(t))
RETURN m ORDER BY m.weight DESC LIMIT 20
```

### Semantic Boost (Phase 2)
```cypher
MATCH (m:Moment)
WHERE m.status IN ['possible', 'active']
RETURN m, vector_similarity(m.embedding, $input_embedding) AS score
ORDER BY score DESC LIMIT 5
```

### Citizen Context (Phase 3)
```cypher
MATCH (c:Character {id: $id})
OPTIONAL MATCH (c)-[b:BELIEVES]->(n:Narrative)
OPTIONAL MATCH (c)-[:AT]->(loc:Place)
OPTIONAL MATCH (c)-[:KNOWS]->(other:Character)
OPTIONAL MATCH (t:Tension)-[:INVOLVES]->(c)
OPTIONAL MATCH (c)-[:CARRIES]->(thing:Thing)
RETURN c,
       collect(DISTINCT n) AS beliefs,
       loc,
       collect(DISTINCT other) AS relationships,
       collect(DISTINCT t) AS tensions,
       collect(DISTINCT thing) AS possessions
```

### Tension to Moments (Phase 2)
```cypher
MATCH (m:Moment)-[:ATTACHED_TO]->(t:Tension {id: $tension_id})
SET m.weight = m.weight + ($pressure * 0.2)
RETURN m
```

---

## Files Reference

| File | Content | Status |
|------|---------|--------|
| `docs/engine/SCHEMA.md` | Current schema v5.1 | Needs update |
| `docs/engine/ANALYSIS_Moment_Graph_Architecture.md` | Full analysis | Created |
| `docs/engine/MAP_Moment_Graph.md` | This file | Created |
| `CLAUDE.md` (world_runner) | World Runner instructions | May need update |
| `playthroughs/{id}/injection_queue.json` | Narrator injections | Format extension needed |
| `mutations/wr_{flip_id}.yaml` | World Runner output | Format extension needed |

---

## Risk Heat Map

```
                    LOW RISK ────────────────────► HIGH RISK
                         │
    ┌────────────────────┼────────────────────────────────┐
    │                    │                                │
    │  Query Performance │  Schema Migration             │
    │  (Vector indexes)  │  (Moment expansion)          │
    │                    │                                │
    │  Integration       │  Complexity                   │
    │  (Clear boundaries)│  (70+ patterns)               │
    │                    │                                │
    │  LLM Costs         │  Consistency                  │
    │  (Tempo control)   │  (3 agent types)              │
    │                    │                                │
    └────────────────────┼────────────────────────────────┘
                         │
                  MEDIUM RISK
```

---

## Implementation Checklist

### Immediate (Schema)
- [ ] Add `status`, `weight`, `tone` to Moment node
- [ ] Add `tick_created`, `tick_spoken`, `tick_decayed`
- [ ] Define `CAN_SPEAK` link type
- [ ] Define `ATTACHED_TO` link type
- [ ] Define `CAN_LEAD_TO` link type
- [ ] Add `player_caused` to `THEN` link

### Phase 1 (MVP)
- [ ] `get_current_view()` query
- [ ] `handle_click()` traversal
- [ ] `update_weights()` decay
- [ ] `on_player_leaves()` / `on_player_arrives()`

### World Runner Updates
- [ ] Extend mutation YAML to include moments
- [ ] Extend injection_queue to include moment types
- [ ] Add tension-to-moment energy flow
- [ ] Report moment activations in mutations

---

*"The graph is the game. The map is the territory."*
