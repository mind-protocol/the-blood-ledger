# Frontend — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Presentation_Layer.md
BEHAVIORS:      ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:      ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:     ./VALIDATION_Frontend_Invariants.md
THIS:           IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:           ./TEST_Frontend_Coverage.md
SYNC:           ./SYNC_Frontend.md

IMPL:           frontend/app/page.tsx
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
frontend/
├── app/                          # Next.js App Router pages
│   ├── page.tsx                  # Main entry - loads GameClient
│   ├── layout.tsx                # Root layout with providers
│   ├── start/page.tsx            # Opening/start screen
│   ├── map/page.tsx              # Map view
│   ├── scenarios/page.tsx        # Scenario selection
│   └── playthroughs/[id]/page.tsx # Dynamic playthrough route
├── components/                   # React components
│   ├── GameClient.tsx            # Main game wrapper, handles loading
│   ├── GameLayout.tsx            # Layout: scene + right panel
│   ├── Providers.tsx             # Context providers
│   ├── scene/                    # Scene rendering components
│   ├── moment/                   # Moment system components
│   ├── map/                      # Map display components
│   ├── panel/                    # Right panel tabs
│   ├── voices/                   # Internal thoughts display
│   ├── chronicle/                # Chronicle display
│   ├── minimap/                  # Minimap component
│   ├── debug/                    # Debug panel
│   └── ui/                       # Generic UI components
├── hooks/                        # Custom React hooks
│   ├── useGameState.ts           # Main game state management
│   └── useMoments.ts             # Moment system state
├── lib/                          # Utilities
│   ├── api.ts                    # API client functions
│   └── map/                      # Map utilities
├── types/                        # TypeScript definitions
│   ├── game.ts                   # Core game types
│   ├── moment.ts                 # Moment types
│   └── map.ts                    # Map types
├── data/                         # Static data
│   └── game-state.json           # Fallback static state
└── public/                       # Static assets
    └── playthroughs/             # Playthrough images
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `hooks/useGameState.ts` | Main game state, API integration | `useGameState`, transform helpers | ~423 | WATCH |
| `lib/api.ts` | Backend API client | `getMap`, `getFaces`, `clickMoment`, etc. | ~419 | WATCH |
| `types/game.ts` | TypeScript type definitions | `GameState`, `Scene`, `Moment`, etc. | ~312 | OK |
| `hooks/useMoments.ts` | Moment system state, SSE | `useMoments` | ~197 | OK |
| `types/moment.ts` | Moment-specific types | `Moment`, `MomentTransition` | ~98 | OK |
| `types/map.ts` | Map-specific types | `MapLocation`, `MapRegion` | ~151 | OK |
| `components/GameClient.tsx` | Game wrapper, loading states | `GameClient` | ~106 | OK |
| `components/GameLayout.tsx` | Scene + panel layout | `GameLayout` | ~63 | OK |
| `app/page.tsx` | Main entry point | Page component | ~12 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

### Scene Components

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `components/scene/CenterStage.tsx` | Main scene display area | ~435 | WATCH |
| `components/scene/SceneView.tsx` | Scene wrapper | ~120 | OK |
| `components/scene/SceneImage.tsx` | Scene image display | ~102 | OK |
| `components/scene/HotspotRow.tsx` | Row of hotspots | ~79 | OK |
| `components/scene/Hotspot.tsx` | Single hotspot element | ~77 | OK |
| `components/scene/SceneBanner.tsx` | Scene banner image | ~69 | OK |
| `components/scene/CharacterRow.tsx` | Character display row | ~66 | OK |
| `components/scene/ObjectRow.tsx` | Object display row | ~63 | OK |
| `components/scene/SettingStrip.tsx` | Setting/location strip | ~61 | OK |
| `components/scene/SceneHeader.tsx` | Scene header | ~42 | OK |
| `components/scene/SceneActions.tsx` | Action buttons | ~33 | OK |
| `components/scene/Atmosphere.tsx` | Atmospheric text | ~20 | OK |

### Moment Components

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `components/moment/MomentDebugPanel.tsx` | Debug info display | ~221 | OK |
| `components/moment/MomentDisplay.tsx` | Single moment display | ~201 | OK |
| `components/moment/ClickableText.tsx` | Text with clickable words | ~137 | OK |
| `components/moment/MomentStream.tsx` | Moment list/stream | ~122 | OK |

Docs for moment components live with the Scene module (`docs/frontend/scene/`), since Scene owns the moment display experience.

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Component-based React with Custom Hooks

**Why this pattern:**
- Next.js App Router enables server/client component split
- Custom hooks encapsulate state logic, keeping components presentational
- Clear separation: hooks manage state, components render UI

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Custom Hook | `useGameState`, `useMoments` | Encapsulate stateful logic, reusable across components |
| Parallel Fetch | `useGameState` initial load | Faster loading via Promise.all |
| SSE Subscription | `useMoments` | Real-time updates without polling |
| Transform Layer | `transformViewToScene` | Convert API shape to UI shape |
| Guard Clause | Click handlers | Prevent concurrent operations |

### Anti-Patterns to Avoid

- **Prop Drilling**: Use context or compose hooks instead of passing props through many layers
- **Direct State Mutation**: Always use setState/dispatch, never mutate state directly
- **God Component**: Split CenterStage.tsx if it grows beyond 500 lines
- **Mixing Concerns**: Keep API logic in hooks/lib, not in components

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Hooks | State logic, API calls | UI rendering | Hook return values |
| API Client | Network requests, error handling | Business logic | Typed functions |
| Components | UI rendering, event handling | State management | Props |

---

## SCHEMA

### GameState (Client)

```yaml
GameState:
  required:
    - player: Player          # Current player state
    - currentScene: Scene     # Rendered scene
    - characters: Character[] # All known characters
    - voices: Voice[]         # Internal thoughts
    - chronicle: ChronicleEntry[]
    - ledger: LedgerEntry[]
    - conversations: Conversation[]
    - map: MapRegion[]
  optional:
    - sceneTree: SceneTree    # Raw Narrator response
```

### Scene

```yaml
Scene:
  required:
    - id: string
    - type: SceneType
    - name: string
    - location: string
    - timeOfDay: TimeOfDay
    - weather: Weather
    - atmosphere: string[]
    - hotspots: Hotspot[]
    - actions: SceneAction[]
  optional:
    - placeId: string
    - bannerImage: string
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Main page load | `app/page.tsx:1` | User navigates to / |
| Game state init | `hooks/useGameState.ts:31` | GameClient mounts |
| Moment click | `hooks/useMoments.ts:96` | User clicks word |
| SSE subscription | `hooks/useMoments.ts:132` | useMoments mounts |

---

## DATA FLOW

### Initial Load Flow

```
┌─────────────────┐
│  app/page.tsx   │
└────────┬────────┘
         │ renders
         v
┌─────────────────┐
│  GameClient.tsx │ ← uses useGameState
└────────┬────────┘
         │ fetches
         v
┌─────────────────┐
│  lib/api.ts     │ ← API client
│  (parallel)     │
└────────┬────────┘
         │ transforms
         v
┌─────────────────┐
│  GameState      │ ← hooks/useGameState.ts
└────────┬────────┘
         │ renders
         v
┌─────────────────┐
│  GameLayout.tsx │ ← Scene + Panel
└─────────────────┘
```

### Moment Interaction Flow

```
┌─────────────────┐
│  ClickableText  │ ← User clicks word
└────────┬────────┘
         │ calls
         v
┌─────────────────┐
│  useMoments     │ ← clickWord()
│  hook           │
└────────┬────────┘
         │ POST
         v
┌─────────────────┐
│  /api/moments/  │ ← Backend
│  click          │
└────────┬────────┘
         │ response
         v
┌─────────────────┐
│  State update   │ ← activeMoments, spokenMoments
└────────┬────────┘
         │ triggers
         v
┌─────────────────┐
│  Re-render      │
└─────────────────┘
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
app/page.tsx
    └── imports → GameClient.tsx
        └── imports → useGameState.ts
            └── imports → lib/api.ts
            └── imports → types/game.ts
        └── imports → GameLayout.tsx
            └── imports → SceneView.tsx
            └── imports → RightPanel.tsx
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `react` | UI framework | All components |
| `next` | App Router, Link | Pages, components |
| `tailwindcss` | Styling | All components |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| gameState | `useGameState` | Per-page | Refreshed on mount, persists during session |
| activeMoments | `useMoments` | Per-location | Updated via API and SSE |
| spokenMoments | `useMoments` | Per-location | Accumulates during session |
| isLoading | Both hooks | Per-hook | Transient during fetches |

### State Transitions

```
Initial → Loading → (Loaded | Error | NeedsOpening)
         ↑                     |
         └──── Refresh ────────┘
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Next.js renders page.tsx
2. GameClient mounts
3. useGameState hook initializes
4. Health check → parallel API fetch → transform
5. setGameState triggers render
6. GameLayout renders scene + panel
```

### Main Loop / Request Cycle

```
1. User interacts (click word, submit action)
2. Hook function called (clickWord, sendAction)
3. API request sent
4. State updated on response
5. React re-renders affected components
6. SSE may push additional updates
```

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `.env.local` | `http://localhost:8000` | Backend API URL |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that should reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `frontend/app/page.tsx` | TBD | `// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM initial load | `hooks/useGameState.ts:39-167` |
| ALGORITHM click traversal | `hooks/useMoments.ts:96-129` |
| BEHAVIOR B1 (initial load) | `hooks/useGameState.ts:39` |
| BEHAVIOR B3 (moment click) | `hooks/useMoments.ts:96` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

Files approaching WATCH/SPLIT status:

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `hooks/useGameState.ts` | ~423L | <400L | `hooks/transformers.ts` | Transform helper functions |
| `lib/api.ts` | ~419L | <400L | `lib/api/moments.ts` | Moment-specific API functions |
| `components/scene/CenterStage.tsx` | ~435L | <400L | `components/scene/CenterStageContent.tsx` | Sub-sections |

### Missing Implementation

- [ ] Add DOCS reference to frontend/app/page.tsx
- [ ] Consider splitting CenterStage.tsx

### Ideas

- IDEA: Extract transform functions to separate file
- IDEA: Create API client class instead of loose functions

### Questions

- QUESTION: Should we add error boundaries around scene components?
- QUESTION: Is 400-line threshold appropriate for React components?
