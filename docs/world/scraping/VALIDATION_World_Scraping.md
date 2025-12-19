# World Scraping — Validation

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_World_Scraping.md
BEHAVIORS:   ./BEHAVIORS_World_Scraping.md
ALGORITHM:   ./ALGORITHM_Pipeline.md
THIS:        VALIDATION_World_Scraping.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
TEST:        ./TEST_World_Scraping.md
SYNC:        ./SYNC_World_Scraping.md
```

---

## How We Know It Works

We validate the pipeline by checking data volume, historical placement, and
travel realism against the documented targets and the known 1067 context.
The checks below are designed to catch missing content, anachronisms, and
route realism regressions before data is injected into the graph.

---

## Invariants

- Every place, character, narrative, belief, and tension has a stable ID and
  a non-empty display name that matches the schema requirements.
- Routes never cross major rivers without a matching crossing or bridge
  feature in the places or route metadata.
- All historical figures placed in 1067 have a birth date earlier than 1067
  and no death date earlier than 1067.
- YAML output files remain loadable and pass schema validation before graph
  injection begins.

---

## Properties

- The dataset preserves the feel of 1067 England by keeping geography,
  political control, and narrative references consistent with known sources.
- Scraped and curated records remain internally consistent (holdings belong
  to characters, characters are placed in known locations, tensions reference
  existing nodes).
- The pipeline is deterministic when run on the same inputs so outputs can be
  diffed and reviewed reliably.

---

## Error Conditions

- Missing or empty YAML outputs for any phase (places, routes, characters,
  narratives, tensions, things) should be treated as a hard failure.
- Invalid or duplicate IDs, or broken references between data types, are
  errors that block injection into FalkorDB.
- Any anachronistic placements (death before 1067, post-1067 events marked as
  current) are treated as data corruption.

---

## Test Coverage

- Unit-style validation scripts assert counts, required fields, and reference
  integrity for YAML outputs before injection.
- Spot checks verify geography realism and political correctness using known
  historical anchors (York, Durham, Malet, etc.).
- Manual playtests validate the narrative feel and detect subtle anachronisms
  or implausible travel behavior.

---

## Verification Procedure

1. Run the scraping pipeline to regenerate YAML outputs for all phases.
2. Execute validation scripts (counts, schema fields, reference integrity).
3. Run manual spot checks for historical placements and geography realism.
4. Inject into the `seed` database only after validation passes.
5. Conduct the playtest checklist to confirm experiential fidelity.

---

## Geography Tests

### Travel times match reality

```python
# Sample routes, compare to Google Maps walking
def test_travel_times():
    york_to_durham = get_route("place_york", "place_durham")
    assert 38 <= york_to_durham.hours <= 58  # ~48h expected, 20% tolerance
```

### Rivers block routes

```python
def test_river_crossings():
    for route in all_routes:
        if crosses_river(route) and not has_crossing(route):
            fail(f"Route {route.id} crosses river without crossing")
```

---

## Political Tests

### Historical figures in correct places

```python
def test_historical_placements():
    malet = get_character("char_malet")
    assert "place_york" in malet.holds  # Domesday confirms
```

### No anachronisms

```python
def test_no_dead_characters():
    for char in all_characters:
        if char.death_date and char.death_date < 1067:
            fail(f"{char.name} died before 1067")
```

---

## Narrative Tests

### Belief network is connected

```python
def test_belief_density():
    for char in all_characters:
        assert len(char.beliefs) >= 5, f"{char.name} has too few beliefs"

    for narr in all_narratives:
        assert len(narr.believers) >= 1, f"{narr.name} has no believers"
```

### Contradictions exist

```python
def test_contradictions():
    contradictions = query_contradicting_pairs()
    assert len(contradictions) >= 30, "Too few contradictions"
```

---

## Tension Tests

### Tensions have pressure

```python
def test_tension_pressure():
    for tension in all_tensions:
        assert tension.pressure > 0.1, f"{tension.id} has no pressure"
```

### Tensions can break

```python
def test_hot_tensions():
    hot = [t for t in all_tensions if t.pressure > 0.5]
    assert len(hot) >= 10, "Too few hot tensions"
```

---

## Density Tests

```python
def test_target_counts():
    assert len(all_places) >= 200
    assert len(all_characters) >= 100
    assert len(all_narratives) >= 200
    assert len(all_beliefs) >= 700
    assert len(all_tensions) >= 40
```

---

## Playtest Checklist

Manual verification:

- [ ] Can travel York to Durham with plausible route
- [ ] characters mention recent events (Harrying)
- [ ] Political situation matches 1067
- [ ] Tensions visible in character dialogue
- [ ] News spreads between characters over time
- [ ] No obvious anachronisms in dialogue
- [ ] Place descriptions match terrain
- [ ] Travel times feel reasonable

---

## Sync Status

Validation notes should align with the current scrape counts and phase status
recorded in `docs/world/scraping/SYNC_World_Scraping.md` to avoid drift.

---

## Gaps / Ideas / Questions

- Do we need automated diff reports between pipeline runs to catch subtle
  regressions in narrative counts or political placements?
- How should we verify that minor places and things remain connected to the
  main narrative web without manual inspection?
