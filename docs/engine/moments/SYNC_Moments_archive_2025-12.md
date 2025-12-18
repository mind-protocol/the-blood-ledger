# Archived: SYNC_Moments.md

Archived on: 2025-12-18
Original file: SYNC_Moments.md

---

## Chain

```
THIS FILE:    SYNC_Moments.md (you are here)
    ↓
PATTERNS:     ./PATTERNS_Moments.md
    ↓
BEHAVIORS:    ./BEHAVIORS_Moments.md
    ↓
ALGORITHMS:
  - ./ALGORITHM_Physics.md      (M2: Physics Tick)
  - ./ALGORITHM_Handlers.md     (M3: Character Handlers)
  - ./ALGORITHM_Canon.md        (M4: Canon Holder)
  - ./ALGORITHM_Input.md        (M5: Player Input)
  - ./ALGORITHM_Actions.md      (M7: Action Processing)
  - ./ALGORITHM_Questions.md    (M8: Question Answering)
  - ./ALGORITHM_Speed.md        (M12: Speed Controller)
  - ./ALGORITHM_View_Query.md   (View computation - legacy, to update)
  - ./ALGORITHM_Transitions.md  (Click handling - legacy, to update)
  - ./ALGORITHM_Lifecycle.md    (Status changes - legacy, to update)
    ↓
SCHEMA:       ./SCHEMA_Moments.md
    ↓
API:          ./API_Moments.md
    ↓
VALIDATION:   ./VALIDATION_Moments.md
    ↓
TEST:         ./TEST_Moments.md
```

---


## What Changed (2024-12-18)

### Architecture v2: "The Graph Is Alive"

Major architectural shift from v1:

| v1 (Old) | v2 (New) |
|----------|----------|
| Cascade with start/end | Continuous circulation |
| Handler triggered by multiple events | Handler triggered on flip only |
| Narrator decides what happens | Physics decides via weight/threshold |
| Mutex blocks simultaneous actions | Simultaneous actions are drama |
| Speed not fully specified | Speed controller with snap transition |

### New Core Principles

1. **The graph is always running.** No start/stop. Continuous physics.
2. **On flip. That's it.** Handlers only trigger when moment crosses threshold.
3. **Physics is the scheduler.** No cooldowns, no caps, no arbitrary triggers.
4. **Simultaneous actions are drama.** Canon Holder records both, action processing handles conflict.
5. **Speed doesn't change content.** Same events at any speed, only display differs.

### New Mechanisms Documented

| Mechanism | File | Purpose |
|-----------|------|---------|
| Physics Tick | ALGORITHM_Physics.md | Inject, decay, propagate, detect |
| Character Handlers | ALGORITHM_Handlers.md | Flip-triggered, parallel, scope-isolated |
| Canon Holder | ALGORITHM_Canon.md | Record history, THEN links, no blocking |
| Player Input | ALGORITHM_Input.md | Parse, create moment, inject energy |
| Action Processing | ALGORITHM_Actions.md | Sequential queue, validate, execute |
| Question Answering | ALGORITHM_Questions.md | Non-blocking, fire-and-complete |
| Speed Controller | ALGORITHM_Speed.md | 1x/2x/3x, interrupts, the snap |

### Key Design Decisions

**Importance formula:**
```
importance = sum of weights of moments ATTACHED_TO character
```
Dynamic, derived from graph, not a static property.

**Proximity:**
```
proximity = 1.0 if character AT player_location else 0.0
```
Binary. You're here or you're not.

**Flip threshold:**
```
Deterministic for v1: weight >= 0.8 → flip
```

**Handler output weight:**
- Handler does NOT set weight
- Physics assigns based on relevance × importance

**Decay:**
- Time-based, not tick-based
- 3x speed doesn't decay faster

---


## Documentation Status

### New Files (v2)

| File | Status |
|------|--------|
| ALGORITHM_Physics.md | Complete |
| ALGORITHM_Handlers.md | Complete |
| ALGORITHM_Canon.md | Complete |
| ALGORITHM_Input.md | Complete |
| ALGORITHM_Actions.md | Complete |
| ALGORITHM_Questions.md | Complete |
| ALGORITHM_Speed.md | Complete |
| VALIDATION_Moments.md | Updated with v2 invariants |
| TEST_Moments.md | Complete with 7 trace scenarios |

### Legacy Files (To Update)

| File | Status | Notes |
|------|--------|-------|
| ALGORITHM_View_Query.md | Needs update | Integrate with physics view |
| ALGORITHM_Transitions.md | Needs update | Now part of physics/canon |
| ALGORITHM_Lifecycle.md | Needs update | Now part of physics |
| SCHEMA_Moments.md | May need update | Check for new fields |
| API_Moments.md | May need update | Check for new endpoints |
| PATTERNS_Moments.md | Being updated | Nicolas updating |
| BEHAVIORS_Moments.md | Being updated | Nicolas updating |

### Phase Files (May Deprecate)

| File | Status |
|------|--------|
| PHASE_1_Core_Graph.md | Review — may fold into main docs |
| PHASE_2_Energy_Emergence.md | Review — energy is now core |
| PHASE_3_Citizen_Autonomy.md | Review — handlers cover this |
| PHASE_4_Social_Dynamics.md | Review — multi-party in traces |
| PHASE_5_Natural_Dynamics.md | Review — cascades in traces |
| INFRASTRUCTURE.md | Review — speed controller covers time |

---


## Implementation Status

### Not Yet Implemented

The documentation describes target architecture. Implementation pending:

- [ ] Physics tick loop (continuous)
- [ ] Energy injection formula
- [ ] Handler trigger on flip
- [ ] Handler scope isolation
- [ ] Canon holder
- [ ] Action processing queue
- [ ] Question answerer
- [ ] Speed controller
- [ ] Interrupt detection
- [ ] The snap transition

### Existing Code to Refactor

| File | Current | Target |
|------|---------|--------|
| engine/db/graph_ops.py | Scene-based | Moment-based physics |
| engine/memory/moment_processor.py | Narrator-driven | Handler-driven |
| tools/stream_dialogue.py | Sync generation | Pre-generation |

---

