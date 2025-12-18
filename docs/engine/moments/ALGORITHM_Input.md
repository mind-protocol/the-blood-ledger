# Moments — Algorithm: Player Input Processing

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_Input.md (you are here)
ALGORITHMS:  ./ALGORITHM_Physics.md, ./ALGORITHM_Canon.md
SCHEMA:      ./SCHEMA_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
TEST:        ./TEST_Moments.md
IMPL:        ../../engine/input/input_processor.py
```

---

## Core Principle

**Player input is a perturbation, not an ignition.**

The graph is already running. Player input adds energy. Energy propagates. Things flip. This is not "starting a cascade" — it's perturbing a living system.

---

## Input Flow

```
Player submits text
    ↓
[SEQUENTIAL] Parse, create moment, link, inject
    ↓
[PHYSICS] Energy spreads through links
    ↓
[PHYSICS] Tick detects flips
    ↓
[CANON] Records, emits to display
    ↓
[PARALLEL] Character handlers triggered
```

---

## Step 1: Parse

Extract references from input text (names, places, things).

```python
def parse_input(text: str, context: SceneContext) -> ParseResult:
    """
    Extract references (names, places, things).
    UI may have already assisted with autocomplete.
    """
    references = []

    # Character names
    for char in context.present_characters:
        if char.name.lower() in text.lower():
            references.append(Reference(type='character', id=char.id, name=char.name))
        # Also check nicknames, titles
        for alias in char.aliases:
            if alias.lower() in text.lower():
                references.append(Reference(type='character', id=char.id, name=alias))

    # Place names
    if context.location.name.lower() in text.lower():
        references.append(Reference(type='place', id=context.location.id, name=context.location.name))

    # Thing names
    for thing in context.visible_things:
        if thing.name.lower() in text.lower():
            references.append(Reference(type='thing', id=thing.id, name=thing.name))

    return ParseResult(text=text, references=references)
```

### UI-Assisted Recognition

Recognition happens at input time, not query time.

```
Player types: "Al"
    ↓
UI shows dropdown: "Aldric"
    ↓
Player selects
    ↓
Text shows: "Aldric" (highlighted)
    ↓
Reference already recognized before submit
```

Direct address strengthens the energy link. "Aldric, what do you think?" hits harder than "What does everyone think?"

---

## Step 2: Create Moment

Create a moment node for the player's input.

```python
def create_player_moment(parsed: ParseResult, player: Character, location: Place) -> Moment:
    """
    Create moment for player's speech.
    """
    moment_id = generate_id('moment')

    query("""
        CREATE (m:Moment {
            id: $id,
            text: $text,
            type: 'dialogue',
            status: 'spoken',
            weight: 1.0,
            tick_created: $tick,
            tick_spoken: $tick
        })
    """, id=moment_id, text=parsed.text, tick=current_tick())

    return get_moment(moment_id)
```

Player moments are immediately `spoken` (canon). They're not potentials — the player said them.

---

## Step 3: Create Links

Link the moment to relevant nodes.

```python
def create_input_links(moment: Moment, parsed: ParseResult, context: SceneContext):
    """
    Create links from player moment to relevant nodes.
    """
    # ATTACHED_TO player (they said it)
    create_link('ATTACHED_TO', moment.id, context.player.id, {
        'presence_required': False,
        'persistent': True
    })

    # ATTACHED_TO current location
    create_link('ATTACHED_TO', moment.id, context.location.id, {
        'presence_required': False,
        'persistent': True
    })

    # ATTACHED_TO all present characters (they heard it)
    for char in context.present_characters:
        create_link('ATTACHED_TO', moment.id, char.id, {
            'presence_required': False,
            'persistent': True
        })

    # REFERENCES for recognized names/things (strong energy transfer)
    for ref in parsed.references:
        create_link('REFERENCES', moment.id, ref.id, {
            'weight': 1.0  # Direct reference = strong link
        })

    # CAN_SPEAK link (player spoke this)
    create_link('CAN_SPEAK', context.player.id, moment.id, {
        'weight': 1.0
    })
```

---

## Step 4: Inject Energy

Add energy to the system based on input.

```python
def inject_input_energy(moment: Moment, parsed: ParseResult, context: SceneContext):
    """
    Player input injects energy. Referenced nodes receive based on strength.
    """
    base_energy = INPUT_ENERGY_BASE  # e.g., 0.5

    # Direct references get full energy
    for ref in parsed.references:
        if ref.type == 'character':
            # Boost all moments attached to this character
            query("""
                MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
                WHERE m.status = 'possible'
                SET m.weight = m.weight + $energy
            """, char_id=ref.id, energy=base_energy)

    # All present characters get partial energy (they heard)
    for char in context.present_characters:
        if char.id not in [r.id for r in parsed.references]:
            query("""
                MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
                WHERE m.status = 'possible'
                SET m.weight = m.weight + $energy
            """, char_id=char.id, energy=base_energy * 0.3)
```

### Names Have Power

```python
# "Aldric, what do you think?"
# Aldric directly referenced → full energy boost

# "What does everyone think?"
# No direct reference → distributed partial energy
```

Direct address targets energy. Indirect speech diffuses it.

---

## Step 5: Trigger Physics

After injection, physics takes over.

```python
def process_input(text: str):
    """
    Full input processing pipeline.
    """
    context = get_current_scene_context()

    # 1. Parse
    parsed = parse_input(text, context)

    # 2. Create moment
    moment = create_player_moment(parsed, context.player, context.location)

    # 3. Create links
    create_input_links(moment, parsed, context)

    # 4. Inject energy
    inject_input_energy(moment, parsed, context)

    # 5. Emit player moment to display (immediate)
    display_queue.add(moment)

    # 6. Trigger physics tick (may be immediate based on settings)
    physics.tick()

    return moment
```

---

## Energy Must Land

When energy enters, it must go somewhere.

```python
def ensure_energy_lands(context: SceneContext):
    """
    If no moments flip after input, energy returns to player character.
    Player character always has a handler → something always happens.
    """
    # After physics tick, check if anything flipped
    if not any_moments_flipped():
        # No response from NPCs
        # Energy flows back to player character
        player_fallback_energy = FALLBACK_ENERGY

        query("""
            MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $player_id})
            WHERE m.status = 'possible'
            SET m.weight = m.weight + $energy
        """, player_id=context.player.id, energy=player_fallback_energy)

        # Player character's handler will produce observation
        # "The silence stretches. No one meets your eye."
```

There is no "nothing happens." There is only "the silence stretches."

---

## Auto-Pause on Input

At any speed, typing auto-pauses or auto-drops to 1x.

```python
def on_input_start():
    """
    Player began typing. Pause or slow down.
    """
    if current_speed() in ['2x', '3x']:
        set_speed('1x')
        # Or: pause until submit
```

Player can resume speed after input processed.

---

## What Input Processing Does NOT Do

- Generate NPC responses (that's Handlers)
- Decide what happens (that's Physics + Canon)
- Block on LLM (input creates moment immediately)

---

## Invariants

1. **Immediate moment creation:** Player input becomes moment instantly
2. **Energy injection:** Input always adds energy to system
3. **Something happens:** Energy must land somewhere (player fallback)
4. **Direct address matters:** Named references get more energy

---

*"Player input is a perturbation, not an ignition."*
