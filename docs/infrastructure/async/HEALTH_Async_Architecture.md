# Async Architecture — Health: Coordination Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-22
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers asynchronous coordination signals (injection hooks, queue behavior, SSE). It exists to prevent:
- Stalled injection queues
- Dropped events due to latency
- Non-idempotent hook behavior
- Unbounded queue growth

It does not verify narrative correctness.

---

## WHY THIS PATTERN

Async hooks bridge producers (API, Runner) and consumers (Narrator). Tests verify individual components, but HEALTH checks verify the full inject→queue→consume pipeline stays responsive. Dock-based checks ensure:
- Hooks respond within latency budget
- Queues don't grow unbounded
- FIFO ordering is maintained

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_Infrastructure_Async.md
PATTERNS:        ./PATTERNS_Async_Architecture.md
BEHAVIORS:       ./BEHAVIORS_Travel_Experience.md
ALGORITHM:       ./ALGORITHM/ALGORITHM_Hook_Injection.md
VALIDATION:      ./VALIDATION_Async_Architecture.md
IMPLEMENTATION:  ./IMPLEMENTATION_Async_Architecture.md
THIS:            HEALTH_Async_Architecture.md
SYNC:            ./SYNC_Async_Architecture.md

IMPL:            tools/health/check_async.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented async health checker
Implement `tools/health/check_async.py` checker script that:
- Executes dock-based verification against VALIDATION criteria INV1-INV4
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: hook_injection
    purpose: Deliver injected events from queue to Narrator.
    triggers:
      - type: event
        source: engine/scripts/check_injection.py
        notes: PostToolUse hook triggered by Narrator session.
    frequency:
      expected_rate: 1-10/min
      peak_rate: 30/min
      burst_behavior: Bursts during world updates.
    risks:
      - Latency budget exceeded
      - Queue file corruption
      - Idempotency violation
    notes: Must complete quickly to not block Narrator.

  - flow_id: queue_management
    purpose: Maintain FIFO queue for injections.
    triggers:
      - type: event
        source: POST /api/inject
        notes: Appends to injection queue file.
    frequency:
      expected_rate: 0.5-5/min
      peak_rate: 20/min
      burst_behavior: Bounded by queue size limits.
    risks:
      - Unbounded growth
      - Lost entries on crash
    notes: File-backed for durability.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Hook responsiveness | async_hook_latency | Slow hooks = blocked Narrator |
| Queue health | queue_depth_stable | Growing queue = stalled consumers |
| Delivery reliability | injection_delivered | Dropped events = missing world updates |

```yaml
health_indicators:
  - name: async_hook_latency
    flow_id: hook_injection
    priority: high
    rationale: UI-critical hooks must stay within latency budget.

  - name: queue_depth_stable
    flow_id: queue_management
    priority: med
    rationale: Queue should not grow unbounded.

  - name: injection_delivered
    flow_id: hook_injection
    priority: high
    rationale: Injected events must reach Narrator.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-22T00:00:00Z
    source: async_hook_latency
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: async_hook_latency
    purpose: Verify hooks respond within latency budget (INV4).
    status: pending
    priority: high

  - name: queue_depth_stable
    purpose: Verify queue size stays bounded (INV2).
    status: pending
    priority: med

  - name: injection_delivered
    purpose: Verify injections reach consumer.
    status: pending
    priority: high
```

---

## INDICATOR: async_hook_latency

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: async_hook_latency
  client_value: UI remains responsive; no blocked interactions.
  validation:
    - validation_id: INV4
      criteria: Hook invocations respond within short window.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum, float_0_1]
  selected: [enum]
  semantics:
    enum: OK (< 100ms), WARN (100-500ms), ERROR (> 500ms)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: hook_trigger
    method: check_injection.main
    location: engine/scripts/check_injection.py:20
  output:
    id: hook_response
    method: check_injection.main
    location: engine/scripts/check_injection.py:50
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Time hook execution, verify under threshold.
  steps:
    - Inject test event to queue.
    - Trigger hook script.
    - Measure execution time.
    - Verify < 100ms for OK, < 500ms for WARN.
  data_required: Queue file access, timing measurements.
  failure_mode: Hook takes > 500ms.
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 1/hour
  burst_limit: 3
  backoff: none
```

### MANUAL RUN

```yaml
manual_run:
  command: |
    python3 - <<'PY'
    import time
    import subprocess
    start = time.time()
    subprocess.run(["python3", "engine/scripts/check_injection.py"], timeout=5)
    elapsed = (time.time() - start) * 1000
    status = "OK" if elapsed < 100 else "WARN" if elapsed < 500 else "ERROR"
    print(f"{status}: hook latency = {elapsed:.0f}ms")
    PY
  notes: Requires injection queue file to exist.
```

---

## HOW TO RUN

```bash
# Run async health checks (manual)
# 1. Check hook latency
python3 - <<'PY'
import time
import subprocess
start = time.time()
result = subprocess.run(["python3", "engine/scripts/check_injection.py"],
                       capture_output=True, timeout=5)
elapsed = (time.time() - start) * 1000
print(f"async_hook_latency: {'OK' if elapsed < 100 else 'WARN' if elapsed < 500 else 'ERROR'} ({elapsed:.0f}ms)")
PY

# 2. Check queue depth
wc -l playthroughs/default/injection_queue.jsonl 2>/dev/null || echo "queue_depth: OK (file empty or missing)"

# Run narrator + runner concurrently and watch logs for latency warnings
```

---

## KNOWN GAPS

- [ ] INV1 (single source of truth) checker not implemented - requires graph inspection.
- [ ] INV2 (bounded queues) automated checker not implemented.
- [ ] INV3 (idempotent actions) checker not implemented.
- [ ] No automated latency measurement for async hooks.
- [ ] No queue depth monitoring in current runtime.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add queue length alerting for stalled readers.
- IDEA: Add timing instrumentation to hook scripts.
- QUESTION: Should queue readers migrate to per-playthrough paths instead of default?
