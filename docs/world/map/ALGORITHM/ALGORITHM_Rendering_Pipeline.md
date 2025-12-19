# Map System — Algorithm: Rendering Pipeline

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

PATTERNS:        ../PATTERNS_Map.md
BEHAVIORS:       ../BEHAVIORS_Map.md
ALGORITHM:       ../ALGORITHM_Map.md
THIS:            ./ALGORITHM_Rendering_Pipeline.md
PLACES:          ./ALGORITHM_Places.md
ROUTES:          ./ALGORITHM_Routes.md
VALIDATION:      ../VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ../TEST_Map_Test_Coverage.md
SYNC:            ../SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Canvas Layers (Draw Order)

1. **Parchment background** — texture, stains, edge darkening.
2. **Coastline + water** — land silhouette, water wash.
3. **Routes** — polylines, road styling.
4. **Fog of war** — multiply blend for unknown areas.
5. **Place icons + labels** — styled by visibility.
6. **Dynamic markers** — player, NPCs, tension pulses.
7. **UI overlay** — compass, scale bar, interaction hints.

---

## Projection

- Lat/lng projected into canvas space via bounds and scale.
- Projection must be consistent across layers to avoid drift.

---

## Layer Details (Concise)

### Parchment
- Use a base fill plus noise/grain overlay.
- Optional edge vignette for age.

### Coastline + Water
- Coastline path derived from geo polygon.
- Water uses low-saturation fill with subtle noise.

### Routes
- Path from waypoint list; style depends on road type.
- Apply slight jitter using deterministic seed per route id.

### Fog of War
- Unknown areas filled; revealed areas erased.
- Multiply blend ensures terrain still visible under fog.

### Place Icons + Labels
- Icon opacity and label style based on visibility level.
- Rumored places use a question mark suffix.

### Dynamic Markers
- Player marker draws at place or interpolated route position.
- NPC markers shown only if known/observed.
- Tension pulses use a radial alpha animation.

### UI Overlay
- Compass indicates north; optional scale bar.
- Hover/selection affordances are rendered on top.

---

## Seeded Random

- Use a stable seed derived from object id to jitter lines.
- Deterministic jitter avoids frame-to-frame flicker.

---

## Hit Detection

- Cache projected positions for places.
- Hit test by radius around icon center.
- Routes are not clickable; selection is place-based.

---

## Performance

### Static Layer Caching
- Cache layers 1-3; re-render only when data changes.

### Visibility-Based Culling
- Skip drawing icons and labels for `unknown` places.
- Skip route drawing when either endpoint is unknown.
