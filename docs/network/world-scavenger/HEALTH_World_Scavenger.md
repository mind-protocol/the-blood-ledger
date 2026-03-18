# World Scavenger — Health: Cache Utilization

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks scavenger cache utilization. It exists to detect when
reuse fails and generation costs spike. It does not verify artifact quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scavenge_Before_Generate.md
BEHAVIORS:       ./BEHAVIORS_Scavenger_Priority_Stack.md
ALGORITHM:       ./ALGORITHM_World_Scavenger.md
VALIDATION:      ./VALIDATION_Scavenger_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scavenger.md
THIS:            HEALTH_World_Scavenger.md
SYNC:            ./SYNC_World_Scavenger.md

IMPL:            tools/health/check_world_scavenger.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented world scavenger health checker
Implement `tools/health/check_world_scavenger.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for cache utilization
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
    source: scavenger_cache_hit_rate
```
