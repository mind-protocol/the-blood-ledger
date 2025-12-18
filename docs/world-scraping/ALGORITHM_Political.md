# Phase 2: Political Structure — Algorithm

**Purpose:** Who Holds What

---

## Sources

| Source | Provides |
|--------|----------|
| Domesday | tenants_in_chief, subtenants, 1066_holders |
| Anglo-Saxon Chronicle | 1067 political state, appointments |
| PASE database | family relationships, titles |

---

## Output

### characters.yaml

**Count:** ~70 historical + ~50 minor

```yaml
- id: char_malet
  name: William Malet
  type: major
  faction: norman
  voice: { tone: cold, style: measured }

- id: char_waltheof
  name: Waltheof
  type: major
  faction: saxon_noble
  voice: { tone: bitter, style: formal }
```

**Fields:**
- `id` — Unique identifier (`char_*`)
- `name` — Full name
- `type` — major, minor, companion
- `faction` — norman, saxon_noble, saxon_common, church
- `voice` — Tone and style for dialogue

### holdings.yaml

**Count:** ~150

```yaml
- character: char_malet
  place: place_york
  type: holds
  since: 1067

- character: char_waltheof
  place: place_york
  type: claims
  lost: 1066
```

**Fields:**
- `character` — Character ID
- `place` — Place ID
- `type` — holds, controls, claims
- `since` / `lost` — When acquired/lost

---

## Script

```python
# scripts/scrape/phase2_political.py

# 1. Get Norman lords from Domesday
lords = dom.tenants_in_chief(regions=TARGET_REGIONS)

# 2. Get their holdings
for lord in lords:
  holdings = dom.holdings(tenant=lord.id)
  # Map to our place IDs
  lord.holds = [match_place(h) for h in holdings]

# 3. Get dispossessed Saxons (1066 holders)
saxons = dom.holders_1066(regions=TARGET_REGIONS)
for saxon in saxons:
  saxon.lost = dom.holdings_1066(holder=saxon.id)

# 4. Cross-reference with Chronicle for 1067 state
# (Manual curation needed - see phase2_manual.md)

# 5. Output
save_yaml(lords + saxons, "data/clean/characters.yaml")
```

---

## Key Historical Figures

| Character | Faction | Significance |
|-----------|---------|--------------|
| William Malet | Norman | Sheriff of Yorkshire, holds York |
| Robert de Comines | Norman | Earl of Northumbria (appointed 1068) |
| Waltheof | Saxon Noble | Earl, will rebel, will be executed |
| Edwin | Saxon Noble | Earl of Mercia, will rebel |
| Morcar | Saxon Noble | Earl of Northumbria (deposed) |
| Edgar Atheling | Saxon Royal | Claimant to throne, in Scotland |

---

## Faction Relationships

```
NORMAN
  └── holds power, castles, land
  └── enemies with: saxon_noble, saxon_common

SAXON_NOBLE
  └── dispossessed, bitter
  └── enemies with: norman
  └── complex with: saxon_common (some collaborate)

SAXON_COMMON
  └── suffering under Harrying
  └── enemies with: norman
  └── depends on: saxon_noble (for leadership)

CHURCH
  └── retains some power
  └── complex with: all (mediator role)
```

---

## Verification

- [ ] Malet holds York (Domesday confirms)
- [ ] No dead characters present (cross-ref death dates)
- [ ] Holdings match Domesday 1086 (extrapolated to 1067)
- [ ] Political relationships match Chronicle
