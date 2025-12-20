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

The graph physics engine and its GraphOps/GraphQueries helpers are implemented and in active use. The remaining gaps are:
1. **API Integration**: A single API endpoint to invoke the orchestrator loop so player actions drive ticks and flips.
2. **Runtime Integration**: The core Canon Holder exists (`engine/infrastructure/canon/canon_holder.py`) but is not yet wired into the `Orchestrator` loop.
3. **Handlers**: Flip-triggered character handlers are planned but not yet implemented (missing `engine/handlers/`).

---

## IN PROGRESS

- Defining the `/api/action` endpoint contract and how it should integrate with existing playthrough and narration flows without breaking clients.
- Planning the integration of `CanonHolder` into the `Orchestrator` to record dialogue as moments.

---

## KNOWN ISSUES

- No API endpoint currently wires player actions to the orchestrator loop.
- Dialogue produced by the Narrator is not yet recorded as `Moment` nodes in the graph via the `CanonHolder`.
- Handlers for flip resolution are missing.

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
- Filled the graph behaviors template sections to eliminate drift warnings.

### Suggestions
- [ ] Add a lightweight unit test for `emit_event` to cover listener registration/removal behavior.

### Propositions
- None.


---

## ARCHIVE

Older content archived to: `SYNC_Graph_archive_2025-12.md`
