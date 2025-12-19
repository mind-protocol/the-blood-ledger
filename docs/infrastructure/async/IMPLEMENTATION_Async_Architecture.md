# Async Architecture - Implementation: Injection Hooks and Queue Integration

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Async_Architecture.md
BEHAVIORS:      ./BEHAVIORS_Travel_Experience.md
ALGORITHM:      ./ALGORITHM_Async_Architecture.md
VALIDATION:     ./VALIDATION_Async_Architecture.md
THIS:           IMPLEMENTATION_Async_Architecture.md (you are here)
TEST:           ./TEST_Async_Architecture.md
SYNC:           ./SYNC_Async_Architecture.md

IMPL:           engine/scripts/check_injection.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

### Module Code (Implemented)

```
engine/
|-- scripts/
|   |-- check_injection.py       # Hook script: consume JSONL queue, return injection context
|   `-- inject_to_narrator.py    # CLI helper: write injection queue or call Narrator directly
```

### Related Integration Points (Outside This Module)

- `engine/infrastructure/api/app.py` - `/api/inject` endpoint writes to `injection_queue.jsonl`.
- `engine/infrastructure/api/playthroughs.py` - playthrough bootstrapping creates `injection_queue.json`.
- `agents/narrator/CLAUDE.md` - Narrator instructions for consuming injections.
- `agents/world_runner/CLAUDE.md` - World Runner instructions for emitting injections.

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/scripts/check_injection.py` | PostToolUse hook reader for injection queue (JSONL) | `main()` | ~50 | OK |
| `engine/scripts/inject_to_narrator.py` | Manual injection helper (queue or direct call) | `inject()`, `inject_via_queue()` | ~122 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Event-driven interrupts with a file-backed queue.

**Why this pattern:** Hook scripts must be lightweight and decoupled from the Narrator. A JSONL queue provides a simple FIFO buffer that survives process restarts and can be appended to by multiple producers (API, Runner, CLI).

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| FIFO queue | `engine/scripts/check_injection.py:main` | Consume the oldest injection first without blocking the Narrator loop. |
| Command-line facade | `engine/scripts/inject_to_narrator.py:main` | Provide an operator-friendly way to inject events or call the Narrator directly. |

### Anti-Patterns to Avoid

- **Dual queue formats**: Mixing `injection_queue.json` and `injection_queue.jsonl` makes hooks non-deterministic.
- **Long-running hook work**: The hook must only read/write the queue and return.
- **Hidden side effects**: Avoid mutating graph state in hook scripts; keep them as relays.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Hook injection | Queue read/write and hook payload translation | Narrator handling, Runner generation | `injection_queue.jsonl`, PostToolUse hook payload |
| Manual injection | CLI script and narrator state check | Narrator process management | `inject_to_narrator.py` CLI |

---

## SCHEMA

### Injection Queue Entry (JSONL)

```yaml
InjectionEvent:
  required:
    - type: string            # Event type (player_abort, character_speaks, etc.)
  optional:
    - character: string       # Character ID (if applicable)
    - prompt: string          # Narration prompt or player action
    - current_position: string
    - timestamp: string       # ISO 8601
    - source: string          # writer identifier (frontend, runner, cli)
  constraints:
    - Each entry is one JSON object per line (FIFO consumption).
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Hook injection reader | `engine/scripts/check_injection.py:20` | Claude Code PostToolUse hook for Narrator session |
| Manual injection CLI | `engine/scripts/inject_to_narrator.py:109` | Developer/operator CLI call |

---

## DATA FLOW

### Hook Injection: API/Runner -> Queue -> Narrator

```
Producer(s) (frontend, runner, api)
  -> injection_queue.jsonl (FIFO file queue)
  -> check_injection.py (PostToolUse hook)
  -> Narrator session (handles injection)
```

### Manual Injection: CLI -> Queue or Direct Call

```
CLI command
  -> inject_to_narrator.py
     - if narrator running: write injection_queue.json
     - else: subprocess call to claude -p
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
check_injection.py
    -> uses injection_queue.jsonl (playthroughs/default)

inject_to_narrator.py
    -> reads playthroughs/narrator_state.json
    -> writes playthroughs/{id}/injection_queue.json
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `json` | Serialization of queue entries | `check_injection.py`, `inject_to_narrator.py` |
| `os` | Filesystem paths | `check_injection.py` |
| `pathlib` | Path management | `inject_to_narrator.py` |
| `subprocess` | Direct narrator call | `inject_to_narrator.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| injection queue (JSONL) | `playthroughs/default/injection_queue.jsonl` | per-playthrough | append, consume FIFO |
| narrator status | `playthroughs/narrator_state.json` | global | updated by Narrator runtime |
| injection queue (JSON) | `playthroughs/{id}/injection_queue.json` | per-playthrough | rewritten on inject_to_narrator calls |

---

## CONCURRENCY MODEL

File-backed queues are append/read in separate processes. There is no locking or atomic queue rotation; producers append JSONL lines, and the hook consumes the first line and rewrites the file. This is safe for single-writer, single-reader flows and should be revisited for concurrent writers.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `INJECTION_FILE` | `engine/scripts/check_injection.py` | `playthroughs/default/injection_queue.jsonl` | Queue read by hook script |
| `NARRATOR_STATE_FILE` | `engine/scripts/inject_to_narrator.py` | `playthroughs/narrator_state.json` | Determines whether Narrator is running |

---

## BIDIRECTIONAL LINKS

### Code -> Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/scripts/check_injection.py` | 7 | `DOCS: docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| Hook injection reader | `engine/scripts/check_injection.py:20` |
| Manual injection CLI | `engine/scripts/inject_to_narrator.py:109` |

---

## GAPS / IDEAS / QUESTIONS

### Missing Implementation

- [ ] Reconcile `injection_queue.json` vs `injection_queue.jsonl` format and update producers/consumers to a single queue.
- [ ] Add file lock or atomic rotation for JSONL queue consumption if multiple writers are expected.

### Ideas

- IDEA: Move injection queue helpers into a shared module (e.g., `engine/infrastructure/api/injection_queue.py`).

### Questions

- QUESTION: Should hook consumption switch to per-playthrough injection paths instead of hard-coded `default`?
