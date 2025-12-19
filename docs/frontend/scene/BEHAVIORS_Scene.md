# Scene View — Behaviors

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
THIS:        BEHAVIORS_Scene.md (you are here)
ALGORITHM:   ./ALGORITHM_Scene.md
VALIDATION:  ./VALIDATION_Scene.md
TEST:        ./TEST_Scene.md
SYNC:        ./SYNC_Scene.md
```

---

## BEHAVIORS

### B1: Framed Atmosphere
```
GIVEN:  Player enters a location
WHEN:   Scene view renders
THEN:   2-3 lines of sensory grounding appear before dialogue, keeping it brief and readable
```

### B2: Narrative Voices
```
GIVEN:  Narratives with high weight attach to present characters
WHEN:   Scene loads
THEN:   The player sees inner voices / ledger whispers inline with the main dialogue to reinforce stakes
```

### B3: Clickable Language
```
GIVEN:  CAN_LEAD_TO links specify require_words
WHEN:   Scene renders
THEN:   Clickable words are highlighted and trigger transitions quickly to avoid breaking flow
```

### B4: Waiting Has Consequences
```
GIVEN:  Wait-triggered transitions exist
WHEN:   The player pauses for the configured ticks
THEN:   The scene advances (new moment, consequence narration) without input after the wait threshold
```

### B5: Ledger Integration
```
GIVEN:  Ledger entries are affected by conversation
WHEN:   Critical obligations are referenced
THEN:   The corresponding ledger entries glow or link for immediate inspection in the right panel
```

---

## INPUTS / OUTPUTS

**Inputs**
- Scene view state from hooks (`useMoments`, `useGameState`) including moments, voices, people, and actions to render.
- Scene metadata such as location name, banner image, and atmosphere text from the current playthrough state.
- Interaction payloads for clickable words or action buttons, as passed down from parent components.

**Outputs**
- Rendered scene layout with header, banner, people rows, atmosphere block, voices, and action controls.
- User interactions emitted via callbacks (word clicks, action selections, talk targets) to the parent handler layer.
- Visual emphasis updates (opacity, highlight state) reflecting voice weight and focus changes.

---

## EDGE CASES

- Scene loads with no people or voices; UI should avoid empty gaps and still present atmosphere + actions.
- Missing or empty banner image; fallback visuals must prevent layout collapse and keep header readable.
- Long atmosphere text; should remain constrained to keep scrolling and pacing consistent with brief scenes.
- Clickable words list is empty; avoid rendering highlight affordances that imply interactivity.

---

## ANTI-BEHAVIORS

- Do not render multi-paragraph exposition that pushes actions below the fold on first load.
- Do not show more voices than the weight-based cap; extra voices should be suppressed, not stacked.
- Do not block the UI waiting for an image; the scene should render with a placeholder instead.
- Do not trigger clickable-word transitions without clear highlighting or cursor affordance.

---

## GAPS / IDEAS / QUESTIONS

- How should voice selection be filtered beyond weight (recency, relevance, or character proximity)?
- What is the minimum viable action set for quiet scenes without making choices feel menu-like?
- Do we need a fallback for scenes with zero moments, or should the banner/atmosphere suffice?
- Should clickable-word transitions be debounced or animated to make state changes feel intentional?
