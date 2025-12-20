# Vision — Algorithm: Systems That Create Engagement

```
CREATED: 2024-12-16
STATUS: Draft — preliminary mapping, will evolve
LINKS_TO:
  - docs/engine/ (detailed specs, not yet written)
  - docs/views/ (presentation specs, not yet written)
```

---

## CHAIN

- `docs/design/PATTERNS_Vision.md` (design intent and scope)
- `docs/design/BEHAVIORS_Vision.md` (player-facing experience outcomes)
- `docs/design/ALGORITHM_Vision.md` (this doc, system mapping)
- `docs/design/VALIDATION_Vision.md` (validation criteria and proof)
- `docs/design/IMPLEMENTATION_Vision.md` (doc architecture and ownership)
- `docs/design/TEST_Vision.md` (vision validation checklist)
- `docs/design/SYNC_Vision.md` (current state and handoffs)

---

## OVERVIEW

This algorithm doc maps the vision into named systems and their relations, so
future module specs can be built from a shared structural outline rather than
from scattered narratives or ad hoc assumptions.

---

## DATA STRUCTURES

- **System Map:** A list of engine and presentation systems with short goals,
  dependencies, and known unknowns to keep orientation stable over time.
- **Drive Matrix:** A table that links each system to player drives so we can
  verify engagement coverage as systems evolve and move to implementation.
- **Open Questions Register:** A scoped list of unresolved decisions that
  should be promoted into module docs once they become tractable.

---

## ALGORITHM: map_vision_systems

1. Enumerate core engine systems (graph, weight, tension, world update, scene).
2. Enumerate presentation systems (views, voices) and their dependencies.
3. Link each system to its engagement purpose and known open questions.
4. Record system-to-drive mappings for coverage and future validation.
5. Capture missing systems and uncertainties for follow-up documentation.

---

## KEY DECISIONS

- Separate engine from presentation so the simulation can run headless while
  views remain a window into state rather than a driver of state.
- Treat voices and ledger/faces views as primary engagement levers, since they
  best realize the "people who remember you" success metric.
- Keep this document high-level and defer formulas and prompts to module docs
  to avoid premature specificity before validation.

---

## DATA FLOW

Graph state feeds weight computation, which drives tension detection and world
updates; scene creation then materializes the active context for the views and
voices, which present the player-facing experience loop.

---

## COMPLEXITY

This mapping is qualitative rather than computational, but the intent is to
keep algorithmic hotspots (weight, tension, world update) in module specs so
their complexity can be measured and optimized once implemented.

---

## HELPER FUNCTIONS

- `list_engine_systems()` returns the named engine subsystems and purpose.
- `list_presentation_systems()` returns the view and voice subsystems.
- `record_open_questions()` stores unresolved topics for module doc follow-up.

---

## INTERACTIONS

- Graph implementation docs live in the ngram repo; see
  `data/ARCHITECTURE — Cybernetic Studio.md` for current references.
- `docs/agents/narrator/` for director and scene generation responsibilities.
- `docs/frontend/scene/` for voice presentation and player-facing outputs.
- `docs/world/map/` for the map view presentation and world awareness.

---

## Purpose

This document is a **preliminary mapping** of systems to behaviors.

It is NOT:
- A complete list (we'll discover more as we build)
- Fully specified (detailed specs live in module docs)
- Final (this evolves as we learn)

It IS:
- A first pass at structure
- A way to see the shape of what we're building
- A place to capture questions and uncertainties

**The real specifications will live in `docs/engine/` and `docs/views/`.** This document provides orientation, not detail.

---

## Architecture: Two Layers

I see two distinct layers:

### Engine Layer
The core simulation — what's true, what happens, what changes.

Lives in: `docs/engine/` and `engine/`

### Presentation Layer
How the player experiences the engine — what they see, hear, interact with.

Lives in: `docs/views/` and the frontend

**My opinion:** This separation matters. The engine should be complete without any presentation — you could run world updates, process breaks, evolve the graph, all in headless mode. The presentation is a window into the engine, not part of it.

**Open question:** Where does the Director fit? It reads player behavior (presentation) but affects the engine (focus adjustments). Is it engine? Presentation? A bridge?

---

## Engine Systems (Preliminary)

These create the simulation. Presentation reads from them.

### The Graph
> *Links to: graph implementation docs in the ngram repo (see
> `data/ARCHITECTURE — Cybernetic Studio.md`).*

**What it does:** Holds all state — characters, places, things, narratives, beliefs, connections.

**Why it matters for engagement:**
- Creates memory (everything persists)
- Creates relationships (narratives between entities)
- Creates traceability (you can query why anything happened)

**Open questions:**
- What's the exact schema? (→ will be in ALGORITHM_Schema.md)
- How do we handle graph growth over time?
- What about archiving/pruning distant narratives?

**My uncertainty:** The design doc describes four node types (CHARACTER, PLACE, THING, NARRATIVE). Is that complete? What about FACTION? EVENT? Or do those emerge from narratives?

---

### Weight / Energy
> *Links to: graph implementation docs in the ngram repo (see
> `data/ARCHITECTURE — Cybernetic Studio.md`).*

**What it does:** Computes importance of narratives based on beliefs, connections, contradictions.

**Why it matters for engagement:**
- Creates focus (only high-weight enters context)
- Creates emergence (what matters is computed, not declared)
- Prevents diffusion (energy clusters around player)

**Open questions:**
- What's the actual computation? Recursive? Iterative?
- How does focus (narrator-set) interact with computed weight?
- What are the decay rates for distant narratives?

**My uncertainty:** The engine spec talks about weight but doesn't give a formula. Is that intentional (LLM judges) or a gap to fill?

---

### Tension / Breaks
> *Links to: `docs/engine/mechanisms/` (not yet written)*

**What it does:** Detects narratives under unsustainable pressure; processes their resolution into events.

**Why it matters for engagement:**
- Creates drama (contradictions become confrontations)
- Creates inevitability (unresolved tension builds until it breaks)
- Creates emergence (events from structure, not scripts)

**Open questions:**
- How does the LLM identify "must break"? What's the prompt structure?
- How do we prevent cascade runaway?
- What's the relationship between tension detection and weight?

**My opinion:** This is the highest-risk system. If break detection doesn't work well, the game feels random. If break resolution isn't specific, it feels generic. This needs careful validation.

---

### World Update
> *Links to: `docs/engine/orchestration/` (not yet written)*

**What it does:** When time passes, processes all active narratives. Parallel storylines advance. News propagates.

**Why it matters for engagement:**
- Creates living world ("what happened while I was away?")
- Creates organic urgency (situations evolve)
- Creates scale (you're part of something larger)

**Open questions:**
- How do we scale this? Processing ALL narratives could be expensive.
- How detailed are distant events vs nearby events?
- How does news propagation actually work?

---

### Scene Creation
> *Links to: `docs/engine/orchestration/` (not yet written)*

**What it does:** Gathers high-weight context + physical grounding → generates the present moment.

**Why it matters for engagement:**
- Creates presence (you're HERE)
- Creates choices (options emerge from situation)
- Creates character (characters speak from their beliefs)

**Open questions:**
- What's the context window budget?
- How do we ensure brevity?
- How do choices emerge? Generated? Template + fill?

**My opinion:** Scene creation is where everything collapses into experience. This is the craft layer — the writing quality matters as much as the system.

---

### The Director
> *Links to: `docs/agents/narrator/` (not yet written)*

**What it does:** Maintains Story Document (arcs, setups, payoffs) and Player Document (preferences, patterns). Adjusts focus.

**Why it matters for engagement:**
- Creates personalization (learns what you care about)
- Creates pacing (slow builds, explosive releases)
- Creates coherence (setups pay off)

**Open questions:**
- How much autonomy does the Director have?
- How do we prevent the Director from railroading?
- Where's the line between "tuning" and "scripting"?

**My uncertainty:** The Director feels like the least specified system. It's mentioned in the engine spec but with less detail than others. Is that intentional (emergent from LLM) or a gap?

---

## Presentation Systems (Preliminary)

These create the player experience. They read from the engine.

### The Views
> *Links to: `docs/views/` (not yet written)*

Five views that present different aspects of state:

| View | Shows | Engine Source |
|------|-------|---------------|
| **Scene** | The present moment | Scene Creation output |
| **Map** | Spatial state, fog of war | Graph (places, player knowledge) |
| **Chronicle** | History as player believes it | Graph (player's believed narratives, chronological) |
| **Ledger** | Obligations — debts, oaths, blood | Graph (obligation-type narratives) |
| **Faces** | People and relationships | Graph (characters + narratives about them) |

**Open questions:**
- Are these five views complete? Will we need more?
- How do views update in real-time vs on navigation?
- What's the visual language? (pure text? ASCII? rendered UI?)

**My opinion:** The Ledger and Faces views feel most important for the "deep relationships" success metric. If those are great, a lot else can be rough. If those are weak, nothing else saves us.

---

### The Voices (Graph Speaks)
> *Links to: `docs/frontend/scene/` (not yet written)*

**What it does:** High-weight narratives speak as internal monologue — debts, oaths, companions commenting.

**Why it matters for engagement:**
- Creates presence of history (your past speaks)
- Creates internal conflict (voices pull different directions)
- Creates the unique mechanic (no other game does this)

**Open questions:**
- How many voices per scene? Too many = noise.
- How do we vary voice "tone" by narrative type?
- Do companions speak AS themselves or AS your perception of them?

**My opinion:** This is THE differentiator. If we nail this, we have something genuinely new. If we don't, we're just another text game. Deserves significant attention.

---

## What's Missing (Summary)

Key gaps to resolve: character depth generation, conversation model, action system beyond dialogue, conflict/combat handling, image generation/portraits, voice and audio integration, and persistence/save strategy.

---

## Systems → Drives (Preliminary Mapping)

This is approximate. Will refine as we understand better.

| System | Primary Drives Served |
|--------|----------------------|
| Graph | Ownership, Social Influence |
| Weight | Unpredictability, Focus |
| Breaks | Loss Avoidance, Unpredictability |
| World Update | Scarcity, Epic Meaning |
| Scene Creation | Creativity, Social Influence |
| Director | All (tuning) |
| Views (Ledger) | Ownership (primary) |
| Views (Faces) | Social Influence (primary) |
| Voices | Ownership, Social Influence, Loss Avoidance |

---

## Implementation Thinking (Summary)

Initial dependency ordering and detailed module specs will live in engine/view module docs as they are created. This doc keeps only the high-level map.

---

## My Current Uncertainties

Being honest about what I don't yet understand:

1. **Weight computation** — The design docs describe it conceptually but not algorithmically. Is that intentional?

2. **Director scope** — How much does it do? Is it active (generates events) or passive (adjusts focus)?

3. **Character depth** — The success metric requires asking about grandmother. Where does that knowledge come from?

4. **Conversation model** — How do open-ended character conversations work? Pure LLM? Structured + LLM?

5. **Scale** — How big can the graph get? What happens at hour 50?

---

## Evolution Notes

This document should evolve as we:
- [ ] Write detailed engine module docs
- [ ] Write detailed view docs
- [ ] Build POC and learn what's missing
- [ ] Discover systems we didn't anticipate

When something here is superseded by detailed docs, we should note that and link to the authoritative source.

---

## GAPS / IDEAS / QUESTIONS

- What is the canonical weight computation and how does focus override it?
- How should the Director scope be bounded to avoid railroading?
- Where does character depth data originate (schema, generation, or memory)?
- What is the conversation model for open-ended player interactions?
- What limits keep the graph performant at long play durations?

---

*"This is a map of territory we haven't fully explored. It will be wrong in places. That's fine — maps are for navigation, not truth."*
