# World Runner — Algorithm: Graph Ticks vs Narrative Flips

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## Two Different Things

**Graph Ticks** — Mechanical. Math. No LLM. Fast.

**Narrative Flips** — Story. Reasoning. World Runner (LLM). Only when needed.

---

## Graph Ticks (Mechanical)

Time passes → pressures accumulate.

```yaml
tick:
  trigger: time_elapsed ≥ 5 minutes

  does:
    - tension.pressure += time * base_rate * focus
    - weight recalculated from structure
    - decay on distant narratives

  no_llm: true
  pure_computation: true
```

Simple math. No reasoning. Fast.

### What Gets Computed

```typescript
function graphTick(graph: Graph, time_elapsed: Duration): TickResult {
  // Tension accumulation
  for (const tension of graph.tensions) {
    tension.pressure += time_elapsed * tension.base_rate * tension.focus;
  }

  // Weight recalculation (from structure)
  for (const narrative of graph.narratives) {
    narrative.weight = computeWeight(narrative, graph);
  }

  // Distance decay
  for (const narrative of graph.narratives) {
    if (distanceFromPlayer(narrative, graph) > threshold) {
      narrative.weight *= decay_factor;
    }
  }

  // Check for flips
  const flips = graph.tensions.filter(t => t.pressure > t.breaking_point);

  return { flips };
}
```

---

## Narrative Flips (World Runner)

Pressure crosses threshold → something breaks → need to know WHAT happens.

```yaml
flip:
  trigger:
    - tension.pressure > breaking_point
    - OR contradiction becomes unsustainable
    - OR oath comes due
    - OR secret exposed

  does:
    - World Runner called
    - "What happens when this breaks?"
    - Cascades computed
    - Graph mutated with events

  requires_llm: true
  requires_reasoning: true
```

### What World Runner Receives

```typescript
interface FlipRequest {
  tension: Tension;              // What flipped
  graph_context: GraphSnapshot;  // Current state
  trigger_reason: string;        // Why it flipped
}
```

### What World Runner Returns

```typescript
interface FlipResult {
  event: string;                 // What happened
  new_narratives: Narrative[];   // Created by the break
  belief_changes: BeliefChange[];// Who learned what
  cascades: FlipRequest[];       // Other tensions that now flip
}
```

---

## The Flow

```
Player talks to Aldric for 30 minutes
    │
    ▼
Graph ticks (mechanical)
    - tension_confrontation: 0.85 → 0.87
    - tension_aldric_loyalty: 0.40 → 0.41
    - No threshold crossed
    │
    ▼
No World Runner call
    │
    ▼
Continue conversation

═══════════════════════════════════════════════

Player travels 2 days to York
    │
    ▼
Graph ticks (mechanical)
    - tension_confrontation: 0.87 → 0.95 → FLIP
    - tension_edmund_position: 0.80 → 0.92 → FLIP
    │
    ▼
World Runner called (only for flips)
    - "Edmund's position flipped. What happens?"
    - "Confrontation tension flipped. What happens?"
    │
    ▼
Events determined, graph mutated
    │
    ▼
Narrator receives world_injection
```

---

## Why This Split

| | Graph Tick | Narrative Flip |
|---|---|---|
| **Frequency** | Every 5+ min | Only when threshold crossed |
| **LLM** | No | Yes |
| **Speed** | Fast (ms) | Slow (seconds) |
| **Purpose** | Accumulate pressure | Determine what happens |
| **Output** | Updated numbers | New narratives, events |

**Most time → no LLM.** 30 minutes of conversation? Just tick the numbers.

**LLM only when needed.** Something actually breaks? Now we need reasoning.

**Clear trigger.** Not "has 5 minutes passed?" but "has anything flipped?"

---

## Tick Frequency

```
time_elapsed < 5 min  → No tick
time_elapsed ≥ 5 min  → Tick
flips detected?       → World Runner for each flip
```

Ticks are cheap. Run them liberally. World Runner is expensive. Run only for flips.

---

## Cascade Handling

When World Runner processes a flip, it may cause cascades:

```
Flip A processed
    │
    ▼
Graph mutated
    │
    ▼
Tick graph (check new state)
    │
    ▼
New flips detected? → World Runner for each
    │
    ▼
Repeat until stable
```

The cascade loop alternates: tick (mechanical) → check flips → World Runner (if needed) → tick → check → ...

---

*"Ticks are math. Flips are story. World Runner only runs for story."*
