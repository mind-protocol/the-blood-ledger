# Voyager System — Health: Import Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks Voyager import activity. It exists to detect missing
imports or unsafe transpositions. It does not verify story quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Trauma_Without_Memory.md
BEHAVIORS:       ./BEHAVIORS_Voyager_Import_Experience.md
ALGORITHM:       ./ALGORITHM_Voyager_Transposition.md
VALIDATION:      ./VALIDATION_Voyager_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Voyager_System.md
THIS:            HEALTH_Voyager_System.md
SYNC:            ./SYNC_Voyager_System.md

IMPL:            tools/health/check_voyager.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented voyager health checker
Implement `tools/health/check_voyager.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for voyager imports
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
    source: voyager_import_activity
```
