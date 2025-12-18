# Scraping Pipeline — Algorithm

**Purpose:** Five phases. Each builds on previous.

---

## Overview

```
Raw scrape → Clean → Enrich → Link → Verify
```

```
data/
├── raw/           # Scraped JSON
├── clean/         # Processed YAML
├── world/         # Final game data
└── scripts/       # Scraping tools
```

---

## Phases

| Phase | Name | Output |
|-------|------|--------|
| 1 | Geography | `places.yaml`, `routes.yaml` |
| 2 | Political | `characters.yaml`, `holdings.yaml` |
| 3 | Events | `events.yaml` |
| 4 | Narratives | `narratives.yaml`, `beliefs.yaml` |
| 5 | Tensions | `tensions.yaml` |

---

## Data Sources

### Phase 1: Geography

| Source | URL | Provides |
|--------|-----|----------|
| Domesday | `https://opendomesday.org/api/` | settlements, holders, values |
| OSM | Overpass API | coordinates, rivers, terrain |
| Ancient Roam | `https://github.com/ancient-roam` | roman_roads as GeoJSON |

### Phase 2: Political

| Source | Provides |
|--------|----------|
| Domesday | tenants_in_chief, subtenants, 1066_holders |
| Anglo-Saxon Chronicle | 1067 political state, appointments |
| PASE database | family relationships, titles |

### Phase 3: Events

| Source | Provides |
|--------|----------|
| Chronicle | events 1065-1070, dates, places, people |
| Secondary sources | Harrying details, rebellion timeline |

### Phases 4-5: Narratives & Tensions

Generated from phases 1-3 plus manual relationship patterns.

---

## Phase Dependencies

```
Phase 1 (Geography)
    │
    ▼
Phase 2 (Political) ──────┐
    │                     │
    ▼                     │
Phase 3 (Events) ─────────┤
    │                     │
    ▼                     ▼
Phase 4 (Narratives) ◄────┘
    │
    ▼
Phase 5 (Tensions)
```

---

## Output Files

| File | Location | Count |
|------|----------|-------|
| `places.yaml` | `data/world/` | ~215 |
| `routes.yaml` | `data/world/` | ~400 |
| `characters.yaml` | `data/world/` | ~120 |
| `narratives.yaml` | `data/world/` | ~250 |
| `beliefs.yaml` | `data/world/` | ~800 |
| `tensions.yaml` | `data/world/` | ~50 |
