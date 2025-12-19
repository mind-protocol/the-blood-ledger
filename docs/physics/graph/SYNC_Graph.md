# Graph — Current State

```
UPDATED: 2024-12-16
STATUS: Documented, not implemented
```

---

## What Exists

### Documentation
- [x] PATTERNS_Graph.md — Core philosophy (energy as attention, computed weight)
- [x] BEHAVIORS_Graph.md — What the graph does (flow, propagation, decay, pressure, flips, criticality)
- [x] ALGORITHM_Energy_Flow.md — Per-tick processing with link-type propagation
- [x] ALGORITHM_Weight_Computation.md — How weight emerges from structure

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

## Key Design Decisions

### Energy Sources Are Characters

Characters are the ONLY energy sources. Their energy is computed:
```
character.energy = relationship_intensity × geographical_proximity
```

Agents (Narrator, World Runner) don't inject energy. They update link strengths. Energy emerges from structure automatically.

**Approach creates tension automatically.** When player travels toward York, Edmund's proximity changes from 0.2 to 0.7. His energy triples. His narratives heat up. Confrontation tension rises. No one decided this. Physics decided this.

### Link-Type Dependent Propagation

| Type | Direction | Effect |
|------|-----------|--------|
| Contradicts | Bidirectional | Both sides heat up |
| Supports | Bidirectional | Allies rise together |
| Elaborates | Parent → Child | Detail inherits from general |
| Subsumes | Child → Parent | Specific feeds general |
| Supersedes | Old → New | Replacement drains original |

### Open System with Criticality Feedback

**Not energy conservation.** Open system with sources and sinks.

- Sources: Characters pump energy in
- Sinks: Decay pulls energy out
- Equilibrium: Each narrative stabilizes where inflow = outflow

`decay_rate` is the global damper — adjusted dynamically to maintain criticality.

### Three Pressure Types

| Type | Behavior |
|------|----------|
| Gradual | Ticks upward steadily, uncertain when breaks |
| Scheduled | Follows timeline, can jump overnight |
| Hybrid | Both — has floor from schedule, can exceed via events |

### Cascades Have Limits

Maximum 5 cascade breaks per cycle. If more would occur, pause and let Narrator present what happened.

### Graph Is The Only Channel

World Runner and Narrator never communicate directly. World Runner writes to graph. Narrator reads from graph.

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

## The Full Energy Cycle

```
Characters pump energy (computed from relationship × proximity)
    ↓
Narratives receive energy (via belief links)
    ↓
Energy propagates (via narrative links)
    ↓
Energy decays (2% per tick)
    ↓
Equilibrium: inflow = outflow
    ↓
Pressure ticks (gradual/scheduled/hybrid)
    ↓
Threshold exceeded? → Flip → World Runner
    ↓
World Runner writes graph updates
    ↓
Narrator reads graph, renders experience
    ↓
Repeat
```

---

## Open Questions

1. **Where does graph engine run?**
   - Python script? TypeScript? Same as orchestrator?

2. **Graph storage during play**
   - JSON files? In-memory? FalkorDB?

3. **Tick timing**
   - Who triggers ticks? Narrator's time_elapsed? Real time?

---

## Next Steps

1. **Implement graph tick**
   - Energy computation
   - Propagation
   - Decay
   - Pressure

2. **Integrate with orchestrator**
   - Call graph tick after narrator response
   - Trigger World Runner on flips

3. **Test energy dynamics**
   - Verify equilibrium behavior
   - Tune parameters for criticality

---

*"Characters are batteries. Narratives are circuits. Energy flows through links."*

---

## CONFLICTS

### DECISION: Graph Health Check Incomplete Impl
- Conflict: Repair task flagged `add_issue`, `error_count`, `warning_count`, `is_healthy`, and `load_schema` as empty in `engine/graph/health/check_health.py`, but each function already implements concrete behavior.
- Resolution: Treat the issue as already resolved; no code changes required.
- Reasoning: The functions already manage issues, counts, health status, and schema loading for the health report flow.
- Updated: `docs/physics/graph/SYNC_Graph.md`

### DECISION: Graph Ops Event Listener Incomplete Impl
- Conflict: Repair task flagged `add_mutation_listener` and `remove_mutation_listener` as empty in `engine/physics/graph/graph_ops_events.py`, but both functions already implement registration and removal logic.
- Resolution: Treat the issue as already resolved; no code changes required.
- Reasoning: The functions already mutate the listener registry and are exercised by graph ops event emission.
- Updated: `docs/physics/graph/SYNC_Graph.md`

### DECISION: Graph Queries Moments Incomplete Impl
- Conflict: Repair task flagged empty implementations for `get_narrative_moments`, `get_narratives_from_moment`, `get_available_transitions`, and `get_clickable_words` in `engine/physics/graph/graph_queries_moments.py`, but each function already contains full query logic.
- Resolution: Treat the issue as already resolved; no code changes required.
- Reasoning: The functions execute concrete Cypher queries and result parsing for narrative, transition, and clickable word lookups.
- Updated: `docs/physics/graph/SYNC_Graph.md`

### DECISION: Graph Queries Moments Incomplete Impl
- Conflict: Repair task flagged `get_narrative_moments`, `get_narratives_from_moment`, `get_available_transitions`, and `get_clickable_words` as empty in `engine/physics/graph/graph_queries_moments.py`, but each function already contains concrete Cypher query logic.
- Resolution: Treat the issue as already resolved; no code changes required.
- Reasoning: The functions already query FalkorDB and parse results as part of `GraphQueries` moment/view flows.
- Updated: `docs/physics/graph/SYNC_Graph.md`

### DECISION: Graph Ops Types Incomplete Impl
- Conflict: Repair task flagged `__str__` and `success` as empty in `engine/physics/graph/graph_ops_types.py`, but both functions already implement formatting and error-free status checks.
- Resolution: Treat the issue as already resolved; no code changes required.
- Reasoning: `SimilarNode.__str__` and `ApplyResult.success` already provide concrete behavior used by graph ops apply reporting.
- Updated: `docs/physics/graph/SYNC_Graph.md`

## Agent Observations

### Remarks
- Repair task appears stale relative to `engine/physics/graph/graph_ops_events.py`.
- Repair task appears stale relative to `engine/physics/graph/graph_queries_moments.py`.
- Repair task appears stale relative to `engine/physics/graph/graph_ops_types.py`.
- Repair task appears stale relative to `engine/graph/health/check_health.py`.

### Suggestions
- None.

### Propositions
- None.
