# Scene View — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: ngram repair agent
STATUS: CANONICAL
```

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

## IN PROGRESS

Documentation alignment is the only active work right now, focused on keeping the scene SYNC template complete for repair #16.

---

## KNOWN ISSUES

No active functional bugs are tracked for SceneView; the only known issue was documentation template drift that is now being addressed.

---

## TODO

Add basic component tests for SceneView and SceneBanner once a frontend test harness is settled, and confirm action button wiring as backend APIs evolve.

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
- The test doc now records the missing automation coverage to keep gaps visible.

### Suggestions
- [ ] Add basic component tests for SceneView and SceneBanner to cover fallback rendering.
- [ ] Add a Playwright smoke test for voice ordering and action button presence.

### Propositions
- Consider a shared scene fixture in frontend tests to standardize validation inputs.

---

## CONSCIOUSNESS TRACE

This update focuses on documentation hygiene only; I kept the additions narrow to avoid implying any unverified UI behavior or implementation changes.


---

## ARCHIVE

Older content archived to: `SYNC_Scene_archive_2025-12.md`
