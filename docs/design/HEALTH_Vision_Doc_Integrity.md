# Design Vision — Health: Documentation Integrity

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file ensures the design vision docs remain coherent and linked.
It exists to prevent drift between vision, behaviors, and implementation notes.
It does not verify runtime behavior.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Vision.md
BEHAVIORS:       ./BEHAVIORS_Vision.md
ALGORITHM:       ./ALGORITHM_Vision.md
VALIDATION:      ./VALIDATION_Vision.md
IMPLEMENTATION:  ./IMPLEMENTATION_Vision.md
THIS:            HEALTH_Vision_Doc_Integrity.md
SYNC:            ./SYNC_Vision.md

IMPL:            tools/health/check_vision_docs.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented vision docs health checker
Implement `tools/health/check_vision_docs.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for vision doc integrity
- Updates `status.result.value` in this file
- Runs throttled (max 1/day in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: vision_chain_consistent
    flow_id: vision_docs
    priority: low
    rationale: Vision docs must remain navigable for implementation guidance.
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
    source: vision_chain_consistent
```

---

## HOW TO RUN

```bash
# Manual: verify chain completeness
rg -n "CHAIN" docs/design/*.md
```
