# Vision — Tests / Validation Signals

```
CREATED: 2024-12-17
STATUS: CANONICAL_METRICS
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Vision.md
BEHAVIORS:   ./BEHAVIORS_Vision.md
ALGORITHM:   ./ALGORITHM_Vision.md
VALIDATION:  ./VALIDATION_Vision.md
IMPLEMENTATION: ./IMPLEMENTATION_Vision.md
THIS:        TEST_Vision.md (you are here)
SYNC:        ./SYNC_Vision.md
```

---

## Experience Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Companion familiarity | Player can describe 2 companions after 1 hour | Post-session interview |
| Memory surprise | Player recalls at least 1 "they remembered" moment | Diary study |
| Agency clarity | Player can state next action without hints | Think-aloud observation |

---

## Build Verification

- Playthrough smoke (UI) — follow Launch Protocol in README, record issues.
- Backend uptime — `curl /health` every minute, alert on >2 failures.
- Narrative probes — Use prompts in `docs/design/opening/CONTENT.md` to ensure responses remain grounded.

---

## TEST STRATEGY

Focus on mixed-method validation: qualitative playtests for experiential goals,
paired with lightweight instrumentation and checklist-based reviews so design
claims can be traced to specific observations rather than anecdotes. Capture
notes in a shared playtest log (date, scenario, facilitator) so session results
can be compared over time.

---

## UNIT TESTS

No unit-level automation is defined for vision targets; instead, enforce a
repeatable rubric for design reviews so single-feature assessments are
consistent across sessions and reviewers.

---

## INTEGRATION TESTS

Run end-to-end playthrough sessions that combine UI, narrative output, and
memory features, then compare results against the Experience Metrics table to
confirm the integrated experience matches intent.

---

## EDGE CASES

Validate onboarding and retention for players who skip tutorials, return after
long gaps, or attempt unusual interactions so the vision holds under atypical
usage patterns and not just idealized flows.

---

## TEST COVERAGE

Coverage is expressed as completed qualitative sessions, instrumented runs, and
design review checklists; track which vision outcomes have been directly
observed versus those still supported only by assumptions.

---

## HOW TO RUN

Schedule a 60-minute playtest using the Launch Protocol, capture a screen
recording, and complete the interview rubric in `docs/design/testing/` to log
observations for each metric in the Experience Metrics table.

---

## KNOWN TEST GAPS

Longitudinal retention is not yet validated; repeated-session memory surprise
and companion familiarity data needs at least three multi-session studies with
the same players.

---

## FLAKY TESTS

Playtest outcomes can vary with facilitator tone and player mood; log any
session where facilitation changes materially affect the metrics so results are
not over-interpreted.

---

## GAPS / IDEAS / QUESTIONS

- Should we define a minimum sample size for declaring a vision metric stable?
- What is the smallest viable instrumentation set to capture memory surprise?
- How do we log "agency clarity" without biasing the player's next choice?
```
