# Archived: SYNC_World_Scraping_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

Archived on: 2025-12-18
Original file: SYNC_World_Scraping_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

---

## Database Injection

```bash
# Inject to seed database (default)
python3 data/scripts/inject_world.py --clear

# Inject to different database
python3 data/scripts/inject_world.py --graph blood_ledger --clear
```

### Graph Contents (`seed`)

| Data Type | Count |
|-----------|-------|
| Characters | 49 |
| Places | 88 |
| Things | 28 |
| Narratives | 141 |
| Tensions | 22 |
| Beliefs | ~2,040 |
| Presences | ~60 |
| Geography | 113 |
| Thing Locations | 24 |
| Thing Ownership | 11 |

---












## Directory Structure

```
data/
├── raw/              # Scraped JSON (from APIs)
├── clean/            # Processed YAML (intermediate)
├── world/            # Final game data
│   ├── places.yaml         ✓ 62 major places
│   ├── places_minor.yaml   ✓ 26 minor locations (NEW)
│   ├── routes.yaml         ✓ 113 routes
│   ├── characters.yaml     ✓ 49 characters
│   ├── holdings.yaml       ✓ 56 holdings
│   ├── things.yaml         ✓ 28 things (NEW)
│   ├── thing_locations.yaml ✓ 24 thing-place links (NEW)
│   ├── thing_ownership.yaml ✓ 11 character-thing links (NEW)
│   ├── events.yaml         ✓ 22 events
│   ├── narratives.yaml     ✓ 141 narratives
│   ├── beliefs.yaml        ✓ ~2,040 beliefs
│   └── tensions.yaml       ✓ 22 tensions
├── manual/           # Human-curated data
│   ├── events_raw.yaml
│   └── relationships.yaml
└── scripts/
    ├── inject_world.py       ✓ Database injection
    └── scrape/
        ├── phase1_geography.py   ✓
        ├── phase2_political.py   ✓
        ├── phase3_events.py      ✓
        ├── phase4_narratives.py  ✓
        └── phase5_tensions.py    ✓
```

---












## New Content: Things

Objects in the world that characters carry, protect, covet, or hide.

### Thing Types

| Type | Count | Examples |
|------|-------|----------|
| relic | 4 | St. Cuthbert's bones, Hild's shrine, Ripon Gospels |
| document | 7 | Royal writ, Durham charter, tax rolls, safe conduct |
| weapon | 5 | Harold's sword (lost), Saxon axe, Norman mail |
| treasure | 5 | Tax silver, Gospatric's buried gold, church silver |
| token | 6 | Sheriff's seal, castle keys, Waltheof's ring |
| provisions | 4 | York granary, salt stores, healing herbs |

### Key Thing Narratives

- "Harold's sword was lost at Hastings. Some say Malet knows where."
- "Gospatric buried gold before submitting. Only he knows where."
- "The keys to St. Cuthbert's shrine are held by the Bishop alone."
- "Tax silver moves from York every few weeks. A tempting target."

---












## New Content: Minor Locations

Smaller places for atmosphere, ambush sites, meeting points, and outlaw camps.

### Location Types

| Type | Count | Examples |
|------|-------|----------|
| crossing | 7 | Aldwark Ford, Piercebridge, Ferrybridge |
| ruin | 4 | Cawthorn Roman Camps, Catterick, Aldborough |
| forest | 3 | Galtres Forest, Pickering Forest, Knaresborough Forest |
| wilderness | 2 | Cleveland Hills, North York Moors |
| camp | 2 | Wulfric's Camp (hidden), Moor Men's Camp (hidden) |
| holy_well | 1 | St Helen's Well |
| standing_stones | 1 | Devil's Arrows |
| hill | 1 | Roseberry Topping |
| monastery | 1 | Lastingham |
| crossroads | 2 | Scotch Corner, Croft-on-Tees |
| village | 2 | Newburn (Copsi murdered here), Wharram Percy |

---












## Upcoming Work

Although core scraping passes are complete, we still need to:

1. **Export Moment Seeds** — Identify narratives/tensions that should instantiate initial moments for the graph migration.
2. **Automate Consistency Checks** — Wire tests from `docs/world-scraping/TEST_World_Scraping.md` into CI.
3. **Refresh Dataset Quarterly** — Schedule next scrape (Jan 2025) to capture new historical research notes.

Add new tasks/handoffs here when changes land.

### Outlaw Leaders (In Yorkshire)

| Character | Band | Territory |
|-----------|------|-----------|
| Wulfric of Galtres | Galtres Wolves | Galtres Forest (north of York) |
| Siward Barn | Moor Men | Cleveland Hills |
| Ketil | Cleveland Band | Cleveland Hills |
| Osmund | Pickering Ghosts | Cawthorn Roman Camps |

### Outlaw Band Profiles

**Galtres Wolves** — Dispossessed thegns. "Take from Normans only." Wulfric has a code.

**Moor Men** — Ex-huscarls who survived Hastings. Siward Barn has earl's blood. Waiting for the Danes.

**Cleveland Band** — Desperate men, not noble outlaws. "Ketil learned cruelty from his masters."

**Pickering Ghosts** — Use Roman ruins and roads. "Normans search but never find them."

---












## Character Breakdown (Updated)

| Faction | Count |
|---------|-------|
| Norman | 14 |
| Saxon | 16 |
| Church | 5 |
| Danish | 2 |
| Scottish | 1 |
| Norse | 1 |
| Saxon Resistance | 6 |
| Outlaw | 4 |

| Type | Count |
|------|-------|
| major | 29 |
| minor | 15 |
| background | 4 |
| companion | 1 |

| Gender | Count |
|--------|-------|
| male | 45 |
| female | 4 |

---












## Schema Examples

### Thing Schema

```yaml
id: thing_cuthbert_bones
name: "Bones of St. Cuthbert"
type: relic
portable: false
significance: legendary
quantity: 1
description: "The incorrupt body of Northumbria's greatest saint."
modifiers: []
_location: place_durham_cathedral
_holder: null
```

### Minor Location Schema

```yaml
id: place_galtres_camp
name: Wulfric's Camp
type: camp
region: Galtres Forest
description: "Hidden deep in Galtres. Only those who know the signs can find it."
lat: 54.08
lng: -1.03
_hidden: true
```

### Outlaw Character Schema

```yaml
id: char_wulfric_galtres
name: Wulfric of Galtres
type: minor
alive: true
gender: male
face: hard
skills:
  fighting: skilled
  tracking: skilled
  sneaking: skilled
voice:
  tone: bitter
  style: blunt
personality:
  approach: cunning
  values: [loyalty, survival]
  flaw: wrath
backstory:
  wound: 'Lost everything. The fire still burns in his dreams.'
  why_here: 'Leads the Galtres Wolves. Takes from Normans only. Has a code.'
_faction: outlaw
_base_place: place_galtres_camp
```

---











