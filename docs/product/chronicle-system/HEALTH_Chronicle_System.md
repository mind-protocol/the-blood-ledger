# Chronicle System — Health: Pipeline Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the Chronicle generation pipeline. It exists to
detect failures where chronicles are generated without assets or metadata. It
does not verify narrative quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
BEHAVIORS:       ./BEHAVIORS_Chronicle_Types_And_Structure.md
ALGORITHM:       ./ALGORITHM_Chronicle_Generation_Pipeline.md
VALIDATION:      ./VALIDATION_Chronicle_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Chronicle_System.md
THIS:            HEALTH_Chronicle_System.md
SYNC:            ./SYNC_Chronicle_System.md

IMPL:            tools/health/check_chronicle.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented chronicle health checker
Implement `tools/health/check_chronicle.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for chronicle generation
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: chronicle_output_ready
    flow_id: chronicle_generation
    priority: high
    rationale: Chronicles must produce a publishable artifact.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: chronicle_output_ready
```

---

## HOW TO RUN

```bash
# Manual: verify chronicle output package is produced
# (no runtime pipeline implemented in this repo yet)
```
