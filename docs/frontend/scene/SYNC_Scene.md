# Scene View — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: ngram repair agent
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- Scene view layout with header, banner, people, voices, actions
- CenterStage with animated line rendering and reading time calculations
- Clickable text/word interaction system
- Integration with useMoments hook
- Dark atmospheric styling with Tailwind CSS

**What's still being designed:**
- Voice selection algorithm (which narratives speak, how many)
- Choice generation (how to make choices feel emergent)
- Conversation flow (what happens when you talk to someone)

**What's proposed (v2+):**
- Real-time image generation
- Audio/ambient sound integration
- Enhanced animations and transitions

---

## CURRENT STATE

The scene view is **implemented and functional**. It is the main game view where players experience the world.

**Implementation:** `frontend/components/scene/`

| File | Purpose |
|------|---------|
| `SceneView.tsx` | Main scene component - header, banner, people, voices, actions |
| `CenterStage.tsx` | Animated text display with reading time, typing indicators, clickable words |
| `SceneHeader.tsx` | Scene title/location header |
| `SceneBanner.tsx` | Scene banner image display |
| `SceneImage.tsx` | Scene image component |
| `Atmosphere.tsx` | Atmosphere text display |
| `CharacterRow.tsx` | Character display row |
| `HotspotRow.tsx` | Hotspot interaction row |
| `Hotspot.tsx` | Individual hotspot component |
| `ObjectRow.tsx` | Object display row |
| `SceneActions.tsx` | Action buttons |
| `SettingStrip.tsx` | Setting/location strip |

**Key Features Implemented:**
- Scene renders with atmosphere, location header, banner image
- People present are displayed with portraits and descriptions
- Voices display (sorted by weight, top 4 shown with opacity based on weight)
- Action buttons: Talk (per person), Travel, Write
- CenterStage provides animated text reveal with reading time calculations
- Clickable word interactions for deeper exploration

---

## RECENT CHANGES

### 2025-12-19: Expanded scene PATTERNS template sections

- **What:** Added CHAIN, problem/pattern framing, scope, dependencies,
  inspirations, principles, and gaps sections to `PATTERNS_Scene.md`.
- **Why:** Resolve doc-template drift for the scene patterns document and keep
  the chain aligned with the frontend scene implementation.
- **Files:** `docs/frontend/scene/PATTERNS_Scene.md`
- **Struggles/Insights:** Kept descriptions scoped to presentation behavior to
  avoid implying unverified backend generation logic.

### 2025-12-19: Map moment components to scene docs

- **What:** Linked `frontend/components/moment/**` to the Scene docs in `modules.yaml` and added a DOCS reference in `frontend/components/moment/index.ts`.
- **Why:** Establish documentation mapping for the moment UI components used by Scene.
- **Files:** `modules.yaml`, `frontend/components/moment/index.ts`
- **Struggles/Insights:** None.

---

## DESIGN QUESTIONS (from PATTERNS)

These remain open for iteration:

| Question | Status | Notes |
|----------|--------|-------|
| Voice selection (which narratives speak) | Open | Currently shows top 4 by weight |
| How many voices per scene | Partially resolved | Limited to 4 in UI |
| Choice emergence (not menu feel) | Open | Actions are hardcoded types |
| Character consistency across scenes | Open | Needs character sheets in prompt |
| Image generation pipeline | Partial | Static images used, no dynamic gen |
| Conversation flow | Open | TBD how dialogue works |

---

## INTEGRATION

**Hooks:**
- `useMoments` - Used by CenterStage for moment system integration
- `useGameState` - Used for broader game state (may deprecate)

**API:**
- Scene data comes from `/api/view` (see `docs/physics/API_Physics.md`)

**Related Components:**
- `frontend/components/moment/` - MomentDisplay, MomentStream, ClickableText
- `frontend/components/panel/` - Right panel with Chronicle/Ledger tabs

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement or VIEW_Extend

**Where things are:**
- Scene components: `frontend/components/scene/`
- Main layout: `SceneView.tsx` (simpler) or `CenterStage.tsx` (animated)
- Moment integration: Look at `useMoments` hook

**Key patterns:**
- Dark atmospheric styling (stone-900 backgrounds, amber accents)
- Voices sorted by weight, opacity reflects weight
- CenterStage uses reading time calculations for pacing

**What might need work:**
- Voice selection algorithm (currently just top 4 by weight)
- Making choices feel emergent vs. menu-like
- Conversation flow when talking to characters

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Scene view is implemented and works. The core layout exists with header, image, people, voices, and actions. CenterStage provides animated text reveal for immersive experience.

**Key design decisions made:**
- Top 4 voices shown, sorted by weight
- Opacity reflects voice weight (0.5 + weight * 0.5)
- Talk action per person, plus Travel and Write global actions
- Reading time calculations: 40ms per char, 800-4000ms bounds

**Needs your input:**
- Voice selection algorithm refinement
- How should conversation flow work?
- Should choice buttons feel different from current hardcoded actions?

## RECENT CHANGES

### 2025-12-19: Documented scene module mapping and DOCS link

- **What:** Added module mapping in `modules.yaml` and linked `SceneView.tsx` to scene docs.
- **Why:** Ensure scene components resolve to their dedicated documentation chain.
- **Files:** `modules.yaml`, `frontend/components/scene/SceneView.tsx`
- **Struggles/Insights:** None.

### 2025-12-19: Expanded scene validation template

- **What:** Filled missing template sections in `VALIDATION_Scene.md` (invariants, properties, error conditions, test coverage, verification procedure, sync status, gaps).
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the scene validation document and keep the chain complete.
- **Files:** `docs/frontend/scene/VALIDATION_Scene.md`
- **Struggles/Insights:** Kept statements aligned with current SceneView/SceneBanner behavior to avoid unverified claims.

### 2025-12-19: Verified scene validation doc completeness

- **What:** Re-checked `VALIDATION_Scene.md` against the template requirements; no additional edits needed.
- **Why:** Confirmed the repair target is already satisfied before closing the issue.
- **Files:** `docs/frontend/scene/VALIDATION_Scene.md`
- **Struggles/Insights:** None; verification only.

---

## POINTERS

| What | Where |
|------|-------|
| Scene components | `frontend/components/scene/` |
| Moment components | `frontend/components/moment/` |
| useMoments hook | `frontend/hooks/useMoments.ts` |
| Types | `frontend/types/game.ts` |
| Design patterns | `docs/frontend/scene/PATTERNS_Scene.md` |
| Frontend overview | `docs/frontend/SYNC_Frontend.md` |

---

## Agent Observations

### Remarks
- The validation doc now mirrors the actual SceneView/SceneBanner fallbacks, reducing drift risk.

### Suggestions
- [ ] Add basic component tests for SceneView and SceneBanner to cover fallback rendering.
- [ ] Add a Playwright smoke test for voice ordering and action button presence.

### Propositions
- Consider a shared scene fixture in frontend tests to standardize validation inputs.
