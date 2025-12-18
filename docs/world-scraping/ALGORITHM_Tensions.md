# Phase 5: Tensions — Algorithm

**Purpose:** What's About To Break

---

## Sources

| Source | Provides |
|--------|----------|
| Phase 4 | narratives, beliefs |
| Manual | conflict_patterns |

---

## Output

### tensions.yaml

**Count:** ~50

```yaml
- id: tension_york_claim
  narratives: [narr_malet_holds_york, narr_waltheof_claim_york]
  pressure_type: gradual
  pressure: 0.6
  base_rate: 0.001
  breaking_point: 0.9
  description: "Waltheof has not forgotten York"

- id: tension_northern_rebellion
  narratives: [narr_norman_occupation, narr_saxon_resistance]
  pressure_type: scheduled
  trigger_at: "1068-01"
  description: "The North will rise"
```

**Fields:**
- `id` — Unique identifier (`tension_*`)
- `narratives` — Conflicting narratives (2+)
- `pressure_type` — gradual, event, scheduled
- `pressure` — Current pressure (0.0-1.0)
- `base_rate` — Increase per tick (gradual)
- `breaking_point` — When it breaks (0.0-1.0)
- `description` — Narrator context

---

## Tension Templates

### Norman-Saxon Holdings

For each holding with dispossessed Saxon still alive:

```yaml
- id: tension_{place}_claim
  narratives: [narr_{norman}_control, narr_{saxon}_claim]
  pressure_type: gradual
  pressure: 0.3
  description: "{saxon} has not forgotten {place}"
```

### Political Tensions

Known historical tensions:

```yaml
- id: tension_northern_rebellion
  narratives: [narr_norman_occupation, narr_saxon_resistance]
  pressure_type: scheduled
  trigger_at: "1068-01"  # Historical rebellion date
```

### Local Contradictions

Generated from contradicting narratives:

```python
for narr_a, narr_b in contradicting_pairs:
  if believers_overlap(narr_a, narr_b):
    create_tension(narr_a, narr_b, pressure=0.4)
```

---

## Pressure Types

| Type | Behavior | Example |
|------|----------|---------|
| gradual | Increases over time | Resentment building |
| event | Triggered by player/world action | Discovery of secret |
| scheduled | Fires at specific game time | Historical rebellion |

---

## Breaking Points

When `pressure >= breaking_point`:

1. Tension "breaks"
2. Break event generated
3. Narratives may change
4. Characters may act
5. New tensions may form

---

## Initial Pressure Distribution

| Category | Starting Pressure | Notes |
|----------|-------------------|-------|
| Norman-Saxon claims | 0.3-0.5 | Fresh wounds |
| Political rivalries | 0.4-0.6 | Active conflict |
| Personal enmities | 0.2-0.4 | Simmering |
| Scheduled events | N/A | Time-triggered |

---

## Verification

- [ ] No tension at 0.0 pressure (world should feel alive)
- [ ] At least 10 tensions above 0.5 pressure
- [ ] All scheduled tensions have valid dates
- [ ] Breaking points are achievable
