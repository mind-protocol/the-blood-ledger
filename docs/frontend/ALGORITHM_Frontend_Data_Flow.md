# Frontend — Algorithm: Data Flow and State Transformation

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against current implementation
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
THIS:            ALGORITHM_Frontend_Data_Flow.md (you are here)
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/hooks/useGameState.ts
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

The frontend fetches game state from multiple backend API endpoints and transforms it into a unified GameState structure for rendering. Real-time updates arrive via SSE and are merged into state. The moment system provides an interactive layer where clicking words triggers graph traversals.

---

## DATA STRUCTURES

### GameState (Client-Side)

```
Unified structure consumed by React components:
- player: { name, title, day, location }
- currentScene: Scene (transformed from view/moments)
- sceneTree: SceneTree (raw Narrator response)
- characters: Character[]
- voices: Voice[]
- chronicle: ChronicleEntry[]
- ledger: LedgerEntry[]
- conversations: Conversation[]
- map: MapRegion[]
```

### Moment (from API)

```
Represents a piece of narrative content:
- id: string
- text: string
- type: 'narration' | 'dialogue' | 'action' | etc.
- status: 'active' | 'possible' | 'spoken'
- weight: number (0-1, prominence)
- clickable_words: string[]
- speaker?: string (for dialogue)
```

### MomentTransition (from API)

```
Defines traversal between moments:
- from_id: string
- to_id: string
- trigger: string
- require_words: string[]
- weight_transfer: number
- consumes_origin: boolean
```

---

## ALGORITHM: Initial State Loading

### Step 1: Health Check

Check if backend is available before making API calls.

```
healthy = await fetch('/health').ok
if not healthy:
    setIsConnected(false)
    setError('Backend not available')
    return
```

### Step 2: Parallel Data Fetch

Fetch multiple endpoints concurrently for faster loading.

```
[mapData, facesData, ledgerData, chronicleData] = await Promise.all([
    api.getMap(playthroughId),
    api.getFaces(playthroughId),
    api.getLedger(playthroughId),
    api.getChronicle(playthroughId)
])
```

### Step 3: Fetch Current View

Get the moment system's current state.

```
view = await api.getCurrentView(playthroughId)
if view has no moments:
    setNeedsOpening(true)
    return
```

### Step 4: Transform to GameState

Convert API responses to unified client structure.

```
scene = transformViewToScene(view)
voices = transformMomentsToVoices(view.moments)
characters = merge(facesData.companions, facesData.known_characters)
map = transformMapData(mapData)
ledger = transformLedgerData(ledgerData)
chronicle = transformChronicleData(chronicleData)

gameState = { player, currentScene: scene, sceneTree: view, ... }
```

---

## ALGORITHM: View to Scene Transformation

### Step 1: Extract Location

```
location = view.location
sceneName = location.name.toUpperCase()
sceneType = mapPlaceType(location.type)
```

### Step 2: Build Atmosphere

```
narrationMoments = view.moments.filter(m => m.type in ['narration', 'action'])
atmosphereText = narrationMoments.map(m => m.text)
if empty:
    atmosphereText = ['The scene unfolds before you...']
```

### Step 3: Extract Clickable Words

```
clickables = []
for transition in view.transitions:
    for word in transition.words:
        if word not in clickables:
            clickables.append(word)
```

### Step 4: Build Hotspots

Combine clickable words and characters into interactive elements.

```
hotspots = [
    ...clickables.map(word => {
        type: 'object',
        name: word,
        position: calculated_grid_position,
        actions: [{ id: `click_${word}`, label: word }]
    }),
    ...view.characters.map(char => {
        type: 'person',
        name: char.name,
        imageUrl: character_image_path,
        actions: [{ id: `talk_${char.id}`, label: 'Talk' }]
    })
]
```

---

## ALGORITHM: Moment Click Traversal

### Step 1: Guard Against Concurrent Clicks

```
if isLoading:
    return  // Ignore click while traversal in progress
setIsLoading(true)
```

### Step 2: Call Backend API

```
response = await api.clickMoment(playthroughId, momentId, word, tick)
```

### Step 3: Update State Based on Response

```
if response.traversed and response.target_moment:
    if response.consumed_origin:
        // Move origin moment from active to spoken
        origin = activeMoments.find(m => m.id == momentId)
        spokenMoments.push({ ...origin, status: 'spoken' })
        activeMoments.remove(origin)

    // Add new active moments
    activeMoments.extend(response.new_active_moments)
```

---

## KEY DECISIONS

### D1: Moment Status Change

```
IF transition.consumes_origin:
    Origin moment moves to 'spoken' (history)
    No longer clickable
ELSE:
    Origin moment remains 'active'
    Can be clicked again with different words
```

### D2: Empty View Handling

```
IF view.moments.length == 0:
    User needs opening sequence
    Set needsOpening = true
    Do not build empty scene
ELSE:
    Transform and display normally
```

### D3: SSE vs Polling

```
Frontend uses SSE for real-time updates (not polling):
    moment_activated: Add to activeMoments
    moment_spoken: Move from active to spoken
    weight_updated: Update weight in activeMoments
Reason: Lower latency, server-driven updates
```

---

## DATA FLOW

### Initial Load Flow

```
Page Mount
    |
    v
useGameState hook initializes
    |
    v
Health check (/health)
    |
    +-- fail --> Error state, show toast
    |
    +-- pass --> Continue
         |
         v
Parallel API fetch (map, faces, ledger, chronicle)
    |
    v
Fetch current view (/api/view/{id})
    |
    +-- no moments --> needsOpening = true
    |
    +-- has moments --> Transform to GameState
         |
         v
setGameState(state)
    |
    v
React renders components
```

### Click Interaction Flow

```
User clicks word in moment
    |
    v
useMoments.clickWord(momentId, word)
    |
    v
POST /api/moments/click
    |
    v
Backend processes traversal
    |
    v
Response with new moments
    |
    v
Update activeMoments, spokenMoments
    |
    v
React re-renders
```

### SSE Update Flow

```
Backend event occurs
    |
    v
SSE pushes event to client
    |
    v
subscribeToMomentStream callback fires
    |
    +-- moment_activated --> Add to activeMoments
    +-- moment_spoken --> Move to spokenMoments
    +-- weight_updated --> Update weight
    +-- error --> Show reconnection message
```

---

## COMPLEXITY

**Time:** O(n) for initial load where n = total entities across endpoints

**Space:** O(n) for GameState storage

**Bottlenecks:**
- Parallel fetch waits for slowest endpoint
- Large moment histories could grow spokenMoments array
- SSE reconnection during network instability

---

## HELPER FUNCTIONS

### `mapPlaceType(type: string)`

**Purpose:** Convert backend place types to SceneType enum

**Logic:** Simple mapping lookup with 'CAMP' fallback

### `transformViewToScene(view: CurrentView)`

**Purpose:** Convert moment system view to Scene format

**Logic:** Extract location, build atmosphere from moments, create hotspots

### `transformMomentsToVoices(moments: Moment[])`

**Purpose:** Extract dialogue moments as Voice objects

**Logic:** Filter for dialogue type, map to Voice structure

### `subscribeToMomentStream(callbacks)`

**Purpose:** Establish SSE connection with event handlers

**Logic:** Create EventSource, attach listeners, return close function

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| `/health` | GET | boolean (ok status) |
| `/api/{id}/map` | GET | places[], connections[] |
| `/api/{id}/faces` | GET | companions[], known_characters[] |
| `/api/{id}/ledger` | GET | items[] |
| `/api/{id}/chronicle` | GET | events[] |
| `/api/view/{id}` | GET | CurrentView |
| `/api/moments/click` | POST | ClickMomentResponse |
| `/api/moments/stream/{id}` | SSE | Real-time events |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Document caching strategy (currently none)
- [ ] Document error recovery for partial fetch failures
- IDEA: Implement optimistic updates for click interactions
- IDEA: Add local caching for offline support
- QUESTION: Should moment history be paginated for long playthroughs?
