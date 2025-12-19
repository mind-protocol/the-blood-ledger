# History — Patterns: Distributed Memory Through Narratives

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
THIS:        PATTERNS_History.md (you are here)
BEHAVIORS:   ./BEHAVIORS_History.md
ALGORITHM:   ./ALGORITHM_History.md
VALIDATION:  ./VALIDATION_History.md
IMPLEMENTATION: ./IMPLEMENTATION_History_Service_Architecture.md
TEST:        ./TEST_History.md
SYNC:        ./SYNC_History.md
```

---

## THE PROBLEM

Games traditionally store history in event logs — timestamped records of "what happened." This creates two problems:

**1. Omniscient Memory**
A central event log knows everything. But characters shouldn't. Aldric doesn't know what happened in York while he was with you. The player doesn't know what Edmund believes about the inheritance. An event log either lies (pretending characters don't know what's logged) or grants godlike knowledge.

**2. Dead Data**
Event logs store facts, not meaning. "Day 5: Player killed guard" is data. It doesn't tell you who knows, who cares, how it affects relationships, or whether it will surface later. The log is complete but inert.

The Blood Ledger needs history that is *alive* — distributed across believers, shaped by perspective, capable of surfacing at the right moment.

---

## THE PATTERN

**History Is Distributed, Not Centralized**

There is no event log. There is no timeline table. There is no master record of "what happened."

Instead, the past exists as:
- **Narratives** — stories about what happened, stored as graph nodes
- **Beliefs** — who knows those stories, how they learned them, how certain they are
- **Conversation threads** — the actual words exchanged (for player-experienced history)

Every query about the past is a query about what characters *know* and *remember*. There is no omniscient view. The player's history is what the player believes. Aldric's history is what Aldric believes. They may differ.

**The key insight:** History isn't stored separately from state — it IS state. The same graph that holds relationships, obligations, and tensions also holds memories. A narrative about the past is structurally identical to a narrative about a debt or an oath.

---

## PRINCIPLES

### Principle 1: Beliefs Over Facts

No character has direct access to "what happened." Every memory is mediated through a BELIEVES link.

```
Character -[BELIEVES]-> Narrative
    believes: 0.0-1.0 (confidence)
    source: witnessed | told | rumor | deduced
    when: Day N, time
    where: place_id
```

Why this matters:
- Characters can be wrong
- Confidence can vary
- Sources can be traced
- Memory becomes queryable: "Who believes what, and why?"

### Principle 2: Two Sources, Two Formats

History enters the game from two sources:

**Player-Experienced:** Happened in a scene. The conversation thread IS the history. Narratives point to conversation sections with `source.file` and `source.section`.

**World-Generated:** Happened off-screen. No conversation exists. The narrative's `detail` field carries the description.

Why this matters:
- Player-experienced history has full dialogue available for retrieval
- World-generated history is self-contained
- The system handles both uniformly while preserving richness

### Principle 3: Timestamps as Structure, Not Log

All nodes and edges carry timestamps. But timestamps serve navigation, not logging.

Format: `Day {n}, {time_of_day}` where time_of_day is: dawn, morning, midday, afternoon, dusk, evening, night, midnight

Why this matters:
- "Where was I three days ago?" is answerable
- "Who knew about this before the player?" is answerable
- Chronological ordering for the Chronicle view
- But: No master timeline exists — you assemble chronology from distributed timestamps

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/physics/graph/ | Narratives and beliefs live in the graph |
| docs/views/chronicle/ | Chronicle view assembles history from beliefs |
| docs/agents/narrator/ | Narrator creates narratives during scenes |
| docs/engine/orchestration/ | Runner creates narratives during world updates |

---

## INSPIRATIONS

**Rashomon Effect**
Multiple characters witnessing the same event remember it differently. History is not singular but perspectival.

**Oral Tradition**
Before writing, history was what people remembered and passed on. Accuracy degraded. Versions diverged. This feels more human than a perfect log.

**Mind Protocol Graph**
Beliefs about events stored as edges, not as a separate timeline. The Blood Ledger applies this directly: history is belief state.

---

## WHAT THIS DOES NOT SOLVE

**Contradiction Resolution**
When two characters with conflicting beliefs meet, this system surfaces the conflict but doesn't resolve it. That's the tension/breaks system's job.

**Forgetting**
Currently, beliefs persist indefinitely. A future system might decay beliefs or archive distant memories.

**Objective Truth**
The game needs SOME source of truth (the Director, for story coherence). This system handles character knowledge, not divine knowledge.

---

## GAPS / IDEAS / QUESTIONS

- [ ] How does the Director access objective truth without an event log?
- [ ] Should conversations be stored as markdown files or in the graph?
- [ ] How do we handle very long conversation threads efficiently?
- IDEA: Could add a `heard` field on BELIEVES for how directly someone learned something
- IDEA: Memory decay based on weight and time since last surfacing
- QUESTION: What happens when a character learns their belief was wrong?
