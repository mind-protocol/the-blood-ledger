# THE BLOOD LEDGER — Complete Schema
# Version: 5.1

---

# =============================================================================
# PHILOSOPHY
# =============================================================================

# The Core Insight
# ----------------
# The game is a web of narratives under tension, not a simulation of characters.
# We simulate STORIES — narratives that exist, connect, contradict, and break.
# Characters are how stories express themselves.
#
# This matters because:
# - Relationships become real: Not "trust: 0.65" but "the oath he swore,
#   the doubt seeded when he heard Edmund's version, the loyalty tested."
# - Memory becomes structural: The graph remembers. That promise in hour one
#   is a narrative with weight — it will speak when relevant, break when pressured.
# - Consequences become inevitable: Tension accumulates. What cannot hold, breaks.

principles:
  graph:
    - "Nodes are things that EXIST"
    - "Narratives are stories about nodes"
    - "Relationships ARE narratives — there is no separate relationship state"
    - "Characters never see truth — they believe narratives"
    - "Physical state is ground truth — presence, possession, location"
    - "Everything else is story"

  experience:
    - "Weight over equality — high-weight narratives speak louder, break sooner"
    - "Uncertainty over omniscience — the player's beliefs may be wrong"
    - "Emergence over scripting — events come from tension, not triggers"
    - "Specificity over genericity — THIS character, THIS place, THIS moment"

  dynamics:
    - "Time passes → pressure accumulates → tensions break → consequences emerge"
    - "Beliefs spread through proximity and trust"
    - "Contradicting narratives under pressure MUST eventually resolve"
    - "The world moves without the player — they are not the center"

# =============================================================================
# NODES (4 Types)
# =============================================================================

nodes:

  # ---------------------------------------------------------------------------
  # CHARACTER
  # ---------------------------------------------------------------------------

  character:
    title: "CHARACTER — A person who exists in the world, with voice, history, and agency"
    description: "Anyone who can act, speak, remember, die"

    # -------------------------------------------------------------------------
    # ROLE IN THE EXPERIENCE
    # -------------------------------------------------------------------------
    # Characters are how the player experiences relationships.
    # The goal: "I know them" — the player can predict what Aldric would do.
    # Characters feel real because they ARE real — consistent beliefs, voice, history.
    #
    # Key moments characters create:
    # - "They remembered" — character references something from sessions ago
    # - "I can rely on them" — Player sends companion on mission, confident they'll succeed
    # - "They became real" — Character reveals depth beyond their role
    #
    # Characters are NOT stat blocks. They are people with:
    # - Beliefs (narratives they hold)
    # - Voice (how they speak)
    # - History (backstory that informs behavior)
    # - Agency (they act based on their beliefs, not player commands)

    # -------------------------------------------------------------------------
    # DYNAMICS
    # -------------------------------------------------------------------------
    # - Characters BELIEVE narratives → beliefs drive behavior
    # - Characters SPREAD narratives → news travels through people
    # - Characters MOVE through places → proximity affects tension pressure
    # - Characters ACT when tensions break → World Runner determines what they do
    # - Companions are NEEDED → player can't do everything alone

    when_to_create: |
      - A new person enters the story (met, mentioned, discovered)
      - Player needs to interact with someone
      - World Runner determines someone acted off-screen

    when_to_update: |
      - Character dies (alive: false)
      - Character gains/loses a modifier (wounded, inspired, etc.)
      - Narrator discovers deeper backstory through generation

    attributes:
      id: { type: string, required: true }
      name: { type: string, required: true }
      type:
        type: enum
        values: [player, companion, major, minor, background]
        guide: |
          player: The protagonist (one per game)
          companion: Travels with player, deep characterization
          major: Important characters with full personality
          minor: Named characters with limited depth
          background: Unnamed or barely characterized
      alive: { type: boolean, default: true }
      face: { type: enum, values: [young, scarred, weathered, gaunt, hard, noble] }

      skills:
        description: "What this character can do"
        fighting: { type: enum, values: [untrained, capable, skilled, master] }
        tracking: { type: enum, values: [untrained, capable, skilled, master] }
        healing: { type: enum, values: [untrained, capable, skilled, master] }
        persuading: { type: enum, values: [untrained, capable, skilled, master] }
        sneaking: { type: enum, values: [untrained, capable, skilled, master] }
        riding: { type: enum, values: [untrained, capable, skilled, master] }
        reading: { type: enum, values: [untrained, capable, skilled, master] }
        leading: { type: enum, values: [untrained, capable, skilled, master] }

      voice:
        description: "How this character speaks — for Narrator consistency"
        tone: { type: enum, values: [quiet, sharp, warm, bitter, measured, fierce] }
        style: { type: enum, values: [direct, questioning, sardonic, gentle, blunt] }

      personality:
        description: "How this character thinks and acts"
        approach: { type: enum, values: [direct, cunning, cautious, impulsive, deliberate] }
        values: { type: array, items: [loyalty, survival, honor, ambition, faith, family, justice, freedom, wealth, knowledge, power, peace] }
        flaw: { type: enum, values: [pride, fear, greed, wrath, doubt, rigidity, softness, envy, sloth] }

      backstory:
        description: "Deep character knowledge — Narrator discovers through generation"
        properties:
          family: { type: string }
          childhood: { type: string }
          wound: { type: string }
          why_here: { type: string }

      modifiers: { type: array, items: { $ref: "#/definitions/modifier" } }

      image_prompt:
        type: string
        description: "Read docs/infrastructure/image-generation/PATTERNS_Image_Generation.md before writing. Prompt for character portrait — face, clothing, posture, lighting, mood."
        example: "A cinematic portrait of a weathered Saxon warrior, 10th century England. Man in his thirties, angular face with a pale scar across the jaw, dark hair cropped short, grey streaking at the temples. Worn leather jerkin over wool tunic, iron brooch at the shoulder. Expression guarded, watchful, eyes catching firelight. Warm orange glow from below, cold blue moonlight from above, mixing on his features. Shallow depth of field, background dark and indistinct. 35mm film photography, naturalistic lighting, muted earth tones."

  # ---------------------------------------------------------------------------
  # PLACE
  # ---------------------------------------------------------------------------

  place:
    title: "PLACE — A location where things happen, with atmosphere and geography"
    description: "Anywhere that can be located, traveled to, occupied"

    # -------------------------------------------------------------------------
    # ROLE IN THE EXPERIENCE
    # -------------------------------------------------------------------------
    # Places ground the player in the world.
    # The goal: "I know this place" — some locations become THEIRS.
    #
    # Key moments places create:
    # - "I know this place well" — Familiarity creates ownership, home
    # - "The world moved" — Player arrives and learns events happened here without them
    # - Atmosphere shapes mood — the same place feels different at night, in rain, after battle
    #
    # Places are NOT just containers. They have:
    # - Atmosphere (mood, weather, sensory details)
    # - Geography (connections to other places, travel time)
    # - Memory (events that happened here become narratives)

    # -------------------------------------------------------------------------
    # DYNAMICS
    # -------------------------------------------------------------------------
    # - Places CONTAIN characters → proximity enables interaction
    # - Travel TIME matters → distance creates urgency, cost
    # - Atmosphere SHIFTS → same place, different feel
    # - Events HAPPEN at places → location becomes part of the story
    # - Geography determines what's possible → blocked paths, dangerous roads

    when_to_create: |
      - Player travels to a new location
      - A location is mentioned that might be visited
      - World Runner needs to set events somewhere

    when_to_update: |
      - Atmosphere changes (siege begins, celebration, fire)
      - Modifiers change (burning, flooded, abandoned)

    attributes:
      id: { type: string, required: true }
      name: { type: string, required: true }
      coordinates: { type: array, items: float, description: "[lat, lng] — geographic position" }
      scale:
        type: enum
        values: [region, settlement, district, building, room]
        guide: |
          region: Large area (the North, Wessex)
          settlement: City, town, village, hold, monastery, camp
          district: Named area within settlement (York Market, the docks)
          building: Single structure (the hall, the church, the inn)
          room: Interior space within a building
        movement: |
          Movement within same parent uses implicit times:
          - room → room: ~1 min
          - building → building: ~5 min
          - district → district: ~15 min
          Movement between settlements/regions requires ROUTE link
      type:
        type: enum
        values: [region, city, hold, village, monastery, camp, road, room, wilderness, ruin]
        guide: |
          region: Large area (the North, Wessex)
          city: Major settlement (York, London)
          hold: Fortified position (castle, fort)
          village: Small settlement
          monastery: Religious site
          camp: Temporary location
          road: Travel route
          room: Interior space within another place
          wilderness: Untamed land
          ruin: Destroyed or abandoned structure

      atmosphere:
        description: "Current feel of the place — Narrator uses for scene-setting"
        weather: { type: array, items: [rain, snow, fog, clear, overcast, storm, wind, cold, hot] }
        mood: { type: enum, values: [welcoming, hostile, indifferent, fearful, watchful, desperate, peaceful, tense] }
        details: { type: array, items: string }

      modifiers: { type: array, items: { $ref: "#/definitions/modifier" } }

      image_prompt:
        type: string
        description: "Read docs/infrastructure/image-generation/PATTERNS_Image_Generation.md before writing. Prompt for place illustration — architecture, weather, time, atmosphere."
        example: "A cinematic wide shot of a Norman stone fortress at dusk, 10th century England. Rough-hewn grey stone walls on a low hill, square keep with narrow arrow slits, timber palisade reinforcing the outer wall. Muddy track leading to iron-bound oak gates. Bare trees surrounding, dead bracken at the walls. Overcast sky, recent rain, puddles reflecting torchlight from the gatehouse. Cold, threatening atmosphere, sense of military occupation. No people visible, no banners. Wide establishing shot, slight low angle. Volumetric mist pooling in the ditch. 35mm film photography, desaturated colors, Roger Deakins-style naturalistic lighting."

  # ---------------------------------------------------------------------------
  # THING
  # ---------------------------------------------------------------------------

  thing:
    title: "THING — An object that can be owned, given, stolen, or fought over"
    description: "Anything that can be possessed, transferred, contested"

    # -------------------------------------------------------------------------
    # ROLE IN THE EXPERIENCE
    # -------------------------------------------------------------------------
    # Things create ownership and stakes.
    # The goal: Objects become meaningful through their history and contested nature.
    #
    # Key moments things create:
    # - "This was his" — An object carries emotional weight from its history
    # - "They want it" — Contested ownership creates tension
    # - "I gave my word" — A token represents an oath or bond
    #
    # Things are NOT inventory items. They are:
    # - Story anchors (the sword that killed the father)
    # - Relationship tokens (the ring she gave you)
    # - Stakes (the land Edmund took)

    # -------------------------------------------------------------------------
    # DYNAMICS
    # -------------------------------------------------------------------------
    # - Possession is GROUND TRUTH → they have it or they don't
    # - Ownership is NARRATIVE → who SHOULD have it is a story
    # - Things can be CONTESTED → creates tension
    # - Things carry SIGNIFICANCE → mundane vs legendary affects weight
    # - Transfer creates STORY → giving, stealing, finding all spawn narratives

    when_to_create: |
      - An object becomes relevant to the story
      - Something is given, stolen, found, or fought over
      - A MacGuffin enters the narrative

    when_to_update: |
      - Thing is damaged, hidden, blessed, cursed
      - Quantity changes (provisions consumed)

    attributes:
      id: { type: string, required: true }
      name: { type: string, required: true }
      type:
        type: enum
        values: [weapon, armor, document, letter, relic, treasure, title, land, token, provisions, coin_purse, horse, ship, tool]
        guide: |
          weapon/armor: Combat equipment
          document/letter: Written information
          relic: Religious or magical significance
          treasure: Valuable goods
          title: Legal claim or position
          land: Property (non-portable)
          token: Small symbolic item
          provisions: Consumables
          coin_purse: Money
          horse/ship: Transport
          tool: Practical equipment
      portable: { type: boolean, default: true }
      significance:
        type: enum
        values: [mundane, personal, political, sacred, legendary]
        guide: |
          mundane: Common, replaceable
          personal: Meaningful to someone
          political: Affects power structures
          sacred: Religious importance
          legendary: Known by many, storied
      quantity: { type: integer, default: 1 }
      description: { type: string }
      modifiers: { type: array, items: { $ref: "#/definitions/modifier" } }

      image_prompt:
        type: string
        description: "Read docs/infrastructure/image-generation/PATTERNS_Image_Generation.md before writing. Prompt for thing illustration — material, craftsmanship, condition, lighting, context."
        example: "A cinematic close-up of a Saxon seax, 10th century England. Pattern-welded blade with visible folded steel, worn leather grip wrapped in tarnished silver wire, angular pommel. Small runes etched near the hilt, partially worn away. Blade nicked from use, well-oiled. Resting on rough undyed wool cloth, dark wood table beneath. Warm candlelight catching the edge, deep shadows. Shallow depth of field, background dark. 35mm film photography, rich warm tones, highly detailed metalwork."

  # ---------------------------------------------------------------------------
  # NARRATIVE
  # ---------------------------------------------------------------------------

  narrative:
    title: "NARRATIVE — A story that characters believe, creating all relationships and knowledge"
    description: "A story about characters, places, things, or their relationships"

    # -------------------------------------------------------------------------
    # ROLE IN THE EXPERIENCE
    # -------------------------------------------------------------------------
    # NARRATIVES ARE THE GAME.
    # Everything — relationships, reputation, memory, knowledge — is narrative.
    #
    # Key moments narratives create:
    # - "They remembered" — A narrative from sessions ago surfaces
    # - "My past speaks" — Player's oaths and debts pull in different directions
    # - "I was wrong" — Player discovers their foundational belief was mistaken
    # - "Everything led here" — Accumulated narratives converge in climactic moment
    #
    # What narratives ARE:
    # - "Aldric is loyal" is a narrative, not a stat
    # - "Edmund betrayed me" is a narrative, not a flag
    # - "We are brothers" is a narrative, not a relationship type
    #
    # Characters don't have relationships — they have stories they tell themselves
    # about relationships. The player's beliefs may be WRONG. Truth is director-only.

    # -------------------------------------------------------------------------
    # DYNAMICS
    # -------------------------------------------------------------------------
    # - Narratives have WEIGHT → high-weight narratives speak louder, appear more
    # - Narratives can CONTRADICT → contradiction under pressure creates tension
    # - Narratives SPREAD → characters tell each other stories
    # - Narratives become VOICES → they speak to the player in scenes
    # - Narratives have TRUTH (director-only) → player beliefs can be mistaken
    # - Narratives CLUSTER into tensions → when tension breaks, story advances
    # - Old narratives can be SUPERSEDED → the world evolves

    when_to_create: |
      - Something happens that characters will remember or talk about
      - A relationship forms, changes, or is revealed
      - Information is learned, spread, or discovered
      - An event occurs that affects the world
      - World Runner resolves a flip — creates narratives for what happened

    when_to_update: |
      - Narrator adds notes for continuity
      - Focus adjusted for pacing
      - New voice phrases discovered

    why_this_matters: |
      Narratives are THE core of the system. Everything is story.
      - "Aldric is loyal" is a narrative, not a stat
      - "Edmund betrayed me" is a narrative, not a flag
      - "We are brothers" is a narrative, not a relationship type
      Characters believe narratives. They don't have relationships —
      they have stories they tell themselves about relationships.

    attributes:
      id: { type: string, required: true }
      name: { type: string, required: true, description: "Short label for reference" }
      content: { type: string, required: true, description: "The story itself — what happened, what is believed" }
      interpretation: { type: string, required: true, description: "What it means — the emotional/thematic weight" }

      type:
        type: enum
        required: true
        values:
          # About events
          - memory          # "I saw the flames myself"
          - account         # "Wulfstan told me what he saw"
          - rumor           # "They say the Normans burned it"

          # About characters
          - reputation      # "Edmund is known for his cunning"
          - identity        # "We are Saxons" / "I serve the King"

          # About relationships
          - bond            # "We fought together at Hastings"
          - oath            # "I swore to protect him"
          - debt            # "He saved my life — I owe him"
          - blood           # "He is my brother"
          - enmity          # "Edmund is my enemy"
          - love            # "I loved her once"
          - service         # "I serve Lord Malet"

          # About things
          - ownership       # "This sword is mine"
          - claim           # "The land should be ours"

          # About places
          - control         # "The Normans hold York"
          - origin          # "Aldric is from Thornwick"

          # Meta
          - belief          # "The Normans will never leave"
          - prophecy        # "Winter will be harsh"
          - lie             # "I told him I was a merchant"
          - secret          # "Edmund killed our father"

        guide: |
          Choose type based on what the narrative IS, not what it's about.
          A story about a debt IS a debt narrative.
          A story about what someone saw IS a memory.
          A rumor about a debt is still a rumor (uncertain source).

      about:
        description: "The nodes this narrative concerns — for graph traversal"
        properties:
          characters: { type: array, items: string }
          relationship: { type: array, items: string, description: "Pair of character IDs if about their bond" }
          places: { type: array, items: string }
          things: { type: array, items: string }

      tone:
        type: enum
        values: [bitter, proud, shameful, defiant, mournful, cold, righteous, hopeful, fearful, warm, dark, sacred]
        description: "Emotional color — affects how it surfaces as a Voice"

      voice:
        description: "How this narrative speaks when it becomes a Voice"
        style: { type: enum, values: [whisper, demand, remind, accuse, plead, warn, inspire, mock, question] }
        phrases: { type: array, items: string, description: "Example lines this narrative might say" }

      # System fields
      weight: { type: float, min: 0, max: 1, computed: true, description: "Importance — computed by graph engine" }
      focus: { type: float, min: 0.1, max: 3.0, default: 1.0, description: "Narrator pacing adjustment" }

      # Director only
      truth: { type: float, min: 0, max: 1, default: 1, director_only: true, description: "How true is this? Characters never see this." }
      narrator_notes: { type: string, description: "Narrator's notes for continuity" }


# =============================================================================
# DEFINITIONS
# =============================================================================

definitions:

  modifier:
    description: "Temporary state affecting any node — apply and remove as situations change"

    when_to_apply: |
      - Character is hurt, sick, emotionally affected
      - Place is under siege, burning, celebrating
      - Thing is damaged, hidden, contested

    when_to_remove: |
      - Condition heals or resolves
      - Situation changes
      - Time passes (duration expires)

    properties:
      type:
        type: enum
        values:
          # character
          - wounded       # physically hurt
          - sick          # ill
          - hungry        # lacking food
          - exhausted     # lacking rest
          - drunk         # intoxicated
          - grieving      # mourning loss
          - inspired      # motivated, energized
          - afraid        # fearful
          - angry         # wrathful
          - hopeful       # optimistic
          - suspicious    # distrustful
          # place
          - burning       # on fire
          - flooded       # water damage
          - besieged      # under attack
          - abandoned     # empty
          - celebrating   # festive
          - haunted       # supernatural presence
          - watched       # under surveillance
          - safe          # protected
          # thing
          - damaged       # broken, worn
          - hidden        # concealed
          - contested     # ownership disputed
          - blessed       # holy
          - cursed        # unholy
          - stolen        # taken illegally
      severity: { type: enum, values: [mild, moderate, severe] }
      duration: { type: string, description: "How long — 'until healed', '3 days', 'permanent'" }
      source: { type: string, description: "What caused this — for narrative continuity" }


# =============================================================================
# LINKS (6 Types)
# =============================================================================

links:

  # ---------------------------------------------------------------------------
  # CHARACTER → NARRATIVE (Belief)
  # ---------------------------------------------------------------------------

  character_narrative:
    title: "CHARACTER_NARRATIVE — What a character knows, believes, doubts, hides, or spreads"
    from: character
    to: narrative
    description: "A character's relationship to a narrative — THE source of all belief state"

    # -------------------------------------------------------------------------
    # ROLE IN THE EXPERIENCE
    # -------------------------------------------------------------------------
    # Beliefs create DRAMA. Characters don't know facts — they believe stories.
    #
    # Key moments beliefs create:
    # - "They don't know" — Character acts on incomplete information
    # - "They believe a lie" — Character's actions based on false narrative
    # - "Secrets emerge" — Hidden beliefs surface under pressure
    # - "News travels" — Belief spreads from character to character

    # -------------------------------------------------------------------------
    # DYNAMICS
    # -------------------------------------------------------------------------
    # - heard + believes = character acts as if true
    # - heard + denies = character actively rejects (creates conflict)
    # - heard + doubts = character is uncertain (can be swayed)
    # - hides = knows but won't share (secret keeping)
    # - spreads = actively telling others (news propagation)
    # - High doubt + high belief = CONFLICTED (internal tension)
    #
    # Belief propagation:
    # - Characters in same place can share narratives
    # - Trust affects whether beliefs are accepted
    # - Contradicting beliefs create tension

    when_to_create: |
      - Character encounters a story (heard)
      - Character forms an opinion (believes/doubts/denies)
      - Character decides to act on a narrative (spreads/hides)
      - Character originates a story (originated)

    when_to_update: |
      - Character learns more (heard increases)
      - Character becomes more/less convinced (believes changes)
      - Character starts doubting (doubts increases)
      - Character decides to spread or hide (action attributes change)

    why_this_matters: |
      This link IS how characters know things. There is no "knowledge" stat.
      Aldric knows about the betrayal because he has a link to that narrative
      with heard=1.0 and believes=0.9.

    attributes:
      # Knowledge (0-1) — how much do they know/believe?
      heard:
        type: float, min: 0, max: 1, default: 0
        description: "Has encountered this story. 0=never heard, 1=knows full details"
      believes:
        type: float, min: 0, max: 1, default: 0
        description: "Holds as true. 0=doesn't believe, 1=absolutely certain"
      doubts:
        type: float, min: 0, max: 1, default: 0
        description: "Actively uncertain. High doubt + high belief = conflicted"
      denies:
        type: float, min: 0, max: 1, default: 0
        description: "Rejects as false. Can coexist with heard (knows but denies)"

      # Action (0-1) — what are they doing with this knowledge?
      hides:
        type: float, min: 0, max: 1, default: 0
        description: "Knows but conceals. Won't mention, deflects questions"
      spreads:
        type: float, min: 0, max: 1, default: 0
        description: "Actively promoting. Tells others, brings it up"

      # Origin
      originated:
        type: float, min: 0, max: 1, default: 0
        description: "Created this narrative. 1=they're the source"

      # Metadata — how did they learn?
      source:
        type: enum
        values: [none, witnessed, told, inferred, assumed, taught]
        default: none
        guide: |
          witnessed: Saw it happen
          told: Someone told them
          inferred: Figured it out from evidence
          assumed: Believes without evidence
          taught: Learned as established fact
      from_whom: { type: string, default: "", description: "Who told them (if told)" }
      when: { type: datetime, description: "When they learned" }

  # ---------------------------------------------------------------------------
  # NARRATIVE → NARRATIVE (Story Relationships)
  # ---------------------------------------------------------------------------

  narrative_narrative:
    title: "NARRATIVE_NARRATIVE — How stories relate: contradict, support, elaborate, subsume, supersede"
    from: narrative
    to: narrative
    description: "How narratives relate to each other"

    # -------------------------------------------------------------------------
    # ROLE IN THE EXPERIENCE
    # -------------------------------------------------------------------------
    # Story relationships create STRUCTURE and CONFLICT.
    #
    # Key moments narrative relationships create:
    # - "They can't both be true" — Contradicting narratives force resolution
    # - "It all connects" — Supporting narratives create coherent worldview
    # - "Things have changed" — Superseding narrative replaces old understanding

    # -------------------------------------------------------------------------
    # DYNAMICS
    # -------------------------------------------------------------------------
    # - CONTRADICTS → These narratives cannot both be true. Creates tension.
    #   When believers of both are in proximity, pressure builds.
    # - SUPPORTS → These narratives reinforce each other. Creates clusters.
    #   Believing one makes you more likely to believe the other.
    # - SUPERSEDES → New information replaces old. The world evolves.
    #   "Edmund is dead" supersedes "Edmund is my enemy"
    # - ELABORATES → Adds detail without conflict.
    # - SUBSUMES → Specific case of broader pattern.

    when_to_create: |
      - Two narratives are in tension (contradicts)
      - One narrative reinforces another (supports)
      - One narrative adds detail to another (elaborates)
      - One narrative is a case of a broader pattern (subsumes)
      - New information replaces old (supersedes)

    when_to_update: |
      - Relationship strength changes
      - New evidence strengthens/weakens connection

    why_this_matters: |
      These links create story structure. Contradicting narratives create drama.
      Supporting narratives create belief clusters. Superseding narratives
      let the world evolve.

    attributes:
      contradicts:
        type: float, min: 0, max: 1, default: 0
        description: "These cannot both be true"
        example: "'Edmund betrayed us' contradicts 'Edmund was forced'"
      supports:
        type: float, min: 0, max: 1, default: 0
        description: "These reinforce each other"
        example: "'Aldric is loyal' supports 'Aldric kept his oath'"
      elaborates:
        type: float, min: 0, max: 1, default: 0
        description: "This adds detail to the other"
        example: "'Edmund stole the sword' elaborates 'The betrayal'"
      subsumes:
        type: float, min: 0, max: 1, default: 0
        description: "This is a specific case of the other"
        example: "'Thornwick burned' subsumes 'The Harrying was brutal'"
      supersedes:
        type: float, min: 0, max: 1, default: 0
        description: "This replaces the other — the old one fades"
        example: "'Edmund is dead' supersedes 'Edmund is my enemy'"

  # ---------------------------------------------------------------------------
  # CHARACTER → PLACE (Physical Presence)
  # ---------------------------------------------------------------------------

  character_place:
    title: "CHARACTER_PLACE — Where a character physically is (ground truth)"
    from: character
    to: place
    description: "Physical presence — GROUND TRUTH, not belief"

    when_to_create: |
      - Character is at a location
      - Character arrives somewhere

    when_to_update: |
      - Character moves (present changes)
      - Character hides/reveals themselves (visible changes)

    why_this_matters: |
      This is one of the few GROUND TRUTHS in the system.
      A character IS at a place, regardless of what anyone believes.
      The graph engine uses this for proximity calculations.

    attributes:
      present:
        type: float, min: 0, max: 1, default: 0
        description: "1=here, 0=not here. Usually binary."
      visible:
        type: float, min: 0, max: 1, default: 1
        description: "Can they be seen? 0=hiding, 1=visible"

  # ---------------------------------------------------------------------------
  # CHARACTER → THING (Physical Possession)
  # ---------------------------------------------------------------------------

  character_thing:
    title: "CHARACTER_THING — What a character physically carries (ground truth)"
    from: character
    to: thing
    description: "Physical possession — GROUND TRUTH, not belief"

    when_to_create: |
      - Character acquires something
      - Character is established as owning something

    when_to_update: |
      - Character gives/loses the thing
      - Character hides/reveals the thing

    why_this_matters: |
      Ground truth. They HAVE it or they don't.
      Separate from ownership narratives (who SHOULD have it).

    attributes:
      carries:
        type: float, min: 0, max: 1, default: 0
        description: "1=has it, 0=doesn't. Usually binary."
      carries_hidden:
        type: float, min: 0, max: 1, default: 0
        description: "1=has it secretly, 0=openly carries or doesn't have"

  # ---------------------------------------------------------------------------
  # THING → PLACE (Physical Location)
  # ---------------------------------------------------------------------------

  thing_place:
    title: "THING_PLACE — Where an uncarried thing physically is (ground truth)"
    from: thing
    to: place
    description: "Physical location of thing — GROUND TRUTH"

    when_to_create: |
      - Thing exists at a location (not carried by anyone)
      - Thing is left somewhere

    when_to_update: |
      - Thing is moved
      - Thing is hidden/revealed

    why_this_matters: |
      Where things ARE, not where people think they are.

    attributes:
      located:
        type: float, min: 0, max: 1, default: 0
        description: "1=here, 0=not here"
      hidden:
        type: float, min: 0, max: 1, default: 0
        description: "1=concealed, 0=visible"
      specific_location:
        type: string, default: ""
        description: "Where exactly — 'under the altar', 'in the chest'"

  # ---------------------------------------------------------------------------
  # PLACE → PLACE (Geography)
  # ---------------------------------------------------------------------------

  # Two link types: CONTAINS (hierarchy) and ROUTE (travel)

  place_contains:
    title: "CONTAINS — Hierarchical containment"
    from: place
    to: place
    description: "This place is inside that place — binary relationship, no attributes"

    # -------------------------------------------------------------------------
    # HIERARCHY EXAMPLE
    # -------------------------------------------------------------------------
    # place_york (settlement)
    #     ├── CONTAINS → place_york_market (district)
    #     │                 └── CONTAINS → place_merchants_hall (building)
    #     │                                    └── CONTAINS → place_back_room (room)
    #     └── CONTAINS → place_york_minster (building)

    when_to_create: |
      - Establishing place hierarchy
      - A new sub-location is discovered or entered

    why_this_matters: |
      Scale + containment determines implicit movement times.
      No ROUTE needed for movement within same settlement.

  place_route:
    title: "ROUTE — Travel connection between settlements/regions"
    from: place
    to: place
    description: "Travel path with computed distance and time — GROUND TRUTH"

    # -------------------------------------------------------------------------
    # ROUTE IS FOR INTER-SETTLEMENT TRAVEL ONLY
    # -------------------------------------------------------------------------
    # place_york ──[ROUTE]──> place_durham
    # place_york ──[ROUTE]──> place_scarborough
    #
    # NOT for:
    # place_york_market ──[ROUTE]──> place_york_minster  # NO! Same settlement

    when_to_create: |
      - Establishing travel routes between settlements or regions
      - Player discovers a new path

    when_to_update: |
      - Path becomes blocked/opened
      - Road conditions change

    why_this_matters: |
      Geography determines travel time, which affects proximity,
      which affects how much characters matter to the player.
      Computed from real waypoints — no manual distance entry.

    attributes:
      waypoints:
        type: array
        items: { type: array, items: float }
        description: "[[lat, lng], ...] — traced once from real geography"
      road_type:
        type: enum
        values: [roman, track, path, river, none]
        guide: |
          roman: Paved Roman road (5.0 km/h)
          track: Maintained dirt track (3.5 km/h)
          path: Forest/mountain path (2.5 km/h)
          river: River travel, downstream (8.0 km/h)
          none: Cross-country, no road (1.5 km/h)

      # Computed at link creation from waypoints + road_type
      distance_km:
        type: float
        computed: true
        description: "Haversine distance from waypoints"
      travel_minutes:
        type: integer
        computed: true
        description: "distance_km / speed * 60 — for tick math"
      difficulty:
        type: enum
        values: [easy, moderate, hard, dangerous]
        computed: true
        description: "Derived from road_type: roman=easy, track=moderate, path=hard, none=dangerous"

      detail:
        type: string
        description: "Optional narrative: 'Crosses marshland near Humber'"


# =============================================================================
# TENSIONS
# =============================================================================

tensions:
  title: "TENSION — A cluster of narratives under pressure that will eventually break"
  description: "Clusters of narratives under pressure — when they break, things happen"

  # ===========================================================================
  # ROLE IN THE EXPERIENCE
  # ===========================================================================
  # Tensions are HOW THE WORLD MOVES.
  # They create the feeling: "The world moved without me."
  #
  # Key moments tensions create:
  # - "The world moved" — Player arrives and learns a tension broke while they were away
  # - "I could have prevented this" — If player had been faster, things would differ
  # - "Something is happening elsewhere" — Player senses tensions building beyond their view
  # - "This happened because of that" — Every break traces to accumulated pressure
  #
  # Tensions are NOT scripted events. They are:
  # - Pressure that accumulates over TIME
  # - Contradictions that MUST eventually resolve
  # - Emergent drama, not authored triggers

  # ===========================================================================
  # DYNAMICS
  # ===========================================================================
  # THE TENSION LOOP:
  # 1. Time passes → pressure accumulates (mechanical, no LLM)
  # 2. Pressure exceeds breaking_point → FLIP detected
  # 3. World Runner called → determines WHAT specifically happened
  # 4. New narratives created → graph updated
  # 5. Cascades checked → did this destabilize other tensions?
  #
  # PRESSURE SOURCES:
  # - Time (gradual accumulation via base_rate)
  # - Proximity (believers of contradicting narratives in same place)
  # - Events (direct pressure from player actions or other breaks)
  # - Deadlines (scheduled pressure floors)
  #
  # WHY THIS MATTERS:
  # The player is NOT the center. While they talk to Aldric for 30 minutes,
  # Edmund gets 30 minutes closer to York. Tensions tick. The world moves.

  when_to_create: |
    - Contradicting narratives that must eventually resolve
    - Approaching deadline or event
    - Building confrontation between characters
    - Any situation where "something has to give"

  when_to_update: |
    - Pressure changes (gradual accumulation or events)
    - Narratives added/removed from tension
    - Narrator adjusts for pacing

  attributes:
    id: { type: string, required: true }
    narratives: { type: array, items: string, description: "Narrative IDs in tension" }
    description: { type: string, description: "What this tension is about" }
    narrator_notes: { type: string, description: "Narrator's notes for how to handle the break" }

    pressure_type:
      type: enum
      values: [gradual, scheduled, hybrid]
      default: gradual
      guide: |
        gradual: Slow burn. Pressure ticks up over time. Uncertain when it breaks.
          Use for: relationship strain, growing suspicion, accumulating debt
        scheduled: Deadline. Pressure follows a timeline with cliff jumps.
          Use for: approaching event, traveling character, oath due date
        hybrid: Both. Has a floor that rises on schedule, but events can exceed it.
          Use for: confrontation where characters are converging

    pressure: { type: float, min: 0, max: 1, description: "Current pressure level" }
    breaking_point: { type: float, min: 0, max: 1, default: 0.9 }

    # For gradual
    base_rate: { type: float, default: 0.001, description: "Pressure increase per minute" }

    # For scheduled/hybrid
    trigger_at: { type: string, description: "When this tension must break" }
    progression:
      type: array
      description: "Timeline of pressure escalation"
      items:
        at: { type: string }
        pressure: { type: float, description: "For scheduled type" }
        pressure_floor: { type: float, description: "For hybrid type" }

  examples:

    gradual_example:
      id: tension_aldric_loyalty
      narratives: [narr_aldric_oath, narr_aldric_thornwick]
      pressure_type: gradual
      pressure: 0.4
      base_rate: 0.001
      breaking_point: 0.9
      description: "Aldric is bound by oath, but the north's wounds are his wounds."

    scheduled_example:
      id: tension_malet_inspection
      narratives: [narr_malet_suspicious, narr_rolf_in_york]
      pressure_type: scheduled
      trigger_at: "Day 16, morning"
      progression:
        - { at: "Day 14", pressure: 0.1 }
        - { at: "Day 15", pressure: 0.4 }
        - { at: "Day 16 dawn", pressure: 0.9 }
        - { at: "Day 16 morning", pressure: 1.0 }
      breaking_point: 0.9
      description: "Sheriff Malet will inspect the garrison."

    hybrid_example:
      id: tension_edmund_confrontation
      narratives: [narr_edmund_betrayal, narr_rolf_oath_vengeance]
      pressure_type: hybrid
      pressure: 0.5
      base_rate: 0.001
      progression:
        - { at: "Day 12", pressure_floor: 0.5 }
        - { at: "Day 13", pressure_floor: 0.7 }
        - { at: "Day 14", pressure_floor: 0.85 }
      breaking_point: 0.9
      description: "Rolf approaches York. Events may accelerate this."


# =============================================================================
# MOMENT
# =============================================================================

moment:
  title: "MOMENT — A single unit of narrated content"
  description: "Every piece of text shown to the player becomes a Moment"

  # -------------------------------------------------------------------------
  # ROLE IN THE EXPERIENCE
  # -------------------------------------------------------------------------
  # Moments enable:
  # - Semantic search across all game content ("when did Aldric mention his sister?")
  # - Temporal queries ("what happened yesterday?")
  # - Source attribution for narratives
  # - Full transcript preservation

  # -------------------------------------------------------------------------
  # DYNAMICS
  # -------------------------------------------------------------------------
  # - Every dialogue line → Moment
  # - Every narration line → Moment
  # - Every player action → Moment
  # - Every hint/voice → Moment
  # - Moments link to Place (where), Character (who said), Narrative (source for)

  when_to_create: |
    - Every dialogue line (narrator or character speaks)
    - Every narration line (scene description)
    - Every player action (click, type, choose)
    - Every hint/voice

  attributes:
    id:
      type: string
      required: true
      description: "Pattern: {place}_{day}_{time}_{type}_{suffix}"
      example: "crossing_d5_dusk_dialogue_143521"
    text: { type: string, required: true, description: "The actual text content" }
    type:
      type: enum
      values: [narration, dialogue, hint, player_click, player_freeform, player_choice]
    tick: { type: integer, required: true, description: "World tick when this occurred" }
    line: { type: integer, description: "Line number in transcript.json" }
    embedding: { type: array, items: float, description: "768-dim vector (if text > 20 chars)" }

  # NOTE: Speaker is NOT an attribute. Use SAID link: Character -[SAID]-> Moment

  links:
    said:
      title: "CHARACTER_MOMENT (SAID) — Character produced this dialogue/action"
      from: character
      to: moment
      description: "Who said or did this"

    moment_at:
      title: "MOMENT_PLACE (AT) — Where moment occurred"
      from: moment
      to: place

    moment_then:
      title: "MOMENT_MOMENT (THEN) — Sequence within scene"
      from: moment
      to: moment
      description: "First moment -[THEN]-> second moment"

    narrative_from:
      title: "NARRATIVE_MOMENT (FROM) — Narrative sourced from moment"
      from: narrative
      to: moment
      description: "Source attribution for narratives"

  examples:

    dialogue_example:
      id: camp_d3_night_dialogue_aldric_oath
      text: "I swore an oath. That hasn't changed."
      type: dialogue
      tick: 4320
      speaker: char_aldric
      line: 47

    narration_example:
      id: crossing_d5_dusk_narration_blade
      text: "The blade lies in two pieces at his feet."
      type: narration
      tick: 7200
      line: 142

    player_action_example:
      id: york_d8_morning_player_freeform_ask
      text: "Tell me about the garrison."
      type: player_freeform
      tick: 11520
      speaker: char_player
      line: 203


# =============================================================================
# NARRATOR NOTES
# =============================================================================

narrator_notes:
  description: "How the Narrator maintains continuity and engagement"

  stored_on:
    - narratives (per-narrative notes)
    - tensions (per-tension notes)
    - story_document (arcs, setups)
    - player_document (patterns)

  examples:
    - "Adding focus — player enjoys political consequences"
    - "Planted grandmother reference in scene 3 — setup for Aldric reveal"
    - "Player ignored church twice — reducing focus"
    - "Edmund meeting scheduled for Day 14 — building toward confrontation"

  used_for:
    - "Continuity across sessions"
    - "Setup/payoff tracking"
    - "Focus adjustments"
    - "Character voice consistency"
