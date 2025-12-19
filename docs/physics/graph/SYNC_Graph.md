# Graph — Current State

```
UPDATED: 2025-12-19
STATUS: Implemented, needs API endpoint
```

---

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- GraphOps/GraphQueries mixins and tick integration are stable and in use.
- Energy flow, decay, and flip detection are treated as production behavior.

What's still being designed:
- External API integration for player actions and streaming responses.

What's proposed (v2):
- Extended orchestration telemetry and richer runtime diagnostics.

---

## CURRENT STATE

The graph physics engine and its GraphOps/GraphQueries helpers are
implemented and in active use. The remaining gap is a single API endpoint
to invoke the orchestrator loop so player actions drive ticks and flips.

---

## IN PROGRESS

- Defining the `/api/action` endpoint contract and how it should integrate
  with existing playthrough and narration flows without breaking clients.

---

## KNOWN ISSUES

- No API endpoint currently wires player actions to the orchestrator loop,
  so full graph ticks require direct service calls instead of HTTP usage.

---

## What Exists ✓

| Component | Status | Location |
|-----------|--------|----------|
| GraphTick | ✓ Complete | `engine/physics/tick.py` |
| Orchestrator | ✓ Complete | `engine/infrastructure/orchestration/orchestrator.py` |
| World Runner | ✓ Complete | `engine/infrastructure/orchestration/world_runner.py` |
| Narrator | ✓ Complete | `engine/infrastructure/orchestration/narrator.py` |
| API app | ✓ Running | `engine/infrastructure/api/app.py` |

---

## What's Missing: ONE ENDPOINT

### ⚠️ AGENT TASK: Add /api/action endpoint

The Orchestrator is built. It calls tick, detects flips, triggers World Runner.
**But no API endpoint calls it.**

**Add this to `engine/infrastructure/api/app.py`:**

```python
@app.post("/api/action")
async def player_action(request: ActionRequest):
    """
    Full game loop: narrator → tick → flips → world runner.
    
    This is the main gameplay endpoint. Use for:
    - Free text input
    - Clicking words that need narrator response
    - Any action that should advance time
    """
    orchestrator = get_orchestrator(request.playthrough_id)
    
    if request.stream:
        # TODO: SSE streaming version
        pass
    
    result = orchestrator.process_action(
        player_action=request.action,
        player_id=request.player_id,
        player_location=request.location
    )
    return result
```

**ActionRequest already exists in app.py:**
```python
class ActionRequest(BaseModel):
    playthrough_id: str
    action: str
    player_id: str = "char_player"
    location: Optional[str] = None
    stream: bool = False
```

**After adding:**
1. Test: `curl -X POST http://localhost:8000/api/action -d '{"playthrough_id":"test","action":"look around"}'`
2. Verify tick runs (check logs for `[GraphTick]`)
3. Verify flips trigger World Runner

---

## Two Paths (Both Valid)

| Path | Endpoint | Use Case |
|------|----------|----------|
| Instant | `/api/moment/click` | Quick clicks, weight updates, no LLM |
| Full Loop | `/api/action` (ADD THIS) | Narrator response, time passes, tick runs |

Frontend should use:
- Moment click → instant feedback
- Action → when narrator response needed

---

## Known False Positives

If ngram doctor flags these as INCOMPLETE_IMPL, mark stale:
- `tick.py` — fully implemented
- `orchestrator.py` — fully implemented  
- `graph_ops_events.py` — mutation listeners optional

---

## RECENT CHANGES

### 2025-12-19
- Normalized SYNC headings (MATURITY, CURRENT STATE, RECENT CHANGES, and
  handoff sections) to match the required template labels for drift checks.
- Filled missing SYNC template sections (maturity, state, handoffs, todo,
  consciousness trace, pointers) to resolve DOC_TEMPLATE_DRIFT for repair #16.
- Expanded `docs/physics/graph/ALGORITHM_Energy_Flow.md` with explicit
  template sections (overview, data structures, algorithm entry point,
  decisions, data flow, complexity, helpers, interactions, gaps) to resolve
  DOC_TEMPLATE_DRIFT for repair #16.
- Normalized the energy flow algorithm headings to the required template
  labels (OVERVIEW, DATA STRUCTURES, ALGORITHM, KEY DECISIONS, and related).
- Completed the missing template sections in
  `docs/physics/graph/PATTERNS_Graph.md` (chain, problem, pattern, principles,
  dependencies, inspirations, scope, gaps) for repair #16.
- Verified `engine/physics/graph/graph_queries_moments.py` moment query helpers (`get_narrative_moments`, `get_narratives_from_moment`, `get_available_transitions`, `get_clickable_words`) are fully implemented; repair task was stale.
- Confirmed the `physics-graph` module mapping in `modules.yaml`, removed the duplicate entry, and verified the `graph_ops.py` DOCS reference.
- Confirmed tick.py, orchestrator.py are complete
- Identified gap: no API endpoint calls orchestrator.process_action()
- Created task spec for agents to add endpoint
- Verified mutation listener helpers in `engine/physics/graph/graph_ops_events.py` are already implemented; repair flagged as INCOMPLETE_IMPL is stale.
- Verified `engine/physics/graph/graph_ops_types.py` helpers (`SimilarNode.__str__`, `ApplyResult.success`) are already implemented; repair flagged as INCOMPLETE_IMPL is stale.
- Verified `engine/physics/graph/graph_queries_moments.py` moment query helpers are implemented; repair flagged as INCOMPLETE_IMPL is stale.
- Removed duplicate graph algorithm doc by consolidating weight computation into `docs/physics/graph/ALGORITHM_Energy_Flow.md` and dropping `docs/physics/graph/ALGORITHM_Weight.md`.
- Reconfirmed `engine/physics/graph/graph_ops_types.py` helper implementations for the current repair run; no code changes required.
- Filled the missing template sections in `docs/physics/graph/SYNC_Graph_archive_2025-12.md` to align the archive with current SYNC requirements for repair #16.
- Verified `docs/physics/graph/SYNC_Graph_archive_2025-12.md` remains template-complete; no further edits were needed for this repair pass.

---

## HANDOFF: FOR AGENTS

Continue with VIEW_Implement_Write_Or_Modify_Code. Focus on adding the
`/api/action` endpoint wiring to the orchestrator without altering graph
physics internals. Keep doc updates confined to graph SYNC and API docs.

---

## HANDOFF: FOR HUMAN

The graph system is stable; the only blocking gap is an API endpoint that
invokes the orchestrator. Once added, player actions will drive ticks and
flip processing through the normal HTTP interface.

---

## TODO

- [ ] Add `/api/action` endpoint in `engine/infrastructure/api/app.py`.
- [ ] Add a minimal integration check that confirms ticks run via API.

---

## CONSCIOUSNESS TRACE

Confidence is high that the graph logic is correct and stable; the missing
endpoint is a product integration gap rather than a physics defect. The
focus is on wiring, not redesigning, to avoid scope creep.

---

## POINTERS

- `docs/physics/graph/ALGORITHM_Energy_Flow.md` for the propagation logic.
- `docs/physics/graph/BEHAVIORS_Graph.md` for observable graph behaviors.
- `engine/physics/tick.py` for the tick entry point and graph integration.

## Agent Observations

### Remarks
- `graph_ops_types.py` already implements the previously flagged helpers; repair appears stale.
- Energy flow algorithm documentation now matches the required template layout.

### Suggestions
- [ ] Add a DOCS reference in `engine/physics/graph/graph_ops_types.py` so `ngram context` resolves the graph documentation chain.

### Propositions
- None.
- Reconfirmed mutation listener helpers (`add_mutation_listener`, `remove_mutation_listener`) are implemented in `engine/physics/graph/graph_ops_events.py` for the current repair run; no code changes required.

## Agent Observations

### Remarks
- The mutation listener helpers already include guard checks to avoid duplicate registrations and safe removal.

### Suggestions
- [ ] Add a lightweight unit test for `emit_event` to cover listener registration/removal behavior.

### Propositions
- None.
