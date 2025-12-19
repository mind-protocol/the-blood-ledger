# Narrator Input Reference

What the Narrator receives from the Orchestrator.

---

## Script Locations

```
engine/infrastructure/orchestration/narrator.py  # Narrator caller + prompt builder
engine/models/                                   # Pydantic models for validation
```

---

## Prompt Structure (High-Level)

```
NARRATOR INSTRUCTION
====================

{SCENE_CONTEXT}

{WORLD_INJECTION if flips occurred}

{GENERATION_INSTRUCTION}
```

---

## Scene Context (Always Provided)

```typescript
interface SceneContext {
  location: LocationContext;
  time: TimeContext;
  present: CharacterBrief[];
  active_narratives: ActiveNarrative[];
  tensions: TensionBrief[];
  player_state: PlayerState;
}
```

---

## World Injection (If Flips Occurred)

```typescript
interface WorldInjection {
  time_since_last: string;
  breaks: Break[];
  news_arrived?: NewsItem[];
  tension_changes?: Record<string, string>;
  interruption?: Interruption | null;
  atmosphere_shift?: string;
  narrator_notes?: string;
}
```

Handling rules: see `BEHAVIORS_Narrator.md`.

---

## Query Patterns (Typical)

1. Recent narratives since last scene
2. Character movements and arrivals
3. Active tensions and breaking points
4. Character beliefs and backstory details
