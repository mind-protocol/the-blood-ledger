# GTM Strategy — Health: Flywheel Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks GTM flywheel health signals (Chronicle output,
acquisition conversions). It exists to prevent blind execution without
feedback loops. It does not verify gameplay quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Direct_Whale_Acquisition.md
BEHAVIORS:       ./BEHAVIORS_Acquisition_Flywheel.md
ALGORITHM:       ./ALGORITHM_GTM_Flywheel.md
VALIDATION:      ./VALIDATION_GTM_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_GTM_Strategy.md
THIS:            HEALTH_GTM_Strategy.md
SYNC:            ./SYNC_GTM_Strategy.md
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: gtm_flywheel_active
    flow_id: acquisition_flywheel
    priority: high
    rationale: Without active flywheel signals, acquisition stalls.
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
    source: gtm_flywheel_active
```
