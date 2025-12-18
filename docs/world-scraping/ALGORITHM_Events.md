# Phase 3: Historical Events — Algorithm

**Purpose:** What Happened

---

## Sources

| Source | Provides |
|--------|----------|
| Anglo-Saxon Chronicle | events 1065-1070, dates, places, people |
| Secondary sources | Harrying details, rebellion timeline |

---

## Output

### events.yaml

**Count:** ~40

```yaml
- id: event_hastings
  name: Battle of Hastings
  content: "Harold falls at Hastings. William claims the throne."
  date: 1066-10-14
  places: [place_hastings]
  characters: [char_william, char_harold]

- id: event_york_castle
  name: York Castle Built
  content: "William orders a castle built at York to control the North."
  date: 1067-01
  places: [place_york, place_york_castle]
  characters: [char_william, char_malet]
```

**Fields:**
- `id` — Unique identifier (`event_*`)
- `name` — Short title
- `content` — Narrative description
- `date` — ISO date or year-month
- `places` — Place IDs involved
- `characters` — Character IDs involved

---

## Key Events Timeline

| Date | Event | Impact |
|------|-------|--------|
| 1066-10-14 | Hastings | Harold dies, Norman conquest begins |
| 1066-12 | Submission | Edgar, Edwin, Morcar submit to William |
| 1067-01 | York Castle | Norman control extends north |
| 1068-01 | Northern Rebellion | Edwin and Morcar rebel |
| 1069-01 | Danish Fleet | Danes arrive, support rebellion |
| 1069-1070 | The Harrying | William devastates the North |

---

## Script

```python
# scripts/scrape/phase3_events.py

# Mostly manual curation from Chronicle
# Script validates and links to places/characters

events = load_yaml("data/manual/events_raw.yaml")

for event in events:
  # Link to our place IDs
  event.places = [match_place(p) for p in event.places]
  # Link to our character IDs
  event.characters = [match_char(c) for c in event.characters]
  # Validate dates
  event.date = parse_medieval_date(event.date)

save_yaml(events, "data/clean/events.yaml")
```

---

## The Harrying (Critical Context)

**Date:** Winter 1069-1070

**What happened:**
- William systematically destroyed the North
- Villages burned, crops destroyed, livestock killed
- Famine killed tens of thousands
- Land left waste for a generation

**Game impact:**
- Burned villages everywhere
- Starving refugees
- Fresh wounds and hatred
- Context for every Norman-Saxon interaction

---

## Event Categories

| Type | Count | Examples |
|------|-------|----------|
| Battle | ~5 | Hastings, Stamford Bridge |
| Political | ~10 | Submissions, appointments |
| Construction | ~5 | Castles built |
| Rebellion | ~10 | Northern uprising, Danish invasion |
| Devastation | ~5 | Harrying, specific burnings |
| Religious | ~5 | Church appointments, dedications |

---

## Verification

- [ ] Dates match Chronicle
- [ ] All place references valid
- [ ] All character references valid
- [ ] No anachronistic events
