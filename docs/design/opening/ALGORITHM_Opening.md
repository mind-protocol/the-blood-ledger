# The Opening — Algorithm

```
STATUS: DRAFT
CREATED: 2024-12-17
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Opening.md
BEHAVIORS:   ./BEHAVIORS_Opening.md
THIS:        ALGORITHM_Opening.md (you are here)
CONTENT:     ./CONTENT.md
VALIDATION:  ./VALIDATION_Opening.md
TEST:        ./TEST_Opening.md
SYNC:        ./SYNC_Opening.md
```

---

## OVERVIEW

The opening algorithm turns the authored `opening.json` beats into a
SceneTree that the narrator can run, while keeping the question list
static and the player answers dynamic. The goal is a deterministic
structure that delivers the scripted experience without re-generating
questions at runtime. The nested acknowledgments preserve question order
without requiring additional dialogue planning logic.

## DATA STRUCTURES

- `opening.json` template with `setting`, `beats`, `questions`, and optional
  `transition` strings that frame each beat.
- Scenario metadata with companion `id` and opening narration used to seed
  graph moments before the questions begin.
- SceneTree dict with `narration` entries and nested `freeform_acknowledgment`
  payloads that chain questions and beats together.
- Player answer persistence targets such as `player.yaml` and
  `PROFILE_NOTES.md`, which are populated downstream.

## ALGORITHM: _opening_to_scene_tree

Primary entry point that converts the opening template and scenario metadata
into a nested SceneTree payload used by playthrough bootstrap.

## Primary Flow

1. Load `opening.json` and scenario context (companion id, setting overrides).
2. For each beat, emit narration lines and the first question in that beat.
3. Wrap each question with a `freeform_acknowledgment` that links to the next
   question or next beat using nested `then` lists.
4. Assemble the scene payload with location metadata, characters, and voices.
5. Return the SceneTree for use by playthrough bootstrap and narrator.

## KEY DECISIONS

- Keep authored questions fixed; only answers are dynamic and persisted so the
  companion voice stays stable across playthroughs.
- Nest questions using `freeform_acknowledgment` to avoid separate prompt
  generation logic for follow-up questions.
- Generate opening moments from scenario narration before question flow to
  anchor the scene in the graph early.

## DATA FLOW

`opening.json` plus scenario metadata enters `_opening_to_scene_tree()`, which
outputs a SceneTree payload. Playthrough bootstrap persists the scene, creates
opening moments from the scenario narration, and hands the structure to the
narrator and UI, which collect player responses for later extraction.

## COMPLEXITY

Time is O(B + Q + L) where `B` is beats, `Q` questions, and `L` narration
lines; space is O(B + Q + L) for the constructed SceneTree and nested
acknowledgment nodes.

## HELPER FUNCTIONS

- `build_beat_narration` (inner helper) builds nested narration and ensures
  the `then` chain connects questions across beats.
- Playthrough bootstrap in `engine/infrastructure/api/playthroughs.py` loads
  `opening.json`, builds the scene, and writes opening moments.

## INTERACTIONS

- Narrator consumes the SceneTree to present questions and record responses,
  while the frontend provides freeform input to the API.
- Playthrough bootstrap writes `player.yaml`, `PROFILE_NOTES.md`, and opening
  moment graph entries before regular play begins.
- CONTENT.md remains the authored source of truth that `opening.json` encodes.

## GAPS / IDEAS / QUESTIONS

- [ ] Define the answer-to-ledger mapping rules and storage schema so the
  opening can feed downstream tension systems.
- [ ] Decide whether to persist a structured answer summary per question id or
  keep the raw freeform transcript only.
- [ ] Validate that `opening.json` stays aligned with CONTENT.md wording and
  whether beat ordering should ever change.
