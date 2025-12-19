# Archived: SYNC_Graph.md

Archived on: 2025-12-19
Original file: SYNC_Graph.md

---

## Maturity

STATUS: DEPRECATED

What's canonical (v1):
- The archive preserves prior graph physics decisions for reference; canonical, up-to-date guidance lives in `docs/physics/graph/SYNC_Graph.md`.

What's still being designed:
- Active design work is no longer tracked here; any ongoing graph tuning should be logged in the current SYNC, not this archive.

What's proposed (v2):
- Future proposals should be documented in the live SYNC and promoted here only if this archive is reissued, so history stays readable.

---

## CURRENT STATE

This archive captures older SYNC content for the physics graph module, retained to preserve decision history while the active state continues in `docs/physics/graph/SYNC_Graph.md`.

---

## IN PROGRESS

No active work is tracked in this archive; it exists solely to preserve historical context while ongoing tasks are recorded in the current graph SYNC file.

---

## RECENT CHANGES

2025-12-19: Added the missing archive template sections (maturity, state, handoffs, and pointers) so this file stays aligned with the SYNC format expectations for repair #16.

---

## KNOWN ISSUES

No known issues specific to this archive; if the guidance here appears stale, defer to the live `docs/physics/graph/SYNC_Graph.md` for authoritative updates.

---

## HANDOFF: FOR AGENTS

Use `docs/physics/graph/SYNC_Graph.md` for current work items; this archive is for historical context only and should not be updated unless a new archival snapshot is created.

---

## HANDOFF: FOR HUMAN

This archive is a historical snapshot of the graph SYNC; current priorities and open questions are tracked in the active graph SYNC and should be reviewed there first.

---

## TODO

- [ ] If this archive is updated again, re-run the SYNC template checklist to keep maturity, handoffs, and pointers aligned with protocol requirements.

---

## CONSCIOUSNESS TRACE

Archiving keeps decision history available while reducing noise in the active SYNC, making it easier to distinguish current obligations from settled design context.

---

## POINTERS

- Current graph state and tasks: `docs/physics/graph/SYNC_Graph.md`
- Graph design rationale: `docs/physics/graph/PATTERNS_Graph.md`
- Energy flow algorithm: `docs/physics/graph/ALGORITHM_Energy_Flow.md`

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



---

# Archived: SYNC_Graph.md

Archived on: 2025-12-19
Original file: SYNC_Graph.md

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

### DECISION: graph_ops_events listener registration
- Conflict: Repair task flagged `add_mutation_listener` and `remove_mutation_listener` as empty in `engine/physics/graph/graph_ops_events.py`, but both functions already implement registration/removal logic.
- Resolution: Keep existing implementation; document repair task as stale.
- Reasoning: The listener registry is mutated and used by `emit_event`, so behavior is already present.
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

---



---

# Archived: SYNC_Graph.md

Archived on: 2025-12-19
Original file: SYNC_Graph.md

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

### DECISION: graph_ops_events listener registration
- Conflict: Repair task flagged `add_mutation_listener` and `remove_mutation_listener` as empty in `engine/physics/graph/graph_ops_events.py`, but both functions already implement registration/removal logic.
- Resolution: Keep existing implementation; document repair task as stale.
- Reasoning: The listener registry is mutated and used by `emit_event`, so behavior is already present.
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

---


## Agent Observations

### Remarks
- Repair task appears stale relative to `engine/physics/graph/graph_ops_events.py`.
- Repair task appears stale relative to `engine/physics/graph/graph_queries_moments.py`.
- Repair task appears stale relative to `engine/physics/graph/graph_ops_types.py`; `SimilarNode.__str__` and `ApplyResult.success` are already implemented.
- Repair task appears stale relative to `engine/graph/health/check_health.py`.
- Re-verified `engine/graph/health/check_health.py` already implements health report helpers; no code changes needed.
 - Verified moment query helpers in `engine/physics/graph/graph_queries_moments.py` already implement narrative, transition, and clickable-word queries.
- Implemented markdown formatting and cosine similarity helpers directly in `engine/physics/graph/graph_queries_search.py` to complete search mixin methods.

### Suggestions
- None.

### Propositions
- None.


---



---

# Archived: SYNC_Graph.md

Archived on: 2025-12-19
Original file: SYNC_Graph.md

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

### DECISION: graph_ops_events listener registration
- Conflict: Repair task flagged `add_mutation_listener` and `remove_mutation_listener` as empty in `engine/physics/graph/graph_ops_events.py`, but both functions already implement registration/removal logic.
- Resolution: Keep existing implementation; document repair task as stale.
- Reasoning: The listener registry is mutated and used by `emit_event`, so behavior is already present.
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

---


## Agent Observations

### Remarks
- Repair task appears stale relative to `engine/physics/graph/graph_ops_events.py`.
- Repair task appears stale relative to `engine/physics/graph/graph_queries_moments.py`.
- Repair task appears stale relative to `engine/physics/graph/graph_ops_types.py`; `SimilarNode.__str__` and `ApplyResult.success` are already implemented.
- Repair task appears stale relative to `engine/graph/health/check_health.py`.
- Re-verified `engine/graph/health/check_health.py` already implements health report helpers; no code changes needed.
 - Verified moment query helpers in `engine/physics/graph/graph_queries_moments.py` already implement narrative, transition, and clickable-word queries.
- Implemented markdown formatting and cosine similarity helpers directly in `engine/physics/graph/graph_queries_search.py` to complete search mixin methods.
- Consolidated weight computation into `docs/physics/graph/ALGORITHM_Energy_Flow.md` and redirected `docs/physics/graph/ALGORITHM_Weight.md`.

### Suggestions
- None.

### Propositions
- None.


---
