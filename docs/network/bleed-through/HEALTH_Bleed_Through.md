# Bleed-Through — Health: Scar Injection Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks bleed-through injection activity. It exists to detect
missing cross-world transfers or unsafe injections. It does not verify
narrative quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scars_Cross_Worlds.md
BEHAVIORS:       ./BEHAVIORS_Ghosts_Rumors_Reports.md
ALGORITHM:       ./ALGORITHM_Bleed_Through_Pipeline.md
VALIDATION:      ./VALIDATION_Bleed_Through_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Bleed_Through.md
THIS:            HEALTH_Bleed_Through.md
SYNC:            ./SYNC_Bleed_Through.md

IMPL:            tools/health/check_bleed_through.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented bleed-through health checker
Implement `tools/health/check_bleed_through.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for scar injection
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
    source: bleed_through_activity
```
