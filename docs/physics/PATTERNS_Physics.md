# Physics — Patterns: Why This Shape

```
STATUS: CANONICAL
UPDATED: 2024-12-18
```

---

## CHAIN

```
THIS:           PATTERNS_Physics.md (you are here)
BEHAVIORS:      ./BEHAVIORS_Physics.md
ALGORITHMS:
  - ./ALGORITHM_Physics.md      (M2: Physics Tick)
  - ./ALGORITHM_Handlers.md     (M3: Character Handlers)
  - ./ALGORITHM_Canon.md        (M4: Canon Holder)
  - ./ALGORITHM_Input.md        (M5: Player Input)
  - ./ALGORITHM_Actions.md      (M7: Action Processing)
  - ./ALGORITHM_Questions.md    (M8: Question Answering)
  - ./ALGORITHM_Speed.md        (M12: Speed Controller)
SCHEMA:         ../schema/SCHEMA_Moments.md
API:            ./API_Physics.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
```

---

## Core Principle

**The graph is the only truth.**

Everything else — handlers, ticks, canon — are processes that read from and write to the graph. No process owns state. No process is authoritative except through what it writes to the graph.

---

## P1: Potential vs Actual

Moments exist in two modes:

| Mode | Meaning | Graph State |
|------|---------|-------------|
| **Potential** | Could happen | Has weight, competes with other potentials |
| **Actual** | Did happen | Is canon, has THEN links to what came before |

No process decides what happens. Processes propose potentials. Physics determines what actualizes.

---

## P2: The Graph Is Alive

The graph is a mind. It doesn't stop thinking.

Energy always flows. Weights always decay. Propagation always happens. Player input is a perturbation, not an ignition.

**What we control:**
- Tick rate (speed setting)
- When we sample for display
- When we inject energy (input, world events, handler outputs)

**What we don't control:**
- "Starting" the cascade — it's always running
- "Stopping" the cascade — it doesn't stop

**Graph states:**

| State | Meaning |
|-------|---------|
| **Active** | High energy, many flips, drama unfolding |
| **Quiet** | Low energy, few flips, system settled |
| **Critical** | Energy building, thresholds approaching, tension rising |

But never **stopped**.

---

## P3: Everything Is Moments

There are no separate systems for dialogue, movement, actions, thoughts.

| What | How It's Represented |
|------|---------------------|
| Speech | Moment with type: dialogue |
| Thought | Moment with type: thought |
| Movement | Moment with type: action, action: travel |
| Combat | Moment with type: action, action: attack |
| Observation | Moment with type: narration |

The graph doesn't distinguish structurally — all are Moment nodes.
Physics doesn't distinguish — all propagate energy the same way.

**But:** Action Processing does distinguish. Moments with `action` field modify world state. Thoughts don't. The moment type determines *consequences*, not storage or propagation.

---

## P4: Moments Are Specific, Narratives Emerge

A moment: "That decision at the crossing cost us."
Another moment: "He's led us wrong before."
Another moment: "Someone else should lead."

These accumulate. Their links converge. A narrative emerges: "Leadership is contested."

**Moments are concrete.** They have text, speaker, time.
**Narratives are patterns.** They're recognized across moments, not authored directly.

---

## P5: Energy Must Land

When energy enters the system, it must go somewhere.

```
Player speaks
  → energy flows to all who heard
  → if no relevant moments exist → energy accumulates on characters
  → if no character flips → energy returns to player character
  → player character always has a handler → something always happens
```

There is no "nothing happens." There is "the silence stretches."

---

## P6: Sequential Actions, Parallel Potentials

**Parallel:** Many character handlers can generate potentials simultaneously.
**Sequential:** Actions that modify world state resolve one at a time.

Aldric and Mildred can both think at once.
Aldric and Mildred cannot both grab the sword at once.

---

## P7: The World Moves Without You

The system does not require player input to advance.

Player can press "Play" and observe.
Time passes. Pressure builds. Characters think. Events unfold.

The player is a participant, not a driver.

---

## P8: Time Is Elastic

The player controls the speed of time, not the content.

| Speed | Feel |
|-------|------|
| 1x | Every moment breathes |
| 2x | Time compresses but conversation persists |
| 3x | World rushes until drama demands attention |

The player is a viewer with a remote. Fast-forward through the boring parts. The system knows when to snap back.

**Speed changes rendering, not reality.** Canon is canon regardless of display speed.

---

## P9: Physics Is The Scheduler

No arbitrary triggers. No cooldowns. No caps.

Character important and close? More energy per tick → flips more often → handler runs more.
Character distant or minor? Less energy → flips rarely → handler runs rarely.

**Importance is derived, not assigned:**
```
importance = sum of weights of all moments ATTACHED_TO this character
```

Character with many high-weight potentials = important right now.
Character with few/low potentials = less important right now.

**Proximity is binary:**
```
proximity = 1.0 if character AT player_location else 0.0
```

Same location = full proximity. Different location = World Runner's domain.

---

## P10: Simultaneous Actions Are Drama

**Old thinking:** Aldric grabs sword + Mildred grabs sword = mutex = resolve conflict.

**New thinking:** Both actualize. Both canon.

```
"Aldric reaches for the sword."
"Mildred's hand closes on the hilt at the same moment."
```

That's not a problem. That's a scene. The consequences play out — struggle, tension, drama.

**Actual mutex (rare):** Same character, two incompatible actions, same tick.
- Aldric "walks east" AND Aldric "walks west"
- Resolution: Higher weight wins. Lower becomes potential for next tick.

Most "conflicts" are actually drama to embrace.

---

## What This Pattern Does NOT Solve

- Does not prevent bad drama (but makes state visible)
- Does not guarantee interesting content (handlers must produce it)
- Does not eliminate LLM latency (but pre-generation helps)
- Does not replace thinking (but structures it)

---

## The Philosophy

**Structure creates behavior.**

Moments don't have "speaker" because speakership is a relationship, not an attribute.
Conversations don't have "shape" because shape emerges from links.
Scenes don't exist because presence is computed, not declared.
Cascades don't have boundaries because the graph never stops.

**The graph is the single source of truth. No files. No trees. Just moments, links, and physics.**

---

*"The narrator weaves possibilities. Physics determines what actualizes. The graph remembers everything."*
