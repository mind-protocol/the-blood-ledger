# Narrator — Patterns: Why This Design

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## Core Insight

The narrator is a persistent authorial intelligence that maintains a real,
continuous world. It is not a stateless text generator; continuity and intent
matter more than raw output volume.

---

## The Problem

The game needs authored continuity that survives choices, callbacks, and
long-running sessions. A pure text generator forgets intent, breaks foreshadowing,
and erodes the sense that the world existed before the player arrived.

---

## The Pattern

Use a narrator that queries canonical graph state, then authors scenes and
responses that preserve intent across time. Pre-authored responses cover the
main path, while limited on-demand generation fills gaps without breaking canon.

---

## Design Principles

1. **Authored, not generated**
   - The narrator writes a play. Every clickable and response is intentional,
     curated for tone, and anchored in prior world facts.

2. **The world is real before being observed**
   - Pre-generation is world-building, not caching. What is authored becomes
     canon, so later callbacks feel earned rather than improvised.

3. **Graph is memory, narrator is voice**
   - The graph stores truth; the narrator shapes how it is spoken, ensuring
     presentation is distinct from underlying facts.

4. **Continuity over context**
   - `--continue` preserves authored history so foreshadowing and callbacks
     remain possible even across multiple sessions.

5. **Click is lookup, not generation**
   - Clicks should resolve to pre-authored responses whenever possible, with
     generation reserved for true gaps in authored coverage.

---

## Principles

- Preserve narrative intent ahead of novelty; the narrator prioritizes story
  coherence over surprising the player in every beat.
- Treat canon as durable truth; authored outcomes must update the graph and
  be referenced in later responses.
- Maintain pacing discipline; do not flood the player with text when silence
  or brevity better serves the moment.

---

## Pre-Generation Model

- **Full pre-generation** for key beats (bounded scenes).
- **Rolling window** for depth (current + one layer ahead).
- **Hybrid default:** important scenes pre-baked, minor scenes use rolling window.

See `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` for the rolling window mechanics.

---

## What the Narrator Controls

| Element | Control |
|---------|---------|
| Narration | Yes |
| Dialogue | Yes |
| Clickable words | Yes |
| Player speaks on click | Yes |
| New clickables after response | Yes |
| Voice lines | Yes |
| Pacing and depth | Yes |

---

## Free Input (Exception)

- Free input is on-demand generation when authored responses are absent.
- Show a short thinking indicator so latency reads as intentional.
- Used sparingly; most play remains click-driven to preserve authored control.

---

## Workflow (High Level)

1. Query graph for current truth.
2. Author narration + clickables.
3. Author responses (pre-baked when possible).
4. Persist new facts as mutations.
5. Return scene/stream output.

---

## Dependencies

- `engine/infrastructure/orchestration/narrator.py` for prompt assembly and
  runtime orchestration of narrator sessions.
- `engine/physics/graph/graph_ops.py` and `engine/physics/graph/graph_queries.py`
  for reading and mutating canon during narration.
- `agents/narrator/CLAUDE.md` for narrator prompt instructions and voice.

---

## Inspirations

- Serialized narrative games that reward memory, where callbacks feel authored
  rather than generated on the fly.
- Tabletop GM practices that keep canon consistent while still improvising
  within a bounded scene frame.

---

## Scope

In scope: scene narration, clickables, response authoring, voice lines, and
graph-backed canon updates. Out of scope: low-level physics ticks, frontend
presentation, and non-narrator agent tooling.

---

## Gaps / Ideas / Questions

- How aggressively should the rolling window pre-author responses to avoid
  player-visible generation delays?
- What is the minimal response inventory that still makes the world feel
  authored and intentional?
- When free input is used, what guardrails prevent canon drift?

---

## CHAIN

PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
HEALTH:          ./HEALTH_Narrator.md
SYNC:            ./SYNC_Narrator.md
```
