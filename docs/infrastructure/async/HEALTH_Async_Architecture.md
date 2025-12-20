# Async Architecture — Health: Coordination Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers asynchronous coordination signals (runner output,
queue behavior, SSE). It exists to surface failures where async hooks or
background tasks stall. It does not verify narrative correctness.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Async_Architecture.md
BEHAVIORS:       ./BEHAVIORS_Travel_Experience.md
ALGORITHM:       ./ALGORITHM_Async_Architecture.md
VALIDATION:      ./VALIDATION_Async_Architecture.md
IMPLEMENTATION:  ./IMPLEMENTATION_Async_Architecture.md
THIS:            HEALTH_Async_Architecture.md
SYNC:            ./SYNC_Async_Architecture.md
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: async_hook_latency
    flow_id: async_hooks
    priority: high
    rationale: UI-critical hooks must stay within latency budget.
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
    source: async_hook_latency
```

---

## HOW TO RUN

```bash
# Manual: run narrator + runner concurrently and watch logs for latency warnings
# (no automated runner hook health check yet)
```

---

## KNOWN GAPS

- [ ] No automated latency measurement for async hooks.
- [ ] No queue depth monitoring in current runtime.
