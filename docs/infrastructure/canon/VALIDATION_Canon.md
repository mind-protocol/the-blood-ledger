# Canon Holder — Validation

```
STATUS: SPEC
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Canon.md
BEHAVIORS:       ./BEHAVIORS_Canon.md
ALGORITHM:       ./ALGORITHM_Canon_Holder.md
THIS:            VALIDATION_Canon.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Canon.md
TEST:            ./TEST_Canon.md
SYNC:            ./SYNC_Canon.md
```

---

## INVARIANTS

These must ALWAYS be true:

### V1: Status Progression

```
Moment status can only progress:
  possible → active → spoken
  active → dormant → active (cycle allowed)
  any → decayed (terminal)

Never: possible → spoken (must pass through active)
Never: spoken → active (spoken is terminal except decay)
Never: decayed → any (decayed is terminal)
```

**Checked by:** `test_status_transitions`

### V2: THEN Chain Integrity

```
Every spoken moment (except the first) has exactly one incoming THEN link.
Every THEN link connects two spoken moments.
THEN links form a linear chain (no branches, no cycles).
```

**Checked by:** `test_then_chain_integrity`

### V3: Speaker Presence

```
If moment.type == 'dialogue' AND moment.status == 'spoken':
  THEN exists (c:Character)-[:SAID]->(moment)
  AND c was AT player's location when moment was spoken
  AND c.state == 'awake' AND c.alive == true at that tick
```

**Checked by:** `test_speaker_presence_on_spoken`

### V4: Energy Conservation on Actualization

```
When moment transitions active → spoken:
  moment.energy_after == moment.energy_before * 0.4
```

**Checked by:** `test_actualization_energy_cost`

### V5: Presence Gating

```
If moment has ATTACHED_TO with presence_required=true:
  moment.status can only be 'active' or 'spoken' when ALL such targets
  are AT the same place as char_player
```

**Checked by:** `test_presence_gating`

### V6: Pacing Limit

```
In any single tick, at most MAX_MOMENTS_PER_TICK (3) moments
transition from active → spoken.
```

**Checked by:** `test_pacing_limit`

### V7: Salience Threshold

```
Moment can only transition possible → active when:
  (moment.weight * moment.energy) >= SURFACE_THRESHOLD (0.3)
```

**Checked by:** `test_salience_threshold`

---

## PROPERTIES

For property-based testing:

### P1: Monotonic Tick Progression

```
FORALL moments m1, m2 where m1-[:THEN]->m2:
  m1.tick_spoken < m2.tick_spoken
```

**Tested by:** `test_prop_tick_monotonic`

### P2: Speaker Can Speak

```
FORALL moments m with status='spoken' and type='dialogue':
  EXISTS (c:Character)-[:CAN_SPEAK]->(m)
  WHERE (c)-[:SAID]->(m)
```

**Tested by:** `test_prop_speaker_has_can_speak`

### P3: Dormant Implies Persistent

```
FORALL moments m with status='dormant':
  EXISTS (m)-[:ATTACHED_TO {persistent: true}]->(target)
```

**Tested by:** `test_prop_dormant_is_persistent`

### P4: Active Implies Presence Met

```
FORALL moments m with status='active':
  FORALL (m)-[:ATTACHED_TO {presence_required: true}]->(target):
    (target)-[:AT {present: 1.0}]->(player_location)
```

**Tested by:** `test_prop_active_presence_met`

---

## ERROR CONDITIONS

### E1: No Valid Speaker

```
WHEN:    Dialogue moment is active but no CAN_SPEAK character is present/awake
THEN:    Moment remains active, not spoken
SYMPTOM: Moment stays in active pool across multiple ticks
```

**Tested by:** `test_error_no_speaker_stays_active`

### E2: Presence Lost Mid-Conversation

```
WHEN:    Player moves location while moments are active
THEN:    Moments with presence_required go dormant (if persistent) or stay active (if not)
SYMPTOM: Conversation interrupted, can resume on return
```

**Tested by:** `test_error_presence_lost`

### E3: Energy Already Low

```
WHEN:    Moment becomes spoken but energy < 0.4 (so 40% would be < 0.16)
THEN:    Energy still multiplied by 0.4, may go very low
SYMPTOM: Moment immediately at risk of decay
```

**Tested by:** `test_error_low_energy_actualization`

### E4: Flood of Ready Moments

```
WHEN:    >3 moments cross salience threshold same tick
THEN:    Only top 3 by salience become spoken, rest remain active
SYMPTOM: Backlog of active moments
```

**Tested by:** `test_error_moment_flood`

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Status Progression | `test_status_transitions` | ⚠ NOT YET |
| V2: THEN Chain | `test_then_chain_integrity` | ⚠ NOT YET |
| V3: Speaker Presence | `test_speaker_presence_on_spoken` | ⚠ NOT YET |
| V4: Energy Conservation | `test_actualization_energy_cost` | ⚠ NOT YET |
| V5: Presence Gating | `test_presence_gating` | ⚠ NOT YET |
| V6: Pacing Limit | `test_pacing_limit` | ⚠ NOT YET |
| V7: Salience Threshold | `test_salience_threshold` | ⚠ NOT YET |
| P1: Tick Monotonic | `test_prop_tick_monotonic` | ⚠ NOT YET |
| P2: Speaker Can Speak | `test_prop_speaker_has_can_speak` | ⚠ NOT YET |
| P3: Dormant Persistent | `test_prop_dormant_is_persistent` | ⚠ NOT YET |
| P4: Active Presence | `test_prop_active_presence_met` | ⚠ NOT YET |
| E1: No Speaker | `test_error_no_speaker_stays_active` | ⚠ NOT YET |
| E2: Presence Lost | `test_error_presence_lost` | ⚠ NOT YET |
| E3: Low Energy | `test_error_low_energy_actualization` | ⚠ NOT YET |
| E4: Flood | `test_error_moment_flood` | ⚠ NOT YET |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — Query for moments that skipped active status
[ ] V2 holds — Query for spoken moments without THEN link
[ ] V3 holds — Query for dialogue moments without SAID link
[ ] V4 holds — Log energy before/after actualization
[ ] V5 holds — Try to surface moment with absent target
[ ] V6 holds — Flood test with 10+ ready moments
[ ] V7 holds — Try to surface moment with salience 0.2
```

### Automated

```bash
pytest tests/infrastructure/canon/test_canon_holder.py
pytest tests/infrastructure/canon/test_canon_holder.py --cov=engine/infrastructure/canon
```

---

## GAPS / IDEAS / QUESTIONS

- QUESTION: What if moment energy is already 0? (0 * 0.4 = 0, but weight could be high)
- QUESTION: Should decayed moments be deleted or kept for history?
- IDEA: Property test for graph acyclicity (THEN links)
