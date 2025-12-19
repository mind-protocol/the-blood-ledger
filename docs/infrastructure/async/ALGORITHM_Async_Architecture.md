# Async Architecture — Algorithm

**Purpose:** Step-by-step flows for the async travel architecture: Runner protocol, hook injection, graph SSE, waypoint creation, fog of war, image generation, and discussion trees.

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Async_Architecture.md
BEHAVIORS:      ./BEHAVIORS_Travel_Experience.md
VALIDATION:     ./VALIDATION_Async_Architecture.md
IMPLEMENTATION: ./IMPLEMENTATION_Async_Architecture.md
TEST:           ./TEST_Async_Architecture.md
THIS:           ALGORITHM_Async_Architecture.md (you are here)
SYNC:           ./SYNC_Async_Architecture.md
```

---

## Runner Protocol

**Purpose:** How Narrator spawns Runner as a background task, and how to read its output.

### Invocation

Narrator spawns Runner using `bash` with `run_in_background=true`:

```python
bash(
    command='''
        timeout 600 && \
        cd agents/runner && \
        claude -p "TravelTask: origin=place_camp, destination=place_york, \
                   travellers=[char_rolf, char_aldric], time_span=3days" \
        --dangerously-skip-permissions \
        --allowedTools "Write,Read,graph_query,graph_write" \
        --add-dir ../../
    ''',
    run_in_background=true
)
```

**After invocation:**
- Narrator continues streaming immediately (doesn't wait)
- Runner works in background, writing to graph as it goes
- Frontend sees place creation via SSE

**Multiple Runners:** Can run simultaneously (e.g., player traveling while characters move elsewhere).

### Reading Output

When Runner completes, system sends a reminder:

```
<system-reminder>
Background bash ba7e4e6 has new output: 162 lines...
</system-reminder>
```

Narrator reads via `TaskOutput`:

```python
result = TaskOutput(task_id="ba7e4e6")
```

### During Processing

While Runner works, it writes directly to graph:

**Waypoint Creation**
```
Runner computes route segment →
  Creates place node in graph →
    Graph triggers image generation →
    Graph SSE broadcasts place_created →
      Frontend updates map
```

**Energy Ticking**
```
Runner processes segment →
  Ticks energy values →
    Writes to graph (internal state, frontend doesn't need)
```

**Break Resolution**
```
Tension flips →
  Runner resolves break →
    Creates narrative in graph →
    Updates character positions →
      If character in player's group → writes to injection_queue
      Runner STOPS and waits for injection to be handled
```

**Key:** Runner stops when it creates an injection. It doesn't continue in parallel. The injection response determines what happens next.

**Note:** Injections can also be triggered by non-Narrator activated nodes (e.g., world events, other characters acting independently).

**Visibility Updates**
```
Player "passes through" waypoint →
  Updates player_knows_place →
    Graph SSE broadcasts visibility_update →
      Frontend reveals fog
```

### Completion Payload

Runner outputs JSON to stdout:

```json
{
  "type": "travel_complete",
  "destination": "place_york",
  "time_elapsed": "3 days",
  "waypoints_created": ["place_humber_crossing", "place_north_ridge"],
  "destination_state": {
    "tensions_hot": ["tension_norman_patrol"],
    "characters_present": ["char_merchant_guild_master"],
    "news_available": ["narr_york_siege_rumor"],
    "atmosphere": "The city gates are guarded. Tension in the air."
  }
}
```

**Payload Types**

| Type | Meaning | Narrator Action |
|------|---------|-----------------|
| `travel_complete` | Journey finished normally | Generate arrival scene |
| `encounter` | Something happened mid-journey | Generate encounter scene, then continue or re-spawn |
| `arrival_change` | Destination state changed during travel | Incorporate change into arrival |

### Narrator Handling

```python
result = TaskOutput(task_id)

if result["type"] == "travel_complete":
    generate_arrival_scene(result["destination_state"])

elif result["type"] == "encounter":
    generate_encounter_scene(result)
    # May need to re-spawn Runner for remaining journey

elif result["type"] == "arrival_change":
    generate_modified_arrival(result)
```

### Key Clarifications

**Runner completion uses TaskOutput, NOT hook.**

Hook is for interruptions:
- Character speaks
- Player UI action

TaskOutput is for expected completions:
- Runner finished processing
- Background task done

---

## Hook Injection

**Purpose:** How the world interrupts the Narrator mid-stream.

### Principle

Hook injection is for **INTERRUPTIONS ONLY**.

NOT for:
- Runner completion (use TaskOutput)
- Normal state updates (use SSE)

Hook fires when:
- A character in the player's group is activated via narrative
- Player uses UI (stop button, location click, portrait click)

### Injection File

```
playthroughs/default/injection_queue.jsonl
```

One JSON object per line. First in, first out.

### Writers

**Graph/Runner — Character Activation**

When a narrative activates a character in the player's group:

```python
injection = {
    "type": "character_speaks",
    "character": "char_aldric",
    "trigger": "narr_patrol_spotted",
    "prompt": "Aldric grabs your arm. 'Wait. Movement ahead.'"
}
append_jsonl(INJECTION_FILE, injection)
```

**Frontend — Player UI**

When player clicks stop button:

```javascript
fetch('/api/inject', {
  method: 'POST',
  body: JSON.stringify({
    type: 'player_abort',
    current_position: currentPlaceId
  })
});
```

Backend appends to file:

```python
append_jsonl(INJECTION_FILE, request.json)
```

### Hook Script

File: `engine/scripts/check_injection.py`

Configured in: `agents/narrator/.claude/hooks.json`

Runs on every `PostToolUse` hook **for Narrator only** (not general dev sessions).

```python
import json
import os

INJECTION_FILE = "playthroughs/default/injection_queue.jsonl"

if os.path.exists(INJECTION_FILE):
    with open(INJECTION_FILE) as f:
        lines = f.readlines()

    if lines:
        # Take first injection
        injection = json.loads(lines[0])

        # Rewrite file with remaining injections
        with open(INJECTION_FILE, 'w') as f:
            f.writelines(lines[1:])

        # Return to Claude Code
        print(json.dumps({
            "decision": None,
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": json.dumps(injection)
            }
        }))
        exit()

# No injection
print(json.dumps({"decision": None}))
```

### Narrator Receives

The `additionalContext` field contains the injection. Narrator handles based on type:

```python
# In Narrator's context
injection = json.loads(additional_context)

if injection["type"] == "character_speaks":
    # Insert dialogue, then continue
    stream_dialogue(injection["character"], injection["prompt"])

elif injection["type"] == "player_abort":
    # Generate stop scene at current position
    generate_stop_scene(injection["current_position"])
```

### Injection Types

**character_speaks**

Meaning: Companion reacts to something

```json
{
  "type": "character_speaks",
  "character": "char_aldric",
  "prompt": "Aldric grabs your arm. 'Normans ahead.'"
}
```

Narrator Action: Insert dialogue/action, then continue

**character_acts**

Meaning: Companion does something unprompted

```json
{
  "type": "character_acts",
  "character": "char_aldric",
  "action": "draws sword",
  "reason": "tension_danger broke"
}
```

Narrator Action: Describe action, adjust scene

**player_abort**

Meaning: Player pressed stop

```json
{
  "type": "player_abort",
  "current_position": "place_humber_crossing"
}
```

Narrator Action: Generate stop scene at current position

**location_change**

Meaning: Player clicked destination on map

```json
{
  "type": "location_change",
  "new_destination": "place_lincoln"
}
```

Narrator Action: Acknowledge, potentially redirect travel

### When Character Activation Triggers Hook

```
Runner resolves break →
  Creates narrative in graph →
    Narrative activates character →
      Character is in player's group? →
        YES: Write to injection_queue →
              Hook fires on next PostToolUse →
                Narrator receives, handles
        NO: Just update graph (no hook)
```

### Key Clarifications

| Situation | Mechanism |
|-----------|-----------|
| Runner finishes | TaskOutput |
| Character speaks | Hook injection |
| Player clicks UI | Hook injection |
| Place created | Graph SSE |
| Image ready | Graph SSE |

---

## Graph SSE

**Purpose:** How the graph streams state changes to the frontend in real-time.

### Principle

Graph streams **location and image events only**.
- `position_update` — player moved
- `image_ready` — place image generated

NOT every graph write. Just these two event types.
Frontend subscribes once, receives what it needs for real-time map/image updates.

### Connection

Frontend establishes SSE connection on load:

```javascript
const eventSource = new EventSource('/api/graph/stream?playthrough=default');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleGraphEvent(data);
};
```

### Event Types

**position_update**

Trigger: Runner updates player position in graph

```json
{
  "type": "position_update",
  "player_id": "char_rolf",
  "current_place": "place_humber_crossing"
}
```

Frontend Action: Update current location display, animate if map exists

**image_ready**

Trigger: Image generation completes for place

```json
{
  "type": "image_ready",
  "place_id": "place_humber_crossing",
  "image_url": "/images/places/place_humber_crossing.png"
}
```

Frontend Action: Update left panel if current place, cache image

### Backend Implementation

**Position Update**

When Runner updates player position:

```python
def update_player_position(player_id, place_id):
    # Write to graph
    graph.set_property(player_id, "current_place", place_id)

    # Emit SSE
    sse_manager.broadcast({
        "type": "position_update",
        "player_id": player_id,
        "current_place": place_id
    })
```

**Image Ready**

When image generation completes:

```python
def on_image_generated(place_id, image_url):
    # Update graph
    graph.set_property(place_id, "image_url", image_url)

    # Emit SSE
    sse_manager.broadcast({
        "type": "image_ready",
        "place_id": place_id,
        "image_url": image_url
    })
```

**SSE Manager**

```python
class SSEManager:
    def __init__(self):
        self.clients = {}  # playthrough_id -> list of response objects

    def subscribe(self, playthrough_id, response):
        if playthrough_id not in self.clients:
            self.clients[playthrough_id] = []
        self.clients[playthrough_id].append(response)

    def broadcast(self, playthrough_id, event):
        for client in self.clients.get(playthrough_id, []):
            client.send(json.dumps(event))
```

### Frontend Handling

```javascript
function handleGraphEvent(event) {
  switch (event.type) {
    case 'position_update':
      updateCurrentPlace(event.current_place);
      break;

    case 'image_ready':
      if (event.place_id === currentPlace) {
        updateLeftPanel(event.image_url);
      }
      break;
  }
}
```

### Connection Management

**Reconnection**

```javascript
eventSource.onerror = () => {
  eventSource.close();
  setTimeout(() => {
    reconnectSSE();
  }, 1000);
};
```

**Cleanup**

```javascript
// On unmount
eventSource.close();
```

### Performance Considerations

- Events are small JSON payloads
- One connection per client (not per event type)
- Server buffers events during disconnect, replays on reconnect
- Frontend debounces rapid position updates for smooth animation

---

## Waypoint Creation

**Purpose:** How places materialize during travel.

### Principle

Runner creates ALL intermediate places during travel.
No skeleton. No pre-authored waypoints.
The world materializes as Runner writes to graph.
Images generate automatically on creation.

### Creation Flow

```
1. Runner computes travel segment
2. Runner creates place node in graph
3. Graph triggers image generation (background)
4. Graph SSE broadcasts place_created to frontend
5. Frontend updates map immediately (no image yet)
6. Image generation completes
7. Graph SSE broadcasts image_ready
8. Frontend updates left panel if current place
```

### Place Node Schema

```json
{
  "id": "place_humber_crossing",
  "name": "The Humber Crossing",
  "type": "crossing",
  "terrain": ["river", "mudflats", "reeds"],
  "atmosphere": "Grey water. Cold wind. The smell of salt and decay.",
  "position": { "lat": 53.7, "lng": -0.5 },
  "image_url": null,
  "created_by": "runner",
  "created_during": "travel_camp_to_york"
}
```

### Naming Patterns

| Type | Pattern | Examples |
|------|---------|----------|
| road | The [Adjective] [Road/Way/Path] | The Muddy Way, The North Road |
| crossing | [River] Crossing, [River] Ford | Humber Crossing, Ouse Ford |
| landmark | The [Feature], [Name]'s [Feature] | The Standing Stone, Aldric's Ridge |
| ruin | The [Ruined/Burned/Old] [Building] | The Burned Hall, The Old Chapel |
| camp | A [Terrain] [Clearing/Hollow/Ridge] | A Wooded Hollow, A Windy Ridge |

### Persistence

**Places are canon the moment they enter the graph.**

All created places persist forever:
- Player may return
- characters reference locations
- Events can occur there later
- World builds through travel

There's no "tentative" state. Once written, it's real.

### Graph Write

```python
def create_waypoint(segment):
    place = {
        "id": generate_place_id(),
        "name": generate_evocative_name(segment),
        "type": segment.terrain_type,
        "terrain": segment.terrain_features,
        "atmosphere": generate_atmosphere(segment),
        "position": segment.position,
        "created_by": "runner",
        "created_during": current_travel_id
    }

    # Write to graph (triggers SSE + image generation)
    graph.create_node("Place", place)

    return place["id"]
```

---

## Fog of War

**Purpose:** How the map shows what the player knows.

### Principle

Unknown places are hidden. Rumors create shadows.
Travel reveals. News hints.
Graph tracks visibility. Frontend renders fog.

### Visibility States

| State | Map Display | Can Travel To |
|-------|-------------|---------------|
| `unknown` | Not shown (fog) | No |
| `rumored` | Name only, faded, approximate position | Yes (may get lost) |
| `known` | Full icon, accurate position | Yes |
| `familiar` | Full detail, interior layout | Yes (faster) |

### Reveal Triggers

| Trigger | Result |
|---------|--------|
| Travel through | Becomes `known` |
| Mentioned in conversation | Becomes `rumored` |
| News/event mentions | Becomes `rumored` |
| Detailed description given | Becomes `known` |
| Player lived there | Becomes `familiar` |

### Graph Storage

Link type: `player_knows_place`

```cypher
MATCH (p:Character {id: 'char_rolf'}), (place:Place {id: 'place_york'})
CREATE (p)-[:KNOWS_PLACE {
  visibility: 'rumored',
  accuracy: 0.7,
  source: 'conversation'
}]->(place)
```

### SSE Event

```json
{
  "type": "visibility_update",
  "place_id": "place_york",
  "visibility": "known"
}
```

### Frontend Rendering

```javascript
function renderPlace(place) {
  const visibility = playerKnowledge[place.id] || 'unknown';

  switch (visibility) {
    case 'unknown':
      return null; // Don't render

    case 'rumored':
      return (
        <PlaceMarker
          position={jitterPosition(place.position)} // Approximate
          opacity={0.5}
          showIcon={false}
          label={place.name}
        />
      );

    case 'known':
      return (
        <PlaceMarker
          position={place.position}
          opacity={1.0}
          showIcon={true}
          label={place.name}
        />
      );

    case 'familiar':
      return (
        <PlaceMarker
          position={place.position}
          opacity={1.0}
          showIcon={true}
          label={place.name}
          showInterior={true}
        />
      );
  }
}
```

### Travel Revelation

When Runner updates player position:

```python
def update_player_position(player_id, place_id):
    # Update position
    graph.set_property(player_id, "current_place", place_id)

    # Reveal place
    existing = graph.get_link(player_id, place_id, "KNOWS_PLACE")
    if not existing or existing["visibility"] in ["unknown", "rumored"]:
        graph.upsert_link(player_id, place_id, "KNOWS_PLACE", {
            "visibility": "known",
            "accuracy": 1.0,
            "source": "travel"
        })
        # SSE broadcast handled by graph
```

---

## Image Generation

**Purpose:** How place images generate automatically.

### Principle

Images generate automatically when places enter graph.
No manual trigger. Graph handles it.
Frontend receives `image_ready` via SSE.

### Trigger

Place node created in graph → image generation queued

### Process

```
1. Place created in graph
2. Graph queues image generation (background task)
3. Generator creates image from place attributes
4. Image saved to frontend/public/images/places/
5. Graph updates place.image_url
6. Graph SSE broadcasts image_ready
7. Frontend updates if current place
```

### Prompt Construction

**Inputs:**
- `place.type`
- `place.name`
- `place.terrain`
- `place.atmosphere`
- Current `time_of_day`
- Current `weather`

**Format:**
```
Medieval England, 1068. {time_of_day}. {weather}.
{place.type}: {place.name}
{place.terrain}
{place.atmosphere}
Muted colors, atmospheric, painterly.
No people in frame. Landscape only.
```

**Example:**
```
Medieval England, 1068. Dusk. Light rain.
crossing: The Humber Crossing
River, mudflats, reeds
Grey water. Cold wind. The smell of salt and decay.
Muted colors, atmospheric, painterly.
No people in frame. Landscape only.
```

### Output

| Property | Value |
|----------|-------|
| Format | PNG |
| Aspect | 1:3 (tall, atmospheric) |
| Storage | `frontend/public/images/places/{place_id}.png` |
| URL in graph | `/images/places/{place_id}.png` |

### Implementation

```python
async def generate_place_image(place):
    prompt = build_image_prompt(place)

    # Generate image (async)
    image_data = await image_generator.generate(
        prompt=prompt,
        aspect_ratio="1:3",
        style="painterly"
    )

    # Save to disk
    path = f"frontend/public/images/places/{place['id']}.png"
    save_image(image_data, path)

    # Update graph
    url = f"/images/places/{place['id']}.png"
    graph.set_property(place['id'], "image_url", url)

    # SSE broadcast happens automatically from graph
```

### Graph Hook

When place is created, graph triggers generation:

```python
def on_place_created(place):
    # Broadcast place_created (no image yet)
    sse_manager.broadcast({
        "type": "place_created",
        "place_id": place["id"],
        "name": place["name"],
        "image_url": None
    })

    # Queue image generation
    background_tasks.add(generate_place_image(place))
```

When image is ready:

```python
def on_image_ready(place_id, image_url):
    sse_manager.broadcast({
        "type": "image_ready",
        "place_id": place_id,
        "image_url": image_url
    })
```

---

## Discussion Trees

**Purpose:** How companions have evergreen conversations.

### Principle

Each companion has discussion trees — pre-generated conversation topics.
Generated in background. Deleted when used. Regenerated when low.
Companions feel alive even when nothing's happening.

### Lifecycle

**Generation**

Trigger: Character becomes companion OR remaining branches < 5

Method: Subagent in background bash task

```python
bash(
    command='''
        cd agents/discussion_generator && \
        claude -p "Generate discussion trees for char_aldric" \
        --allowedTools "Write,Read" \
        --add-dir ../../
    ''',
    run_in_background=true
)
```

Output: 5-10 topics, 3-4 depth each

Storage: `playthroughs/default/discussion_trees/{char_id}.json`

**Usage**

| Trigger | Action |
|---------|--------|
| Player clicks portrait | Shows topic list |
| Player selects topic | Tree activates, narration begins |
| 10+ seconds idle during travel | Companion initiates (if content exists) |
| Branch explored | Branch DELETED immediately |

**Regeneration**

Trigger: Remaining unexplored branches < 5

Method: Same subagent, background bash

Timing: Automatic — runs when threshold crossed

Note: Old trees deleted on use, new trees generated fresh

### Tree Structure

```json
{
  "topic": {
    "id": "aldric_past_battles",
    "name": "Past Battles",
    "opener": {
      "narrator": "Aldric stares into the fire, lost in memory.",
      "clickable": {
        "fire": {
          "speaks": "What are you thinking about?",
          "response": {
            "speaker": "char_aldric",
            "text": "Old fights. Men I killed. Men I couldn't save.",
            "clickable": {
              "killed": {
                "speaks": "Tell me about the fights.",
                "response": {
                  "speaker": "char_aldric",
                  "text": "At Stamford Bridge, I stood in the shield wall..."
                }
              },
              "save": {
                "speaks": "Who couldn't you save?",
                "response": {
                  "beat": "His jaw tightens.",
                  "speaker": "char_aldric",
                  "text": "My brother. He was right beside me when the arrow took him."
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Player Triggered

1. Player clicks companion portrait
2. Frontend shows topic list:
   ```
   - Past Battles
   - His Family
   - What He Thinks of Normans
   - A Question for You
   ```
3. Player clicks topic
4. Narrator activates tree, streams narration
5. Each branch explored is deleted

### Idle Triggered

**Conditions:**
- Traveling (not in scene)
- No player input for 10+ seconds
- No injection pending
- Unexplored content exists

**Detection:** Frontend responsibility. Frontend tracks idle time and triggers initiation.

**Presentation:**
```
[silence]
Aldric clears his throat.
"Can I ask you something?"
[tree activates]
```

**Dismissal:**
- Player ignores → silence
- "Not now" → companion respects
- Topic remains available (until used elsewhere)

### Generation Prompt

File: `/prompts/discussion_generator.md`

**Inputs:**
- `character.backstory`
- `character.beliefs`
- `character.relationship_to_player`
- Current narrative context
- Topics already explored (to avoid)

**Outputs:**
- Topic list with full trees
- Each topic 3-4 layers deep
- Natural conversation flow
- Seeds for future payoffs

### File Format

`playthroughs/default/discussion_trees/char_aldric.json`:

```json
{
  "topics": [
    {
      "id": "aldric_past_battles",
      "name": "Past Battles",
      "opener": { ... }
    },
    {
      "id": "aldric_family",
      "name": "His Family",
      "opener": { ... }
    }
  ]
}
```

### Deletion on Use

When a branch is explored:

```python
def on_branch_explored(char_id, topic_id, branch_path):
    tree_file = f"playthroughs/default/discussion_trees/{char_id}.md"
    tree = load_tree(tree_file)

    # Delete the explored branch
    delete_branch(tree, topic_id, branch_path)

    # Save updated tree
    save_tree(tree_file, tree)

    # Check if regeneration needed
    if count_unexplored_branches(tree) < 5:
        trigger_regeneration(char_id)
```
