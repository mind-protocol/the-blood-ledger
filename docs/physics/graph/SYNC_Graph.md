# Graph — Current State

```
UPDATED: 2025-12-19
STATUS: Documented, not implemented
```

---

## What Exists

### Documentation
- [x] PATTERNS_Graph.md — Core philosophy (energy as attention, computed weight)
- [x] BEHAVIORS_Graph.md — What the graph does (flow, propagation, decay, pressure, flips, criticality)
- [x] ALGORITHM_Energy_Flow.md — Per-tick processing with link-type propagation and weight recomputation
- [x] ALGORITHM_Weight.md — Redirect to ALGORITHM_Energy_Flow.md (deprecated duplicate)
- [x] VALIDATION_Living_Graph.md — Validation spec tying behaviors to tests and desired feel

### Data
- [x] `/data/graph.json` — Narrative graph with characters, narratives, tensions

### Frontend
- [x] Scene tree types that reference graph entities
- [x] Click → lookup response (graph not queried yet, uses pre-baked trees)

---

## What's Missing

### Graph Engine (not started)
- [ ] Character energy computation
- [ ] Energy flow (characters → narratives)
- [ ] Energy propagation (narratives → narratives)
- [ ] Energy decay
- [ ] Pressure tick (gradual, scheduled, hybrid)
- [ ] Flip detection
- [ ] Weight computation

### Integration (not started)
- [ ] Orchestrator calls graph engine
- [ ] Graph engine triggers World Runner on flips
- [ ] Narrator reads graph for context

---

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| belief_flow_rate | 0.1 | Character → Narrative |
| propagation_factor | 0.2 | Narrative → Narrative |
| max_propagation_hops | 3 | Prevents infinite chains |
| decay_rate | 0.02 (dynamic) | Adjusted by criticality |
| decay_rate range | 0.005 - 0.1 | Clamped bounds |
| min_weight | 0.01 | Never fully zero |
| base_rate (pressure) | 0.001/min | |
| default_breaking_point | 0.9 | |
| tick_threshold | 5 min | |
| max_cascade_depth | 5 | |

---

## Criticality Targets

The Narrator maintains the system near critical threshold:

| Measure | Target |
|---------|--------|
| Average pressure | 0.4 - 0.6 |
| Max pressure | At least one > 0.7 |
| Break frequency | 0.5 - 2.0 per game-hour |

---

## Open Questions

1. **Where does graph engine run?**
   - Python script? TypeScript? Same as orchestrator?

2. **Graph storage during play**
   - JSON files? In-memory? FalkorDB?

3. **Tick timing**
   - Who triggers ticks? Narrator's time_elapsed? Real time?

---

## Recent Changes

### 2025-12-19: Consolidated weight algorithm docs

- Redirected `ALGORITHM_Weight.md` to the canonical `ALGORITHM_Energy_Flow.md` to remove duplication.

### 2025-12-19: Verified graph health check helpers

- Confirmed `engine/graph/health/check_health.py` already implements health report helpers; repair task marked stale.

---

## Agent Observations

### Remarks
- Health check helper implementations already exist; repair task was stale.

---

## ARCHIVE

Older content archived to: `SYNC_Graph_archive_2025-12.md`


---

## ARCHIVE

Older content archived to: `SYNC_Graph_archive_2025-12.md`
