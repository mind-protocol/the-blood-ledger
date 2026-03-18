# Storms — Health: Overlay Activity

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks storm overlay application. It exists to detect when
storms fail to apply or never expire. It does not verify narrative quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storms_As_Crisis_Overlays.md
BEHAVIORS:       ./BEHAVIORS_Storm_Overlay_Behavior.md
ALGORITHM:       ./ALGORITHM_Storm_Application.md
VALIDATION:      ./VALIDATION_Storm_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storms.md
THIS:            HEALTH_Storms.md
SYNC:            ./SYNC_Storms.md

IMPL:            tools/health/check_storms.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented storms health checker
Implement `tools/health/check_storms.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for storm overlays
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
    source: storm_overlay_activity
```
