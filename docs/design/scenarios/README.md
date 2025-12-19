# Scenario System

Scenarios define different starting points for playthroughs. Each scenario sets up unique initial conditions — location, companion, things, beliefs, tensions, and opening narrative.

## The Five Scenarios

| ID | Name | Location | Companion | Tone |
|----|------|----------|-----------|------|
| `thornwick_betrayed` | The Burned Home | Thornwick | Aldric (existing) | Revenge |
| `york_anonymous` | The Anonymous | York | Sigewulf (new) | Intrigue |
| `durham_burning` | The Witness | Durham | Ligulf (existing) | Revenge |
| `whitby_sanctuary` | The Penitent | Whitby Abbey | Reinfrid (existing) | Redemption |
| `norman_service` | The Turncoat | York Castle | Cynewise (new) | Infiltration |

---

## Directory Structure

```
scenarios/
├── thornwick_betrayed.yaml   # Revenge - Brother's betrayal
├── york_anonymous.yaml       # Intrigue - Hidden identity
├── durham_burning.yaml       # Revenge - Watching Cumin fall
├── whitby_sanctuary.yaml     # Redemption - Seeking sanctuary
└── norman_service.yaml       # Infiltration - Inside the enemy
```

---

## Scenario YAML Structure

Each scenario file contains:

```yaml
# =============================================================================
# METADATA
# =============================================================================
id: scenario_id
name: "Display Name"
location: place_id
tagline: "One-line hook"
tone: revenge|intrigue|redemption|infiltration

starts_with:
  - "What player starts with (for UI)"

# =============================================================================
# PRE-EXISTING NODES (already in seed - reference only)
# =============================================================================
existing_nodes:
  characters: [char_ids]
  places: [place_ids]
  narratives: [narr_ids]
  tensions: [tension_ids]

# =============================================================================
# NEW NODES (created by this scenario)
# =============================================================================
nodes:
  # Player character
  - type: character
    id: char_player
    # name/gender filled at runtime
    character_type: player
    skills: {...}
    voice: {...}
    personality: {...}
    backstory: {...}

  # Companion (if new)
  - type: character
    id: char_companion
    name: "Name"
    gender: male|female
    character_type: companion
    ...

  # Things
  - type: thing
    id: thing_id
    name: "Name"
    thing_type: weapon|document|token|tool|armor|treasure
    portable: true|false
    significance: mundane|personal|political|sacred
    description: "..."

  # Narratives
  - type: narrative
    id: narr_id
    name: "Name"
    content: "What happened"
    interpretation: "What player believes it means"
    narrative_type: memory|secret|bond|oath|claim|blood|belief|prophecy
    about:
      characters: [...]
      things: [...]
      places: [...]
    tone: bitter|mournful|dark|warm|cold|hopeful|shameful
    focus: 0.1-3.0
    truth: 0-1
    narrator_notes: "For narrator context"

# =============================================================================
# LINKS
# =============================================================================
links:
  # Location
  - type: present
    from: char_player
    to: place_id

  # Things carried
  - type: carries
    from: char_player
    to: thing_id

  - type: carries_hidden
    from: char_player
    to: thing_id

  # Beliefs
  - type: belief
    character: char_player
    narrative: narr_id
    believes: 0-1
    originated: 0-1
    heard: 0-1
    hides: 0-1
    source: witnessed|told|inferred|assumed|rumor

# =============================================================================
# COMPANION
# =============================================================================
companion:
  id: char_id
  relationship: "description"
  why_stays: "Why they follow player"
  starting_disposition: loyal|cautious_loyal|cold_alliance|understanding
  voice_note: "How they speak"

# =============================================================================
# OPENING
# =============================================================================
opening:
  time: dawn|morning|evening|night
  weather: "description"
  place: place_id
  characters_present: [char_ids]
  narration: |
    Multi-line opening narration.
```

---

## Things by Scenario

### Thornwick (4 things)
- `thing_father_ring` - Player carries, identity token
- `thing_mother_brooch` - Player carries, grief (narr_mother_dead)
- `thing_thornwick_charter` - Edmund carries, proof of claim (narr_charter_stolen)
- `thing_aldric_brother_sword` - Aldric carries, his loss

### York (5 things)
- `thing_coin_purse` - Player carries, survival
- `thing_sealed_letter` - Player hidden, treasonous intel (narr_letter_contents)
- `thing_forged_papers` - Player carries, false identity
- `thing_resistance_token` - Player hidden, faction ID (narr_resistance_network)
- `thing_sigewulf_lockpicks` - Sigewulf carries, his trade

### Durham (6 things)
- `thing_family_knife` - Player carries, assassination fantasy (narr_knife_intent)
- `thing_durham_map` - Player carries, intelligence
- `thing_burned_timber` - Player carries, grief token (narr_timber_memory)
- `thing_cumin_tax_writ` - Player carries, evidence (narr_tax_evidence)
- `thing_tinder_box` - Player carries, foreshadowing
- `thing_ligulf_seal` - Ligulf carries, lost authority (narr_ligulf_fall)

### Whitby (6 things)
- `thing_monastery_robe` - Player carries, disguise
- `thing_hidden_sword` - Player hidden, can't let go (narr_sword_kept)
- `thing_victim_ring` - Player hidden, guilt (narr_victim_memory)
- `thing_confession_letter` - Player carries, unwritten (narr_confession_struggle)
- `thing_reinfrid_cross` - Player carries, hope (narr_reinfrid_gift)
- `thing_sanctuary_token` - Player carries, 40-day protection

### Norman Service (6 things)
- `thing_servant_clothes` - Player carries, cover
- `thing_hidden_message` - Player hidden, resistance orders
- `thing_castle_key` - Player carries, access (narr_keys_trust)
- `thing_cynewise_poison` - Cynewise hidden, nuclear option (narr_poison_option)
- `thing_malet_cup` - Located at castle, daily intimacy
- `thing_harold_coin` - Malet hidden, his secret (narr_malet_harold_memory)

---

## Historical Grounding

Each scenario plugs into existing seed data:

### Thornwick
- `char_edmund` - Reeve of Thornwick
- `char_aldric` - Saxon warrior (brother died at Stamford Bridge)
- `tension_thornwick_taxes` - Village hungry
- `tension_aldric_revenge` - Aldric's grudge

### York
- `char_malet` - Sheriff, half-English, buried Harold
- `char_waltheof` - Saxon Earl serving Normans
- `narr_malet_sheriff_york` - Who controls York
- `narr_resistance_forming` - Secret meetings
- `tension_york_whispers` - Resistance brewing
- `tension_malet_identity` - Malet's divided loyalty

### Durham
- `char_cumin` - Robert Cumin, cruel Earl (dies in fire 1069)
- `char_ligulf` - Saxon thegn, organizing resistance
- `char_aethelwine` - Bishop, dreams of freedom
- `tension_cumin_cruelty` (0.65!) - "Durham will burn"
- `tension_aethelwine_resistance` - Church politics

### Whitby
- `char_reinfrid` - Norman knight turned monk (perfect mirror!)
- `narr_reinfrid_penance` - "Saw slaughter at Hastings, took holy orders"
- `tension_reinfrid_guilt` - "Can rebuilding atone?"

### Norman Service
- `char_malet` - Conflicted master
- `narr_malet_buried_harold` - SECRET: He knew Harold
- `tension_malet_identity` - Can he serve harsh orders?
- `tension_waltheof_oath` - Serving two masters

---

## API Endpoint

### POST /api/playthrough/scenario

Creates a new playthrough from a scenario.

**Request:**
```json
{
  "scenario_id": "thornwick_betrayed",
  "player_name": "Wulfric",
  "player_gender": "male"
}
```

**Response:**
```json
{
  "playthrough_id": "pt_a1b2c3d4",
  "scenario": "thornwick_betrayed",
  "player_name": "Wulfric",
  "player_gender": "male",
  "status": "created"
}
```

**What it does:**
1. Creates `playthroughs/{id}/` folder structure
2. Saves `player.yaml` with character info
3. Applies scenario nodes/links/tensions to graph
4. Creates initial `scene.json` from scenario opening

---

## Playthrough Folder Structure

After scenario creation:

```
playthroughs/{playthrough_id}/
├── player.yaml           # Name, gender, scenario, created timestamp
├── scene.json            # Current scene state
├── mutations/            # Applied graph mutations
└── conversations/        # Per-character conversation threads
```

---

## Frontend Flow

1. `/start` — Player enters name, selects gender
2. `/scenarios` — Player chooses starting scenario
3. `POST /api/playthrough/scenario` — Backend creates playthrough
4. `/opening` — Scenario-specific opening scene (optional)
5. `/` — Main game with scene from playthrough

---

## Companions

Every scenario has a companion who stays with the player:

| Scenario | Companion | Source | Relationship |
|----------|-----------|--------|--------------|
| Thornwick | Aldric | Existing seed | Oath-bound protector |
| York | Sigewulf | Created by scenario | Debt-bound guide |
| Durham | Ligulf | Existing seed | Fellow dispossessed |
| Whitby | Reinfrid | Existing seed | Fellow penitent |
| Norman | Cynewise | Created by scenario | Fellow infiltrator |

---

## Adding New Scenarios

1. Create `scenarios/{id}.yaml` with full structure
2. Add entry to `SCENARIOS` array in `frontend/app/scenarios/page.tsx`
3. Ensure all referenced nodes (places, characters) exist in base world data
4. Include at least one companion
5. Connect things to narratives via beliefs
6. Test with:
```bash
curl -X POST http://localhost:8000/api/playthrough/scenario \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "your_id", "player_name": "Test", "player_gender": "male"}'
```

---

## Design Principles

1. **Historical grounding** - Every scenario connects to real 1067 England
2. **Companion required** - UI needs someone to talk to
3. **Things tell stories** - Items connect to narratives and beliefs
4. **Tensions inherited** - Scenarios activate existing world tensions
5. **Truth varies** - Player beliefs may not match reality (truth: 0-1)
6. **Narrator notes** - Guide AI without exposing to player
