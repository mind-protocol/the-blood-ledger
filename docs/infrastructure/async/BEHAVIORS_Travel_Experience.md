# Travel Experience — Behaviors

**Purpose:** What travel should feel like to the player.

---

## Core Behavior

**Travel is not a loading screen. Travel is play.**

The player experiences the journey:
- Narration streams as they move
- Map updates in real-time
- Places appear as they're created
- Companions can speak
- Player can converse, ask to stop, change destination

---

## What the Player Sees

### Initiation

```
Player: "Let's travel to York"

[Narrator acknowledges, begins streaming]
[Map shows route fading into fog]
[Player token begins moving]
```

### During Travel

```
[Left panel: current location image (crossfades as location changes)]
[Center: streaming narration of the journey]
[Map: player position animates, new places appear]
[Voices section: companion observations, internal thoughts]
```

### Companion Interaction

During travel, companions can:
- Initiate conversation (idle trigger)
- React to events (injection from breaks)
- Respond to player questions (input queue)

```
[10 seconds of silence]

Aldric: "Can I ask you something?"

[Discussion tree activates if player engages]
[Or fades if player ignores]
```

### Interruptions

```
[Suddenly]
Aldric grabs your arm. "Wait. Movement ahead."

[Narration pauses]
[Player can respond]
```

### Arrival

```
[Narration describes approach]
[Map shows York ahead]
[Left panel crossfades to York image]
[New scene begins]
```

---

## Player Input During Travel

### Conversational

Player types: "Tell me about York"

→ Narrator responds inline, continues journey

### Actions

Player types: "Let's rest here"

→ Narrator generates stop scene at current waypoint

### UI

Player clicks stop button

→ Hook injection → Narrator stops, generates scene

Player clicks different destination

→ Hook injection → Narrator acknowledges, may redirect

---

## Duration

**Narrator takes its time.**

- If Runner processing is quick → Narrator can still elaborate
- If Runner processing is slow → Narrator fills with journey beats
- No fixed duration. Narrative pacing, not timers.

The journey takes as long as it takes to tell well.

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| "Loading... 3 days pass." | Rich narration of the journey |
| Instant teleportation | Animated movement with place reveals |
| Silent waiting | Companion conversation, internal voices |
| Fixed duration timer | Narrative-driven pacing |

---

## Success Metrics

The player should feel:
- "I'm actually traveling through this world"
- "My companions are alive"
- "The world is materializing as I move"
- "I could stop anywhere and something would be here"

The player should NOT feel:
- "I'm waiting for a loading screen"
- "This is just a cutscene"
- "Nothing is happening"
