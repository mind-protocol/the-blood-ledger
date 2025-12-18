# UI and API Changes for Moment Graph Architecture

This document details the required changes to the frontend and API to support the Moment Graph architecture.

---

## API Endpoints (New)

### 1. GET /api/moments/current/{playthrough_id}

Get visible moments for the current scene based on player location and present entities.

**Request:**
```
GET /api/moments/current/pt_abc123?player_id=char_player&location=place_camp
```

**Response:**
```json
{
  "moments": [
    {
      "id": "moment_aldric_edmund_hook",
      "text": "Aldric's eyes darken when you mention Edmund's name.",
      "type": "narration",
      "status": "active",
      "weight": 0.8,
      "tone": "guarded",
      "clickable_words": ["Edmund", "eyes", "name"]
    }
  ],
  "transitions": [
    {
      "from_id": "moment_aldric_edmund_hook",
      "to_id": "moment_aldric_ask_edmund",
      "trigger": "click",
      "require_words": ["Edmund", "knew", "before"]
    }
  ],
  "active_count": 3
}
```

### 2. POST /api/moments/click

Handle player clicking a word in a moment. This is the HOT PATH - must be <50ms.

**Request:**
```json
{
  "playthrough_id": "pt_abc123",
  "moment_id": "moment_aldric_edmund_hook",
  "word": "Edmund",
  "tick": 1234
}
```

**Response:**
```json
{
  "status": "ok",
  "traversed": true,
  "target_moment": {
    "id": "moment_aldric_ask_edmund",
    "text": "You knew Edmund before all this?",
    "type": "player_click",
    "status": "active"
  },
  "consumed_origin": true,
  "new_active_moments": [
    {
      "id": "moment_aldric_edmunds_past",
      "text": "Knew him. We all knew him...",
      "speaker": "char_aldric"
    }
  ]
}
```

### 3. GET /api/moments/{moment_id}

Get a single moment by ID with full details.

**Response:**
```json
{
  "id": "moment_aldric_edmund_hook",
  "text": "Aldric's eyes darken when you mention Edmund's name.",
  "type": "narration",
  "status": "active",
  "weight": 0.8,
  "tone": "guarded",
  "tick_created": 1000,
  "tick_spoken": null,
  "attachments": [
    {"target_id": "char_aldric", "target_type": "Character", "presence_required": true}
  ],
  "can_lead_to": [
    {"to_id": "moment_aldric_ask_edmund", "trigger": "click", "require_words": ["Edmund"]}
  ],
  "speakers": [
    {"character_id": "char_aldric", "weight": 1.0}
  ]
}
```

### 4. POST /api/moments/surface

Manually surface a moment (for testing/admin).

**Request:**
```json
{
  "moment_id": "moment_aldric_edmund_hook",
  "playthrough_id": "pt_abc123"
}
```

### 5. SSE /api/moments/stream/{playthrough_id}

Real-time updates for moment state changes.

**Events:**
- `moment_activated`: A moment became active
- `moment_spoken`: A moment was spoken
- `moment_decayed`: A moment decayed
- `weight_updated`: A moment's weight changed

```
event: moment_activated
data: {"moment_id": "moment_x", "weight": 0.85, "speaker": "char_aldric"}

event: moment_spoken
data: {"moment_id": "moment_x", "text": "...", "speaker": "char_aldric"}
```

---

## API Endpoints (Modified)

### POST /api/scene/click

Update to use moment graph traversal instead of scene tree navigation.

**Changes:**
- Call `MomentTraversal.handle_click()` instead of scene tree lookup
- Return target moment as the "response"
- Update scene.json with new active moments

### GET /api/scene/current/{playthrough_id}

Update to include active moments in the response.

**Changes:**
- Add `active_moments: []` to scene response
- Derive clickable words from CAN_LEAD_TO links

---

## Frontend Components (New)

### 1. ClickableText.tsx

Renders text with clickable words that trigger traversal.

```tsx
interface ClickableTextProps {
  text: string;
  clickableWords: string[];  // From CAN_LEAD_TO require_words
  onWordClick: (word: string) => void;
  disabled?: boolean;  // While traversal in progress
}
```

**Behavior:**
- Scan text for words in `clickableWords` (case-insensitive)
- Render matches as styled spans with click handlers
- Visual feedback: underline, hover glow, cursor pointer
- Disabled state during traversal

### 2. MomentDisplay.tsx

Renders a single moment with appropriate styling.

```tsx
interface MomentDisplayProps {
  moment: Moment;
  onWordClick?: (word: string) => void;
  isLatest?: boolean;  // For animation
}
```

**Behavior:**
- Different rendering for narration vs dialogue vs player actions
- Speaker attribution for dialogue (from SAID link)
- Tone-based styling (bitter = cold color, warm = amber)
- Animation for newly-surfaced moments

### 3. MomentStream.tsx

Replaces DialogueStream with moment-aware rendering.

```tsx
interface MomentStreamProps {
  moments: Moment[];  // Ordered by tick_spoken
  activeMoments: Moment[];  // Currently visible/clickable
  onWordClick: (momentId: string, word: string) => void;
  isLoading?: boolean;
}
```

**Behavior:**
- Render spoken moments as history
- Render active moments as interactive
- Auto-scroll to latest
- Loading state during traversal

### 4. MomentDebugPanel.tsx (Optional)

Debug visualization for moment weights and graph state.

```tsx
interface MomentDebugPanelProps {
  moments: Moment[];
  showWeights: boolean;
  showLinks: boolean;
}
```

**Behavior:**
- Show all possible/active moments with weights
- Visual weight bars (0-1)
- CAN_LEAD_TO arrows between moments
- Status badges (possible/active/spoken/dormant)

---

## Frontend Components (Modified)

### CenterStage.tsx

Update to use MomentStream instead of rendering narration directly.

**Changes:**
- Replace narration array with moments from API
- Pass clickable words derived from graph
- Handle click events -> API call -> update state

### useDialogueStream.ts

Update hook to work with moment-based streaming.

**Changes:**
- Connect to moment SSE endpoint
- Handle moment_activated, moment_spoken events
- Maintain ordered list of spoken moments
- Track active moments separately

---

## Type Definitions

### frontend/types/moment.ts

```typescript
export interface Moment {
  id: string;
  text: string;
  type: 'narration' | 'dialogue' | 'hint' | 'player_click' | 'player_freeform' | 'player_choice';
  status: 'possible' | 'active' | 'spoken' | 'dormant' | 'decayed';
  weight: number;
  tone?: string;
  tick_created: number;
  tick_spoken?: number;
  speaker?: string;  // Character ID, from SAID link
}

export interface MomentTransition {
  from_id: string;
  to_id: string;
  trigger: 'click' | 'wait' | 'auto';
  require_words?: string[];
  weight_transfer: number;
  consumes_origin: boolean;
}

export interface MomentClickResponse {
  status: 'ok' | 'no_match' | 'error';
  traversed: boolean;
  target_moment?: Moment;
  consumed_origin: boolean;
  new_active_moments: Moment[];
}

export interface CurrentMomentsResponse {
  moments: Moment[];
  transitions: MomentTransition[];
  active_count: number;
}
```

---

## Bidirectional Links

Some CAN_LEAD_TO links should be bidirectional for conversations that can flow both ways.

### When to Use Bidirectional

- **Topic exploration**: Player can ask about A then B, or B then A
- **Clarification loops**: "Can you explain that?" -> explanation -> "Tell me more" -> back
- **Player-driven order**: Multiple independent questions

### Implementation

```yaml
links:
  - type: can_lead_to
    from: moment_topic_a
    to: moment_topic_b
    trigger: click
    bidirectional: true  # Creates link in both directions
    require_words: ["about", "tell"]
    weight_transfer: 0.3
```

GraphOps already supports `bidirectional: true` on `add_can_lead_to()`.

### API Handling

When querying transitions, both directions are returned:
- A -> B (if A is active)
- B -> A (if B is active)

---

## Migration Path

### Phase 1: Parallel Running
1. Keep existing scene tree system working
2. Add moment endpoints alongside existing
3. Frontend uses old system by default
4. Debug panel shows moment state

### Phase 2: Integration
1. Derive scene.narration from active moments
2. Click handler calls moment API first, falls back to old
3. SSE events update both systems

### Phase 3: Replacement
1. Remove scene tree navigation
2. All clicks go through moment graph
3. Narrator generates moments, not scene trees

---

## Performance Requirements

| Operation | Target | Current |
|-----------|--------|---------|
| Click traversal | <50ms | TBD |
| Get current moments | <100ms | TBD |
| SSE latency | <50ms | TBD |
| Weight recalc (tick) | <10ms | N/A |

The click path is HOT - no LLM calls, pure graph traversal.

---

## File Locations

### API
- `engine/api/moments.py` - Moment-specific endpoints (NEW)
- `engine/api/app.py` - Mount moments router

### Engine
- `engine/moment_graph/` - Core graph operations (EXISTS)
- `engine/moment_graph/api_models.py` - Pydantic models for API (NEW)

### Frontend
- `frontend/components/moment/` - Moment components (NEW)
  - `ClickableText.tsx`
  - `MomentDisplay.tsx`
  - `MomentStream.tsx`
  - `MomentDebugPanel.tsx`
- `frontend/hooks/useMoments.ts` - Moment state hook (NEW)
- `frontend/types/moment.ts` - Type definitions (NEW)
