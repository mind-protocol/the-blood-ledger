# Ghost Dialogue — Health: Replay Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks ghost dialogue replay availability. It exists to
detect when ghost injection fails or returns empty results. It does not
verify narrative quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ghost_Dialogue_Index.md
BEHAVIORS:       ./BEHAVIORS_Ghost_Dialogue_Replay.md
ALGORITHM:       ./ALGORITHM_Ghost_Dialogue_Replay.md
VALIDATION:      ./VALIDATION_Ghost_Dialogue_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ghost_Dialogue.md
THIS:            HEALTH_Ghost_Dialogue.md
SYNC:            ./SYNC_Ghost_Dialogue.md

IMPL:            tools/health/check_ghost_dialogue.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented ghost dialogue health checker
Implement `tools/health/check_ghost_dialogue.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for ghost replay
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: ghost_dialogue_available
```
