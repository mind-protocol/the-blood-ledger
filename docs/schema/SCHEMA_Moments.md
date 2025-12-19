# Moments — Schema Reference

```
STATUS: CANONICAL
UPDATED: 2024-12-18
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
ALGORITHMS:  ./ALGORITHM_Physics.md
THIS:        SCHEMA_Moments.md (you are here)
API:         ./API_Physics.md
VALIDATION:  ./VALIDATION_Moments.md
TEST:        ./TEST_Moments.md
SYNC:        ./SYNC_Physics.md
IMPL:        ../../engine/db/graph_ops.py
```

---

## How This Document Works

Each node and link includes:
- **Purpose:** Why it exists
- **When to create:** What triggers its creation
- **How to fill:** What goes in each field
- **How to link:** What connections to make

---

# NODES

---

## CHARACTER

**Purpose:** Represents any entity that can speak, act, witness, or be spoken about. The anchor for identity, memory, and relationship.

**When to create:**
- Story requires a named person
- Group needs representation ("The Guards")
- Player character at game start

**How to fill:**

```yaml
id: string          # Unique. Pattern: char_{name_slug}
name: string        # Display name: "Aldric" or "The Guards"
type: string        # See type table below
gender: string      # female | male — affects pronouns in generation
alive: boolean      # Dead characters can still be referenced, just can't act
state: string       # awake | sleeping | unconscious | dead — affects pump rate (see ALGORITHM_Physics.md (Energy Mechanics section))
weight: float       # Importance to story (0.01 - 1.0). Slow, event-driven. (see ALGORITHM_Physics.md (Energy Mechanics section))
energy: float       # Current activation (0.01 - 10.0). Pumps into believed narratives. (see ALGORITHM_Physics.md (Energy Mechanics section))
```

| Type | When to use |
|------|-------------|
| `player` | The player character (exactly one) |
| `companion` | Travels with player, full handler |
| `major` | Plot-critical NPC, full handler |
| `minor` | Named but less important, light handler |
| `background` | Shopkeepers, peasants — minimal handler |
| `group` | Multiple individuals as one ("The Guards") |

```yaml
# For type: group
count: integer      # How many individuals
split_from: string  # If split from parent group, reference parent id

# Identity (optional, enriches handler context)
face: string        # Visual: young, scarred, weathered, gaunt, hard, noble
voice: { tone, style }  # How they speak: "gruff, short sentences"
personality: { approach, values[], flaw }
backstory: { family, childhood, wound, why_here }
skills: { fighting, tracking, healing, persuading, sneaking, riding, reading, leading }

modifiers: []       # Current states: wounded, hungry, inspired
detail: string      # Extended description for rich generation
image_prompt: string
```

**How to link:**

| Link | When |
|------|------|
| `CHARACTER -[AT]-> PLACE` | Always. Every character is somewhere. |
| `CHARACTER -[BELIEVES]-> NARRATIVE` | When they know/believe something |
| `CHARACTER -[CARRIES]-> THING` | When they possess something |
| `CHARACTER -[CAN_SPEAK]-> MOMENT` | When they could say this moment |

**Note:** "Importance" is derived from attached moments, not stored.

---

## PLACE

**Purpose:** A location where things happen. Anchor for scenes, atmosphere, and spatial relationships.

**When to create:**
- Story needs a location
- Characters need somewhere to be
- Scene needs atmosphere context

**How to fill:**

```yaml
id: string          # Unique. Pattern: place_{name_slug}
name: string        # Display name: "York Market"
historical_name: string  # Period-accurate: "Jorvik"
type: string        # region, city, hold, village, monastery, camp, road, room, wilderness, ruin
scale: string       # Determines movement rules (see table)
coordinates: [lat, lng]  # Real geography if applicable
atmosphere: {
  weather: [],      # rain, snow, fog, clear, cold, hot
  mood: string,     # tense, peaceful, foreboding, bustling
  details: []       # "merchants hawking", "mud underfoot"
}
modifiers: []       # besieged, burning, abandoned
detail: string
image_prompt: string
```

| Scale | Movement within | Movement out |
|-------|-----------------|--------------|
| `room` | Instant | To building: ~1 min |
| `building` | ~1 min between rooms | To district: ~5 min |
| `district` | ~5 min between buildings | To settlement: ~15 min |
| `settlement` | ~15 min between districts | Needs ROUTE |
| `region` | Needs ROUTE | Needs ROUTE |

**How to link:**

| Link | When |
|------|------|
| `PLACE -[CONTAINS]-> PLACE` | Hierarchy: York CONTAINS York_Market CONTAINS Merchant_Stall |
| `PLACE -[ROUTE]-> PLACE` | Travel between settlements/regions |

---

## THING

**Purpose:** Objects that can be possessed, used, fought over, or referenced. Anchors for ownership conflict and physical interaction.

**When to create:**
- Object is narratively significant
- Ownership matters
- Can be taken, given, or used

**How to fill:**

```yaml
id: string          # Unique. Pattern: thing_{name_slug}
name: string        # Display name: "Father's Sword"
type: string        # weapon, armor, document, letter, relic, treasure, title, land, token, provisions, coin_purse, horse, ship, tool
portable: boolean   # Can it be carried? (land = false)
significance: string  # mundane, personal, political, sacred, legendary
quantity: integer   # For countable things (coins, arrows)
description: string # What it looks like, feels like
modifiers: []       # damaged, bloodstained, glowing
detail: string
image_prompt: string
```

**How to link:**

| Link | When |
|------|------|
| `THING -[AT]-> PLACE` | Thing is at a location (not carried) |
| `CHARACTER -[CARRIES]-> THING` | Character has it |
| `MOMENT -[TARGETS]-> THING` | Action targets this thing |

---

## NARRATIVE

**Purpose:** A piece of story that can be believed, doubted, spread, or contested. The substrate of memory, reputation, and conflict. NOT moments — narratives are what moments are ABOUT.

**When to create:**
- Fact or rumor exists in the world
- Relationship needs representation
- Something happened that characters can remember/discuss
- Pattern detection finds recurring theme across moments

**How to fill:**

```yaml
id: string          # Unique. Pattern: narr_{summary_slug}
name: string        # Short label: "Aldric's Betrayal"
content: string     # What happened/is believed: "Aldric betrayed his lord at Stamford"
interpretation: string  # What it means: "Aldric cannot be trusted"
type: string        # See type table
about: {            # What nodes this narrative concerns
  characters: [],
  places: [],
  things: [],
  relationships: []  # char_id pairs
}
tone: string        # bitter, proud, shameful, defiant, mournful, cold, righteous, hopeful, fearful, warm, dark, sacred
weight: float       # Importance over time (0.01 - 1.0). Slow, reinforced by use. (see ALGORITHM_Physics.md (Energy Mechanics section))
energy: float       # Current activation (0.01 - 5.0). Receives from believers, transfers via links. (see ALGORITHM_Physics.md (Energy Mechanics section))
focus: float        # 0.1-3.0, how much attention narrator gives this
truth: float        # 0-1, director's knowledge of actual truth
narrator_notes: string  # Guidance for generation
occurred_at: string # When: "Day 12, dawn"
detail: string

# Tension detection fields (tension is computed, not stored)
visibility: string  # public | secret | known_to_few — for secret detection
deadline: datetime  # When this must resolve — for deadline detection
conditions: string[]  # For oaths: conditions that trigger obligation
```

| Type | What it represents |
|------|-------------------|
| `memory` | Character's personal recollection |
| `account` | Witnessed/reported event |
| `rumor` | Unverified information spreading |
| `reputation` | What people think of someone |
| `identity` | Who someone is / sees themselves as |
| `bond` | Positive relationship |
| `oath` | Promise or commitment |
| `debt` | Obligation owed |
| `blood` | Family relationship |
| `enmity` | Hostile relationship |
| `love` | Romantic/deep affection |
| `service` | Loyalty/employment relationship |
| `ownership` | Who owns what |
| `claim` | Disputed ownership/right |
| `control` | Who controls what/whom |
| `origin` | Backstory, where something came from |
| `belief` | Religious/philosophical conviction |
| `prophecy` | Prediction about the future |
| `lie` | Known falsehood |
| `secret` | Hidden truth |

**How to link:**

| Link | When |
|------|------|
| `NARRATIVE -[OCCURRED_AT]-> PLACE` | Where it happened |
| `NARRATIVE -[FROM]-> MOMENT` | Moments that established/support this |
| `NARRATIVE -[CONTRADICTS]-> NARRATIVE` | Two stories conflict |
| `NARRATIVE -[SUPPORTS]-> NARRATIVE` | One reinforces another |
| `CHARACTER -[BELIEVES]-> NARRATIVE` | Character knows/believes this |

---

## MOMENT

**Purpose:** A single piece of content that can be shown to the player. The atomic unit of the game. Everything displayed is a moment.

**When to create:**
- Character handler generates potential dialogue/thought/action
- Player provides input
- Narrator describes scene
- System generates montage (2x speed)

**How to fill:**

```yaml
id: string          # Pattern: {place}_{day}_{time}_{type}_{random}
text: string        # The actual content shown to player
type: string        # See type table
status: string      # See status flow below
weight: float       # Importance over time (0.01 - 1.0). Slow, reinforced by use. (see ALGORITHM_Physics.md (Energy Mechanics section))
energy: float       # Current activation (0.01 - 5.0). Flow-driven. salience = weight × energy. (see ALGORITHM_Physics.md (Energy Mechanics section))
tone: string        # curious, defiant, warm, cold, tense, vulnerable
duration: integer   # Time units this takes (for time passage)
tick_created: integer
tick_spoken: integer
tick_decayed: integer
line: integer       # Position in transcript (for spoken)
embedding: float[]  # 768-dim vector for semantic matching
```

Note: `speaker` is derived from the `SAID` link and can appear in responses or in-memory models,
but it is not stored as a Moment attribute. Legacy inputs may provide `tick` as an alias for
`tick_created`.

| Type | Purpose | Has action? |
|------|---------|-------------|
| `narration` | Describes world, scene, action result | No |
| `dialogue` | Character speaks aloud | No |
| `thought` | Character's internal moment | No |
| `action` | Character does something that changes world | Yes |
| `montage` | Atmospheric summary for 2x speed | No |
| `hint` | System guidance to player | No |
| `player_click` | Player clicked a word | No |
| `player_freeform` | Player typed something | No |
| `player_choice` | Player selected option | No |

**For action moments:**

```yaml
action: string      # travel, attack, take, give, use
# Target is expressed via TARGETS link
```

**For query moments (handler asking Question Answerer):**

```yaml
query: string       # "Who is my father?"
query_type: string  # backstory_gap, world_fact, relationship
query_filled: boolean  # True when answered
```

**Status flow:**

```
possible ─────→ active ─────→ spoken
   │        (surfaced)       (canon)
   │
   ├──→ dormant (player left, persistent=true)
   │       │
   │       └──→ possible (player returned)
   │
   └──→ decayed (pruned)
```

**How to link:**

| Link | When | Required? |
|------|------|-----------|
| `CHARACTER -[CAN_SPEAK]-> MOMENT` | Who could speak this | Yes for dialogue/thought |
| `MOMENT -[ATTACHED_TO]-> Target` | What it's bound to (visibility) | Yes |
| `MOMENT -[CAN_LEAD_TO]-> MOMENT` | Conversation transitions | If transitions exist |
| `MOMENT -[THEN]-> MOMENT` | History chain | Created by Canon Holder |
| `MOMENT -[REFERENCES]-> Target` | Named nodes in text | Created on parse |
| `MOMENT -[TARGETS]-> Target` | Action target | For action moments |
| `MOMENT -[AT]-> PLACE` | Where it occurred | Yes |
| `MOMENT -[THREATENS]-> CHARACTER` | Danger indication | If threatening |
| `MOMENT -[ANSWERED_BY]-> Node` | Question → answer | For query moments |

---

# LINKS

---

## Character Links

### CHARACTER -[AT]-> PLACE

**Purpose:** Where the character physically is. Required for every character.

**When to create:** Always. Update when character moves.

```yaml
present: float      # 1 = here now, 0 = was here
visible: float      # 1 = can be seen, 0 = hiding
traveling_to: string  # place_id if en route
travel_progress: float  # 0-1
travel_eta_hours: float
detail: string
```

---

### CHARACTER -[BELIEVES]-> NARRATIVE

**Purpose:** What a character knows, believes, or has heard. The substrate of conversation and conflict. **Energy pump:** Characters inject energy into narratives via this link (see ALGORITHM_Physics.md (Energy Mechanics section)).

**When to create:** When character learns/hears/believes something.

```yaml
# Energy mechanics
strength: float     # 0-1, affects energy transfer rate
role: string        # creditor, debtor, witness, etc. — semantic for tension detection

# Knowledge state (how much they know/believe)
heard: float        # 0-1, have they heard this?
believes: float     # 0-1, do they believe it?
doubts: float       # 0-1, do they doubt it?
denies: float       # 0-1, do they deny it?

# Action state (what they do with it)
hides: float        # 0-1, are they concealing it?
spreads: float      # 0-1, are they telling others?
originated: float   # 0-1, did they create this narrative? (1.5x energy pump)

# Provenance
source: string      # witnessed, told, inferred, assumed, taught
from_whom: string   # character_id if source=told
when: datetime
where: string       # place_id where they learned
detail: string
```

---

### CHARACTER -[CARRIES]-> THING

**Purpose:** Possession. What the character has on them.

```yaml
carries: float      # 1 = has it
carries_hidden: float  # 1 = concealed
detail: string
```

---

### CHARACTER -[CAN_SPEAK]-> MOMENT

**Purpose:** Who could speak this moment. Multiple characters can have CAN_SPEAK to same moment; highest weight present character speaks. **Weight contribution:** Character energy flows into moment weight (see ALGORITHM_Physics.md (Energy Mechanics section)).

**When to create:** Handler generates moment for character.

```yaml
strength: float     # 0-1, affects weight contribution from character energy
```

---

## Place Links

### PLACE -[CONTAINS]-> PLACE

**Purpose:** Spatial hierarchy. York contains York_Market contains Merchant_Stall.

**When to create:** Defining location structure.

```yaml
# No attributes — relationship is binary
```

---

### PLACE -[ROUTE]-> PLACE

**Purpose:** Travel connection between settlements/regions. Not needed within same scale.

**When to create:** Connecting locations that require travel.

```yaml
waypoints: float[][]  # [[lat, lng], ...] — actual geography
road_type: string     # roman, track, path, river, none
distance_km: float    # Computed from waypoints
travel_minutes: int   # Computed from distance + road_type
difficulty: string    # easy, moderate, hard, dangerous
detail: string        # "Crosses marshland near Humber"
```

| Road type | Speed (km/h on foot) |
|-----------|---------------------|
| roman | 5.0 |
| track | 3.5 |
| path | 2.5 |
| river | 8.0 (downstream) |
| none | 1.5 (cross-country) |

---

## Thing Links

### THING -[AT]-> PLACE

**Purpose:** Where the thing is (when not carried).

```yaml
located: float      # 1 = here
hidden: float       # 1 = concealed
specific_location: string  # "under the floorboards"
detail: string
```

---

## Narrative Links

### NARRATIVE -[OCCURRED_AT]-> PLACE

**Purpose:** Where the narrative event happened.

```yaml
# No attributes — just the connection
```

---

### NARRATIVE -[ABOUT]-> CHARACTER | PLACE | THING

**Purpose:** What the narrative concerns. Focal point for energy — subjects pull energy from narratives about them (see ALGORITHM_Physics.md (Energy Mechanics section)).

**When to create:** When narrative references specific entities. Can be derived from `about` field on Narrative node.

```yaml
strength: float     # 0-1, how central is this entity to the narrative
role: string        # subject, location, object — semantic context
```

**Energy flow:** Reverse direction. Subject pulls from narrative (being talked about energizes you).

---

### NARRATIVE -[FROM]-> MOMENT

**Purpose:** Which moments established or support this narrative. Provenance.

**When to create:** Pattern detection creates narrative from moments. Or moment explicitly establishes narrative.

```yaml
# No attributes — traces source
```

---

### NARRATIVE -[CONTRADICTS/SUPPORTS/ELABORATES/SUBSUMES/SUPERSEDES]-> NARRATIVE

**Purpose:** How narratives relate to each other. **Energy routing:** These links transfer energy between narratives (see ALGORITHM_Physics.md (Energy Mechanics section)).

```yaml
strength: float     # 0-1, affects energy transfer rate
detail: string
```

**Energy flow by type:**

| Link | Direction | Factor | Behavior |
|------|-----------|--------|----------|
| CONTRADICTS | Bidirectional | 0.15×2 | Both pull from each other — arguments heat both sides |
| SUPPORTS | Equilibrating | 0.10 | Energy flows toward balance — allies share fate |
| ELABORATES | Parent → Child | 0.15 | Details inherit from source |
| SUBSUMES | Specific → General | 0.10 | Many specifics feed one generalization |
| SUPERSEDES | Old → New + drain | 0.25 | New truth drains old — replacement is decisive |

---

## Moment Links

### MOMENT -[ATTACHED_TO]-> CHARACTER | PLACE | THING | NARRATIVE

**Purpose:** What the moment is bound to. Determines visibility. **Weight contribution:** Target's energy flows into moment weight (see ALGORITHM_Physics.md (Energy Mechanics section)).

**When to create:** Every moment must attach to at least one node.

```yaml
strength: float             # 0-1, affects weight contribution
presence_required: boolean  # If true, target must be present for moment to be visible
persistent: boolean         # If true, goes dormant (not deleted) when player leaves
dies_with_target: boolean   # If true, delete moment when target is deleted
```

---

### MOMENT -[CAN_LEAD_TO]-> MOMENT

**Purpose:** Conversation transitions. What this moment can lead to.

**When to create:** Designing conversation flow, or handler generates connected moments.

```yaml
trigger: string     # "click", "wait", "auto"
require_words: string[]  # For trigger="click", words that activate
weight_transfer: float   # How much weight flows to target (default: 0.3)
wait_ticks: integer      # For trigger="wait"
bidirectional: boolean   # Create reverse link too
consumes_origin: boolean # If true, origin → spoken after traversal
```

| Trigger | Behavior |
|---------|----------|
| `click` | Player clicks one of require_words |
| `wait` | wait_ticks pass without player input |
| `auto` | Fires immediately after origin |

---

### MOMENT -[THEN]-> MOMENT

**Purpose:** History. What actually happened, in order. Created by Canon Holder, never manually.

**When to create:** Canon Holder records moment as spoken.

```yaml
tick: integer       # When this link was created
player_caused: boolean  # Player triggered (click/type) vs system (wait/auto)
```

**Query pattern:** `MATCH (m1)-[:THEN*]->(m2)` for conversation history.

---

### MOMENT -[REFERENCES]-> CHARACTER | PLACE | THING

**Purpose:** Node detection. When a moment mentions a node by name.

**When to create:** Parse moment text for node names on creation.

```yaml
strength: float     # 1.0 = direct address ("Aldric, what...")
                    # 0.5 = mention ("...like Aldric said")
```

---

### MOMENT -[TARGETS]-> CHARACTER | PLACE | THING

**Purpose:** Action target. What the action affects.

**When to create:** For moments with `action` field set.

```yaml
# No attributes — the link itself indicates target
```

| Action | Target type |
|--------|-------------|
| travel | PLACE |
| attack | CHARACTER |
| take | THING |
| give | CHARACTER (recipient) + THING via separate link |
| use | THING |

---

### MOMENT -[ANSWERED_BY]-> MOMENT | NARRATIVE | CHARACTER

**Purpose:** Links question moment to its answer. Provenance for Question Answerer output.

**When to create:** Question Answerer completes, creates answer nodes.

```yaml
tick: integer       # When answer was generated
```

---

### MOMENT -[THREATENS]-> CHARACTER

**Purpose:** Indicates danger. Interrupt condition — triggers auto-pause to 1x.

**When to create:** Moment represents threat to character.

```yaml
threat_type: string  # physical, social, emotional
severity: float      # 0-1
```

---

### MOMENT -[AT]-> PLACE

**Purpose:** Where moment occurred. For history queries.

**When to create:** Every moment needs a location.

```yaml
# No attributes
```

---

# EXAMPLE: Creating a Scene

```cypher
// 1. Create place
CREATE (camp:Place {
  id: "place_camp_riverside",
  name: "Riverside Camp",
  type: "camp",
  scale: "building",
  atmosphere: { mood: "tense", weather: ["cold"], details: ["dying fire", "nervous horses"] }
})

// 2. Create characters
CREATE (aldric:Character {
  id: "char_aldric",
  name: "Aldric",
  type: "companion",
  voice: { tone: "weary", style: "direct" }
})

CREATE (player:Character {
  id: "char_player",
  name: "You",
  type: "player"
})

// 3. Place characters
CREATE (aldric)-[:AT {present: 1, visible: 1}]->(camp)
CREATE (player)-[:AT {present: 1, visible: 1}]->(camp)

// 4. Create potential moment
CREATE (m:Moment {
  id: "camp_d1_dusk_dialogue_001",
  text: "We should talk about what happened at the crossing.",
  type: "dialogue",
  status: "possible",
  weight: 0.5,
  tone: "tense"
})

// 5. Link moment
CREATE (aldric)-[:CAN_SPEAK {weight: 0.8}]->(m)
CREATE (m)-[:ATTACHED_TO {presence_required: true, persistent: true}]->(aldric)
CREATE (m)-[:ATTACHED_TO {presence_required: true}]->(camp)
CREATE (m)-[:AT]->(camp)
```

---

*"Everything is in the graph. Query it. Link it. Let it speak."*
