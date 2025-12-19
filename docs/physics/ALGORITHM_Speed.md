# Physics — Algorithm: Speed Controller

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Speed.md (you are here)
ALGORITHMS:     ./ALGORITHM_Physics.md, ./ALGORITHM_Canon.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
IMPL:           ../../engine/orchestration/speed.py
```

---

## Core Principle

**The player controls the speed of time, not the content.**

At 1x, every moment breathes. At 2x, time compresses but conversation persists. At 3x, the world rushes until drama demands attention.

Speed changes display, not reality. The same events happen at any speed.

---

## The Interface

```
[⏸]  [ 1x 🗣️ ]  [ 2x 🚶 ]  [ 3x ⏩ ]  [_____________________ input field]
```

---

## Three Speeds

| Speed | Name | Feel | Tick Rate |
|-------|------|------|-----------|
| **1x 🗣️** | Conversation | Present | ~0.2/sec (one per moment) |
| **2x 🚶** | Journey | Montage | ~2/sec (rapid) |
| **3x ⏩** | Skip | Fast-forward | Max system speed |

---

## What Each Speed Shows

### 1x — Everything

```python
def display_at_1x(moment: Moment) -> bool:
    """At 1x, everything displays."""
    return True
```

- Every moment displays fully
- Natural pacing, deliberate
- Player reads, absorbs, responds

### 2x — Montage with Conversation

```python
def display_at_2x(moment: Moment) -> bool:
    """
    At 2x, world compresses but conversation persists.
    """
    if moment.type == 'dialogue':
        return True  # Conversation always shows
    if moment.weight >= HIGH_WEIGHT_THRESHOLD:  # e.g., 0.7
        return True  # Important moments show
    if moment.type == 'montage':
        return True  # Atmospheric moments show (muted)

    return False  # Skip low-weight non-dialogue
```

Two things at once: travel and intimacy. Like film.

### 3x — Only Interrupts

```python
def display_at_3x(moment: Moment) -> bool:
    """
    At 3x, only interrupts break through.
    """
    return is_interrupt(moment)
```

- World runs as fast as system processes
- Display shows blur/motion, streaming text
- Only interrupt moments break through

---

## Display Distinction at 2x

| Type | Visual Style |
|------|--------------|
| World/montage | Muted color, smaller, italic, flows upward |
| Conversation | Full color, larger, centered, pauses for reading |

```python
def get_display_style(moment: Moment, speed: str) -> DisplayStyle:
    if speed == '2x':
        if moment.type in ['dialogue', 'thought']:
            return DisplayStyle.FULL  # Vivid, centered
        else:
            return DisplayStyle.MUTED  # Compressed, streaming

    return DisplayStyle.FULL
```

---

## Weight Filtering

| Weight | 1x | 2x | 3x |
|--------|-----|-----|-----|
| High (≥0.7) | Full display | Full display | Only if interrupt |
| Medium (0.4-0.7) | Full display | Brief or skip | Skip |
| Low (<0.4) | Full display | Skip | Skip |

```python
def should_display(moment: Moment, speed: str) -> bool:
    if speed == '1x':
        return True

    elif speed == '2x':
        if moment.type == 'dialogue':
            return True
        return moment.weight >= 0.4

    elif speed == '3x':
        return is_interrupt(moment)

    return True
```

---

## Interrupt Conditions

Interrupts trigger auto-pause to 1x.

```python
def is_interrupt(moment: Moment) -> bool:
    """
    Check if moment should interrupt fast-forward.
    """
    # Player character directly addressed
    if player_directly_addressed(moment):
        return True

    # Combat initiated
    if moment.action == 'attack':
        return True

    # Major character arrival
    if is_major_arrival(moment):
        return True

    # Tension threshold crossed
    if tension_boiling_over(moment):
        return True

    # Decision point (player choices available)
    if has_player_choices(moment):
        return True

    # Discovery (new significant narrative)
    if is_significant_discovery(moment):
        return True

    # Danger to player or companions
    if threatens_player_or_companions(moment):
        return True

    return False
```

### Interrupt Definitions (Weight/Link Based)

| Interrupt Type | Definition |
|----------------|------------|
| Direct address | Player character's name in REFERENCES link |
| Combat | Moment with `action: attack` becomes canon |
| Major arrival | Character with importance > 0.7 enters scene |
| Tension boils | Detected tension pressure > 0.9 (computed from structure) |
| Decision point | Moment with multiple CAN_LEAD_TO from player |
| Discovery | Narrative node created with player in ATTACHED_TO |
| Danger | Moment with THREATENS → player or companion |

All weight-based or link-based. No magic.

---

## The Snap — 3x to 1x Transition

When interrupt detected at 3x, the transition is visceral.

```python
async def execute_snap(interrupt_moment: Moment):
    """
    The Snap: transition from 3x to 1x.
    """
    # Phase 1: Running (player sees this already)
    # - Motion blur effect
    # - Muted colors
    # - Text small, streaming upward

    # Phase 2: The Beat (300-500ms)
    await display_freeze()
    await asyncio.sleep(0.4)  # The pause where dread lives

    # Phase 3: Arrival
    set_speed('1x')
    display_moment_vivid(interrupt_moment)
    # - Crystal clear, full color
    # - Large, centered, deliberate
```

### Visual Phases

**Phase 1: Running (3x)**
- Motion blur effect
- Muted colors
- Text small, streaming upward, fading fast
- Sound: whoosh/wind (if audio)

**Phase 2: The Beat**
- Screen sharpens (freeze)
- Silence — 300-500ms pause
- Nothing displays
- Tension in the gap

**Phase 3: Arrival (1x)**
- Crystal clear, full color
- Interrupt moment appears
- Large, centered, deliberate
- Sound: ambient returns

The pause is where dread lives. "Something's happening."

---

## Tick Rate by Speed

```python
def get_tick_interval(speed: str) -> float:
    """
    Seconds between physics ticks.
    """
    if speed == '1x':
        return 5.0  # One tick per ~5 seconds (moment duration)
    elif speed == '2x':
        return 0.5  # Rapid ticks
    elif speed == '3x':
        return 0.0  # As fast as possible

    return 5.0
```

---

## Decay and Speed

Decay is time-based, not tick-based. Speed doesn't change total decay.

```python
def calculate_decay(elapsed_real_time: float) -> float:
    """
    Decay based on real time, not tick count.
    3x doesn't decay faster than 1x.
    """
    return DECAY_RATE * elapsed_real_time
```

At 3x, ticks are faster but decay rate per real-time stays constant. Otherwise 3x would decay everything to zero.

---

## Montage Generation

At 2x, system seeds atmospheric summary moments.

```python
def generate_montage_moments(context: SceneContext):
    """
    Generate brief atmospheric moments for journey feel.
    Called by handlers when speed is 2x.
    """
    montage_options = [
        "The road winds through the valley.",
        "Clouds gather on the horizon.",
        "The sun hangs low.",
        "Birdsong fades as evening approaches.",
    ]

    moment = create_moment(
        text=random.choice(montage_options),
        type='montage',
        weight=0.3,  # Low weight, background
        status='possible'
    )

    return moment
```

Not a separate system. Same handlers, context-aware output. The speed is in the prompt context.

---

## Player Input at Any Speed

```python
def on_player_starts_typing():
    """
    Player began typing. Auto-pause or slow down.
    """
    current = get_current_speed()

    if current in ['2x', '3x']:
        set_speed('1x')  # Or pause
        # Player can resume after input processed
```

- Player can type at any speed
- Typing auto-pauses (or auto-drops to 1x)
- Submit processes normally
- Player chooses to resume / change speed

---

## Canon vs Display

**Canon is canon regardless of display.**

```python
# At 3x, low-weight moments:
# - Actualize in graph ✓
# - Create THEN links ✓
# - Become history ✓
# - Display to player ✗ (filtered)

# Player can review history later
def get_skipped_moments(time_range: TimeRange) -> List[Moment]:
    """
    What happened while I was skipping?
    """
    return query("""
        MATCH (m:Moment)
        WHERE m.status = 'spoken'
          AND m.tick_spoken >= $start
          AND m.tick_spoken <= $end
        RETURN m
        ORDER BY m.tick_spoken
    """, start=time_range.start, end=time_range.end)
```

Speed changes rendering, not reality.

---

## Journey Conversations (2x Pattern)

At 2x, travel compresses but conversation persists.

```
The road stretches. (montage, muted)
"I never told you about my brother." (dialogue, vivid)
The sun sets. (montage, muted)
"What happened?" (dialogue, vivid)
You make camp. (montage, muted)
"The Normans." (dialogue, vivid)
```

Two things at once: travel and intimacy. Like film. A day passes in minutes, but the conversation is whole.

---

## Speed State

```python
@dataclass
class SpeedState:
    current: str  # '1x', '2x', '3x'
    paused: bool
    last_interrupt: Optional[Moment]
    time_at_speed: Dict[str, float]  # Track time spent at each speed

def set_speed(new_speed: str):
    state.current = new_speed
    physics.set_tick_interval(get_tick_interval(new_speed))
    display.set_filter(get_display_filter(new_speed))
```

---

## What Speed Controller Does NOT Do

- Change what happens (only what displays)
- Affect canon (history is complete at any speed)
- Change decay rate (time-based, not tick-based)
- Block physics (graph always runs)

---

## Invariants

1. **Speed doesn't change content:** Same events at any speed
2. **Canon is complete:** All moments recorded regardless of display
3. **Time-based decay:** 3x doesn't decay faster
4. **Interrupts break through:** Critical moments always shown

---

*"The player is a viewer with a remote. Fast-forward through the boring parts."*
