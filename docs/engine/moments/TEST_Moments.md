# Moments — Tests: Trace Scenarios

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
ALGORITHMS:  ./ALGORITHM_Physics.md, ./ALGORITHM_Handlers.md, ./ALGORITHM_Canon.md,
             ./ALGORITHM_Input.md, ./ALGORITHM_Actions.md, ./ALGORITHM_Speed.md
SCHEMA:      ./SCHEMA_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
THIS:        TEST_Moments.md (you are here)
SYNC:        ./SYNC_Moments.md
IMPL:        ../../engine/tests/test_moments.py
```

---

## Trace Scenarios

These traces walk through the complete system to verify behavior.

---

## Trace 1: Simple Exchange

**Player asks Aldric a question. Aldric responds.**

### Initial State

```yaml
Characters:
  - char_player: AT place_camp
  - char_aldric: AT place_camp, importance: 0.6

Moments:
  - moment_aldric_greeting:
      text: "We should talk about the road ahead."
      status: possible
      weight: 0.5
      ATTACHED_TO: char_aldric (presence_required: true)
      CAN_SPEAK: char_aldric (weight: 1.0)
```

### Step 1: Player Input

```
Player types: "Aldric, what do you think about York?"
```

**Input Processing (Sequential):**
1. Parse: Extract reference to "Aldric"
2. Create moment:
   ```yaml
   moment_player_question:
     text: "Aldric, what do you think about York?"
     type: dialogue
     status: spoken  # Player input is immediate canon
     weight: 1.0
   ```
3. Create links:
   - ATTACHED_TO: char_player
   - ATTACHED_TO: char_aldric (heard)
   - ATTACHED_TO: place_camp
   - REFERENCES: char_aldric (direct address)
   - CAN_SPEAK: char_player
4. Inject energy:
   - Aldric directly referenced → +0.5 energy to his moments
   - moment_aldric_greeting weight: 0.5 + 0.5 = 1.0

### Step 2: Physics Tick

**Inject:** Characters receive energy (already done via input)

**Decay:** 5% decay
- moment_aldric_greeting: 1.0 * 0.95 = 0.95

**Propagate:** Energy flows through links
- (Minimal propagation needed — weight already high)

**Detect:** Check flip threshold (0.8)
- moment_aldric_greeting: 0.95 >= 0.8 → **FLIP**

### Step 3: Handler Triggered

Aldric's handler runs (triggered by moment_aldric_greeting flip).

**Handler receives:**
- Character: Aldric (beliefs, voice, relationships)
- Location: camp
- Present: [player, Aldric]
- Recent history: [moment_player_question]
- Trigger: moment_aldric_greeting

**Handler produces:**
```yaml
moments:
  - text: "York is dangerous. The Normans hold it tight."
    type: dialogue
  - text: "But if you're set on going, I'll follow."
    type: dialogue
links:
  - CAN_LEAD_TO: moment_1 → moment_2
```

### Step 4: Canon Recording

**Canon Holder records:**
- moment_aldric_greeting → status: spoken
- THEN link: moment_player_question → moment_aldric_greeting

**Handler output injected:**
- moment_aldric_response_1: weight 0.6 (relevance × importance)
- moment_aldric_response_2: weight 0.4

### Step 5: Next Physics Tick

**Detect:**
- moment_aldric_response_1: 0.6 < 0.8 → no flip yet

**Inject:** Aldric still important and present
- moment_aldric_response_1: 0.6 + 0.1 = 0.7

(Continue until flip or decay)

### Expected Outcome

```
Player: "Aldric, what do you think about York?"
Aldric: "York is dangerous. The Normans hold it tight."
(pause)
Aldric: "But if you're set on going, I'll follow."
```

**THEN chain:**
```
moment_player_question → moment_aldric_greeting → moment_aldric_response_1 → moment_aldric_response_2
```

---

## Trace 2: Silence

**Player says something no one can respond to.**

### Initial State

```yaml
Characters:
  - char_player: AT place_camp
  - char_aldric: AT place_camp

Moments:
  - moment_aldric_knows_sword:
      text: "I know where to find a blacksmith."
      ATTACHED_TO: char_aldric
      weight: 0.4
      # This is about blacksmiths, not about philosophy
```

### Step 1: Player Input

```
Player types: "What is the meaning of existence?"
```

**Input Processing:**
- Create moment_player_philosophy
- ATTACHED_TO: char_player, char_aldric (heard), place_camp
- No direct reference to Aldric
- Energy injection: distributed (0.5 * 0.3 = 0.15 to Aldric's moments)

### Step 2: Physics Tick

**Inject:**
- moment_aldric_knows_sword: 0.4 + 0.15 = 0.55

**Decay:**
- moment_aldric_knows_sword: 0.55 * 0.95 = 0.52

**Detect:**
- 0.52 < 0.8 → no flip

### Step 3: Energy Must Land

After several ticks, no NPC moments flip.

**Fallback:** Energy returns to player character.

```python
# Player character always has a handler
# Handler runs with context: "silence"
```

**Player handler produces:**
```yaml
moment_player_observation:
  text: "The silence stretches. No one meets your eye."
  type: narration
  weight: 0.7
```

### Step 4: Physics Tick

**Detect:**
- moment_player_observation: 0.7 < 0.8 → no flip yet

**Inject:** Player character receives fallback energy
- moment_player_observation: 0.7 + 0.15 = 0.85

**Next tick detect:**
- 0.85 >= 0.8 → **FLIP**

### Expected Outcome

```
Player: "What is the meaning of existence?"
(pause)
"The silence stretches. No one meets your eye."
```

**Verified:** Energy always lands. There is no "nothing happens."

---

## Trace 3: Multi-Party

**Player asks the room. Multiple characters respond.**

### Initial State

```yaml
Characters:
  - char_player: AT place_camp
  - char_aldric: AT place_camp, importance: 0.6
  - char_mildred: AT place_camp, importance: 0.5
  - char_godwin: AT place_camp, importance: 0.3

Moments:
  - moment_aldric_opinion:
      text: "The north road is safer."
      ATTACHED_TO: char_aldric
      weight: 0.5
  - moment_mildred_opinion:
      text: "The coast road is faster."
      ATTACHED_TO: char_mildred
      weight: 0.45
  - moment_godwin_opinion:
      text: "Either way, we should leave at dawn."
      ATTACHED_TO: char_godwin
      weight: 0.35
```

### Step 1: Player Input

```
Player types: "Which road should we take?"
```

**Input Processing:**
- No direct reference → distributed energy
- Aldric: +0.15, Mildred: +0.15, Godwin: +0.15

### Step 2: Physics Tick

**After injection:**
- moment_aldric_opinion: 0.5 + 0.15 = 0.65
- moment_mildred_opinion: 0.45 + 0.15 = 0.60
- moment_godwin_opinion: 0.35 + 0.15 = 0.50

**Inject (importance × proximity):**
- Aldric (0.6): +0.06 → 0.71
- Mildred (0.5): +0.05 → 0.65
- Godwin (0.3): +0.03 → 0.53

### Step 3: Subsequent Ticks

Multiple ticks, continuing injection:

**Tick N:**
- moment_aldric_opinion: 0.82 → **FLIP**

**Tick N+1:**
- moment_mildred_opinion: 0.81 → **FLIP**

**Tick N+2:**
- moment_godwin_opinion: 0.65 (may or may not flip, depends on continued injection)

### Step 4: Handlers Triggered (Parallel)

Aldric and Mildred flip in close succession.

**Parallel execution:**
- Aldric's handler runs
- Mildred's handler runs

Both produce follow-up potentials.

### Step 5: Canon Recording

**Canon Holder records in weight order:**
1. moment_aldric_opinion (0.82)
2. moment_mildred_opinion (0.81)

### Expected Outcome

```
Player: "Which road should we take?"
Aldric: "The north road is safer."
Mildred: "The coast road is faster."
(Godwin may or may not speak, depending on energy)
```

**Verified:** Multi-party conversation emerges naturally from weight ordering.

---

## Trace 4: Cascade

**One confession triggers a chain of reactions.**

### Initial State

```yaml
Characters:
  - char_player: AT place_camp
  - char_aldric: AT place_camp
  - char_mildred: AT place_camp
  - char_godwin: AT place_camp

Moments:
  - moment_aldric_confession:
      text: "I killed Edmund. I had no choice."
      ATTACHED_TO: char_aldric
      weight: 0.85  # High weight, about to flip
  - moment_mildred_shock:
      text: "What? Edmund was... he was your brother!"
      ATTACHED_TO: char_mildred
      weight: 0.3
      # Links to confession via energy propagation
  - moment_godwin_anger:
      text: "You've been lying to us this whole time."
      ATTACHED_TO: char_godwin
      weight: 0.25
```

### Step 1: Physics Tick

**Detect:**
- moment_aldric_confession: 0.85 >= 0.8 → **FLIP**

**Canon records:** moment_aldric_confession

**Energy propagation:** (from actualized moment)
- Connected moments receive energy via CAN_LEAD_TO links
- moment_mildred_shock: 0.3 + 0.4 = 0.7
- moment_godwin_anger: 0.25 + 0.35 = 0.6

### Step 2: Handler Triggered

Aldric's handler runs (produced the confession).

**Other characters receive energy** (they witnessed):
- Mildred's moments boosted
- Godwin's moments boosted

### Step 3: Next Tick

**Inject:**
- moment_mildred_shock: 0.7 + (0.5 × 1.0) × 0.1 = 0.75
- moment_godwin_anger: 0.6 + (0.3 × 1.0) × 0.1 = 0.63

**Decay:**
- moment_mildred_shock: 0.75 * 0.95 = 0.71

**Propagation + injection continues...**

**Tick N:**
- moment_mildred_shock: 0.82 → **FLIP**

**Tick N+1:**
- Mildred's handler runs → produces more potentials
- Energy propagates further

**Tick N+2:**
- moment_godwin_anger: 0.81 → **FLIP**

### Expected Outcome

```
Aldric: "I killed Edmund. I had no choice."
(beat)
Mildred: "What? Edmund was... he was your brother!"
(beat)
Godwin: "You've been lying to us this whole time."
(cascade continues...)
```

**Verified:** Cascade creates drama through natural energy propagation.

---

## Trace 5: Action Conflict

**Two characters try to grab the same sword.**

### Initial State

```yaml
Characters:
  - char_aldric: AT place_camp
  - char_mildred: AT place_camp

Things:
  - thing_sword: AT place_camp

Moments:
  - moment_aldric_grab:
      text: "Aldric reaches for the sword."
      type: action
      action: take
      action_target: thing_sword
      ATTACHED_TO: char_aldric
      weight: 0.85
  - moment_mildred_grab:
      text: "Mildred lunges for the blade."
      type: action
      action: take
      action_target: thing_sword
      ATTACHED_TO: char_mildred
      weight: 0.82
```

### Step 1: Physics Tick

**Detect:**
- moment_aldric_grab: 0.85 >= 0.8 → **FLIP**
- moment_mildred_grab: 0.82 >= 0.8 → **FLIP**

**Both flip.** This is NOT mutex. This is drama.

### Step 2: Canon Recording

**Canon Holder records both** (in weight order):
1. moment_aldric_grab (0.85)
2. moment_mildred_grab (0.82)

THEN links created for both.

### Step 3: Action Processing (Sequential)

**Action queue:**
1. moment_aldric_grab (take sword)
2. moment_mildred_grab (take sword)

**Process moment_aldric_grab:**
- Validate: sword at camp? Yes
- Execute: sword.carried_by = char_aldric
- Consequence: "Aldric's hand closes on the hilt."

**Process moment_mildred_grab:**
- Validate: sword available? **No** (Aldric has it)
- **Validation fails**
- Consequence: "Mildred's hand grasps empty air."

### Step 4: Consequences Injected

```yaml
moment_aldric_success:
  text: "Aldric's hand closes on the hilt."
  weight: 0.6

moment_mildred_blocked:
  text: "Mildred's hand grasps empty air."
  weight: 0.6
  ATTACHED_TO: char_mildred
```

### Step 5: Handler Triggered

Mildred's handler runs (received blocked consequence).

**Handler produces:**
```yaml
moment_mildred_frustration:
  text: "She glares at Aldric. 'That was mine.'"
  type: dialogue
```

### Expected Outcome

```
"Aldric reaches for the sword."
"Mildred lunges for the blade."
"Aldric's hand closes on the hilt."
"Mildred's hand grasps empty air."
(beat)
Mildred: "She glares at Aldric. 'That was mine.'"
```

**Verified:** Simultaneous actions are drama. Action processing handles conflict naturally.

---

## Trace 6: The Snap (3x to 1x)

**Player at 3x speed. Interrupt triggers snap to 1x.**

### Initial State

```yaml
Speed: 3x
Characters:
  - char_player: AT place_road (traveling)
  - char_aldric: AT place_road
  - char_enemy: approaching (will enter scene)

Moments:
  - moment_travel_1: "The road stretches." (weight: 0.3, montage)
  - moment_travel_2: "Clouds gather." (weight: 0.3, montage)
  - moment_enemy_attack:
      text: "Bandits burst from the treeline!"
      type: action
      action: attack
      action_target: char_player
      weight: 0.2  # Building up
```

### Step 1: Fast Physics Ticks (3x)

**Display:** Motion blur, streaming text
**Canon:** All moments recorded normally

**Tick N:**
- moment_travel_1 flips → canon (not displayed, low weight)
- moment_travel_2 flips → canon (not displayed)

**Tick N+5:**
- char_enemy enters scene → energy injected
- moment_enemy_attack: 0.2 + 0.5 = 0.7

**Tick N+6:**
- moment_enemy_attack: 0.7 + 0.15 = 0.85 → **FLIP**

### Step 2: Interrupt Detection

```python
is_interrupt(moment_enemy_attack):
    # action: attack → combat initiated
    return True  # INTERRUPT
```

### Step 3: The Snap

**Phase 1: Running** (already in progress)
- Motion blur
- Muted colors

**Phase 2: The Beat**
- Screen freezes
- 400ms silence
- Tension builds

**Phase 3: Arrival**
- Speed → 1x
- Full color, crystal clear
- moment_enemy_attack displays prominently

### Expected Outcome

```
[3x speed - blur, streaming]
...road...clouds...dust...
[FREEZE - 400ms silence]
[1x speed - vivid]
"Bandits burst from the treeline!"
```

**Verified:** Interrupt breaks through. The snap is visceral.

---

## Trace 7: Journey Conversation (2x)

**Travel at 2x with conversation.**

### Initial State

```yaml
Speed: 2x
Characters:
  - char_player: traveling
  - char_aldric: traveling with player

Moments:
  - moment_montage_1: "The road winds." (type: montage, weight: 0.3)
  - moment_montage_2: "Sun sets." (type: montage, weight: 0.3)
  - moment_aldric_personal:
      text: "I never told you about my brother."
      type: dialogue
      weight: 0.6
      ATTACHED_TO: char_aldric
```

### Step 1: Physics Ticks (2x rate)

**Tick N:**
- moment_montage_1: 0.3 → 0.4 → 0.5 → ... → 0.85 → **FLIP**
- Display: muted, streaming

**Tick N+2:**
- moment_aldric_personal: 0.6 → 0.7 → 0.8 → 0.85 → **FLIP**
- Display: **vivid, full color** (dialogue at 2x shows fully)

**Tick N+4:**
- moment_montage_2 flips
- Display: muted, streaming

### Step 2: Display Distinction

```
[muted, streaming] The road winds.
[vivid, centered] "I never told you about my brother."
[muted, streaming] Sun sets.
```

### Expected Outcome

Travel and conversation interleaved. Time passes, but emotional beats preserved.

**Verified:** Journey conversations work. Montage + dialogue coexist.

---

## Test Coverage Summary

| Trace | Tests |
|-------|-------|
| 1: Simple Exchange | Input → Physics → Handler → Canon → Display |
| 2: Silence | Energy must land, player fallback |
| 3: Multi-Party | Parallel handlers, weight ordering |
| 4: Cascade | Energy propagation, chain reactions |
| 5: Action Conflict | Simultaneous actions, sequential processing |
| 6: The Snap | 3x speed, interrupt detection, transition |
| 7: Journey | 2x speed, montage + dialogue display |

---

## Implementation Test Files

```
engine/tests/
├── test_physics.py        # Inject, decay, propagate, detect
├── test_handlers.py       # Trigger, output, injection
├── test_canon.py          # Recording, THEN links, ordering
├── test_input.py          # Parsing, moment creation, energy
├── test_actions.py        # Queue, validation, execution
├── test_speed.py          # Display filtering, interrupts, snap
├── test_traces.py         # Full trace scenarios above
└── test_invariants.py     # All validation invariants
```

---

*"Traces prove the system works end-to-end."*
