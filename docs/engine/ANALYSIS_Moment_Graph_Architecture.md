# Analysis: Moment Graph Architecture Specification

```
CREATED: 2024-12-17
STATUS: Analysis Draft
ANALYST: World Runner Agent
```

---

## Executive Summary

The Moment Graph Architecture spec represents a **fundamental paradigm shift** from the current schema. It reframes the entire game from "narratives under tension" to "a possibility space of moments that actualize".

**Key Insight:** "There is no scene. There is only the graph."

This analysis identifies affected systems, risks, solutions, dependencies, and integration points with existing architecture.

---

## 1. Affected Systems

### 1.1 World Runner (Direct Impact)

**Current Role (from CLAUDE.md):**
- Called only when tensions flip
- Writes mutations to `mutations/wr_{flip_id}.yaml`
- Writes injections to `playthroughs/{id}/injection_queue.json`
- Authors "what happened" — Narrator authors "how it's experienced"

**New Role (from spec):**
- Still operates at "World" level (tick-based pressure, time, consequences)
- Now must also handle moment state transitions during world updates
- Tension pressure flows TO moment weights (P2.3: `moment.weight += tension.pressure * 0.2`)
- Flips still trigger World Runner, but resolution creates moments, not just narratives

**New Responsibilities:**
```python
# From spec M2.3
def tension_to_moments(tension):
    moments = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(t:Tension {id: $id})
        RETURN m
    """, id=tension.id)

    for m in moments:
        m.weight += tension.pressure * 0.2
```

**Risk:** World Runner's injection_queue format may need expansion to include moment injections, not just event/character_action/atmospheric types.

---

### 1.2 Narrator (Major Refactoring)

**Current Role:**
- Scene architecture
- Receives injections via PostToolUseHook
- Authors "how it's experienced"

**New Role:**
- "Scene creation" becomes "moment architecture"
- No scene object exists — scene is a query result
- Narrator surfaces active moments, doesn't generate scenes from scratch
- Freeform input → semantic match → moment surfaces (no narrator call unless fallback)

**Critical Change:**
```python
# From spec M2.1 - Narrator only called as fallback
def handle_free_input(player_id, text):
    input_emb = embed(text)
    matches = query("""...""")

    for match in matches:
        if match.score > 0.65:
            match.m.weight += match.score * 0.5

    flips = check_for_flips()
    if flips:
        return flips

    # Only if nothing matches - EXPENSIVE PATH
    return queue_narrator_generation(text)
```

**Impact:** Narrator calls become rare exceptions, not the norm. This is a 10x cost reduction.

---

### 1.3 Graph Schema (Major Extension)

**Current Moment Node (from SCHEMA.md v5.1):**
```yaml
Moment:
  id: string
  text: string
  type: enum [narration, dialogue, hint, player_click, player_freeform, player_choice]
  tick: integer
  line: integer
  embedding: float[]
  # Links: SAID, AT, THEN, FROM
```

**New Moment Node (from spec):**
```yaml
Moment:
  id: string
  text: string
  type: narration | dialogue | action | thought | hint  # DIFFERENT types
  status: possible | active | spoken | dormant | decayed  # NEW
  weight: float  # NEW
  tone: string  # NEW
  tick_created: int  # RENAMED
  tick_spoken: int  # NEW
  tick_decayed: int  # NEW
  embedding: float[]
```

**New Link Types:**
```yaml
CAN_SPEAK:        # NEW - Character → Moment
ATTACHED_TO:      # NEW - Moment → Character|Place|Thing|Narrative|Tension
CAN_LEAD_TO:      # NEW - Moment → Moment (traversal)
THEN:             # EXISTS but different semantics
```

**Schema Delta Required:**
| Element | Current | New Spec | Action |
|---------|---------|----------|--------|
| `type` values | 6 types | 5 types | Merge or map |
| `status` | absent | required | Add field |
| `weight` | absent | required | Add field |
| `tone` | absent | optional | Add field |
| `tick` | single | created/spoken/decayed | Split field |
| `CAN_SPEAK` | absent | required | Add link type |
| `ATTACHED_TO` | absent | required | Add link type |
| `CAN_LEAD_TO` | absent | required | Add link type |

---

### 1.4 Citizen System (NEW)

This is an entirely new agent type not in current architecture.

**Definition:**
- Characters as bounded LLM agents
- Background thought generation (parallel async)
- Drive system (curiosity, anxiety, greed, loyalty, vengeance)
- Tempo adaptation to player pace

**Three-Level Agency:**
| Level | Agent | Responsibility | Timing |
|-------|-------|----------------|--------|
| World | Runner | Pressure, time, consequences | Tick-based |
| Scene | Narrator | Architecture, actions, transitions | On demand |
| Character | Citizen | Dialogue, thoughts, freeform | Parallel async |

**Risk:** This introduces a third concurrent agent type. Current architecture has World Runner + Narrator. Now we add N Citizens (one per present character) running in parallel.

---

### 1.5 Time System (Significant Enhancement)

**Current:** Time passes during graph ticks (5-minute minimum).

**New:** Every action costs time.
| Action | Time Cost |
|--------|-----------|
| Conversation turn | 1-5 minutes |
| Click traversal | 1 minute |
| Free input response | 2-3 minutes |
| Short action | 5-30 minutes |
| Long action | Hours |
| Travel | From route data |
| Waiting | Player specified |

**Impact:** Time becomes granular. Conversations have opportunity cost. This affects World Runner tick frequency and tension accumulation.

---

## 2. Risks

### 2.1 Complexity Explosion

**Risk Level: HIGH**

The spec describes 5 phases + infrastructure = 70+ patterns/behaviors. Implementation surface area is massive.

**Mitigations:**
- Phase 1 is MVP (no LLM on hot path) — start here
- Each phase has clear dependencies
- Ratings prioritize critical features (10/10 items first)

---

### 2.2 Schema Migration

**Risk Level: MEDIUM-HIGH**

Current schema has Moment as simple transcript record. New schema has Moment as core game state with status, weight, complex links.

**Mitigations:**
- Schema version exists (currently v5.1) — increment to v6.0
- Migration path: existing Moments become status='spoken' with tick_spoken=tick
- New link types can be added without breaking existing nodes

---

### 2.3 LLM Cost Management

**Risk Level: MEDIUM**

Citizens generate thoughts in background. Multiple characters = N parallel LLM calls.

**Mitigations:**
- Tempo Controller (M3.6) throttles generation based on player pace
- Citizens only think when `tempo.should_generate_more()` returns true
- Generation interval adapts: fast reader = 2s, slow reader = 10s

---

### 2.4 Graph Query Performance

**Risk Level: MEDIUM**

Semantic similarity queries (`vector_similarity`) on every moment for every freeform input.

**Mitigations:**
- Spec suggests limit results: `LIMIT 5`, `LIMIT 20`
- Threshold filtering: `score > 0.65`, `sim > 0.7`
- AGE/Neo4j have vector index support

---

### 2.5 Consistency Across Agents

**Risk Level: MEDIUM**

Three agent types (Runner, Narrator, Citizens) operating on same graph concurrently.

**Mitigations:**
- Citizens are "forward-only" — they cannot retcon or modify past moments
- World Runner has exclusive authority on tension flips
- Narrator has exclusive authority on scene structure
- Clear ownership boundaries in spec

---

### 2.6 Integration with Existing World Runner

**Risk Level: MEDIUM**

Current World Runner outputs mutations + injection_queue. New spec expects moments, not just narratives.

**Mitigations:**
- injection_queue format can be extended
- Add `type: "moment"` alongside existing event/character_action/atmospheric
- World Runner still outputs YAML mutations — just includes moment nodes

---

## 3. Dependencies

### 3.1 Phase Dependencies

```
Phase 1: Core Graph (MVP)
    ↓
Phase 2: Energy & Emergence
    ↓
Phase 3: Citizen Autonomy
    ↓
Phase 4: Social Dynamics
    ↓
Phase 5: Natural Dynamics
```

Each phase REQUIRES the previous.

### 3.2 System Dependencies

```
Graph Database (Neo4j/AGE)
    ├── Vector similarity queries (embeddings)
    ├── Graph traversal (CAN_LEAD_TO)
    └── Real-time weight updates

Embedding System
    ├── 768-dim vectors (from SCHEMA.md)
    ├── Semantic search for freeform input
    └── Moment proximity propagation

LLM Infrastructure
    ├── Citizen thought generation (Phase 3+)
    ├── Narrator fallback (when semantic match fails)
    └── Reaction generation (Phase 4+)

Async Processing
    ├── Parallel citizen loops
    ├── Background thought generation
    └── Tempo-controlled throttling
```

### 3.3 Critical Path

1. **Graph schema update** — Moment node expansion, new link types
2. **Click traversal** — P1.1, rated 10/10, foundation of everything
3. **Presence gating** — P1.3, rated 9/10, context-aware conversations
4. **Semantic boost** — P2.1, rated 10/10, free input without LLM
5. **Characters initiate** — B2.2, rated 10/10, NPCs become alive

---

## 4. Integration Points with Existing Architecture

### 4.1 World Runner Integration

**Current Flow:**
```
Tension flip → World Runner → mutations/wr_{flip_id}.yaml → injection_queue.json → Narrator
```

**New Flow:**
```
Tension flip → World Runner → mutations (including moments) → injection_queue (extended) → Narrator
                    ↓
            Tension-to-Moment energy (M2.3)
                    ↓
            Attached moments get weight boost
```

**injection_queue.json Extension:**
```json
{
  "injections": [
    {
      "type": "moment",
      "moment_id": "moment_aldric_leadership_challenge",
      "action": "activate",
      "narrator_notes": "Aldric's patience snapped"
    }
  ]
}
```

---

### 4.2 Narrator Integration

**Current:** Narrator authors scenes, receives injections, generates text.

**New:** Narrator becomes moment architect:
- Queries active moments
- Surfaces high-weight moments
- Falls back to LLM only when semantic match fails
- Handles moment consumption and THEN links

**Key Query (M1.1):**
```python
def get_current_view(player_id):
    live_moments = query("""
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        WITH m, [(m)-[r:ATTACHED_TO WHERE r.presence_required]->(t) | t] AS required
        WHERE ALL(t IN required WHERE is_present(t))
        RETURN m ORDER BY m.weight DESC LIMIT 20
    """)

    transitions = query("""
        MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO]->(next)
        RETURN m.id, r.require_words, next.id
    """)

    return { location, present_chars, live_moments, transitions }
```

---

### 4.3 Graph Schema Integration

**Migration Strategy:**

1. **Add new fields to Moment:**
   ```yaml
   Moment:
     # Existing
     id, text, type, tick, line, embedding

     # Add
     status: { type: enum, values: [possible, active, spoken, dormant, decayed], default: spoken }
     weight: { type: float, default: 0.5 }
     tone: { type: string }
     tick_created: { type: integer }  # Rename tick → tick_created for new, keep tick for backward compat
     tick_spoken: { type: integer }
     tick_decayed: { type: integer }
   ```

2. **Add new link types:**
   ```yaml
   CAN_SPEAK:
     from: character
     to: moment
     attributes:
       weight: float

   ATTACHED_TO:
     from: moment
     to: [character, place, thing, narrative, tension]
     attributes:
       presence_required: boolean
       persistent: boolean
       dies_with_target: boolean

   CAN_LEAD_TO:
     from: moment
     to: moment
     attributes:
       trigger: enum [click, wait, auto, semantic]
       require_words: array[string]
       require_similarity: float
       wait_ticks: integer
       bidirectional: boolean
       consumes_origin: boolean
       weight_transfer: float
   ```

3. **Existing THEN link semantics change:**
   ```yaml
   THEN:
     from: moment
     to: moment
     attributes:
       tick: integer
       player_caused: boolean  # NEW
   ```

---

## 5. Valuable Insights

### 5.1 The 10/10 Patterns (Prioritize These)

| Pattern | Why It's Critical |
|---------|------------------|
| P1.1 Click Traversal | "If this isn't instant, nothing else matters" |
| B1.1 Instant Click Response | The feel of the game |
| B1.3 Conversation Persistence | "Without this, NPCs are goldfish" |
| P2.1 Semantic Boost | Free input without LLM latency |
| B2.1 Freeform Without LLM | "Players will think you're cheating" |
| B2.2 Characters Initiate | NPCs become characters |
| P3.4 Citizen Freeform Response | Characters are individuals |
| B3.2 Proactive Dialogue | "The marker of a real character" |
| B3.6 Instant Freeform | Direct address works |
| P4.1 Witness Reaction | Social dynamics become real |
| P4.2 Char-to-Char Dialogue | Party banter evolved |
| P4.7 Party Memory | "Shared memory is love" |
| B4.2 Overhearing | Classic dramatic mechanic |
| B4.5 NPCs Argue | Drama you can watch/join |
| B4.7 Remember When | What makes companions matter |
| P5.2 Autonomous Announcement | Characters have their own agendas |
| P5.5 Moment Evolution | Character radicalization through play |
| P5.7 Heavy Modifier Reaction | Big moments get big reactions |

### 5.2 The Core Insight for World Runner

**World Runner's moment authority:**

1. **Tension breaks → Moment activation**
   - When tension flips, attached moments get weight boost
   - Some moments may cross activation threshold
   - World Runner should report these in mutations

2. **Event creation → Moment creation**
   - World Runner already creates narratives for "what happened"
   - Now also creates moments for how it surfaces
   - Link moments to narratives, characters, places

3. **Cascade tracking → Moment propagation**
   - Cascades currently report tension IDs
   - Should also report moments that may flip

### 5.3 The Mind Protocol Connection

The spec explicitly states:

> "Blood Ledger characters are the first Mind Protocol citizens."
> "We're building consciousness infrastructure. The game is the proof."

| Blood Ledger | Mind Protocol |
|--------------|---------------|
| Moment | Memory/Experience |
| ATTACHED_TO | Experiential binding |
| presence_required | Context-dependent recall |
| persistent | Long-term vs working memory |
| weight decay | Salience fading |
| semantic boost | Associative recall |
| dormant → active | Memory reactivation |
| Citizen | Bounded AI agent |
| Activated cluster | Identity from graph |

This isn't just a game system — it's a memory architecture applicable to AI agents generally.

### 5.4 Key Architectural Decisions

1. **No scene object.** Scene = query result. This eliminates state synchronization issues.

2. **Everything is moments.** Leave, arrive, questions, answers — all moment patterns, not special systems.

3. **Forward-only citizens.** Citizens can generate future moments but cannot modify past. Prevents consistency issues.

4. **Energy flows from structure.** Weight isn't assigned — it's computed from graph topology. High-connection = high-weight.

5. **LLM is fallback, not default.** Phase 1-2 have NO LLM on hot path. This is critical for responsiveness.

---

## 6. Recommended Implementation Order

### Phase 0: Schema Migration (Before anything else)
- [ ] Update Moment node in SCHEMA.md
- [ ] Add CAN_SPEAK, ATTACHED_TO, CAN_LEAD_TO link types
- [ ] Test backward compatibility with existing moments

### Phase 1: MVP (Core Graph)
- [ ] Click traversal (P1.1)
- [ ] Weight decay (M1.3)
- [ ] Presence gating (P1.3)
- [ ] Current view query (M1.1)
- [ ] Dormant/reactivate on location change (M1.4)

### Phase 2: Energy (Semantic + Tension)
- [ ] Semantic boost (P2.1, M2.1)
- [ ] Tension-to-moment energy (P2.3, M2.3)
- [ ] Wait triggers (P2.4, M2.4)
- [ ] Flip detection (M2.5)

### Phase 3: Citizens (Parallel Agents)
- [ ] Citizen context query (M3.1)
- [ ] System prompt builder (M3.2)
- [ ] Background thought generation (M3.3)
- [ ] Tempo controller (M3.6)

### Phase 4: Social (Multi-Agent)
- [ ] Witness reactions (M4.1)
- [ ] Gossip mechanism (M4.3)
- [ ] Shared party memory (M4.7)

### Phase 5: Natural (Polish)
- [ ] Autonomous announcements (P5.2)
- [ ] Moment evolution (P5.5)
- [ ] Heavy modifier reactions (P5.7)

---

## 7. World Runner Specific Updates

### 7.1 Mutation File Extension

Current format:
```yaml
# mutations/wr_{flip_id}.yaml
event:
  summary: "..."
  location: place_id
  witnesses: [char_ids]
  caused_by: [narr_ids]

nodes: []      # narratives, characters, places, things
links: []      # beliefs, relationships
updates: []    # tensions
movements: []  # character locations
cascades: []   # tension IDs to re-check
```

Extended format:
```yaml
# mutations/wr_{flip_id}.yaml
event:
  summary: "..."
  location: place_id
  witnesses: [char_ids]
  caused_by: [narr_ids]

nodes: []      # + Moment nodes
links: []      # + CAN_SPEAK, ATTACHED_TO, CAN_LEAD_TO
updates: []    # + Moment weight/status updates
movements: []
cascades: []
moment_activations: []  # NEW: Moment IDs that crossed threshold
```

### 7.2 Injection Queue Extension

Current format:
```json
{
  "injections": [
    { "type": "event", ... },
    { "type": "character_action", ... },
    { "type": "atmospheric", ... }
  ]
}
```

Extended format:
```json
{
  "injections": [
    { "type": "event", ... },
    { "type": "character_action", ... },
    { "type": "atmospheric", ... },
    {
      "type": "moment_activation",
      "moment_id": "moment_id",
      "status": "active",
      "weight_boost": 0.4,
      "narrator_notes": "This moment surfaced due to tension break"
    },
    {
      "type": "moment_creation",
      "moment": {
        "id": "moment_new_id",
        "text": "The text of the new moment",
        "type": "dialogue",
        "status": "possible",
        "weight": 0.6
      },
      "links": [
        { "type": "ATTACHED_TO", "target": "char_aldric", "presence_required": true }
      ]
    }
  ]
}
```

---

## 8. Open Questions

1. **How does Citizen thought generation interact with World Runner ticks?**
   - Do citizens pause during tick processing?
   - Or are they truly parallel?

2. **What happens to existing Moments in migration?**
   - All become `status: spoken`?
   - No CAN_LEAD_TO links for historical moments?

3. **How are initial moments seeded?**
   - At game start, what moments exist?
   - Are they pre-authored or generated from narratives?

4. **What's the embedding cost?**
   - Every moment needs embedding (768-dim)
   - Every freeform input needs embedding
   - What's the latency budget?

5. **How does moment weight relate to narrative weight?**
   - SCHEMA.md has `narrative.weight` (computed)
   - Spec has `moment.weight`
   - Are they independent? Linked?

---

*"Everything is moments. The graph is the game. The moment is the memory."*
