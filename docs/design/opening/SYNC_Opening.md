# The Opening — Sync

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: ngram repair agent
STATUS: Scripted transcript active
MATURITY: CANONICAL
```

---

## Chain Reference

| Doc | Purpose |
|-----|---------|
| PATTERNS_Opening.md | Philosophy — why static questions work |
| BEHAVIORS_Opening.md | Experience description — what player feels |
| ALGORITHM_Opening.md | Implementation outline — bootstrap steps |
| CONTENT.md | Actual script + prompts (17 questions, 10 beats) |
| VALIDATION_Opening.md | Success metrics |
| TEST_Opening.md | Planned coverage (STATUS: TODO) |
| SYNC_Opening.md | This file |

---

## MATURITY

STATUS: CANONICAL

What's stable (v1):
- Scripted opening flow in `opening.json`, plus scene conversion in playthroughs bootstrap.
- Canonical companion voice and question sequence tracked in CONTENT.md for revisions.

What's still being designed:
- Automated answer extraction into ledger/tension mapping for downstream systems.
- Testing harness for replaying scripted openings with persistence assertions.

What's proposed (v2):
- Adaptive follow-ups based on answer sentiment without rewriting core prompts.
- Opening recap surfaced as a reusable memory artifact in later scenes.

---

## CURRENT STATE

**What's working:**
- `opening.json` provides structured question flow (10 beats, 17 questions)
- `playthroughs.py::_opening_to_scene_tree()` converts opening.json → SceneTree format
- Playthrough bootstrap writes `player.yaml` AND moment graph (fixed since 2024-12-17)
- Opening moments created from scenario narration in graph via `add_moment()`
- `PROFILE_NOTES.md` created per playthrough for tracking player answers

**What's not yet implemented:**
- Automated extraction of answers → ledger entries (still manual via PROFILE_NOTES)
- Answer-to-tension mapping helper (originally planned for `engine/orchestration/opening.py`)
- Tests (TEST_Opening.md still shows STATUS: TODO)

---

## Code Locations

Since 2025-12 restructure:
- `engine/infrastructure/api/playthroughs.py` — opening scene generation, moment creation
- `docs/design/opening/opening.json` — structured question template
- Orchestration now at `engine/infrastructure/orchestration/` (not `engine/orchestration/`)

---

## IN PROGRESS

This opening flow remains in active design maintenance, with current work
focused on documenting the authored questions and aligning the sync template
to avoid drift warnings in the doc health checks.

---

## RECENT CHANGES

- 2025-12-19: Added clarification in ALGORITHM_Opening.md overview to explain
  how nested acknowledgments preserve question order for repair #16.
- 2025-12-19: Filled missing PATTERNS_Opening.md template sections (problem,
  pattern, principles, dependencies, inspirations, scope) for repair #16.
- 2025-12-19: Expanded ALGORITHM_Opening.md with full template sections and
  longer descriptions to resolve DOC_TEMPLATE_DRIFT for repair #16.
- 2025-12-19: Filled missing SYNC template sections and expanded notes to
  satisfy DOC_TEMPLATE_DRIFT checks for repair #16.
- 2025-12-19: Expanded TEST_Opening.md with full test template sections and
  noted current gaps for repair #16.
- 2025-12-19: Expanded VALIDATION_Opening.md with properties, error conditions,
  test coverage, verification procedure, and sync status for repair #16.
- 2025-12-19: Restored BEHAVIORS_Opening.md template sections (behaviors,
  inputs/outputs, anti-behaviors) to resolve doc drift for repair #16.
- 2025-12-19: Expanded BEHAVIORS_Opening.md text to meet template-length
  guidance for behaviors, inputs/outputs, and anti-behaviors in repair #16.

---

## KNOWN ISSUES

- Opening answer capture is still manual, so downstream systems do not receive
  structured ledger or tension updates without human transcription.
- Tests for the opening sequence are still marked TODO and have not been run.

---

## HANDOFF: FOR AGENTS

If you continue, use VIEW_Implement_Write_Or_Modify_Code and verify whether
`opening.json` still matches CONTENT.md before editing any prompts. Focus on
automating answer extraction without changing the authored question list.

---

## HANDOFF: FOR HUMAN

This repair only filled in missing SYNC template sections; no behavior or
script content changed. If you want the opening to feed the ledger, confirm
the desired mapping rules before implementation begins.

---

## TODO

- [ ] Define the answer-to-ledger mapping rules and where they should live.
- [ ] Implement a replayable opening test harness per TEST_Opening.md.

---

## CONSCIOUSNESS TRACE

I focused on template alignment and kept content faithful to the existing
opening behavior, avoiding changes that would imply unverified behavior.

---

## POINTERS

- `docs/design/opening/CONTENT.md` for the scripted question list and beats.
- `engine/infrastructure/api/playthroughs.py` for the current opening scene flow.

---

## Upcoming Work

1. **Answer Storage** — Map each question's player response to ledger/tension updates automatically. Create helper in `engine/infrastructure/orchestration/opening.py`.
2. **Test Coverage** — Implement scripted session replay, sentiment analysis, persistence checks per TEST_Opening.md.

---

## Notes

- Static questions in CONTENT.md remain the most engaging approach per design philosophy
- LLM's role: present questions with life/timing, listen, build player profile, reflect back authentically
- Companion reflection template in CONTENT.md guides post-question synthesis

---

## Agent Observations

### Remarks
- TEST_Opening.md now reflects intended coverage but remains unimplemented in code.
- ALGORITHM_Opening.md now documents the opening SceneTree construction flow.
- BEHAVIORS_Opening.md now includes the required template sections.

### Suggestions
- [ ] Add a lightweight test harness for opening.json replay in engine/tests.

### Propositions
- Consider a golden transcript fixture to detect CONTENT.md drift over time.
