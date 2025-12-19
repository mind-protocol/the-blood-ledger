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
engine/scripts/check_injection.py       # Hook script: consume JSONL queue, return injection context
engine/scripts/inject_to_narrator.py    # CLI helper: write injection queue or call Narrator directly
```

### Related Integration Points (Outside This Module)

- `engine/infrastructure/api/app.py` - `/api/inject` endpoint appends to the injection queue file configured in `engine/scripts/check_injection.py`.
- `engine/infrastructure/api/playthroughs.py` - playthrough bootstrapping initializes the per-playthrough injection queue handled by `engine/scripts/inject_to_narrator.py`.
- `agents/narrator/CLAUDE.md` - Narrator instructions for consuming injections.
- `agents/world_runner/CLAUDE.md` - World Runner instructions for emitting injections.

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/scripts/check_injection.py` | PostToolUse hook reader for injection queue (JSONL) | `main()` | ~52 | OK |
| `engine/scripts/inject_to_narrator.py` | Manual injection helper (queue or direct call) | `inject()`, `inject_via_queue()`, `inject_via_direct_call()` | ~124 | OK |

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

- **Dual queue formats**: Mixing JSON and JSONL queue formats makes hooks non-deterministic.
- **Long-running hook work**: The hook must only read/write the queue and return.
- **Hidden side effects**: Avoid mutating graph state in hook scripts; keep them as relays.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Hook injection | Queue read/write and hook payload translation | Narrator handling, Runner generation | Injection queue file referenced by `engine/scripts/check_injection.py`, PostToolUse hook payload |
| Manual injection | CLI script and narrator state check | Narrator process management | `engine/scripts/inject_to_narrator.py` CLI |

---

## SCHEMA

### Injection Queue Entry (JSONL)

Stored at `playthroughs/default/injection_queue.jsonl`.

```
Each line is a JSON object written directly from /api/inject.
No schema validation exists at write time; payload is passed through to the hook.
```

### Injection Queue Entry (JSON Array)

Stored at `playthroughs/{playthrough_id}/injection_queue.json`.

```yaml
InjectionEvent:
  required:
    - message: string
    - timestamp: string       # ISO 8601
    - source: string          # writer identifier (world_runner)
  constraints:
    - File is a JSON array of InjectionEvent objects.
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Hook injection reader | `engine/scripts/check_injection.py:20` | Claude Code PostToolUse hook for Narrator session |
| Manual injection CLI | `engine/scripts/inject_to_narrator.py:111` | Developer/operator CLI call |

---

## DATA FLOW

### Hook Injection: API/Runner -> Queue -> Narrator

```
Producer(s) (frontend, runner, api)
  -> `/api/inject` appends JSON to `playthroughs/default/injection_queue.jsonl`
  -> engine/scripts/check_injection.py (PostToolUse hook)
  -> Narrator session (handles injection payload)
```

### Manual Injection: CLI -> Queue or Direct Call

```
CLI command
  -> engine/scripts/inject_to_narrator.py
     - if narrator running: append to `playthroughs/{playthrough_id}/injection_queue.json`
     - else: subprocess call to claude -p
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/scripts/check_injection.py
    -> uses the JSONL injection queue file (path configured in-script)

engine/scripts/inject_to_narrator.py
    -> reads narrator state (path configured in-script)
    -> writes the per-playthrough JSON injection queue file
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `json` | Serialization of queue entries | `engine/scripts/check_injection.py`, `engine/scripts/inject_to_narrator.py` |
| `os` | Filesystem paths | `engine/scripts/check_injection.py` |
| `pathlib` | Path management | `engine/scripts/inject_to_narrator.py` |
| `subprocess` | Direct narrator call | `engine/scripts/inject_to_narrator.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| injection queue (JSONL) | `playthroughs/default/injection_queue.jsonl` | default/global | append, consume FIFO |
| narrator status | `playthroughs/narrator_state.json` | global | updated by Narrator runtime |
| injection queue (JSON array) | `playthroughs/{playthrough_id}/injection_queue.json` | per-playthrough | rewritten on inject_to_narrator calls |

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
| `engine/scripts/check_injection.py` | 7 | `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` |
| `engine/scripts/inject_to_narrator.py` | 8 | `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| Hook injection reader | `engine/scripts/check_injection.py:20` |
| Manual injection CLI | `engine/scripts/inject_to_narrator.py:111` |

---

## GAPS / IDEAS / QUESTIONS

### Missing Implementation

- [ ] Reconcile JSON vs JSONL injection queue formats and update producers/consumers to a single queue.
- [ ] Align `engine/infrastructure/api/playthroughs.py` initialization (`{"injections": []}`) with the array format expected by `engine/scripts/inject_to_narrator.py`.
- [ ] Add file lock or atomic rotation for JSONL queue consumption if multiple writers are expected.

### Ideas

- IDEA: Move injection queue helpers into a shared module under `engine/infrastructure/api/`.

### Questions

- QUESTION: Should hook consumption switch to per-playthrough injection paths instead of hard-coded `default`?
