# Tempo Controller — Implementation: Code Architecture

```
STATUS: IMPLEMENTED
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Tempo.md
BEHAVIORS:      ./BEHAVIORS_Tempo.md
ALGORITHM:      ./ALGORITHM_Tempo_Controller.md
VALIDATION:     ./VALIDATION_Tempo.md
THIS:           IMPLEMENTATION_Tempo.md
TEST:           ./TEST_Tempo.md
SYNC:           ./SYNC_Tempo.md

IMPL:           engine/infrastructure/tempo/tempo_controller.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/tempo/
├── engine/infrastructure/tempo/__init__.py            # Exports TempoController
└── engine/infrastructure/tempo/tempo_controller.py    # Main loop and speed management
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/tempo/__init__.py` | Module exports | - | ~10 | OK |
| `engine/infrastructure/tempo/tempo_controller.py` | Main loop, speed mgmt | `TempoController` | ~320 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Async event loop with state machine

**Why this pattern:**
- Speed is a state machine (pause/1x/2x/3x)
- Main loop runs async for non-blocking ticks
- Input handling via asyncio Event
- Components (physics, canon) accessed synchronously within loop

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| State Machine | speed state | Clean transitions between modes |
| Event Signal | input event | Wake up pause mode on player input |
| Lazy Import | SSE broadcast | Avoid circular dependency |
| Backpressure | 1x mode | Prevent queue overflow |

### Anti-Patterns to Avoid

- **Blocking calls in async**: Physics/Canon are sync, but called from async context
- **Tight spin loops**: Always sleep between ticks (even 0.01s at 3x)
- **Unbounded queues**: Backpressure limit prevents frontend overwhelm

---

## SCHEMA

### Speed Modes

```yaml
Speed:
  pause: Player-driven, one moment per input
  1x: Real-time, ~1 tick/sec, all moments display
  2x: Fast travel, ~5 ticks/sec, dialogue + high weight
  3x: Maximum speed, only interrupts display
```

### Tick Intervals

| Speed | Interval | Display Filter |
|-------|----------|----------------|
| pause | ∞ (wait for input) | 1 moment only |
| 1x | 1.0 sec | All |
| 2x | 0.2 sec | dialogue OR weight > 0.7 |
| 3x | 0.01 sec | interrupt=true only |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `TempoController.__init__()` | `engine/infrastructure/tempo/tempo_controller.py:43` | API on playthrough start |
| `TempoController.run()` | `engine/infrastructure/tempo/tempo_controller.py:69` | asyncio.create_task() |
| `TempoController.on_player_input()` | `engine/infrastructure/tempo/tempo_controller.py:104` | `/api/tempo/input` |
| `TempoController.set_speed()` | `engine/infrastructure/tempo/tempo_controller.py:90` | `/api/tempo/speed` |

---

## DATA FLOW

### Main Loop Flow

```
┌─────────────────────┐
│   TempoController   │
│       .run()        │
└──────────┬──────────┘
           │ speed check
           ▼
┌─────────────────────┐     ┌─────────────────────┐
│ speed == 'pause'?   │────▶│  _wait_for_input()  │
│       NO ↓          │     │  (await Event)      │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │ on input
           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│ _tick_continuous()  │     │   _tick_once()      │
│  - interval wait    │     │  - one tick cycle   │
│  - physics.tick()   │     └─────────────────────┘
│  - detect_ready()   │
│  - canon.record()   │
│  - check_interrupt  │
└─────────────────────┘
```

### Moment Detection Flow

```
┌─────────────────────┐
│ _detect_ready_      │
│    moments()        │
└──────────┬──────────┘
           │ Q1: Salience check
           ▼
┌─────────────────────┐
│ MATCH (m:Moment)    │
│ WHERE status =      │
│   'possible'        │
│ AND salience >= SALIENCE_THRESHOLD │
└──────────┬──────────┘
           │ candidates
           ▼
┌─────────────────────┐
│ Q2: Presence check  │
│ For each candidate: │
│ - ATTACHED_TO chars │
│ - Are they here?    │
└──────────┬──────────┘
           │ ready[]
           ▼
┌─────────────────────┐
│ Return filtered     │
│ moments             │
└─────────────────────┘
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/tempo/tempo_controller.py
    └── imports → GraphQueries (engine.physics.graph)
    └── imports → GraphTick (engine.physics)
    └── imports → CanonHolder (engine.infrastructure.canon)
    └── lazy imports → sse_broadcast (engine.infrastructure.api)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `asyncio` | Async loop, Event | engine/infrastructure/tempo/tempo_controller.py |
| `time` | Tick timing | engine/infrastructure/tempo/tempo_controller.py |
| `logging` | Logging | engine/infrastructure/tempo/tempo_controller.py |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| `speed` | Instance var | Per-playthrough | Session |
| `running` | Instance var | Per-playthrough | Session |
| `tick_count` | Instance var | Per-playthrough | Session |
| `display_queue_size` | Instance var | Per-playthrough | Updated by frontend |

`display_queue_size` updates are normalized to non-negative integers in
`update_display_queue_size` to keep backpressure checks stable.

### State Transitions

```
pause ──set_speed('1x')──▶ 1x
  ▲                         │
  │                         ▼
  └───player_input───────── pause (if at 3x)

1x ◀──interrupt────── 2x ◀──interrupt────── 3x
   ──set_speed('2x')──▶    ──set_speed('3x')──▶
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. API creates TempoController(playthrough_id)
2. Controller connects to graph (GraphQueries, GraphTick, CanonHolder)
3. asyncio.create_task(tempo.run()) starts main loop
4. Default speed: 1x
```

### Main Loop Cycle

```
1. Check self.running (exit if False)
2. If pause: await _input_event, then _tick_once()
3. If 1x/2x/3x: _tick_continuous()
   a. Sleep until interval elapsed
   b. physics.tick()
   c. _detect_ready_moments()
   d. For each ready moment (up to MAX=3):
      - canon.record_to_canon()
      - Check interrupt → snap to 1x if true
   e. Backpressure check at 1x
4. Loop
```

### Shutdown

```
1. tempo.stop() called (or running = False)
2. pending input cleared; _input_event set (wake up if waiting)
3. run() loop exits cleanly
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| `run()` | async | Main loop awaits intervals |
| `on_player_input()` | sync call, async signal | Sets Event for pause mode |
| `physics.tick()` | sync | Blocking call within async loop |
| `canon.record_to_canon()` | sync | Blocking call within async loop |

**Considerations:**
- One TempoController per playthrough
- Multiple playthroughs run concurrent TempoControllers
- Graph operations are sync (FalkorDB client)

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `SALIENCE_THRESHOLD` | `engine/infrastructure/tempo/tempo_controller.py:24` | 0.3 | Min salience for surfacing |
| `MAX_MOMENTS_PER_TICK` | `engine/infrastructure/tempo/tempo_controller.py:25` | `3` | Max moments recorded per tick |
| `BACKPRESSURE_LIMIT` | `engine/infrastructure/tempo/tempo_controller.py:26` | `5` | Queue size before slowdown |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/tempo/tempo_controller.py` | 1 | DOCS pointer to `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md` |
| `engine/infrastructure/tempo/__init__.py` | 1 | DOCS pointer to `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM: Main Loop | `engine/infrastructure/tempo/tempo_controller.py:69` (`run`) |
| ALGORITHM: Speed Modes | `engine/infrastructure/tempo/tempo_controller.py:178` (`_tick_interval`) |
| ALGORITHM: Q1+Q2 | `engine/infrastructure/tempo/tempo_controller.py:188` (`_detect_ready_moments`) |
| ALGORITHM: Interrupt | `engine/infrastructure/tempo/tempo_controller.py:265` (`_check_interrupt`) |

---

## GAPS / IDEAS / QUESTIONS

### Missing

- [ ] API endpoints (`/api/tempo/*`)
- [ ] Frontend speed selector UI
- [ ] Frontend display filtering
- [ ] Tests for TempoController

### Ideas

- IDEA: Metrics for tick latency
- IDEA: Configurable tick intervals per playthrough
- IDEA: "Rewind" feature to see skipped moments at 3x

### Questions

- QUESTION: Should GraphTick be replaced with a lighter physics call?
- QUESTION: How does narrator get triggered? Separate loop?
