# Shadow Feed — Health: Rumor Flow Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks rumor import and cache availability. It exists to
detect when the shadow feed runs dry or fails safety locks. It does not verify
rumor quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Shadow_Feed_Rumor_Cache.md
BEHAVIORS:       ./BEHAVIORS_Rumor_Import.md
ALGORITHM:       ./ALGORITHM_Shadow_Feed_Import.md
VALIDATION:      ./VALIDATION_Shadow_Feed_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_Shadow_Feed.md
THIS:            HEALTH_Shadow_Feed.md
SYNC:            ./SYNC_Shadow_Feed.md

IMPL:            tools/health/check_shadow_feed.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented shadow feed health checker
Implement `tools/health/check_shadow_feed.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for rumor flow
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
    source: shadow_feed_active
```
