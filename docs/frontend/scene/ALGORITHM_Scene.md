# Scene View — Algorithm

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
BEHAVIORS:   ./BEHAVIORS_Scene.md
THIS:        ALGORITHM_Scene.md (you are here)
VALIDATION:  ./VALIDATION_Scene.md
TEST:        ./TEST_Scene.md
SYNC:        ./SYNC_Scene.md
```

---

## OVERVIEW

The Scene algorithm assembles the current view payload, renders the scene stack
(header, banner, atmosphere, people, voices, actions), annotates moments for
interactive words, and listens for streamed updates to keep the UI in sync.

---

## DATA STRUCTURES

- **SceneViewPayload**: response from `GET /api/view/{playthrough_id}` with
  location, atmosphere text, people, voices, and current moments for display.
- **Moment**: text block with identifiers, weight, and metadata used for
  ordering, opacity, and clickable word highlighting in the stream.
- **Transition**: click-target metadata that maps words to destinations or
  follow-up moments for traversal (used by click handlers).
- **SceneAction**: action tokens or labels that drive button rendering and
  dispatch (talk, travel, write, or free text input).

---

## ALGORITHM: RenderSceneView

1. **Load Current View**
   - Call `GET /api/view/{playthrough_id}` to fetch the latest scene payload.
   - Normalize response into local SceneView state for rendering.
2. **Render the Scene Stack**
   - Show header and banner (with image fallback if needed).
   - Render atmosphere text, people rows, and voice callouts.
   - Render the moment stream sorted by weight or display order.
3. **Annotate Interactive Moments**
   - Resolve speakers from payload; default to narration when missing.
   - Mark clickable words based on transition metadata.
   - Add ledger/tooltip affordances for debt or oath references.
4. **Handle Interaction Inputs**
   - Word click → `POST /api/moments/click` with moment + word info.
   - Free text action → `POST /api/moment` with player action text.
   - Action buttons → call the shared action handler (talk/travel/write).
5. **Subscribe to Stream Updates**
   - Open `EventSource` on `/api/moments/stream/{playthrough_id}`.
   - On event, refresh or reconcile local state with latest payloads.
6. **Update Rendering**
   - Re-render SceneView with updated moments, voices, and actions.
   - Preserve the current reading flow and interaction highlights.

---

## KEY DECISIONS

- Scene rendering is driven by backend truth; the UI rehydrates from view and
  stream updates instead of maintaining long-lived client-owned state.
- Moment stream ordering prioritizes salience/weight to keep the most relevant
  narrative beats visible without flooding the player with text.
- Interaction paths stay explicit: clicks are fast graph traversals, while
  free-text actions can tolerate slower backend processing.

---

## DATA FLOW

```
GET /api/view/{playthrough_id}
    ↓
SceneViewPayload → local scene state
    ↓
Render header/banner/people/voices/moments/actions
    ↓
Click or free-text action
    ↓
POST /api/moments/click OR POST /api/moment
    ↓
SSE /api/moments/stream/{playthrough_id}
    ↓
Refresh/reconcile → re-render
```

---

## COMPLEXITY

- Initial render is O(n) over people + moments + actions in the payload.
- Click handling is O(1) on the client, with network latency dominating.
- Stream updates are O(1) per event plus O(n) if a full refresh is triggered.

---

## HELPER FUNCTIONS

- `fetchView(playthroughId)` in `frontend/lib/api.ts` retrieves the scene view.
- `sendMoment(playthroughId, text, source)` posts free-text actions.
- `sendMomentClick(payload)` sends click traversals to `/api/moments/click`.
- `subscribeToMomentStream(playthroughId, handlers)` wires SSE updates.

---

## INTERACTIONS

- `SceneView` composes the visual stack and delegates text flow to
  `CenterStage`, which handles animated reveal and click dispatch.
- `SceneActions` and per-character buttons feed the shared action handler.
- The scene relies on hooks (`useGameState`, `useMoments`) for state refresh
  and for keeping the moment stream synchronized with backend updates.

---

## GAPS / IDEAS / QUESTIONS

- Should moment updates be reconciled incrementally instead of full refreshes
  to reduce redraw churn when streams are busy?
- How should voice selection evolve beyond top-weight filtering, and should
  the algorithm include recency or narrative category weighting?
- Are action buttons sufficient for emergent choice, or should we render
  context-specific action chips generated from the current scene payload?
