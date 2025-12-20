# Canon Holder — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Canon.md
BEHAVIORS:      ./BEHAVIORS_Canon.md
ALGORITHM:      ./ALGORITHM_Canon_Holder.md
VALIDATION:     ./VALIDATION_Canon.md
THIS:           IMPLEMENTATION_Canon.md
HEALTH:         ./HEALTH_Canon.md
SYNC:           ./SYNC_Canon.md

IMPL:           engine/infrastructure/canon/canon_holder.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/canon/
├── __init__.py          # Exports record_to_canon, CanonHolder
├── canon_holder.py      # Core recording logic
└── speaker.py           # Speaker resolution and rules
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/canon/canon_holder.py` | Spoken status lifecycle | `CanonHolder` | ~310 | OK |
| `engine/infrastructure/canon/speaker.py` | Speaker selection | `determine_speaker` | ~90 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Persistent Transactional Facade (Transactional conceptually).

**Why this pattern:** The Canon Holder ensures that multiple graph updates (status flip, energy cost, THEN link, SAID link) happen as a single logical unit before broadcasting to the player.

---

## SCHEMA

### Moment (Final Canon)

```yaml
Moment:
  required:
    - id: string
    - status: 'spoken'
    - tick_spoken: int
    - energy: float (0.4x original)
```

### Links

```yaml
SAID:
  from: Character
  to: Moment
THEN:
  from: Moment
  to: Moment
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| record_to_canon | `canon_holder.py:54` | Orchestrator after narrating |
| process_ready_moments | `canon_holder.py:153` | Batch tick processing |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Recording Flow: Creation → Reality → SSE

This flow handles the transition of a potential story beat into the immutable game history (canon).

```yaml
flow:
  name: canon_recording
  purpose: Finalize a moment and notify the UI.
  scope: Active Moment -> Graph Update -> Links -> SSE Broadcast
  steps:
    - id: step_1_validate
      description: Check if moment exists and isn't already spoken.
      file: engine/infrastructure/canon/canon_holder.py
      function: record_to_canon
      input: moment_id
      output: boolean status
      trigger: caller invocation
      side_effects: none
    - id: step_2_speaker
      description: Identify the best character to voice the dialogue.
      file: engine/infrastructure/canon/speaker.py
      function: determine_speaker
      input: moment_id, playthrough_id
      output: speaker_id (str)
      trigger: record_to_canon workflow
      side_effects: none
    - id: step_3_update
      description: Flip status and links in FalkorDB.
      file: engine/infrastructure/canon/canon_holder.py
      function: _create_said_link, _create_then_link
      input: speaker_id, previous_moment_id
      output: void
      trigger: successful validation
      side_effects: Graph state mutated
  docking_points:
    guidance:
      include_when: story facts are locked in or the player is notified
    available:
      - id: canon_input
        type: custom
        direction: input
        file: engine/infrastructure/canon/canon_holder.py
        function: record_to_canon
        trigger: Orchestrator
        payload: {moment_id, speaker_id, tick}
        async_hook: optional
        needs: none
        notes: Boundary between narration and fact
      - id: canon_output
        type: event
        direction: output
        file: engine/infrastructure/api/sse_broadcast.py
        function: broadcast_moment_event
        trigger: successful graph write
        payload: MomentSpokenEvent
        async_hook: required
        needs: none
        notes: Real-time update for the frontend
    health_recommended:
      - dock_id: canon_output
        reason: Verification of history chain continuity and delivery.
```

---

## LOGIC CHAINS

### LC1: Speaker Determination

**Purpose:** Select the highest-weight present speaker.

```
moment_id
  → speaker.py:determine_speaker()
    → query characters at player_location
      → filter by state='awake'
        → sort by CAN_SPEAK.strength
          → speaker_id
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/canon/canon_holder.py
    ├── imports → engine.physics.graph
    ├── imports → engine.infrastructure.canon.speaker
    └── lazy imports → engine.infrastructure.api.sse_broadcast
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| History Chain | FalkorDB (THEN links) | Global | Persistent |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Graph Update | Sync | Sequential per playthrough to maintain THEN chain |