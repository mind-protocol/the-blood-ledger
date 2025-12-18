# Archived: SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

Archived on: 2025-12-18
Original file: SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

---

## Key Design Decisions

### Scale Hierarchy (5 Levels)

```
region → settlement → district → building → room
```

Movement within settlements is free. Movement between settlements requires routes.

### Route Computation

- Waypoints traced manually (dev tool)
- Distance computed via haversine
- Travel time = distance / speed (by road type)
- Speed: roman (5 km/h) → none (1.5 km/h)

### Canvas Layers (7)

1. Parchment background
2. Coastline + water
3. Routes
4. Fog of war
5. Place icons + labels
6. Dynamic markers
7. UI overlay

Static layers cached. Dynamic layers re-rendered each frame.

### Visibility (4 Levels)

```
unknown → rumored → known → familiar
```

Places emerge from fog as player discovers them. Rumored places have approximate positions.

### Seeded Random

Hand-drawn wobble uses seeded random. Same route always looks the same.

---












## Data Files

### Places

```
data/world/places.yaml
```

```yaml
places:
  - id: place_york
    name: York
    coordinates: [53.96, -1.08]
    scale: settlement
    type: city
    detail: "The second city of England."
    contains:
      - place_york_market
      - place_york_minster
```

### Routes

```
data/world/routes.yaml
```

```yaml
routes:
  - from: place_york
    to: place_durham
    waypoints:
      - [53.96, -1.08]
      - [54.12, -1.20]
      - [54.35, -1.45]
      - [54.78, -1.57]
    road_type: roman
```

### Coastline

```
data/world/coastline.yaml
```

```yaml
coastline:
  - [55.5, -1.6]
  - [55.3, -1.55]
  - [55.0, -1.42]
  # ... North Sea coast
```

### Player Visibility (per playthrough)

```
playthroughs/{id}/visibility.yaml
```

```yaml
places:
  place_york:
    level: familiar
    discovered_at: 0
    visited_at: 0
```

---












## Implementation Plan

```
Phase 1: Data & Graph
├── [ ] Create places.yaml with Northern England settlements
├── [ ] Create routes.yaml with major roads
├── [ ] Create coastline.yaml with North Sea coast
├── [ ] Place/Route graph schema in FalkorDB
└── [ ] Import scripts for YAML → graph

Phase 2: Route Tracing Tool
├── [ ] Simple React canvas for tracing
├── [ ] Click to add waypoints
├── [ ] Select road type
├── [ ] Export to YAML
└── [ ] Trace major routes (York-Durham, York-Scarborough, etc.)

Phase 3: Core Rendering
├── [ ] MapCanvas React component
├── [ ] Projection functions (equirectangular)
├── [ ] Parchment background layer
├── [ ] Coastline layer
├── [ ] Route layer with hand-drawn wobble
└── [ ] Seeded random utility

Phase 4: Fog of War
├── [ ] Separate fog canvas
├── [ ] Radial gradient holes for known places
├── [ ] Multiply blend mode composition
└── [ ] Visibility state management

Phase 5: Places & Interaction
├── [ ] Place icon rendering
├── [ ] Label rendering with visibility levels
├── [ ] Hit detection for clicks/hover
├── [ ] Hover info panel
└── [ ] Click to select/travel

Phase 6: Dynamic Elements
├── [ ] Player marker
├── [ ] NPC movement along routes
├── [ ] Tension pulse animation
├── [ ] Animation loop

Phase 7: Integration
├── [ ] Connect to Narrator (travel requests)
├── [ ] Visibility updates from graph_mutations
├── [ ] Position updates during travel
└── [ ] News/event indicators
```

---












## Component Structure

```
components/
├── Map/
│   ├── MapCanvas.tsx          # Main canvas component
│   ├── layers/
│   │   ├── ParchmentLayer.ts
│   │   ├── CoastlineLayer.ts
│   │   ├── RoutesLayer.ts
│   │   ├── FogLayer.ts
│   │   ├── PlacesLayer.ts
│   │   ├── MarkersLayer.ts
│   │   └── UILayer.ts
│   ├── hooks/
│   │   ├── useMapState.ts
│   │   ├── useVisibility.ts
│   │   └── useInteraction.ts
│   ├── utils/
│   │   ├── projection.ts
│   │   ├── haversine.ts
│   │   ├── seededRandom.ts
│   │   └── hitDetection.ts
│   └── types.ts
└── RouteTracer/
    └── RouteTracer.tsx        # Dev tool
```

---












## Open Questions

### Zoom/Pan

Current spec: Fixed view of Northern England. Future consideration:
- Zoom to settlement → show districts
- Pan beyond bounds → extend map

### Mobile

Canvas touch interaction. Current spec assumes desktop mouse.

### Performance

At 100+ places and routes, may need:
- Spatial indexing for hit detection
- Level-of-detail for distant places
- WebGL for complex effects

### Animated Travel

Current: Position jumps after travel. Future:
- Smooth animation along route during journey
- Integrate with World Runner tick-by-tick progress

---












## Connection to Other Systems

### Graph

Places and routes are graph nodes/links:
- `Place` nodes with coordinates, scale, type
- `CONTAINS` links for hierarchy
- `ROUTE` links with computed travel time

Map reads from graph. Doesn't write.

### Narrator

Travel flow:
1. Player clicks destination on map
2. Map emits `onRequestTravel(from, to)`
3. UI passes to Narrator
4. Narrator: "You travel to York. Two days on foot."
5. Narrator calls World Runner
6. Injection returns (interrupted or completed)
7. Map updates player position

### World Runner

During travel:
- Runner knows player path from route waypoints
- Can check "is player at this location at tick N?"
- Flip at location on path → interrupt travel

### Visibility

Updated by Narrator graph_mutations:

```yaml
visibility_updates:
  - place: place_durham
    event: told_about
```

Engine applies after each Narrator response. Map re-renders with new visibility.

---











