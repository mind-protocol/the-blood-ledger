# Canon Holder — Behaviors

```
STATUS: CANONICAL
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Canon.md
THIS:            BEHAVIORS_Canon.md (you are here)
ALGORITHM:       ./ALGORITHM_Canon_Holder.md
VALIDATION:      ./VALIDATION_Canon.md
IMPLEMENTATION:  ./IMPLEMENTATION_Canon.md
TEST:            ./TEST_Canon.md
SYNC:            ./SYNC_Canon.md
```

---

## BEHAVIORS

### B1: Moment Surfaces When Salient

```
GIVEN:  A moment with status='possible'
WHEN:   salience (weight × energy) reaches 0.3
AND:    All presence requirements are met
THEN:   Moment status becomes 'active'
AND:    Frontend receives 'moment_activated' event
```

### B2: Active Moment Becomes Canon

```
GIVEN:  A moment with status='active'
WHEN:   Canon Holder processes it
AND:    A valid speaker is available (for dialogue)
THEN:   Moment status becomes 'spoken'
AND:    THEN link is created to previous spoken moment
AND:    Game time advances by moment duration
AND:    Frontend receives 'moment_spoken' event
```

### B3: Speaking Costs Energy

```
GIVEN:  A moment becoming spoken
WHEN:   Canon Holder records it
THEN:   Moment energy is reduced by 60%
```

### B4: Highest Weight Speaker Wins

```
GIVEN:  A dialogue moment with multiple CAN_SPEAK links
WHEN:   Canon Holder determines speaker
THEN:   Character with highest CAN_SPEAK.strength speaks
AND:    Character must be present at player's location
AND:    Character must be awake and alive
```

### B5: Moment Goes Dormant When Player Leaves

```
GIVEN:  An active moment with presence_required=true
WHEN:   Player leaves the location
AND:    ATTACHED_TO link has persistent=true
THEN:   Moment status becomes 'dormant'
```

### B6: Dormant Moment Reactivates

```
GIVEN:  A dormant moment
WHEN:   Player returns to location
AND:    Presence requirements are met again
THEN:   Moment status becomes 'active'
AND:    Frontend receives 'moment_activated' event
```

### B7: Moments Decay When Unimportant

```
GIVEN:  A moment with weight < 0.01
WHEN:   Decay check runs
THEN:   Moment status becomes 'decayed'
```

### B8: Multiple Moments Are Paced

```
GIVEN:  Multiple moments ready to become spoken same tick
WHEN:   Canon Holder processes them
THEN:   Maximum 3 moments become spoken per tick
AND:    Highest salience moments are processed first
AND:    THEN links chain them in order
```

### B9: Dialogue Without Speaker Waits

```
GIVEN:  A dialogue moment with status='active'
WHEN:   No valid speaker is present
THEN:   Moment remains 'active'
AND:    Moment is NOT recorded to canon
```

---

## INPUTS / OUTPUTS

### Primary Function: `record_to_canon()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| moment | Moment | The moment to record |
| speaker | Character? | Who speaks (None for narration) |
| previous | Moment? | Previous spoken moment for THEN link |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| recorded | bool | Whether recording succeeded |

**Side Effects:**

- Moment status changes to 'spoken'
- Moment energy reduced by 60%
- THEN link created in graph
- Game time advances
- SSE event broadcast to frontend

---

## EDGE CASES

### E1: No Previous Moment

```
GIVEN:  First moment of a playthrough (no previous spoken)
WHEN:   Canon Holder records it
THEN:   No THEN link is created
AND:    Recording still succeeds
```

### E2: Narration Moment

```
GIVEN:  A moment with type='narration'
WHEN:   Canon Holder records it
THEN:   speaker is set to None
AND:    No speaker resolution occurs
```

### E3: All Speakers Asleep

```
GIVEN:  A dialogue moment where all CAN_SPEAK characters are asleep
WHEN:   Canon Holder attempts to record
THEN:   Moment remains 'active'
AND:    No recording occurs
```

### E4: Player Input Moment

```
GIVEN:  A moment created from player click or freeform input
WHEN:   Canon Holder records it
THEN:   THEN link has player_caused=true
```

---

## ANTI-BEHAVIORS

### A1: No Skipping Active

```
GIVEN:  A moment with status='possible'
WHEN:   Any process attempts to record it
MUST NOT: Moment go directly to 'spoken'
INSTEAD:  Moment must first become 'active'
```

### A2: No Speaking Without Presence

```
GIVEN:  A dialogue moment
WHEN:   No CAN_SPEAK character is at player's location
MUST NOT: Moment become 'spoken'
INSTEAD:  Moment stays 'active', waiting
```

### A3: No Infinite Moment Flood

```
GIVEN:  Many moments ready same tick
WHEN:   Canon Holder processes
MUST NOT: All moments become spoken immediately
INSTEAD:  Maximum 3 per tick, rest wait
```

### A4: No Lost History

```
GIVEN:  A moment becoming spoken
WHEN:   Previous spoken moment exists
MUST NOT: Fail to create THEN link
INSTEAD:  Always chain spoken moments
```

---

## SSE EVENTS

| Event | Trigger | Payload |
|-------|---------|---------|
| `moment_activated` | B1, B6 | `{moment_id, weight, text}` |
| `moment_spoken` | B2 | `{moment_id, text, speaker, tick}` |
| `moment_decayed` | B5, B7 | `{moment_id}` |

---

## GAPS / IDEAS / QUESTIONS

- QUESTION: Should dormant moments decay slower than active?
- QUESTION: What happens if moment energy is already < 0.4 when spoken?
- IDEA: Priority queue for moments based on narrative importance
