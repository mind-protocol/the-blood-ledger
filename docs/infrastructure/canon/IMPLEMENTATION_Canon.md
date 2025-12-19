# Canon Holder — Implementation: Code Architecture

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Canon.md
BEHAVIORS:      ./BEHAVIORS_Canon.md
ALGORITHM:      ./ALGORITHM_Canon_Holder.md
VALIDATION:     ./VALIDATION_Canon.md
THIS:           IMPLEMENTATION_Canon.md
TEST:           ./TEST_Canon.md
SYNC:           ./SYNC_Canon.md

IMPL:           engine/infrastructure/canon/canon_holder.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/canon/__init__.py      # Exports record_to_canon, CanonHolder, determine_speaker
engine/infrastructure/canon/canon_holder.py  # Main recording logic
engine/infrastructure/canon/speaker.py       # Speaker resolution
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/canon/__init__.py` | Module exports | - | ~25 | OK |
| `engine/infrastructure/canon/canon_holder.py` | Main recording logic | `CanonHolder`, `record_to_canon()` | ~310 | OK |
| `engine/infrastructure/canon/speaker.py` | Speaker resolution | `determine_speaker()`, `get_moment_type()` | ~90 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Class-based with graph state

**Why this pattern:**
- `CanonHolder` class holds playthrough context (id, graph connection)
- State lives in FalkorDB graph, not in-memory
- Class instance created per-orchestrator for connection reuse

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Lazy Import | `engine/infrastructure/canon/canon_holder.py:132` | Avoid circular dependency with api module |
| Query Builder | `engine/infrastructure/canon/speaker.py` | Construct Cypher queries for speaker resolution |
| Event Emitter | `engine/infrastructure/canon/canon_holder.py` | SSE broadcast after recording |

### Anti-Patterns to Avoid

- **Dual State**: Don't cache moment state locally—always read from graph
- **Silent Failures**: If recording fails, log warning (don't swallow)
- **SSE Without Recording**: Never broadcast before graph write commits
- **Circular Imports**: Use lazy imports when importing from api module

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Canon Module | Recording logic | Moment creation, weight propagation | `CanonHolder.record_to_canon()` |
| SSE | Notification | Client management | `broadcast_moment_event()` |

---

## SCHEMA

### Moment (after recording)

```yaml
Moment:
  required:
    - id: str                    # mom_xxx
    - text: str                  # The spoken text
    - type: str                  # narration | dialogue | action
    - status: str                # 'spoken' after recording
    - tick_spoken: int           # When recorded
    - energy: float              # Reduced by 60% on recording
  optional:
    - action: str                # travel:place_xxx, take:thing_xxx
  constraints:
    - status must be 'spoken'
    - tick_spoken must be set
    - Speaker is NOT stored on moment (see SAID link)
```

### SAID Link

```yaml
SAID:
  from: Character
  to: Moment
  properties:
    - tick: int                  # When spoken
  notes:
    - Created when dialogue moment is recorded
    - Links speaker to moment they spoke
    - Query SAID link to get speaker (not stored on moment)
```

### THEN Link

```yaml
THEN:
  from: Moment
  to: Moment
  properties:
    - tick: int                  # When link was created
    - player_caused: bool        # True if player click triggered
  notes:
    - Links previous moment to current
    - Forms history chain
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `CanonHolder.record_to_canon()` | `engine/infrastructure/canon/canon_holder.py:54` | Orchestrator after narrator |
| `CanonHolder.process_ready_moments()` | `engine/infrastructure/canon/canon_holder.py:153` | Tick loop (future) |
| `determine_speaker()` | `engine/infrastructure/canon/speaker.py:20` | Called by record_to_canon |
| `record_to_canon()` (convenience) | `engine/infrastructure/canon/canon_holder.py:282` | Direct calls |

---

## DATA FLOW

### Recording Flow: Moment → Canon

```
┌─────────────────────┐
│  Active Moment      │ (in graph, status='active')
└──────────┬──────────┘
           │ moment_id
           ▼
┌─────────────────────┐
│  engine/infrastructure/canon/canon_holder.py    │ ← CanonHolder.record_to_canon()
│  1. validate status │
│  2. update moment   │ (Q6 Step 1)
│  3. create SAID     │ (Q6 Step 2)
│  4. create THEN     │ (Q6 Step 3)
│  5. broadcast SSE   │
└──────────┬──────────┘
           │ commit
           ▼
┌─────────────────────┐
│  Spoken Moment      │ (in graph, status='spoken')
│  + SAID link        │ (if dialogue)
│  + THEN link        │ (if previous)
└──────────┬──────────┘
           │ event
           ▼
┌─────────────────────┐
│  SSE to Frontend    │ (moment_spoken event)
└─────────────────────┘
```

### Integration Flow: Orchestrator → Canon Holder

```
┌─────────────────────┐
│    Orchestrator     │
│  orchestrator.py    │
└──────────┬──────────┘
           │ narrator output (scene.narration, scene.voices)
           ▼
┌─────────────────────┐
│ _record_narrator_   │ ← orchestrator.py:336
│   output()          │
│  - create Moment    │
│  - call Canon       │
└──────────┬──────────┘
           │ for each narration/voice
           ▼
┌─────────────────────┐
│ CanonHolder.        │
│ record_to_canon()   │
│  - engine/infrastructure/canon/speaker.py       │
│  - sse_broadcast    │
└─────────────────────┘
```

---

## LOGIC CHAINS

### LC1: Record Single Moment (Q6)

**Purpose:** Record one moment to canon

```
moment (active)
  → validate status != 'spoken'       # Early return if already spoken
    → determine_speaker() if dialogue # Q5 from ALGORITHM
      → Q6 Step 1: SET status, tick_spoken, energy
        → Q6 Step 2: CREATE SAID link (if speaker)
          → Q6 Step 3: CREATE THEN link (if previous)
            → broadcast_moment_event()   # SSE to frontend
```

**Data transformation:**
- Input: `Moment` with status='active'
- After Q6 Step 1: `Moment` with status='spoken', tick_spoken set, energy *= 0.4
- After Q6 Step 2: New `SAID` edge from Character to Moment
- After Q6 Step 3: New `THEN` edge from previous Moment
- Output: SSE event sent, result dict returned

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/canon/canon_holder.py
    └── imports → engine/infrastructure/canon/speaker.py (determine_speaker, get_moment_type)
    └── lazy imports → sse_broadcast.py (broadcast_moment_event)
    └── imports → GraphQueries (from engine.physics.graph)

engine/infrastructure/canon/speaker.py
    └── imports → GraphQueries (from engine.physics.graph)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `logging` | Error/debug logging | All files |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Moment data | FalkorDB graph | Per-playthrough | Persistent |
| Current tick | Passed as parameter | Per-call | Transient |
| Last spoken moment | Queried from graph | Per-request | Transient |
| SSE client queues | sse_broadcast module | Per-playthrough | Session |

### State Transitions

```
active ──record_to_canon()──▶ spoken
         (creates SAID, THEN links)
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Orchestrator creates CanonHolder(playthrough_id)
2. CanonHolder connects to FalkorDB graph
3. Ready to record moments
```

### Main Recording Cycle

```
1. Caller invokes record_to_canon(moment_id, speaker_id, previous_id, tick)
2. Validate moment exists and status != 'spoken'
3. For dialogue: resolve speaker if not provided
4. Q6 Step 1: Update graph (status='spoken', tick_spoken, energy *= 0.4)
5. Q6 Step 2: Create SAID link (if speaker_id)
6. Q6 Step 3: Create THEN link (if previous_id)
7. Broadcast SSE moment_spoken event
8. Return result dict
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| `record_to_canon` | sync | Called from async context, graph ops are sync |
| SSE broadcast | async queue | put_nowait into client queues |

**Considerations:**
- Graph writes are individual queries (not transactional)
- Multiple concurrent recordings need sequencing by caller
- Current design: orchestrator sequences calls

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `ACTUALIZATION_COST` | `engine/infrastructure/canon/canon_holder.py:26` | 0.6 | Energy cost when speaking (keeps 40%) |
| `MAX_MOMENTS_PER_TICK` | `engine/infrastructure/canon/canon_holder.py:27` | `3` | Max moments recorded per tick |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/canon/canon_holder.py` | 1 | `docs/infrastructure/canon/IMPLEMENTATION_Canon.md` |
| `engine/infrastructure/canon/speaker.py` | 1 | `docs/infrastructure/canon/IMPLEMENTATION_Canon.md` |
| `engine/infrastructure/canon/__init__.py` | 1 | `docs/infrastructure/canon/IMPLEMENTATION_Canon.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM Q5 (speaker) | `engine/infrastructure/canon/speaker.py:20` (`determine_speaker`) |
| ALGORITHM Q6 Step 1 | `engine/infrastructure/canon/canon_holder.py:113` (SET status='spoken') |
| ALGORITHM Q6 Step 2 | `engine/infrastructure/canon/canon_holder.py:221` (`_create_said_link`) |
| ALGORITHM Q6 Step 3 | `engine/infrastructure/canon/canon_holder.py:243` (`_create_then_link`) |
| ALGORITHM Q7 | `engine/infrastructure/canon/canon_holder.py:269` (`_get_last_spoken_moment_id`) |

---

## GAPS / IDEAS / QUESTIONS

### Completed

- [x] Create `engine/infrastructure/canon/` directory
- [x] Implement `engine/infrastructure/canon/canon_holder.py` with `CanonHolder` class
- [x] Implement `engine/infrastructure/canon/speaker.py` with `determine_speaker()`
- [x] Integrate with orchestrator
- [x] Create SAID link per ALGORITHM Q6 Step 2

### Missing Implementation

- [ ] Time advancement module (not implemented)
- [ ] Strength mechanics module (not implemented)
- [ ] Comprehensive test suite
- [ ] detect_and_surface() for possible → active (tick loop)

### Ideas

- IDEA: Add transaction wrapper for atomic recording
- IDEA: Metrics for recording latency

### Questions

- QUESTION: Should graph writes be transactional?
- QUESTION: How to handle partial failures (SAID succeeds, THEN fails)?
