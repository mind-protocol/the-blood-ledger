# Moments — Algorithm: View Query

```
CREATED: 2024-12-17
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_View_Query.md (you are here)
ALGORITHMS:  ./ALGORITHM_Transitions.md, ./ALGORITHM_Lifecycle.md
SCHEMA:      ./SCHEMA_Moments.md
API:         ./API_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
IMPL:        ../../engine/db/graph_queries.py, ../../engine/api/app.py
```

---

## What The View Contains

The current view is everything the player can see and interact with right now.

```python
@dataclass
class CurrentView:
    location: Place           # Where the player is
    characters: List[Character]  # Who is present
    things: List[Thing]       # What is present
    moments: List[Moment]     # What can be read/heard
    transitions: List[Transition]  # What can be clicked
```

---

## The Query

```python
def get_current_view(player_id: str) -> CurrentView:
    # 1. Where is player?
    location = get_player_location(player_id)

    # 2. Who's here?
    characters = get_present_characters(location.id)

    # 3. What's here?
    things = get_present_things(location.id, characters)

    # 4. What narratives does player know?
    known_narratives = get_known_narratives(player_id)

    # 5. What moments are live?
    moments = get_live_moments(
        location_id=location.id,
        character_ids=[c.id for c in characters],
        thing_ids=[t.id for t in things],
        narrative_ids=known_narratives
    )

    # 6. Resolve speakers for dialogue moments
    for moment in moments:
        if moment.type == 'dialogue':
            moment.speaker = resolve_speaker(moment.id, characters)

    # 7. What transitions are available?
    transitions = get_transitions([m.id for m in moments if m.status == 'active'])

    return CurrentView(location, characters, things, moments, transitions)
```

---

## Step 1: Player Location

```cypher
MATCH (p:Character {id: $player_id})-[:AT]->(loc:Place)
RETURN loc
```

Simple lookup. Player is always AT exactly one place.

---

## Step 2: Present Characters

```cypher
MATCH (c:Character)-[:AT]->(loc:Place {id: $location_id})
WHERE c.alive = true
RETURN c
```

All living characters at the same location.

---

## Step 3: Present Things

Things can be at a location or carried by present characters.

```cypher
// Things at location
MATCH (t:Thing)-[:AT]->(loc:Place {id: $location_id})
RETURN t

UNION

// Things carried by present characters
MATCH (c:Character)-[:AT]->(loc:Place {id: $location_id})
MATCH (c)-[:CARRIES]->(t:Thing)
RETURN t
```

---

## Step 4: Known Narratives

What the player believes.

```cypher
MATCH (p:Character {id: $player_id})-[b:BELIEVES]->(n:Narrative)
WHERE b.believes > 0.5
RETURN n.id
```

---

## Step 5: Live Moments

This is the core query. A moment is live when:
1. Status is 'possible' or 'active'
2. All presence_required attachments are satisfied

```cypher
MATCH (m:Moment)
WHERE m.status IN ['possible', 'active']

// Get all required attachments
WITH m, [(m)-[r:ATTACHED_TO WHERE r.presence_required = true]->(target) | target] AS required

// Check all required targets are present
WHERE ALL(target IN required WHERE
    // Place: must be current location
    (target:Place AND target.id = $location_id)
    // Character: must be in present list
    OR (target:Character AND target.id IN $character_ids)
    // Thing: must be in present list
    OR (target:Thing AND target.id IN $thing_ids)
    // Narrative: player must know it
    OR (target:Narrative AND target.id IN $narrative_ids)
)

RETURN m
ORDER BY m.weight DESC
LIMIT 20
```

### Empty Required List

If a moment has no presence_required attachments, it's always visible (assuming weight is high enough).

### Weight Ordering

Higher weight moments appear first. This determines what's "on top" in the UI.

---

## Step 6: Speaker Resolution

For each dialogue moment, find who speaks it.

```python
def resolve_speaker(moment_id: str, present_characters: List[Character]) -> Optional[str]:
    """
    Returns character_id of who should speak this moment.
    None if no valid speaker (moment becomes narration).
    """
    present_ids = [c.id for c in present_characters]

    # Query CAN_SPEAK links
    links = query("""
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $moment_id})
        WHERE c.id IN $present_ids
        RETURN c.id AS char_id, r.weight AS weight
        ORDER BY r.weight DESC
    """, moment_id=moment_id, present_ids=present_ids)

    if links:
        return links[0].char_id  # Highest weight present

    return None  # No valid speaker
```

### No Speaker Found

If no CAN_SPEAK link matches a present character:
- Moment becomes narration (no speaker shown)
- Or moment is hidden (depending on moment.type)

---

## Step 7: Available Transitions

What can be clicked from active moments.

```cypher
MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO]->(next:Moment)
WHERE m.id IN $active_moment_ids
  AND next.status IN ['possible', 'dormant']
RETURN
    m.id AS from_id,
    r.require_words AS words,
    next.id AS to_id,
    r.trigger AS trigger
```

### Transition Structure

```python
@dataclass
class Transition:
    from_moment: str      # Source moment ID
    words: List[str]      # Clickable words (from require_words)
    to_moment: str        # Target moment ID
    trigger: str          # 'click' or 'wait'
```

---

## View Rendering

The frontend receives the view and renders:

```typescript
interface CurrentView {
  location: {
    id: string;
    name: string;
    type: string;
  };
  characters: Array<{
    id: string;
    name: string;
  }>;
  things: Array<{
    id: string;
    name: string;
  }>;
  moments: Array<{
    id: string;
    text: string;
    type: 'narration' | 'dialogue';
    speaker?: string;  // Resolved
    status: 'possible' | 'active' | 'spoken';
    tone?: string;
  }>;
  transitions: Array<{
    from: string;
    words: string[];
    to: string;
  }>;
}
```

### Highlighting Clickable Words

Frontend scans moment text for words in any transition.words array:

```typescript
function highlightClickables(moment: Moment, transitions: Transition[]): string {
    let text = moment.text;

    const clickableWords = transitions
        .filter(t => t.from === moment.id)
        .flatMap(t => t.words);

    for (const word of clickableWords) {
        // Case-insensitive replace with highlighted version
        const regex = new RegExp(`\\b(${word})\\b`, 'gi');
        text = text.replace(regex, `<span class="clickable">$1</span>`);
    }

    return text;
}
```

---

## Performance Considerations

### Moment Limit

Query returns at most 20 moments. Weighted by importance.

### Caching

The view can be cached with invalidation on:
- Player moves (location change)
- Character moves (presence change)
- Moment created/updated
- Transition taken

### Incremental Updates

For SSE streaming, send diffs:
- moment_created
- moment_updated
- moment_removed
- transition_added
- transition_removed

---

## Example View

Player at camp with Aldric, carrying father's ring.

```json
{
  "location": {
    "id": "place_camp",
    "name": "Roadside Camp",
    "type": "camp"
  },
  "characters": [
    { "id": "char_player", "name": "Rolf" },
    { "id": "char_aldric", "name": "Aldric" }
  ],
  "things": [
    { "id": "thing_ring", "name": "Father's Ring" }
  ],
  "moments": [
    {
      "id": "moment_fire_crackles",
      "text": "The fire crackles, throwing shadows.",
      "type": "narration",
      "status": "active"
    },
    {
      "id": "moment_aldric_speaks",
      "text": "You haven't said why we're going to York.",
      "type": "dialogue",
      "speaker": "char_aldric",
      "status": "active",
      "tone": "questioning"
    }
  ],
  "transitions": [
    {
      "from": "moment_aldric_speaks",
      "words": ["York", "why"],
      "to": "moment_player_explains"
    }
  ]
}
```

---

*"The view is computed, not stored. The graph IS the state."*
