# Storm Loader — Health: Mutation Application

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks storm mutation application. It exists to detect when
storm files are ignored or fail to apply. It does not verify storm quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storm_Loader_As_Diff.md
BEHAVIORS:       ./BEHAVIORS_Storm_Loader_Mutations.md
ALGORITHM:       ./ALGORITHM_Storm_Loader_Pipeline.md
VALIDATION:      ./VALIDATION_Storm_Loader_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storm_Loader.md
THIS:            HEALTH_Storm_Loader.md
SYNC:            ./SYNC_Storm_Loader.md

IMPL:            tools/health/check_storm_loader.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented storm loader health checker
Implement `tools/health/check_storm_loader.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for storm mutation application
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
    source: storm_loader_activity
```
