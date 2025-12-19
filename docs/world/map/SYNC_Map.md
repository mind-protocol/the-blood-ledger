# Map System — Sync: Current State

```
LAST_UPDATED: 2024-12-16
STATUS: Documented, ready for implementation
```

---

## Current State

**Documentation complete.** Map system fully specified:
- Place schema and hierarchy
- Route computation and movement rules
- Canvas rendering with 7 layers
- Visibility system with 4 levels
- Interaction behaviors

**Not yet implemented.** Waiting for:
- Frontend setup (Next.js)
- Graph infrastructure (FalkorDB)
- Integration with Narrator

---

## Documentation Status

| Doc | Purpose | Status |
|-----|---------|--------|
| `PATTERNS_Map.md` | Why this design | Complete |
| `ALGORITHM_Places.md` | Place schema, scale, hierarchy | Complete |
| `ALGORITHM_Routes.md` | Routes, computation, movement | Complete |
| `ALGORITHM_Rendering.md` | Canvas layers, projection, fog | Complete |
| `BEHAVIORS_Map.md` | Visibility, interaction | Complete |
| `SYNC_Map.md` | Current state | This file |

---

## Summary Table

| Component | Implementation |
|-----------|----------------|
| Place scale | 5 levels: region → room |
| CONTAINS | Hierarchy link (no attributes) |
| ROUTE | Waypoints + computed distance/time |
| Movement | Scale-based defaults, ROUTE for between settlements |
| Projection | Equirectangular for Northern England |
| Rendering | 7 Canvas layers, seeded random for hand-drawn |
| Fog of war | Separate canvas, radial gradient holes, multiply blend |
| Visibility | 4 levels: unknown → familiar |
| Hit detection | Distance threshold from projected coordinates |

---

*"The map is documented. Implementation awaits the frontend."*


---

## ARCHIVE

Older content archived to: `SYNC_Map_archive_2025-12.md`
