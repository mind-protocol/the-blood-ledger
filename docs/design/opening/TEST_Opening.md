# The Opening — Tests

```
STATUS: TODO
CREATED: 2024-12-17
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Opening.md
BEHAVIORS:   ./BEHAVIORS_Opening.md
ALGORITHM:   ./ALGORITHM_Opening.md
VALIDATION:  ./VALIDATION_Opening.md
THIS:        TEST_Opening.md (you are here)
SYNC:        ./SYNC_Opening.md
```

---

## Planned Checks

| Test | Description |
|------|-------------|
| Scripted session | Replay canonical transcript → ensure outputs match `CONTENT.md` |
| Sentiment analysis | Confirm Aldric mirrors player's tone (positive/neutral/guarded) |
| Persistence | Ensure answers stored in `playthrough/player.yaml` |

---

## TEST STRATEGY

Focus first on replaying the scripted opening transcript end-to-end, then
layer in smaller checks around `opening.json` parsing, scene conversion, and
answer persistence so drift between CONTENT.md and runtime output is caught.

---

## UNIT TESTS

No dedicated unit tests exist yet; add isolated tests for
`playthroughs.py::_opening_to_scene_tree()` and the opening.json loader so
ordering, question IDs, and beat structure remain deterministic.

---

## INTEGRATION TESTS

Integration coverage should create a playthrough, run the opening sequence,
and assert that the SceneTree output, moment creation, and player profile
files are persisted consistently across the full bootstrap path.

---

## EDGE CASES

Edge cases to exercise include empty or malformed opening.json, skipped or
one-word answers, repeated question IDs, missing beat metadata, and ensuring
graceful handling when the companion response template is absent.

---

## TEST COVERAGE

Current coverage is design-only: the planned checks above describe what must
be verified, but no automated tests are wired up in `engine/tests/` yet for
the opening flow or its persistence outputs.

---

## HOW TO RUN

When tests land, run `pytest engine/tests/test_opening.py -v` for focused
coverage or `pytest engine/tests -v` for the full suite; integration checks
may require scenario fixtures and a writable playthrough output directory.

---

## KNOWN TEST GAPS

There is no automated verification of Aldric's tone mirroring, no regression
test for CONTENT.md drift, and no assertion that player answers map to the
expected profile notes after the opening completes.

---

## FLAKY TESTS

No flaky opening tests are tracked yet; if integration runs depend on external
LLM responses or filesystem timing, record any intermittent failures here.

---

## GAPS / IDEAS / QUESTIONS

- Should the opening transcript replay be deterministic without LLM calls?
- Do we need fixtures that freeze `opening.json` + CONTENT.md together?
- Which file should own the golden expected transcript for diffing?
