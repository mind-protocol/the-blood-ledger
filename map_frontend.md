# Repository Map: the-blood-ledger/frontend

*Generated: 2026-03-12 08:47*

## Statistics

- **Files:** 48
- **Directories:** 25
- **Total Size:** 225.7K
- **Doc Files:** 0
- **Code Files:** 48
- **Areas:** 10 (docs/ subfolders)
- **Modules:** 48 (subfolders in areas)
- **DOCS Links:** 24 (0.5 avg per code file)

### By Language

- tsx: 33
- typescript: 14
- css: 1

## File Tree

```
├── app/ (25.2K)
│   ├── api/ (9.6K)
│   │   ├── playthroughs/ (8.3K)
│   │   │   └── route.ts (8.3K)
│   │   └── scenarios/ (1.3K)
│   │       └── route.ts (1.3K)
│   ├── map/ (182)
│   │   └── (..1 more files)
│   ├── playthroughs/ (440)
│   │   └── [id]/ (440)
│   │       └── (..1 more files)
│   ├── scenarios/ (5.4K)
│   │   └── page.tsx (5.4K) →
│   ├── start/ (6.2K)
│   │   └── page.tsx (6.2K) →
│   ├── globals.css (1.6K)
│   ├── layout.tsx (916) →
│   └── page.tsx (885) →
├── components/ (136.7K)
│   ├── chronicle/ (4.3K)
│   │   └── ChroniclePanel.tsx (4.3K) →
│   ├── debug/ (13.1K)
│   │   └── DebugPanel.tsx (13.1K) →
│   ├── map/ (27.5K)
│   │   ├── MapCanvas.tsx (22.7K) →
│   │   ├── MapClient.tsx (4.7K) →
│   │   └── (..1 more files)
│   ├── minimap/ (7.8K)
│   │   ├── Minimap.tsx (3.8K) →
│   │   └── SunArc.tsx (4.0K) →
│   ├── moment/ (19.4K)
│   │   ├── ClickableText.tsx (3.6K)
│   │   ├── MomentDebugPanel.tsx (6.6K)
│   │   ├── MomentDisplay.tsx (5.4K)
│   │   ├── MomentStream.tsx (3.4K)
│   │   └── (..1 more files)
│   ├── panel/ (9.3K)
│   │   ├── ChronicleTab.tsx (1.6K)
│   │   ├── ConversationsTab.tsx (3.1K)
│   │   ├── LedgerTab.tsx (2.3K)
│   │   └── RightPanel.tsx (2.3K) →
│   ├── scene/ (40.1K)
│   │   ├── CenterStage.tsx (15.7K)
│   │   ├── CharacterRow.tsx (2.4K)
│   │   ├── Hotspot.tsx (2.6K)
│   │   ├── HotspotRow.tsx (2.8K)
│   │   ├── ObjectRow.tsx (2.1K)
│   │   ├── SceneBanner.tsx (2.6K)
│   │   ├── SceneHeader.tsx (1.1K)
│   │   ├── SceneImage.tsx (3.2K)
│   │   ├── SceneView.tsx (4.1K) →
│   │   ├── SettingStrip.tsx (2.1K)
│   │   └── (..2 more files)
│   ├── ui/ (3.1K)
│   │   └── Toast.tsx (3.1K) →
│   ├── voices/ (1.7K)
│   │   └── Voices.tsx (1.7K) →
│   ├── GameClient.tsx (3.7K)
│   ├── GameLayout.tsx (2.9K)
│   ├── SpeedControl.tsx (3.6K) →
│   └── (..1 more files)
├── data/ (11.8K)
│   ├── map-data.ts (9.5K)
│   ├── saxon_names.ts (511)
│   └── scenarios.ts (1.8K)
├── hooks/ (23.7K)
│   ├── useGameState.ts (15.3K) →
│   ├── useMoments.ts (5.7K) →
│   └── useTempo.ts (2.8K) →
├── lib/ (15.1K)
│   ├── map/ (3.6K)
│   │   ├── projection.ts (2.7K) →
│   │   ├── random.ts (777) →
│   │   └── (..1 more files)
│   └── api.ts (11.5K) →
└── types/ (15.9K)
    ├── game.ts (9.9K) →
    ├── map.ts (4.1K) →
    └── moment.ts (1.9K) →
```

## File Details

### `app/api/playthroughs/route.ts`

**Definitions:**
- `POST()`
- `GET()`
- `injectNode()`
- `injectLink()`

### `app/api/scenarios/route.ts`

**Definitions:**
- `GET()`

### `app/scenarios/page.tsx`

**Docs:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`

**Definitions:**
- `handleBegin()`

### `app/start/page.tsx`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `rollRandomName()`
- `handleBegin()`

### `app/layout.tsx`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

### `app/page.tsx`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

### `components/chronicle/ChroniclePanel.tsx`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `ChroniclePanel()`
- `handleSubmit()`
- `handleKeyDown()`

### `components/debug/DebugPanel.tsx`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `DebugPanel()`
- `connectSSE()`
- `addEvent()`
- `clearEvents()`
- `getEventColor()`
- `handleQuery()`
- `getTypeColor()`
- `formatEventSummary()`

### `components/map/MapCanvas.tsx`

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

**Definitions:**
- `getPlaceVisibility()`
- `getRouteVisibility()`
- `wobblePoint()`
- `drawParchmentLayer()`
- `drawTerrainLayer()`
- `radiusPx()`
- `cpx()`
- `cpy()`
- `drawCoastlineLayer()`
- `midX()`
- `midY()`
- `drawRoutesLayer()`
- `drawFogLayer()`
- `drawPlacesLayer()`
- `drawMarkersLayer()`
- `drawUILayer()`
- `MapCanvas()`

### `components/map/MapClient.tsx`

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

**Definitions:**
- `MapClient()`
- `updateDimensions()`

### `components/minimap/Minimap.tsx`

**Docs:** `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`

**Definitions:**
- `Minimap()`

### `components/minimap/SunArc.tsx`

**Docs:** `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md (Future UI: Minimap + Sun Arc)`

**Definitions:**
- `SunArc()`
- `dayProgress()`
- `getPeriod()`

### `components/moment/ClickableText.tsx`

**Definitions:**
- `ClickableText()`

### `components/moment/MomentDebugPanel.tsx`

**Definitions:**
- `MomentDebugPanel()`
- `getTransitionsFrom()`
- `getTransitionsTo()`
- `StatusBadge()`
- `WeightBar()`

### `components/moment/MomentDisplay.tsx`

**Definitions:**
- `getCharacterImageUrl()`
- `MomentDisplay()`
- `getTypeStyles()`
- `getToneStyles()`
- `getAnimationClass()`
- `getStatusBadge()`
- `renderText()`

### `components/moment/MomentStream.tsx`

**Definitions:**
- `MomentStream()`
- `handleWordClick()`

### `components/panel/ChronicleTab.tsx`

**Definitions:**
- `ChronicleTab()`

### `components/panel/ConversationsTab.tsx`

**Definitions:**
- `ConversationsTab()`

### `components/panel/LedgerTab.tsx`

**Definitions:**
- `LedgerTab()`
- `renderSection()`

### `components/panel/RightPanel.tsx`

**Docs:** `docs/frontend/right-panel/PATTERNS_Tabbed_Right_Panel.md`

**Definitions:**
- `RightPanel()`

### `components/scene/CenterStage.tsx`

**Definitions:**
- `calculateReadTime()`
- `AnimatedLine()`
- `TypingIndicator()`
- `ClickableWord()`
- `MomentText()`
- `MomentBlock()`
- `useRevealAnimation()`
- `CenterStage()`
- `handleWordClick()`
- `handleSubmit()`
- `getReadTime()`

### `components/scene/CharacterRow.tsx`

**Definitions:**
- `CharacterRow()`

### `components/scene/Hotspot.tsx`

**Definitions:**
- `Hotspot()`
- `handleClick()`
- `handleAction()`

### `components/scene/HotspotRow.tsx`

**Definitions:**
- `HotspotRow()`

### `components/scene/ObjectRow.tsx`

**Definitions:**
- `ObjectRow()`

### `components/scene/SceneBanner.tsx`

**Definitions:**
- `getFallbackStyle()`
- `SceneBanner()`

### `components/scene/SceneHeader.tsx`

**Definitions:**
- `SceneHeader()`

### `components/scene/SceneImage.tsx`

**Definitions:**
- `SceneImage()`
- `handleBackgroundClick()`

### `components/scene/SceneView.tsx`

**Docs:** `docs/frontend/scene/PATTERNS_Scene.md`

**Definitions:**
- `SceneView()`

### `components/scene/SettingStrip.tsx`

**Definitions:**
- `SettingStrip()`

### `components/ui/Toast.tsx`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `showToast()`
- `useToast()`
- `ToastProvider()`
- `ToastItem()`

### `components/voices/Voices.tsx`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `Voices()`

### `components/GameClient.tsx`

**Definitions:**
- `GameClient()`
- `handleAction()`

### `components/GameLayout.tsx`

**Definitions:**
- `GameLayout()`

### `components/SpeedControl.tsx`

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `SpeedControl()`
- `fetchSpeed()`

### `hooks/useGameState.ts`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `useGameState()`
- `view()`
- `mapPlaceType()`
- `transformScene()`
- `clickables()`
- `placeId()`
- `transformVoices()`
- `transformViewToScene()`
- `transformMomentsToVoices()`
- `createFallbackScene()`

### `hooks/useMoments.ts`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `useMoments()`

### `hooks/useTempo.ts`

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `useTempo()`
- `fetchState()`

### `lib/map/projection.ts`

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

**Definitions:**
- `project()`
- `x()`
- `y()`
- `unproject()`
- `lng()`
- `haversine()`
- `lat1()`
- `lon1()`
- `lat2()`
- `lon2()`
- `routeDistance()`
- `getPositionAtProgress()`
- `t()`

### `lib/map/random.ts`

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

**Definitions:**
- `seededRandom()`
- `hashString()`

### `lib/api.ts`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `handleApiError()`
- `createPlaythrough()`
- `sendMoment()`
- `getPlaythrough()`
- `getMap()`
- `getFaces()`
- `getLedger()`
- `getChronicle()`
- `semanticQuery()`
- `fetchCurrentMoments()`
- `clickMoment()`
- `getMomentStats()`
- `subscribeToMomentStream()`
- `getCurrentView()`
- `checkHealth()`

### `types/game.ts`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

### `types/map.ts`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

### `types/moment.ts`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`
