# Narrator — Patterns: Why This Design

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## Core Insight

The narrator is a persistent authorial intelligence that maintains a real, continuous world. It is not a stateless text generator.

---

## Design Principles

1. **Authored, not generated**
   - The narrator writes a play. Every clickable and response is intentional.

2. **The world is real before being observed**
   - Pre-generation is world-building, not caching. What is authored becomes canon.

3. **Graph is memory, narrator is voice**
   - The graph stores truth; the narrator shapes how it is spoken.

4. **Continuity over context**
   - `--continue` preserves authored history so foreshadowing and callbacks remain possible.

5. **Click is lookup, not generation**
   - Clicks should resolve to pre-authored responses whenever possible.

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

- Free input is on-demand generation.
- Show a short thinking indicator.
- Used sparingly; most play is click-driven.

---

## Workflow (High Level)

1. Query graph for current truth.
2. Author narration + clickables.
3. Author responses (pre-baked when possible).
4. Persist new facts as mutations.
5. Return scene/stream output.

---

## CHAIN

PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md
