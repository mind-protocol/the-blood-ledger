# Map System — Patterns: Why This Design

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## The Core Insight

**The map is not a GPS — it's a medieval traveler's knowledge.**

Players don't see everything. They see what they know. Places emerge from fog as they're discovered, heard about, or visited. Routes are hand-drawn lines, not satellite imagery.

---

## What the Map Does

| Function | How It Works |
|----------|--------------|
| **Shows known world** | Fog of war hides unknown places |
| **Enables travel** | Click destination → Narrator handles journey |
| **Reveals relationships** | Routes connect, hierarchy contains |
| **Creates atmosphere** | Parchment aesthetic, hand-drawn feel |
| **Tracks player** | Current location always visible |

---

## Design Principles

### 1. Knowledge, Not Omniscience

The player sees what their character knows:
- **Unknown** — Not on map at all
- **Rumored** — Faded, approximate position, "Name?"
- **Known** — Clear, accurate position
- **Familiar** — Bright, detailed, travel times shown

This creates discovery. The map grows as the player explores.

### 2. Scale Hierarchy

Places nest inside places:

```
Northumbria (region)
  └── York (settlement)
        └── York Market (district)
              └── Merchant's Hall (building)
                    └── Back Room (room)
```

Movement within a settlement is free. Movement between settlements requires routes.

### 3. Routes Are Real

Not point-to-point teleportation. Routes have:
- **Waypoints** — Actual path traced on the map
- **Distance** — Computed from waypoints (haversine)
- **Travel time** — Based on road type and distance
- **Difficulty** — Easy (roman road) to dangerous (cross-country)

When player travels, the World Runner runs for that duration. Things can happen on the road.

### 4. Hand-Drawn Aesthetic

The map looks like a medieval document:
- Parchment background with grain and age stains
- Coastlines and routes with slight wobble
- Seeded random ensures consistent look across renders
- Icons are symbolic, not photorealistic

### 5. Layers, Not Clutter

Seven canvas layers, drawn in order:
1. Parchment background
2. Coastline + water
3. Routes
4. Fog of war
5. Place icons + labels
6. Dynamic markers (player, NPCs, tensions)
7. UI overlay

Each layer has one job. Composition creates the final map.

---

## Why These Choices

### Why Fog of War?

**Creates discovery.** The player's first journey to York reveals the route. Hearing rumors about Durham puts it on the map — faded, approximate. Visiting makes it clear.

**Supports uncertainty.** A rumored place might be mispositioned. The player's beliefs about geography can be wrong.

**Enables "the world moved."** When player returns, new places might have appeared (via news) or old places changed (via events).

### Why Scale Hierarchy?

**Reflects reality.** You can walk across York Market in 15 minutes. You can't walk to Durham in 15 minutes.

**Simplifies movement.** Within a settlement → free. Between settlements → route required.

**Enables zoom.** Could show settlement detail when clicked (future). Hierarchy supports drilling down.

### Why Compute Routes?

**Accurate travel time.** Haversine distance from waypoints gives real-world km. Speed by road type gives hours. World Runner runs for that duration.

**Consistent world.** If York to Durham is 19 hours, it's always 19 hours. No narrative fudging.

**Traceable events.** "Ambushed on the road to Durham" — we know exactly when that could happen based on route progress.

### Why Canvas Layers?

**Separation of concerns.** Fog of war doesn't need to know about routes. Routes don't need to know about player position.

**Performance.** Static layers (parchment, coastline) rendered once. Dynamic layers (markers, pulses) re-rendered each frame.

**Compositing.** Fog uses multiply blend mode. Wouldn't work if everything was one layer.

### Why Seeded Random?

**Consistency.** The route from York to Durham should wobble the same way every time. Hash the route ID, use as seed.

**Hand-drawn feel.** Slight variations make lines feel drawn, not computed. But same variations each render prevents flickering.

---

## Connection to Other Systems

### Graph

Places and routes are graph nodes and links:
- `Place` nodes with coordinates, scale, type
- `CONTAINS` links for hierarchy
- `ROUTE` links for travel

Map reads from graph, doesn't write to it.

### World Runner

When player travels:
1. Map provides route (waypoints, travel time)
2. Narrator calls Runner with that duration
3. Runner can interrupt mid-journey
4. Map shows player position along route

### Narrator

Map is a view, not a controller:
- Player clicks destination → emits event
- Narrator decides what happens ("You travel to York")
- Narrator calls Runner
- Map updates when journey complete (or interrupted)

### Visibility (Player Knowledge)

Separate from graph. Player-specific state:
- Which places are known?
- At what level (rumored/known/familiar)?
- When discovered?

Stored per playthrough, not in global graph.

---

## What the Map Is NOT

### Not a Mini-Game

No pathfinding puzzles. No "collect all locations." The map serves the story, not the other way around.

### Not Real-Time

Player position doesn't animate smoothly along routes. When traveling, the scene changes to the journey. When arrived (or interrupted), position updates.

### Not Complete

The map never shows everything. Even a fully explored map has fog at the edges. The world is larger than the player's knowledge.

### Not Accurate

Rumored places are approximate. The map reflects player belief, not ground truth. A place might be marked wrong until visited.

---

## Player Experience

**First session:**
- Map is mostly fog
- A few places known from starting location
- Routes visible only to immediate neighbors
- "Where is York?" creates motivation to learn

**Mid-game:**
- Network of known places
- Routes traced from travel
- Some rumored places from conversations
- "I know this region now"

**Late-game:**
- Most of Northern England visible
- Familiar places have detail
- Strategic view: "If I go here, I can reach there"
- "This is my territory"

---

*"The map is what you know. And you don't know everything."*
