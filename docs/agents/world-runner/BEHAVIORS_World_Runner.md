# World Runner — Behaviors: What It Produces

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## Injection Interface

The Runner returns a structured **Injection** for the Narrator.

```typescript
interface Injection {
  interrupted: boolean;
  at_minute?: number;
  remaining?: number;
  event?: Event;

  completed?: boolean;
  time_elapsed?: number;

  world_changes: WorldChange[];
  news_available: News[];
}
```

See `docs/agents/world-runner/TOOL_REFERENCE.md` for canonical schemas.

---

## Interrupted Injection

- Trigger: a flip affects the player.
- Behavior: stop immediately, return `interrupted: true` and `event`.
- Narrator writes the scene, resolves it, then resumes with `remaining` minutes.

---

## Completed Injection

- Trigger: time span ends without a player-facing flip.
- Behavior: return `completed: true`, `time_elapsed`, and any background world changes/news.

---

## Injection Queue (In-Scene Events)

The Runner can append low-urgency events to `playthroughs/{id}/injection_queue.json` for the Narrator to weave into the current scene. These do **not** interrupt. Typical uses: companion actions, reactions, minor scene beats.

---

## Event / WorldChange / News

```typescript
interface Event {
  type: EventType;
  location: string;
  description: string;
  characters: string[];
  narrator_notes?: string;
}

type EventType = 'ambush' | 'encounter' | 'discovery' | 'arrival' | 'message' | 'event';
```

```typescript
interface WorldChange {
  type: WorldChangeType;
  id: string;
  summary?: string;
  pressure?: number;
}

type WorldChangeType =
  | 'narrative_created'
  | 'narrative_updated'
  | 'tension_created'
  | 'tension_resolved'
  | 'tension_pressure_changed'
  | 'character_moved'
  | 'belief_changed';
```

```typescript
interface News {
  summary: string;
  narrative_id?: string;
  source: string;
  reliability: number;
  location_heard?: string;
}
```

---

## Resume Pattern (Narrator)

```
1. Narrator writes interrupt scene
2. Player responds and resolves
3. Narrator calls Runner with remaining time
4. Runner continues until next interrupt or completion
```

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
