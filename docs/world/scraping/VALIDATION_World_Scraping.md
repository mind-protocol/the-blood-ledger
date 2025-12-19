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
TEST:        ./TEST_World_Scraping.md
SYNC:        ./SYNC_World_Scraping.md
```

---

## How We Know It Works

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
