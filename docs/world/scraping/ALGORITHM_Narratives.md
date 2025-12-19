# Phase 4: Narratives & Beliefs — Algorithm

**Purpose:** Stories & Knowledge

---

## Sources

| Source | Provides |
|--------|----------|
| Phase 2 | characters, holdings |
| Phase 3 | events |
| Manual | relationship_patterns |

---

## Output

### narratives.yaml

**Count:** ~250

```yaml
- id: narr_malet_holds_york
  name: "Malet controls York"
  content: "William Malet, Sheriff of Yorkshire, holds York for the King"
  type: control
  about:
    characters: [char_malet]
    places: [place_york]
  truth: 1.0

- id: narr_waltheof_claim_york
  name: "Waltheof's claim"
  content: "Waltheof was Earl here before the Normans came"
  type: claim
  about:
    characters: [char_waltheof]
    places: [place_york]
  truth: 1.0
```

**Fields:**
- `id` — Unique identifier (`narr_*`)
- `name` — Short title
- `content` — Full narrative text
- `type` — control, claim, memory, rumor, secret
- `about` — Characters and places involved
- `truth` — 0.0-1.0 (director knowledge)

### beliefs.yaml

**Count:** ~800

```yaml
- character: char_malet
  narrative: narr_malet_holds_york
  believes: 1.0
  heard: 1.0
  originated: 0.0

- character: char_waltheof
  narrative: narr_malet_holds_york
  believes: 0.9
  heard: 1.0
  originated: 0.0
```

**Fields:**
- `character` — Who holds this belief
- `narrative` — What they believe
- `believes` — How strongly (0.0-1.0)
- `heard` — Whether they've heard it (0.0-1.0)
- `originated` — Whether they started it (0.0-1.0)

---

## Narrative Templates

### Holdings

For each lord + holding:

```yaml
- id: narr_{lord}_{place}_control
  content: "{lord.name} holds {place.name}"
  type: control
  about: { characters: [lord.id], places: [place.id] }
  truth: 1.0
```

### Dispossession

For each Saxon who lost land:

```yaml
- id: narr_{saxon}_lost_{place}
  content: "{saxon.name} was lord of {place.name} before the Normans"
  type: claim
  about: { characters: [saxon.id], places: [place.id] }
  truth: 1.0
```

### Events

For each historical event:

```yaml
- id: narr_{event.id}
  content: "{event.content}"
  type: memory
  about: { characters: event.characters, places: event.places }
  truth: 1.0
```

---

## Belief Distribution Rules

### Lords know their holdings

```python
for lord in lords:
  for holding in lord.holds:
    create_belief(lord, narr_control, believes=1.0, heard=1.0)
```

### Locals know local events

```python
for event in events:
  for place in event.places:
    for char in characters_at(place):
      create_belief(char, narr_event, heard=0.8, believes=0.7)
```

### News spreads with distance decay

```python
for event in major_events:
  for char in all_characters:
    distance = distance_to_event(char, event)
    heard = max(0, 1.0 - distance * 0.1)
    create_belief(char, narr_event, heard=heard)
```

---

## Narrative Types

| Type | Count | Description |
|------|-------|-------------|
| control | ~100 | Who holds what |
| claim | ~50 | Disputed ownership |
| memory | ~40 | Historical events |
| rumor | ~30 | Unverified news |
| secret | ~20 | Hidden knowledge |
| debt | ~10 | Obligations owed |

---

## Verification

- [ ] Every character believes at least 5 narratives
- [ ] Every narrative believed by at least 1 character
- [ ] At least 30 contradicting narrative pairs
- [ ] Belief network is connected (no isolated clusters)
