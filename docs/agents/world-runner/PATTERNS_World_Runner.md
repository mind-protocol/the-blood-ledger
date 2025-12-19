# World Runner — Patterns: Why This Shape

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## The Core Insight

**The Runner owns time. The Narrator owns story.**

When the player takes a time-consuming action, the Narrator hands control to the Runner to advance the world. The Runner simulates time and detects player-affecting flips, then returns an Injection for the Narrator to write the moment or the summary.

---

## Interrupt/Resume Pattern

```
NARRATOR                              RUNNER
   │                                     │
   │ long action                           │
   │─────────────────────────────────────► │
   │                                     │ runs tick loop
   │                                     │ flip affects player
   │         Injection (interrupted)     │
   │ ◄────────────────────────────────────
   │ writes scene + resolves             │
   │                                     │
   │ resume with remaining time          │
   │─────────────────────────────────────►│
   │                                     │ runs to completion
   │         Injection (completed)       │
   │ ◄────────────────────────────────────
```

**Key rule:** Runner runs until interrupted OR completed. Narrator handles the interrupt, then resumes.

---

## Stateless Runner

The Runner does not keep memory between calls. The graph is the memory.

- Inputs: action, duration, player context, graph context
- Output: Injection + graph mutations already applied
- Next call reads updated graph and continues

---

## What the Runner Is Not

- **Not a full simulation:** It ticks only what matters for narratives under tension.
- **Not random events:** Events come from narrative tension, not dice rolls.
- **Not a time system:** Time is a trigger, not a physics engine.
- **Not the Narrator's boss:** Injection is information, not instruction.

---

## Player Impact Threshold

**Only flips that affect the player interrupt.** Everything else becomes world changes or news.

See `docs/agents/world-runner/ALGORITHM_World_Runner.md` for the `affects_player()` logic.

---

## Why Separation Matters

- **Focus:** Narrator writes scenes; Runner handles world evolution.
- **Continuity:** Offscreen changes happen consistently.
- **Clean interrupts:** Player-facing events become explicit moments.

---

## CHAIN

PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
INPUTS:          ./INPUT_REFERENCE.md
TOOLS:           ./TOOL_REFERENCE.md
SYNC:            ./SYNC_World_Runner.md
