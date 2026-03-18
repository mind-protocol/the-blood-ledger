# Tempo Controller — Algorithm

```
CREATED: 2025-12-19
STATUS: SPEC (not implemented)
```

---

## Overview

Tempo Controller manages game speed and the main loop. It determines when ticks run, when moments surface, and when to auto-pause.

**No "Next" button.** Only speed settings.

```
[⏸]  [ 1x 🗣️ ]  [ 2x 🚶 ]  [ 3x ⏩ ]
```

---

## Speed Modes

| Mode | Icon | Feel | Tick Rate | Canon Rate | Display |
|------|------|------|-----------|------------|---------|
| **Pause** | ⏸ | Turn-based | None | On input only | 1 moment then stop |
| **1x** | 🗣️ | Present | Normal (~1/sec) | Continuous | All, until queue > 5 |
| **2x** | 🚶 | Montage | Fast (~5/sec) | Normal for dialogue | Dialogue + high weight |
| **3x** | ⏩ | Skip | Max | Max | Only interrupts |

---

## Pause Mode (⏸)

Player-driven. World waits.

```
Player input → Tick runs → Canon surfaces → 1 moment displays → Stop
```

**Rules:**
- No automatic ticking
- Player click/input triggers exactly ONE tick cycle
- Canon processes ready moments
- First moment (highest salience) displays
- System waits for next player input

**Use case:** Careful play, reading everything, deliberate choices.

---

## 1x Mode (🗣️)

Real-time presence. Every moment breathes.

```
Tick interval (1 sec) → Physics → Canon surfaces → Display all
```

**Rules:**
- Ticks run continuously at ~1 second interval
- All moments display at natural pace
- **Backpressure:** If queued moments > 5, pause ticking until caught up
- Player input injects moment, doesn't interrupt flow

**Use case:** Deep conversation, combat, dramatic scenes.

---

## 2x Mode (🚶)

TV travel speed. World advances fast, conversations persist.

```
Tick interval (0.2 sec) → Physics (fast) → Canon (selective) → Display filtered
```

**Rules:**
- World ticks 5x faster (time passes, travel progresses, energy flows)
- Dialogue moments still render at normal pace
- Action/narration moments compressed or skipped unless high weight
- **Interrupt detection:** If interrupt moment surfaces → snap to 1x

**The TV Effect:**
- Two riders travel for a day
- Player sees: 2-3 conversations + montage moments
- "The road winds through the valley. The sun arcs overhead."
- Feels like: hours pass, but dialogue still has weight

**Display filter at 2x:**
```python
def should_display_2x(moment):
    if moment.type == 'dialogue':
        return True  # Always show dialogue
    if moment.weight > 0.7:
        return True  # High weight actions
    if moment.type == 'montage':
        return True  # Atmospheric summaries
    return False  # Skip low-weight narration
```

**Use case:** Travel, waiting, downtime with character bonding.

---

## 3x Mode (⏩)

Maximum speed until drama demands attention.

```
Tick (max speed) → Physics → Canon → Check interrupt → Display only interrupts
```

**Rules:**
- Ticks run as fast as system can process
- Moments processed but NOT displayed
- Graph updates, time passes, energy flows
- **Only interrupt moments display**
- When interrupt detected → snap to 1x, display interrupt moment

**Visual treatment:**
- Motion blur / muted colors
- Small text streaming upward, fading
- "Time passes... the road stretches..."
- Then: THE SNAP (see below)

**Use case:** "Skip to the siege", long journeys, waiting for specific event.

---

## Interrupt Conditions

These force 3x/2x → 1x:

| Condition | Detection |
|-----------|-----------|
| Player addressed | moment.text contains player name |
| Combat initiated | moment.action == 'attack' or tension.type == 'combat' |
| Major arrival | character with importance > 0.7 enters player location |
| Tension boils over | tension.pressure > breaking_point |
| Decision point | moment has CAN_LEAD_TO links (choices) |
| Discovery | new narrative created with player involvement |
| Danger | threat to player or companion detected |

**Moment property:**
```yaml
Moment:
  interrupt: bool  # Set by narrator or derived from conditions
```

---

## The Snap (3x → 1x)

When interrupt detected at 3x, visceral transition:

**Phase 1: Running**
- Motion blur, muted colors
- Text small, streaming, fading

**Phase 2: The Beat**
- Screen sharpens (freeze)
- Silence — 300-500ms pause
- Nothing displays
- Tension in the gap

**Phase 3: Arrival**
- Crystal clear, full color
- Interrupt moment appears large, centered
- Ambient sound returns

The pause is where dread lives.

---

## Main Loop

```python
class TempoController:
    def __init__(self, playthrough_id: str):
        self.playthrough_id = playthrough_id
        self.speed: Literal['pause', '1x', '2x', '3x'] = '1x'
        self.display_queue: List[Moment] = []
        self.last_tick: float = 0
        self.running: bool = True
        
        # Components
        self.physics = GraphTick(playthrough_id)
        self.canon = CanonHolder(playthrough_id)
    
    async def run(self):
        """Main game loop."""
        while self.running:
            if self.speed == 'pause':
                await self.wait_for_input()
            else:
                await self.tick_continuous()
    
    async def on_player_input(self, text: str):
        """Handle player input at any speed."""
        # Create player moment
        moment_id = self.create_player_moment(text)
        
        if self.speed == 'pause':
            # Tick once, surface one response
            await self.tick_once()
        elif self.speed == '3x':
            # Player input interrupts 3x
            self.speed = '1x'
            broadcast('speed_changed', {'speed': '1x', 'reason': 'player_input'})
    
    async def tick_once(self):
        """Single tick cycle (pause mode)."""
        # Run physics
        self.physics.tick()
        
        # Detect and surface ready moments
        ready = self.detect_ready_moments()
        if ready:
            # Process only first (highest salience)
            moment = ready[0]
            result = self.canon.record_to_canon(moment['id'])
            # SSE broadcast happens inside record_to_canon
    
    async def tick_continuous(self):
        """Continuous ticking (1x/2x/3x)."""
        interval = self.tick_interval()
        
        while self.speed != 'pause' and self.running:
            now = time.time()
            elapsed = now - self.last_tick
            
            if elapsed < interval:
                await asyncio.sleep(0.01)
                continue
            
            self.last_tick = now
            
            # Run physics
            self.physics.tick()
            
            # Detect ready moments
            ready = self.detect_ready_moments()
            
            for moment in ready[:MAX_MOMENTS_PER_TICK]:
                # Record to canon
                result = self.canon.record_to_canon(moment['id'])
                
                if result.get('status') != 'ok':
                    continue
                
                # Check interrupt
                if self.check_interrupt(moment):
                    self.speed = '1x'
                    broadcast('speed_changed', {'speed': '1x', 'reason': 'interrupt'})
                    return  # Exit to main loop
                
                # At 2x/3x, SSE still fires but frontend filters display
            
            # Backpressure at 1x
            if self.speed == '1x':
                queue_size = self.get_display_queue_size()
                if queue_size > 5:
                    await asyncio.sleep(1.0)  # Let frontend catch up
    
    def tick_interval(self) -> float:
        return {
            'pause': float('inf'),
            '1x': 1.0,
            '2x': 0.2,
            '3x': 0.01  # Near-instant
        }[self.speed]
    
    def detect_ready_moments(self) -> List[Dict]:
        """Q1 + Q2: Find moments ready to surface."""
        # Salience threshold check
        cypher = """
        MATCH (m:Moment)
        WHERE m.status = 'possible'
          AND (m.weight * m.energy) >= 0.3
        RETURN m.id, m.weight, m.energy, m.type, m.text, m.interrupt
        ORDER BY (m.weight * m.energy) DESC
        """
        candidates = self.query(cypher)
        
        # Filter by presence requirements
        ready = []
        player_location = self.get_player_location()
        
        for m in candidates:
            if self.check_presence(m['m.id'], player_location):
                ready.append({
                    'id': m['m.id'],
                    'weight': m['m.weight'],
                    'energy': m['m.energy'],
                    'type': m['m.type'],
                    'text': m['m.text'],
                    'interrupt': m['m.interrupt']
                })
        
        return ready
    
    def check_interrupt(self, moment: Dict) -> bool:
        """Check if moment should interrupt 2x/3x."""
        if self.speed == '1x':
            return False  # Already at 1x
        
        if moment.get('interrupt'):
            return True
        
        # Additional interrupt detection
        # (Could check for combat, arrivals, etc.)
        
        return False
```

---

## SSE Events

| Event | When | Payload |
|-------|------|---------|
| `moment_spoken` | Canon records moment | `{moment_id, text, speaker, tick, type}` |
| `speed_changed` | Speed changes | `{speed, reason}` |

**Frontend filters display based on current speed:**
```typescript
function shouldDisplay(moment: Moment, speed: Speed): boolean {
  if (speed === 'pause' || speed === '1x') return true;
  if (speed === '2x') {
    return moment.type === 'dialogue' || moment.weight > 0.7;
  }
  if (speed === '3x') {
    return moment.interrupt === true;
  }
  return true;
}
```

---

## API Endpoints

### Set Speed

```
POST /api/tempo/speed
Body: { "playthrough_id": "...", "speed": "1x" }
Response: { "status": "ok", "speed": "1x" }
```

### Get State

```
GET /api/tempo/{playthrough_id}
Response: { 
  "speed": "1x", 
  "queue_length": 3,
  "tick": 1542,
  "running": true
}
```

### Player Input

```
POST /api/tempo/input
Body: { "playthrough_id": "...", "text": "I look around" }
Response: { "status": "ok", "moment_id": "mom_xxx" }
```

---

## Startup / Shutdown

```python
# On playthrough start
tempo = TempoController(playthrough_id)
asyncio.create_task(tempo.run())

# On playthrough end / disconnect
tempo.running = False
```

**Per-playthrough:** Each playthrough has its own TempoController instance.

---

## Integration Points

| Component | How Tempo Uses It |
|-----------|-------------------|
| `GraphTick` | Calls `tick()` for physics simulation |
| `CanonHolder` | Calls `record_to_canon()` for surfacing |
| `GraphQueries` | Q1, Q2 for detecting ready moments (ngram repo runtime) |
| `SSE Broadcast` | Sends events to frontend |
| Frontend | Speed selector, display filtering |

---

## Chain

```
PATTERNS:        ./PATTERNS_Tempo.md
BEHAVIORS:       ./BEHAVIORS_Tempo.md
THIS:            ALGORITHM_Tempo_Controller.md
VALIDATION:      ./VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
TEST:            ./TEST_Tempo.md
SYNC:            ./SYNC_Tempo.md
```

---

## Gaps / Questions

- QUESTION: Should pause mode show ALL ready moments or just highest salience? → Just highest (one response)
- QUESTION: At 2x, should montage moments be auto-generated or pre-authored?
- QUESTION: How does narrator get called? Separate citizen_think loop or on-demand?
- IDEA: "Rewind" feature at 3x to see what was skipped
- IDEA: Sound design cues for speed transitions

---

## Future UI: Minimap + Sun Arc

At 2x/3x speeds, emphasize passage of time visually:

**Minimap expansion:**
- At 1x: normal minimap size
- At 2x: minimap grows ~1.5x, becomes focal point
- At 3x: minimap dominates right panel, text fades

**Sun arc display:**
- Arc over minimap showing sun position
- Sun moves along arc as ticks advance
- Dawn → noon → dusk → night cycle visible
- At 3x, sun visibly racing across sky

```
        ☀️
      ╭───╮
     ╱     ╲
    ╱       ╲
   ●─────────●
   dawn    dusk

   [  MINIMAP  ]
```

**Implementation notes:**
- 1 tick = 5 minutes of world time
- Day = 288 ticks (24 hours)
- Sun position = (world_tick % 288) / 288
- Frontend calculates arc position from tempo state tick count
- Sun arc rendering lives in `frontend/components/minimap/SunArc.tsx`
