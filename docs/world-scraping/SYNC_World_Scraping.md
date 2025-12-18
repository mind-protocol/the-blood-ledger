# World Scraping — State & Progress

**Last Updated:** 2024-12-16
**Status:** COMPLETE (Enriched)
**Database:** `seed` (FalkorDB)

---

## Phase Status

| Phase | Name | Status | Output |
|-------|------|--------|--------|
| 1 | Geography | **COMPLETE** | `places.yaml`, `places_minor.yaml`, `routes.yaml` |
| 2 | Political | **COMPLETE** | `characters.yaml`, `holdings.yaml` |
| 3 | Events | **COMPLETE** | `events.yaml` |
| 4 | Narratives | **COMPLETE** | `narratives.yaml`, `beliefs.yaml` |
| 5 | Tensions | **COMPLETE** | `tensions.yaml` |
| 6 | Things | **COMPLETE** | `things.yaml`, `thing_locations.yaml`, `thing_ownership.yaml` |

---

## Current Counts (YAML)

| Data Type | Previous | Current | Added |
|-----------|----------|---------|-------|
| Places (main) | 62 | 62 | — |
| Places (minor) | 0 | 26 | +26 |
| Routes | 113 | 113 | — |
| Characters | 39 | 49 | +10 |
| Holdings | 56 | 56 | — |
| Things | 0 | 28 | +28 |
| Thing Locations | 0 | 24 | +24 |
| Thing Ownership | 0 | 11 | +11 |
| Events | 22 | 22 | — |
| Narratives | 77 | 141 | +64 |
| Beliefs | 1,520 | ~2,040 | +520 |
| Tensions | 17 | 22 | +5 |

---

## New Content: Characters

### Historical Figures (Outside Yorkshire)

| Character | Role | Location |
|-----------|------|----------|
| Eadric the Wild | Resistance leader | Welsh marches (rumored) |
| Gytha | Harold's mother | Exeter (funding resistance) |
| Godwine Haroldson | Harold's eldest son | Ireland (gathering ships) |
| Edmund Haroldson | Harold's son | Ireland |
| Magnus Haroldson | Harold's son | Ireland |
| Aldgyth | Harold's widow, Edwin/Morcar's sister | Hiding |

---

## New Content: Tensions

| Tension | Pressure | Type | Description |
|---------|----------|------|-------------|
| Harold's sons return | 0.6 | scheduled (1068-06) | Ships gathering in Dublin |
| Galtres Wolves | 0.35 | gradual | Wulfric grows bolder |
| Siward Barn rising | 0.3 | event | Waiting for the Danes |
| Gytha at Exeter | 0.5 | scheduled (1068-01) | William will march west |
| Aldgyth prize | 0.25 | gradual | Someone will find her |

---

## Narrative Breakdown (Updated)

| Type | Count |
|------|-------|
| control | 37 |
| memory | 35 |
| rumour | 25 |
| belief | 15 |
| claim | 8 |
| secret | 7 |
| reputation | 6 |
| debt | 3 |

---

## Data Sources

| Source | URL | Status | Notes |
|--------|-----|--------|-------|
| OpenDomesday | opendomesday.org/api/ | **DOWN (404)** | API not responding |
| OSM/Nominatim | nominatim.openstreetmap.org | **USED** | Geocoding |
| Manual Historical | - | **USED** | Domesday records, Anglo-Saxon Chronicle |
| Claude Knowledge | - | **USED** | Historical figures, things, outlaw bands |

---

## Blockers Resolved

- [x] ~~Verify OpenDomesday API~~ → Down, used manual data
- [x] ~~Find reliable coordinate source~~ → OSM Nominatim
- [x] ~~Need human review for character selection~~ → Core 49 selected
- [x] ~~Schema compliance~~ → All fields populated
- [x] ~~Database injection~~ → `seed` database ready
- [x] ~~Add Things/Items~~ → 28 things with locations and ownership
- [x] ~~Add minor locations~~ → 26 locations (crossings, ruins, camps)
- [x] ~~Add outlaw bands~~ → 4 bands with leaders and territories
- [x] ~~Add historical figures~~ → 6 characters outside Yorkshire

---

## Optional Expansion

| Task | Priority |
|------|----------|
| Add scops/bards (traveling storytellers) | Medium |
| Add songs and tales (as narratives) | Medium |
| Add marriage alliances (narrative links) | Medium |
| Add garrison strengths (narratives) | Low |
| Add more female characters | Medium |
| Add patrol routes (narratives) | Low |


---

## ARCHIVE

Older content archived to: `SYNC_World_Scraping_archive_2025-12.md`
