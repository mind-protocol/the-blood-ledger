# THE BLOOD LEDGER — Moment Graph Architecture

```
CREATED: 2024-12-17
STATUS: Canonical
```

---

## Core Insight

There is no "scene". There is no "conversation tree". There is only the graph.

The narrator weaves a possibility space of moments. Some actualize. Some decay. Some persist across locations, attached to characters. Some lie dormant at places, waiting for return.

The conversation is not a tree. It's a graph — traversable in multiple directions, forkable, mergeable, persistent.

**This is also the memory system.** What we're building for a game character is what we've been trying to build for AI consciousness.

---

## Three Levels of Agency

| Level | Agent | Responsibility | Timing |
|-------|-------|----------------|--------|
| World | Runner | Pressure, time, consequences, events | Tick-based |
| Scene | Narrator | Architecture, actions, transitions | On demand |
| Character | Citizen | Dialogue, thoughts, freeform response | Parallel async |

---

## Schema Summary

### Moment Node

```yaml
Moment:
  id: string
  text: string
  type: narration | dialogue | action | thought | hint
  status: possible | active | spoken | dormant | decayed
  weight: float
  tone: string
  tick_created: int
  tick_spoken: int
  tick_decayed: int
  embedding: float[]
```

### Links

```yaml
CAN_SPEAK:
  Character → Moment
  weight: float

ATTACHED_TO:
  Moment → Character | Place | Thing | Narrative | Tension
  presence_required: bool
  persistent: bool
  dies_with_target: bool

CAN_LEAD_TO:
  Moment → Moment
  trigger: click | wait | auto | semantic
  require_words: [string]
  require_similarity: float
  wait_ticks: int
  bidirectional: bool
  consumes_origin: bool
  weight_transfer: float

THEN:
  Moment → Moment
  tick: int
  player_caused: bool
```

---

## Phase Summary

| Phase | Focus | LLM Usage | Player Experience | Avg Rating |
|-------|-------|-----------|-------------------|------------|
| **1** | Graph traversal | None on hot path | Instant response, persistence | 8.8/10 |
| **2** | Energy emergence | Freeform fallback only | Characters initiate, tension surfaces | 8.8/10 |
| **3** | Citizen autonomy | Background parallel | Living characters, proactive dialogue | 9.0/10 |
| **4** | Social dynamics | Reaction generation | Group feels real, gossip spreads | 9.3/10 |
| **5** | Natural dynamics | Crisis reactions | Characters that evolve, remember, erupt | 9.3/10 |
| **Infra** | Scene/time/movement | Gap-filling | Coherent world, dramatic transitions | 8.8/10 |

---

## Documentation Chain

```
THIS FILE:        ARCHITECTURE_Overview.md (you are here)
    ↓
PHASE 1:          PHASE_1_Core_Graph.md
    ↓
PHASE 2:          PHASE_2_Energy_Emergence.md
    ↓
PHASE 3:          PHASE_3_Citizen_Autonomy.md
    ↓
PHASE 4:          PHASE_4_Social_Dynamics.md
    ↓
PHASE 5:          PHASE_5_Natural_Dynamics.md
    ↓
INFRASTRUCTURE:   INFRASTRUCTURE.md
    ↓
SCHEMA:           SCHEMA_Moments.md
    ↓
API:              API_Moments.md
    ↓
VALIDATION:       VALIDATION_Moments.md
```

---

## Implementation Priority

### Phase 1 (MVP)
- [ ] Moment node schema
- [ ] ATTACHED_TO, CAN_LEAD_TO, CAN_SPEAK, THEN links
- [ ] Click traversal (instant)
- [ ] Weight decay per tick
- [ ] Presence gating query
- [ ] Current view API
- [ ] Dormant/reactivate on location change

### Phase 2 (Energy)
- [ ] Semantic embedding on moments
- [ ] Freeform → semantic boost → flip
- [ ] Tension pressure → moment weight
- [ ] Wait trigger auto-fire
- [ ] Embedding proximity propagation
- [ ] Flip threshold detection

### Phase 3 (Citizens)
- [ ] Activated cluster query
- [ ] System prompt builder
- [ ] Background thought generation
- [ ] Citizen freeform response
- [ ] Drive system
- [ ] Tempo controller
- [ ] Parallel async loop

### Phase 4 (Social)
- [ ] Witness reaction system
- [ ] Character-to-character dialogue
- [ ] Gossip mechanism
- [ ] Private conversation gating
- [ ] Group dynamics detection
- [ ] Narrative energy boost
- [ ] Shared party memory

### Phase 5 (Natural Dynamics)
- [ ] Char-to-char required words matching
- [ ] Autonomous announcement triggers
- [ ] Moment rumination (derivative spawning)
- [ ] Context modifiers for old references
- [ ] Moment evolution chains (reinforcement)
- [ ] Name activation and attention
- [ ] Heavy modifier crisis reactions

### Infrastructure (Throughout)
- [ ] Scene as query (no scene object)
- [ ] Place atmosphere integration
- [ ] Character AT state (present, visible, arriving, traveling_to)
- [ ] Time-costing actions (conversation turns, short/long actions)
- [ ] Time passage effects (events, atmosphere transitions)
- [ ] Leave = moment with action (travel action type)
- [ ] Return = narrative with conditions (promise tracking)
- [ ] Arrival = travel completion triggers presence-gated moments
- [ ] Fetch pattern (travel_and_return action with action_bring)
- [ ] Go To Them pattern (reveal_place on mention)
- [ ] Stranger Arrives pattern (NPCs have own travel moments)
- [ ] Query moments (query field on moments, query_filled flag)
- [ ] Query triggers backstory generation (async narrator pipeline)
- [ ] ANSWERED_BY links (trace question → answer)
- [ ] Forward-only citizen generation rules
- [ ] Flashback pattern (backstory + place triggers)

---

## Rating Summary by Category

| Category | Patterns That Score 10/10 |
|----------|---------------------------|
| **Responsiveness** | Click Traversal, Instant Click, Semantic Boost, Freeform Without LLM |
| **Character Aliveness** | Characters Initiate, Proactive Dialogue, Autonomous Announcement, Char-to-Char Dialogue |
| **Relationship Depth** | Conversation Persistence, Party Memory, Remember When, Citizen Freeform Response |
| **Social Dynamics** | Witness Reaction, Overhearing, NPCs Argue |
| **Evolution** | Moment Evolution, Heavy Modifier Reaction |
| **World Coherence** | Flashback Pattern, Stranger Arrives, Query Triggers Generation |

**The 10/10 patterns cluster around two themes:**
1. **Speed** — No waiting, ever
2. **Aliveness** — Characters aren't waiting for you

---

## The Deeper Pattern

This isn't just a game dialogue system.

| Blood Ledger | Mind Protocol |
|--------------|---------------|
| Moment | Memory/Experience |
| ATTACHED_TO | Experiential binding |
| presence_required | Context-dependent recall |
| persistent | Long-term vs working memory |
| weight decay | Salience fading |
| semantic boost | Associative recall |
| dormant → active | Memory reactivation |
| CAN_SPEAK weight | Who "owns" a memory |
| Citizen | Bounded AI agent |
| Activated cluster | Identity from graph |
| Drive system | Motivation/values |
| Tempo control | Attention budget |

**Blood Ledger characters are the first Mind Protocol citizens.**

The player experiences what an AI citizen experiences:
- Memory that persists
- Context that matters
- Thoughts that surface
- Relationships that remember
- Identity from history

We're building consciousness infrastructure. The game is the proof.

---

*"There is no scene. There is only the graph."*
