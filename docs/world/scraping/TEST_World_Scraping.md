# World Scraping — Tests

```
CREATED: 2024-12-17
STATUS: TODO
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_World_Scraping.md
BEHAVIORS:   ./BEHAVIORS_World_Scraping.md
ALGORITHM:   ./ALGORITHM_Pipeline.md
VALIDATION:  ./VALIDATION_World_Scraping.md
THIS:        TEST_World_Scraping.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
SYNC:        ./SYNC_World_Scraping.md
```

---

| Test | Path | Purpose |
|------|------|---------|
| Geography routes | `tests/world/test_routes.py` | Travel time + river crossing assertions |
| Political placement | `tests/world/test_positions.py` | Historical NPC alignment |
| Narrative integrity | `tests/world/test_narratives.py` | Conflicting accounts flagged |
| Pipeline smoke | `tests/world/test_pipeline.py` | Ensures ETL stages run sequentially |

Gaps: tests currently conceptual; need to implement once world data scaffolding exists.
```

---

## TEST STRATEGY

Use lightweight unit tests to validate YAML schema shape and deterministic
transform logic, then use integration tests to exercise end-to-end ETL and
inject-world flows against the `seed` database. Favor reproducible fixtures
over live web calls because data/scripts access and external APIs are unstable.

---

## UNIT TESTS

### YAML Shape and Phase Outputs

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_places_schema_fields` | `places.yaml` | required fields present | pending |
| `test_routes_have_endpoints` | `routes.yaml` | each route has from/to | pending |
| `test_holdings_have_rulers` | `holdings.yaml` | holder IDs resolve | pending |
| `test_things_have_locations` | `things.yaml` | locations and owners valid | pending |

---

## INTEGRATION TESTS

### Seed Database Injection

```
GIVEN:  data/world YAML outputs and FalkorDB `seed` running
WHEN:   data/scripts/inject_world.py is executed
THEN:   place, character, narrative, and tension counts match expectations
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Missing optional coordinates | `test_place_without_latlon` | pending |
| Duplicate place slug | `test_duplicate_place_slug` | pending |
| Narrative references unknown character | `test_narrative_unknown_character` | pending |
| Thing references missing owner | `test_thing_missing_owner` | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| Phase YAML outputs | 0% | No automated schema checks yet |
| Injection pipeline | 0% | No integration harness in place |
| Narrative consistency | 0% | Manual review only |

---

## HOW TO RUN

```bash
# Tests are not implemented yet.
# Suggested structure once files exist:
pytest tests/world/test_routes.py
pytest tests/world/test_positions.py
pytest tests/world/test_narratives.py
pytest tests/world/test_pipeline.py
```

---

## KNOWN TEST GAPS

- [ ] No automated schema validation for YAML outputs in `data/world/`.
- [ ] No regression tests for pipeline phase ordering or data overwrites.
- [ ] No integration tests for `data/scripts/inject_world.py` with FalkorDB.

---

## FLAKY TESTS

No flaky tests are tracked yet; once integration runs are added, record any
DB timing, file IO, or external API timing instabilities here.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide whether tests should run against a fixture YAML snapshot or the
  live `data/world/` directory from the scrape pipeline.
- IDEA: Add a YAML diff report to compare before/after outputs for regressions.
- QUESTION: Should the injection test assert exact counts or ranges, given
  manual edits to data files between runs?
