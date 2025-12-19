# Graph — Current State

```
UPDATED: 2025-12-19
STATUS: Implemented, needs API endpoint
```

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

## Recent Changes

### 2025-12-19
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

## Agent Observations

### Remarks
- `graph_ops_types.py` already implements the previously flagged helpers; repair appears stale.

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
