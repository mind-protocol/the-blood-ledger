# Map System — Algorithm: Rendering, Places, Routes

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Rendering.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Canvas Layers

Seven layers, drawn in order:

| Layer | Purpose | Update Frequency |
|-------|---------|------------------|
| 0 | Parchment background | Once |
| 1 | Coastline + water | Once |
| 2 | Routes | When visibility changes |
| 3 | Fog of war | When visibility changes |
| 4 | Place icons + labels | When visibility changes |
| 5 | Dynamic markers | Every frame |
| 6 | UI overlay | Once |

```javascript
function renderMap(ctx, state, tick) {
  const { width, height } = ctx.canvas;

  // Layer 0: Parchment (cached)
  drawParchment(ctx, width, height, PARCHMENT_SEED);

  // Layer 1: Coastline (cached)
  drawCoastline(ctx, COASTLINE_POINTS, width, height);

  // Layer 2: Routes
  for (const route of state.routes) {
    const visibility = state.routeVisibility[route.id];
    drawRoute(ctx, route.waypoints, visibility, hashString(route.id), width, height);
  }

  // Layer 3: Fog of war (separate canvas, composite)
  drawFogOfWar(fogCtx, state.knownPlaces, width, height);
  ctx.globalCompositeOperation = 'multiply';
  ctx.drawImage(fogCanvas, 0, 0);
  ctx.globalCompositeOperation = 'source-over';

  // Layer 4: Place icons
  for (const place of state.places) {
    const visibility = state.placeVisibility[place.id];
    drawPlace(ctx, place, visibility, width, height);
  }

  // Layer 5: Dynamic markers
  drawPlayerMarker(ctx, state.playerPosition, width, height);
  for (const npc of state.npcsMoving) {
    drawNPCMoving(ctx, npc.route, npc.progress, width, height);
  }
  for (const tension of state.tensions) {
    drawTensionPulse(ctx, tension.place, tension.level, tick, width, height);
  }

  // Layer 6: UI
  drawCompass(ctx, width - 50, 50, 30);
}
```

---

## Projection

Simple equirectangular projection for Northern England:

```javascript
const BOUNDS = {
  north: 55.5,
  south: 53.0,
  east: 0.5,
  west: -3.0
};

function project(lat, lng, width, height) {
  /**
   * Convert [lat, lng] to [x, y] canvas coordinates.
   */
  const x = ((lng - BOUNDS.west) / (BOUNDS.east - BOUNDS.west)) * width;
  const y = ((BOUNDS.north - lat) / (BOUNDS.north - BOUNDS.south)) * height;
  return [x, y];
}

function unproject(x, y, width, height) {
  /**
   * Convert [x, y] canvas coordinates to [lat, lng].
   */
  const lng = (x / width) * (BOUNDS.east - BOUNDS.west) + BOUNDS.west;
  const lat = BOUNDS.north - (y / height) * (BOUNDS.north - BOUNDS.south);
  return [lat, lng];
}
```

**Why equirectangular?** Good enough for the small region. Mercator distortion negligible at this scale. Simple math.

---

## Layer 0: Parchment Background

```javascript
function drawParchment(ctx, width, height, seed) {
  const rng = seededRandom(seed);

  // Base color
  ctx.fillStyle = '#f4e4bc';
  ctx.fillRect(0, 0, width, height);

  // Grain texture (pixel noise)
  const imageData = ctx.getImageData(0, 0, width, height);
  for (let i = 0; i < imageData.data.length; i += 4) {
    const noise = (rng() - 0.5) * 20;
    imageData.data[i] += noise;     // R
    imageData.data[i+1] += noise;   // G
    imageData.data[i+2] += noise;   // B
    // Alpha unchanged
  }
  ctx.putImageData(imageData, 0, 0);

  // Age stains (subtle darker circles)
  for (let i = 0; i < 5; i++) {
    const x = rng() * width;
    const y = rng() * height;
    const r = 50 + rng() * 100;

    const gradient = ctx.createRadialGradient(x, y, 0, x, y, r);
    gradient.addColorStop(0, 'rgba(139, 119, 85, 0.1)');
    gradient.addColorStop(1, 'rgba(139, 119, 85, 0)');

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  // Edge darkening (vignette)
  const vignette = ctx.createRadialGradient(
    width/2, height/2, Math.min(width, height) * 0.3,
    width/2, height/2, Math.max(width, height) * 0.7
  );
  vignette.addColorStop(0, 'rgba(0, 0, 0, 0)');
  vignette.addColorStop(1, 'rgba(0, 0, 0, 0.1)');
  ctx.fillStyle = vignette;
  ctx.fillRect(0, 0, width, height);
}
```

---

## Layer 1: Coastline + Water

```javascript
// Coastline points: [lat, lng] tracing the North Sea coast
const COASTLINE_POINTS = [
  [55.5, -1.6],   // North edge
  [55.3, -1.55],
  [55.0, -1.42],
  [54.7, -1.20],
  [54.5, -0.60],  // Whitby area
  [54.3, -0.35],
  [54.0, -0.15],
  [53.8, 0.10],
  [53.5, 0.20],
  [53.0, 0.30],   // South edge
];

function drawCoastline(ctx, coastlinePoints, width, height) {
  // Sea color
  ctx.fillStyle = '#c9d9e8';

  // Coast stroke
  ctx.strokeStyle = '#2c1810';
  ctx.lineWidth = 2;

  ctx.beginPath();

  // Project coastline points
  const projected = coastlinePoints.map(([lat, lng]) =>
    project(lat, lng, width, height)
  );

  // Start at first coast point
  ctx.moveTo(projected[0][0], projected[0][1]);

  // Draw coast
  for (const [x, y] of projected.slice(1)) {
    ctx.lineTo(x, y);
  }

  // Close polygon to edge of canvas (sea is east)
  ctx.lineTo(width, projected[projected.length-1][1]);
  ctx.lineTo(width, 0);
  ctx.lineTo(projected[0][0], 0);
  ctx.closePath();

  ctx.fill();
  ctx.stroke();
}
```

---

## Layer 2: Routes

Hand-drawn wobble using seeded random:

```javascript
function drawRoute(ctx, waypoints, visibility, seed, width, height) {
  // Don't draw unknown routes
  if (visibility === 'unknown') return;

  const rng = seededRandom(seed);

  // Style based on visibility
  if (visibility === 'rumored') {
    ctx.strokeStyle = 'rgba(44, 24, 16, 0.3)';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
  } else {
    ctx.strokeStyle = 'rgba(44, 24, 16, 0.7)';
    ctx.lineWidth = 2;
    ctx.setLineDash([]);
  }

  ctx.beginPath();

  const projected = waypoints.map(([lat, lng]) =>
    project(lat, lng, width, height)
  );

  ctx.moveTo(projected[0][0], projected[0][1]);

  // Hand-drawn effect: subdivide segments with wobble
  for (let i = 1; i < projected.length; i++) {
    const [x0, y0] = projected[i-1];
    const [x1, y1] = projected[i];

    // Number of subdivisions based on segment length
    const segmentLength = Math.hypot(x1 - x0, y1 - y0);
    const steps = Math.ceil(segmentLength / 20);

    for (let s = 1; s <= steps; s++) {
      const t = s / steps;
      // Interpolate with random wobble
      const x = x0 + (x1 - x0) * t + (rng() - 0.5) * 3;
      const y = y0 + (y1 - y0) * t + (rng() - 0.5) * 3;
      ctx.lineTo(x, y);
    }
  }

  ctx.stroke();
  ctx.setLineDash([]);  // Reset dash
}
```

---

## Layer 3: Fog of War

Separate canvas, composited with multiply blend mode:

```javascript
function drawFogOfWar(fogCtx, knownPlaces, width, height) {
  // Fill with dark fog
  fogCtx.fillStyle = 'rgba(20, 15, 10, 0.7)';
  fogCtx.fillRect(0, 0, width, height);

  // Cut holes for known places
  fogCtx.globalCompositeOperation = 'destination-out';

  for (const place of knownPlaces) {
    const [x, y] = project(place.lat, place.lng, width, height);

    // Hole size based on visibility level
    const radius = {
      'familiar': 60,
      'known': 40,
      'rumored': 20
    }[place.visibility] || 30;

    // Soft-edge gradient
    const gradient = fogCtx.createRadialGradient(x, y, 0, x, y, radius);
    gradient.addColorStop(0, 'rgba(0, 0, 0, 1)');
    gradient.addColorStop(0.7, 'rgba(0, 0, 0, 0.8)');
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

    fogCtx.fillStyle = gradient;
    fogCtx.beginPath();
    fogCtx.arc(x, y, radius, 0, Math.PI * 2);
    fogCtx.fill();
  }

  fogCtx.globalCompositeOperation = 'source-over';
}
```

**Compositing in main render:**

```javascript
// After drawing layers 0-2
ctx.globalCompositeOperation = 'multiply';
ctx.drawImage(fogCanvas, 0, 0);
ctx.globalCompositeOperation = 'source-over';
// Continue with layers 4+
```

---

## Layer 4: Place Icons + Labels

```javascript
const PLACE_ICONS = {
  city:       { symbol: '⬡', size: 24 },
  town:       { symbol: '◆', size: 18 },
  village:    { symbol: '●', size: 12 },
  monastery:  { symbol: '†', size: 16 },
  hold:       { symbol: '▲', size: 14 },
  crossing:   { symbol: '═', size: 12 },
  landmark:   { symbol: '★', size: 14 },
  market:     { symbol: '◇', size: 14 },
  hall:       { symbol: '⌂', size: 12 },
  church:     { symbol: '✝', size: 12 },
  tavern:     { symbol: '⌐', size: 12 }
};

function drawPlace(ctx, place, visibility, width, height) {
  // Don't draw unknown places
  if (visibility === 'unknown') return;

  const [x, y] = project(place.lat, place.lng, width, height);
  const icon = PLACE_ICONS[place.type] || PLACE_ICONS.village;

  // Opacity based on visibility
  const alpha = {
    'familiar': 1.0,
    'known': 0.85,
    'rumored': 0.5
  }[visibility];

  // Draw icon
  ctx.fillStyle = `rgba(44, 24, 16, ${alpha})`;
  ctx.font = `${icon.size}px serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(icon.symbol, x, y);

  // Draw label
  const label = visibility === 'rumored' ? `${place.name}?` : place.name;
  const fontWeight = visibility === 'familiar' ? 'bold ' : '';
  ctx.font = `${fontWeight}12px serif`;
  ctx.fillText(label, x, y + icon.size);
}
```

---

## Layer 5: Dynamic Markers

### Player Marker

```javascript
function drawPlayerMarker(ctx, position, width, height) {
  const [lat, lng] = Array.isArray(position)
    ? position
    : getPlaceCoordinates(position);

  const [x, y] = project(lat, lng, width, height);

  // Outer ring
  ctx.fillStyle = '#8b0000';
  ctx.beginPath();
  ctx.arc(x, y, 8, 0, Math.PI * 2);
  ctx.fill();

  // Inner highlight
  ctx.strokeStyle = '#f4e4bc';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Center dot
  ctx.fillStyle = '#f4e4bc';
  ctx.beginPath();
  ctx.arc(x, y, 2, 0, Math.PI * 2);
  ctx.fill();
}
```

### NPC Moving Along Route

```javascript
function drawNPCMoving(ctx, route, progress, width, height) {
  // Get position along route
  const position = getPositionAtProgress(route, progress);
  const [x, y] = project(position[0], position[1], width, height);

  // Simple marker
  ctx.fillStyle = '#4a4a4a';
  ctx.beginPath();
  ctx.arc(x, y, 5, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = '#2c1810';
  ctx.lineWidth = 1;
  ctx.stroke();
}
```

### Tension Pulse

```javascript
function drawTensionPulse(ctx, place, level, tick, width, height) {
  const [x, y] = project(place.lat, place.lng, width, height);

  // Pulsing animation
  const pulse = Math.sin(tick * 0.1) * 0.3 + 0.7;
  const radius = 20 + level * 30;

  // Outer pulse ring
  ctx.strokeStyle = `rgba(139, 0, 0, ${pulse * level})`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(x, y, radius * pulse, 0, Math.PI * 2);
  ctx.stroke();

  // Inner glow
  if (level > 0.7) {
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 0.5);
    gradient.addColorStop(0, `rgba(139, 0, 0, ${level * 0.3})`);
    gradient.addColorStop(1, 'rgba(139, 0, 0, 0)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x, y, radius * 0.5, 0, Math.PI * 2);
    ctx.fill();
  }
}
```

---

## Layer 6: UI Overlay

### Compass

```javascript
function drawCompass(ctx, x, y, size) {
  ctx.save();
  ctx.translate(x, y);

  // Outer circle
  ctx.strokeStyle = '#2c1810';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(0, 0, size, 0, Math.PI * 2);
  ctx.stroke();

  // N pointer (red triangle)
  ctx.fillStyle = '#8b0000';
  ctx.beginPath();
  ctx.moveTo(0, -size + 5);
  ctx.lineTo(-5, -size/2);
  ctx.lineTo(5, -size/2);
  ctx.closePath();
  ctx.fill();

  // S pointer (lighter)
  ctx.fillStyle = '#5a4a3a';
  ctx.beginPath();
  ctx.moveTo(0, size - 5);
  ctx.lineTo(-5, size/2);
  ctx.lineTo(5, size/2);
  ctx.closePath();
  ctx.fill();

  // N label
  ctx.fillStyle = '#2c1810';
  ctx.font = 'bold 12px serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('N', 0, -size - 10);

  ctx.restore();
}
```

### Scale Bar (Optional)

```javascript
function drawScaleBar(ctx, x, y, width, height) {
  // 50km scale bar
  const kmPerPixel = (BOUNDS.east - BOUNDS.west) * 111 / width;  // ~111 km per degree
  const barWidthPx = 50 / kmPerPixel;

  ctx.strokeStyle = '#2c1810';
  ctx.lineWidth = 2;

  // Bar
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + barWidthPx, y);
  ctx.stroke();

  // End caps
  ctx.beginPath();
  ctx.moveTo(x, y - 5);
  ctx.lineTo(x, y + 5);
  ctx.moveTo(x + barWidthPx, y - 5);
  ctx.lineTo(x + barWidthPx, y + 5);
  ctx.stroke();

  // Label
  ctx.font = '10px serif';
  ctx.textAlign = 'center';
  ctx.fillText('50 km', x + barWidthPx/2, y + 15);
}
```

---

## Seeded Random

Consistent "hand-drawn" appearance across renders:

```javascript
function seededRandom(seed) {
  /**
   * Linear congruential generator.
   * Returns a function that produces deterministic "random" values.
   */
  let state = seed;
  return function() {
    state = (state * 1103515245 + 12345) & 0x7fffffff;
    return state / 0x7fffffff;
  };
}

function hashString(str) {
  /**
   * Simple string hash for seed generation.
   */
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;  // Convert to 32bit integer
  }
  return Math.abs(hash);
}

// Usage
const routeSeed = hashString(route.from + route.to);
drawRoute(ctx, route.waypoints, visibility, routeSeed, width, height);
```

---

## Hit Detection

Finding what's under the cursor:

```javascript
function findPlaceAtPoint(x, y, places, visibility, width, height) {
  const threshold = 20;  // pixels

  for (const place of places) {
    // Skip unknown places
    if (visibility[place.id] === 'unknown') continue;

    const [px, py] = project(place.lat, place.lng, width, height);
    const dist = Math.hypot(x - px, y - py);

    if (dist < threshold) {
      return place;
    }
  }

  return null;
}

function findRouteAtPoint(x, y, routes, visibility, width, height) {
  const threshold = 10;  // pixels

  for (const route of routes) {
    if (visibility[route.id] === 'unknown') continue;

    // Check distance to each segment
    const projected = route.waypoints.map(([lat, lng]) =>
      project(lat, lng, width, height)
    );

    for (let i = 1; i < projected.length; i++) {
      const dist = pointToSegmentDistance(
        x, y,
        projected[i-1][0], projected[i-1][1],
        projected[i][0], projected[i][1]
      );

      if (dist < threshold) {
        return route;
      }
    }
  }

  return null;
}

function pointToSegmentDistance(px, py, x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const lengthSq = dx * dx + dy * dy;

  if (lengthSq === 0) return Math.hypot(px - x1, py - y1);

  let t = ((px - x1) * dx + (py - y1) * dy) / lengthSq;
  t = Math.max(0, Math.min(1, t));

  const nearestX = x1 + t * dx;
  const nearestY = y1 + t * dy;

  return Math.hypot(px - nearestX, py - nearestY);
}
```

---

## Performance Optimization

### Static Layer Caching

```javascript
class MapRenderer {
  constructor(width, height) {
    this.width = width;
    this.height = height;

    // Cache canvases for static layers
    this.parchmentCanvas = this.createCache();
    this.coastlineCanvas = this.createCache();
    this.fogCanvas = this.createCache();

    // Draw static layers once
    this.drawStaticLayers();
  }

  createCache() {
    const canvas = document.createElement('canvas');
    canvas.width = this.width;
    canvas.height = this.height;
    return canvas;
  }

  drawStaticLayers() {
    drawParchment(
      this.parchmentCanvas.getContext('2d'),
      this.width, this.height,
      PARCHMENT_SEED
    );

    drawCoastline(
      this.coastlineCanvas.getContext('2d'),
      COASTLINE_POINTS,
      this.width, this.height
    );
  }

  render(ctx, state, tick) {
    // Blit cached static layers
    ctx.drawImage(this.parchmentCanvas, 0, 0);
    ctx.drawImage(this.coastlineCanvas, 0, 0);

    // Dynamic layers...
  }
}
```

### Visibility-Based Culling

```javascript
function getVisiblePlaces(places, visibility, bounds) {
  return places.filter(place => {
    if (visibility[place.id] === 'unknown') return false;

    const [lat, lng] = place.coordinates;
    return lat >= bounds.south && lat <= bounds.north &&
           lng >= bounds.west && lng <= bounds.east;
  });
}
```

---

*"Seven layers. Parchment to UI. Each has one job. Composition creates the map."*

---

## Place Schema

```yaml
Place:
  id: string              # place_york, place_york_market
  name: string            # "York", "York Market"
  coordinates: [float, float]  # [lat, lng]
  scale: string           # region | settlement | district | building | room
  type: string            # city | village | monastery | hold | crossing | etc
  detail: string          # Atmosphere, description
  detail_embedding: float[]  # Embedded if detail > 20 chars
```

### Field Details

| Field | Required | Notes |
|-------|----------|-------|
| `id` | Yes | Unique, prefixed `place_` |
| `name` | Yes | Display name |
| `coordinates` | Yes | [latitude, longitude] |
| `scale` | Yes | Determines movement rules |
| `type` | Yes | Determines icon |
| `detail` | No | Atmosphere/description for Narrator |
| `detail_embedding` | Auto | Generated if detail > 20 chars |

---

## Scale Levels

Five hierarchical scales:

| Scale | Examples | Typical Area | Movement Within |
|-------|----------|--------------|-----------------|
| `region` | Northumbria, Yorkshire | 1000+ km² | Requires ROUTE |
| `settlement` | York, Durham, Whitby | 1-10 km² | Free (~15 min between districts) |
| `district` | York Market, Minster Quarter | 0.1-1 km² | Free (~5 min between buildings) |
| `building` | Merchant's Hall, The Minster | 100-10000 m² | Free (~1 min between rooms) |
| `room` | Back Room, Crypt | 10-500 m² | Instant |

### Scale Rules

```python
SCALE_HIERARCHY = ['region', 'settlement', 'district', 'building', 'room']

def can_contain(parent_scale, child_scale):
    """Check if parent scale can contain child scale."""
    parent_idx = SCALE_HIERARCHY.index(parent_scale)
    child_idx = SCALE_HIERARCHY.index(child_scale)
    return child_idx == parent_idx + 1

# region can contain settlement
# settlement can contain district
# district can contain building
# building can contain room
# room contains nothing
```

---

## Place Types

Types determine map icons:

| Type | Icon | Typical Scale |
|------|------|---------------|
| `city` | ⬡ | settlement |
| `town` | ◆ | settlement |
| `village` | ● | settlement |
| `monastery` | † | settlement/building |
| `hold` | ▲ | settlement/building |
| `crossing` | ═ | settlement |
| `landmark` | ★ | any |
| `market` | ◇ | district |
| `quarter` | □ | district |
| `hall` | ⌂ | building |
| `church` | ✝ | building |
| `tavern` | ⌐ | building |
| `house` | ⌂ | building |

---

## CONTAINS Link (Hierarchy)

Binary relationship — no attributes:

```cypher
(parent:Place)-[:CONTAINS]->(child:Place)
```

### Example Hierarchy

```
place_northumbria (region)
    │
    └── CONTAINS
            │
            ▼
        place_york (settlement)
            │
            ├── CONTAINS → place_york_market (district)
            │                  │
            │                  └── CONTAINS → place_merchants_hall (building)
            │                                     │
            │                                     └── CONTAINS → place_back_room (room)
            │
            └── CONTAINS → place_york_minster (building)
```

### Query: Get Parent

```cypher
MATCH (parent:Place)-[:CONTAINS]->(child:Place {id: $place_id})
RETURN parent
```

### Query: Get Children

```cypher
MATCH (parent:Place {id: $place_id})-[:CONTAINS]->(child:Place)
RETURN child
ORDER BY child.name
```

### Query: Get Full Path

```cypher
MATCH path = (region:Place {scale: 'region'})-[:CONTAINS*]->(place:Place {id: $place_id})
RETURN [node IN nodes(path) | node.name] AS path_names
```

---

## Creating Places

### Validation

```python
def validate_place(place: dict) -> bool:
    """Validate place before creation."""

    # Required fields
    required = ['id', 'name', 'coordinates', 'scale', 'type']
    for field in required:
        if field not in place:
            raise ValueError(f"Missing required field: {field}")

    # ID format
    if not place['id'].startswith('place_'):
        raise ValueError("Place ID must start with 'place_'")

    # Coordinates
    lat, lng = place['coordinates']
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise ValueError("Invalid coordinates")

    # Scale
    if place['scale'] not in SCALE_HIERARCHY:
        raise ValueError(f"Invalid scale: {place['scale']}")

    return True
```

### Cypher: Create Place

```cypher
CREATE (p:Place {
  id: $id,
  name: $name,
  coordinates: $coordinates,
  scale: $scale,
  type: $type,
  detail: $detail
})
RETURN p
```

### Cypher: Add to Hierarchy

```cypher
MATCH (parent:Place {id: $parent_id})
MATCH (child:Place {id: $child_id})
CREATE (parent)-[:CONTAINS]->(child)
```

---

## Example Places

### Region

```yaml
- id: place_northumbria
  name: Northumbria
  coordinates: [54.5, -1.5]
  scale: region
  type: region
  detail: "The great northern kingdom, now under Norman control."
```

### Settlement

```yaml
- id: place_york
  name: York
  coordinates: [53.96, -1.08]
  scale: settlement
  type: city
  detail: "The second city of England. Norman banners fly from its walls."
```

### District

```yaml
- id: place_york_market
  name: York Market
  coordinates: [53.959, -1.082]
  scale: district
  type: market
  detail: "The heart of trade. Stalls crowd the square. Voices in English and Norman."
```

### Building

```yaml
- id: place_merchants_hall
  name: Merchant's Hall
  coordinates: [53.958, -1.081]
  scale: building
  type: hall
  detail: "Stone and timber. The smell of wool and coin."
```

### Room

```yaml
- id: place_back_room
  name: Back Room
  coordinates: [53.958, -1.081]
  scale: room
  type: room
  detail: "Private. A table, two chairs, a locked chest."
```

---

## Coordinate System

### Northern England Bounds

```python
BOUNDS = {
    'north': 55.5,
    'south': 53.0,
    'east': 0.5,
    'west': -3.0
}
```

### Reference Coordinates

| Place | Lat | Lng |
|-------|-----|-----|
| York | 53.96 | -1.08 |
| Durham | 54.78 | -1.57 |
| Scarborough | 54.28 | -0.40 |
| Whitby | 54.49 | -0.61 |
| Ripon | 54.14 | -1.52 |
| Newcastle | 54.97 | -1.61 |

### Rooms Share Parent Coordinates

Rooms within a building use the building's coordinates. No sub-meter precision needed.

```python
def get_display_coordinates(place: Place, graph) -> tuple:
    """Get coordinates for display. Rooms inherit from building."""
    if place.scale == 'room':
        parent = graph.get_parent(place)
        return parent.coordinates
    return place.coordinates
```

---

## Scale-Based Defaults

When Narrator needs movement time within a location:

```python
WITHIN_SCALE_MINUTES = {
    'room': 0,        # Instant
    'building': 1,    # ~1 min between rooms
    'district': 5,    # ~5 min between buildings
    'settlement': 15  # ~15 min between districts
}

def get_movement_within(place: Place) -> int:
    """Default movement time within a place."""
    return WITHIN_SCALE_MINUTES.get(place.scale, 0)
```

---

## Embedding Detail

For semantic search of places by description:

```python
def maybe_embed_detail(place: dict, embed_fn) -> dict:
    """Embed detail if long enough."""
    detail = place.get('detail', '')

    if len(detail) > 20:
        place['detail_embedding'] = embed_fn(detail)

    return place
```

### Query: Find Places by Description

```python
def find_places_by_description(query: str, embed_fn, graph, top_k=5):
    """Semantic search for places."""
    query_embedding = embed_fn(query)

    # Get all places with embeddings
    places = graph.query("""
        MATCH (p:Place)
        WHERE p.detail_embedding IS NOT NULL
        RETURN p.id, p.name, p.detail_embedding
    """)

    # Compute similarities
    scored = []
    for place in places:
        sim = cosine_similarity(query_embedding, place['detail_embedding'])
        scored.append((place, sim))

    # Return top-k
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored[:top_k]]
```

---

## Data File

Places stored in `data/world/places.yaml`:

```yaml
places:
  # Regions
  - id: place_northumbria
    name: Northumbria
    coordinates: [54.5, -1.5]
    scale: region
    type: region
    contains:
      - place_york
      - place_durham
      - place_whitby

  # Settlements
  - id: place_york
    name: York
    coordinates: [53.96, -1.08]
    scale: settlement
    type: city
    detail: "The second city of England."
    contains:
      - place_york_market
      - place_york_minster

  # Districts
  - id: place_york_market
    name: York Market
    coordinates: [53.959, -1.082]
    scale: district
    type: market
    contains:
      - place_merchants_hall
```

---

*"Places nest. Settlements contain districts. Districts contain buildings. The hierarchy is the map."*

---

## ROUTE Link Schema

Routes connect settlements and regions. Not used within settlements.

```yaml
ROUTE:
  # Stored (traced input)
  waypoints: float[][]      # [[lat, lng], [lat, lng], ...]
  road_type: string         # roman | track | path | river | none

  # Computed at creation
  distance_km: float
  travel_minutes: int
  difficulty: string        # easy | moderate | hard | dangerous

  # Optional
  detail: string            # "Crosses marshland near Humber"
```

### Field Details

| Field | Source | Notes |
|-------|--------|-------|
| `waypoints` | Traced | Array of [lat, lng] points |
| `road_type` | Manual | Determines speed and difficulty |
| `distance_km` | Computed | Sum of haversine distances |
| `travel_minutes` | Computed | distance / speed |
| `difficulty` | Derived | From road_type |
| `detail` | Optional | For Narrator flavor |

---

## Route Types

| Type | Speed (km/h) | Difficulty | Description |
|------|--------------|------------|-------------|
| `roman` | 5.0 | easy | Paved roads from Roman era |
| `track` | 3.5 | moderate | Unpaved but clear path |
| `path` | 2.5 | hard | Rough trail through terrain |
| `river` | 8.0 | moderate | Downstream by boat |
| `none` | 1.5 | dangerous | Cross-country, no path |

---

## Distance Computation

### Haversine Formula

```python
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1: list, coord2: list) -> float:
    """
    Distance in km between two [lat, lng] points.
    Uses haversine formula for great-circle distance.
    """
    R = 6371  # Earth radius in km

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c
```

### Route Distance

```python
def compute_route_distance(waypoints: list) -> float:
    """Total distance along waypoints in km."""
    total = 0
    for i in range(len(waypoints) - 1):
        total += haversine(waypoints[i], waypoints[i+1])
    return round(total, 2)
```

---

## Travel Time Computation

```python
SPEEDS_KMH = {
    "roman": 5.0,      # Good road, on foot
    "track": 3.5,      # Unpaved but clear
    "path": 2.5,       # Rough trail
    "river": 8.0,      # Downstream by boat
    "none": 1.5        # Cross-country
}

DIFFICULTIES = {
    "roman": "easy",
    "track": "moderate",
    "path": "hard",
    "river": "moderate",
    "none": "dangerous"
}

def compute_travel_time(distance_km: float, road_type: str) -> int:
    """Compute travel time in minutes."""
    speed = SPEEDS_KMH[road_type]
    travel_hours = distance_km / speed
    return int(travel_hours * 60)
```

---

## Creating Routes

```python
def create_route(
    from_place: str,
    to_place: str,
    waypoints: list,
    road_type: str,
    detail: str = None
) -> dict:
    """
    Create a route with computed attributes.

    Args:
        from_place: Starting place ID
        to_place: Destination place ID
        waypoints: List of [lat, lng] coordinates
        road_type: Type of road (roman, track, path, river, none)
        detail: Optional description

    Returns:
        Route dict ready for graph insertion
    """
    distance_km = compute_route_distance(waypoints)
    travel_minutes = compute_travel_time(distance_km, road_type)

    return {
        "from": from_place,
        "to": to_place,
        "waypoints": waypoints,
        "road_type": road_type,
        "distance_km": distance_km,
        "travel_minutes": travel_minutes,
        "difficulty": DIFFICULTIES[road_type],
        "detail": detail
    }
```

### Example

```python
route = create_route(
    from_place="place_york",
    to_place="place_durham",
    waypoints=[
        [53.96, -1.08],   # York
        [54.12, -1.20],   # Waypoint
        [54.35, -1.45],   # Waypoint
        [54.78, -1.57]    # Durham
    ],
    road_type="roman",
    detail="The old Roman road north. Well-maintained."
)

# Result:
# {
#   "from": "place_york",
#   "to": "place_durham",
#   "waypoints": [...],
#   "road_type": "roman",
#   "distance_km": 96.5,
#   "travel_minutes": 1158,  # ~19.3 hours
#   "difficulty": "easy",
#   "detail": "The old Roman road north..."
# }
```

---

## Graph Storage

### Cypher: Create Route

```cypher
MATCH (from:Place {id: $from_id})
MATCH (to:Place {id: $to_id})
CREATE (from)-[r:ROUTE {
  waypoints: $waypoints,
  road_type: $road_type,
  distance_km: $distance_km,
  travel_minutes: $travel_minutes,
  difficulty: $difficulty,
  detail: $detail
}]->(to)
```

### Bidirectional Routes

Most routes work both ways. Create two links:

```python
def create_bidirectional_route(route_data: dict, graph):
    """Create route in both directions."""
    # Forward
    graph.create_route(
        from_place=route_data['from'],
        to_place=route_data['to'],
        **route_data
    )

    # Reverse (swap endpoints, reverse waypoints)
    graph.create_route(
        from_place=route_data['to'],
        to_place=route_data['from'],
        waypoints=list(reversed(route_data['waypoints'])),
        road_type=route_data['road_type'],
        distance_km=route_data['distance_km'],
        travel_minutes=route_data['travel_minutes'],
        difficulty=route_data['difficulty'],
        detail=route_data.get('detail')
    )
```

**Exception: Rivers.** Downstream is faster than upstream.

```python
def create_river_route(route_data: dict, graph):
    """River routes with different upstream/downstream speeds."""
    # Downstream (fast)
    graph.create_route(
        from_place=route_data['from'],
        to_place=route_data['to'],
        road_type='river',
        travel_minutes=route_data['travel_minutes'],
        **route_data
    )

    # Upstream (slower - 3 km/h instead of 8)
    upstream_time = int(route_data['distance_km'] / 3.0 * 60)
    graph.create_route(
        from_place=route_data['to'],
        to_place=route_data['from'],
        waypoints=list(reversed(route_data['waypoints'])),
        road_type='river',
        travel_minutes=upstream_time,
        difficulty='hard',
        detail="Upstream. Slow going."
    )
```

---

## Movement Rules

### Within Same Place

No route needed. Use scale-based defaults:

```python
WITHIN_SCALE_MINUTES = {
    'room': 0,        # Instant
    'building': 1,    # ~1 min between rooms
    'district': 5,    # ~5 min between buildings
    'settlement': 15  # ~15 min between districts
}
```

### Between Different Places

```python
def get_travel_time(from_place: Place, to_place: Place, graph) -> int | None:
    """
    Get travel time between two places.

    Returns:
        Travel time in minutes, or None if no route exists.
    """
    # Same place
    if from_place.id == to_place.id:
        return 0

    # Get parents
    from_parent = graph.get_parent(from_place)
    to_parent = graph.get_parent(to_place)

    # Same parent → use scale-based default
    if from_parent and from_parent.id == to_parent.id:
        return WITHIN_SCALE_MINUTES.get(from_place.scale, 15)

    # Different parents → check for route at settlement level
    from_settlement = graph.get_containing_settlement(from_place)
    to_settlement = graph.get_containing_settlement(to_place)

    if from_settlement.id == to_settlement.id:
        # Same settlement, different districts
        return 15

    # Different settlements → need route
    route = graph.get_route(from_settlement.id, to_settlement.id)
    if route:
        return route['travel_minutes']

    # No direct route
    return None
```

### Finding Containing Settlement

```python
def get_containing_settlement(place: Place, graph) -> Place:
    """Walk up hierarchy to find settlement."""
    current = place

    while current.scale != 'settlement':
        parent = graph.get_parent(current)
        if parent is None:
            return current  # Already at top
        current = parent

    return current
```

---

## Route Queries

### Get Direct Route

```cypher
MATCH (from:Place {id: $from_id})-[r:ROUTE]->(to:Place {id: $to_id})
RETURN r
```

### Get All Routes From Place

```cypher
MATCH (from:Place {id: $place_id})-[r:ROUTE]->(to:Place)
RETURN to.id, to.name, r.travel_minutes, r.difficulty
ORDER BY r.travel_minutes
```

### Find Path (Multi-Hop)

```cypher
MATCH path = shortestPath(
  (from:Place {id: $from_id})-[:ROUTE*..5]->(to:Place {id: $to_id})
)
RETURN [node IN nodes(path) | node.id] AS places,
       [rel IN relationships(path) | rel.travel_minutes] AS times
```

---

## Position Along Route

For showing player/NPC during travel:

```python
def get_position_at_progress(route: dict, progress: float) -> list:
    """
    Get [lat, lng] position along route.

    Args:
        route: Route with waypoints
        progress: 0.0 (start) to 1.0 (end)

    Returns:
        [lat, lng] coordinate
    """
    waypoints = route['waypoints']
    total_dist = route['distance_km']
    target_dist = total_dist * progress

    accumulated = 0
    for i in range(1, len(waypoints)):
        segment_dist = haversine(waypoints[i-1], waypoints[i])

        if accumulated + segment_dist >= target_dist:
            # Interpolate within segment
            t = (target_dist - accumulated) / segment_dist
            lat = waypoints[i-1][0] + (waypoints[i][0] - waypoints[i-1][0]) * t
            lng = waypoints[i-1][1] + (waypoints[i][1] - waypoints[i-1][1]) * t
            return [lat, lng]

        accumulated += segment_dist

    # At end
    return waypoints[-1]
```

---

## Data File

Routes stored in `data/world/routes.yaml`:

```yaml
routes:
  # York to Durham (Roman road)
  - from: place_york
    to: place_durham
    waypoints:
      - [53.96, -1.08]
      - [54.12, -1.20]
      - [54.35, -1.45]
      - [54.78, -1.57]
    road_type: roman
    detail: "The old Roman road north."

  # York to Scarborough (track)
  - from: place_york
    to: place_scarborough
    waypoints:
      - [53.96, -1.08]
      - [54.05, -0.85]
      - [54.15, -0.60]
      - [54.28, -0.40]
    road_type: track
    detail: "East through the wolds."

  # York to Whitby (path through moors)
  - from: place_york
    to: place_whitby
    waypoints:
      - [53.96, -1.08]
      - [54.15, -0.90]
      - [54.30, -0.75]
      - [54.49, -0.61]
    road_type: path
    detail: "Hard going through the North York Moors."
```

---

## Route Tracing Tool

One-time dev tool to trace routes on the map:

```javascript
function RouteTracer({ onSaveRoute }) {
  const [waypoints, setWaypoints] = useState([]);
  const [roadType, setRoadType] = useState('track');
  const [selectedFrom, setSelectedFrom] = useState(null);
  const [selectedTo, setSelectedTo] = useState(null);

  const handleMapClick = (e) => {
    const [lat, lng] = unproject(e.offsetX, e.offsetY, width, height);
    setWaypoints([...waypoints, [lat, lng]]);
  };

  const handleSave = () => {
    if (!selectedFrom || !selectedTo || waypoints.length < 2) return;

    onSaveRoute({
      from: selectedFrom,
      to: selectedTo,
      waypoints,
      road_type: roadType
    });

    // Reset
    setWaypoints([]);
    setSelectedFrom(null);
    setSelectedTo(null);
  };

  const handleUndo = () => {
    setWaypoints(waypoints.slice(0, -1));
  };

  // Render map with click handler and current waypoints
  // ...
}
```

**Usage:**
1. Select "from" place
2. Select "to" place
3. Click map to add waypoints
4. Choose road type
5. Save → exports to YAML

---

*"Routes are real paths, not teleportation. Distance matters. Road type matters. The journey is part of the story."*
---

## Places

## Place Schema

```yaml
Place:
  id: string              # place_york, place_york_market
  name: string            # "York", "York Market"
  coordinates: [float, float]  # [lat, lng]
  scale: string           # region | settlement | district | building | room
  type: string            # city | village | monastery | hold | crossing | etc
  detail: string          # Atmosphere, description
  detail_embedding: float[]  # Embedded if detail > 20 chars
```

### Field Details

| Field | Required | Notes |
|-------|----------|-------|
| `id` | Yes | Unique, prefixed `place_` |
| `name` | Yes | Display name |
| `coordinates` | Yes | [latitude, longitude] |
| `scale` | Yes | Determines movement rules |
| `type` | Yes | Determines icon |
| `detail` | No | Atmosphere/description for Narrator |
| `detail_embedding` | Auto | Generated if detail > 20 chars |

---

## Scale Levels

Five hierarchical scales:

| Scale | Examples | Typical Area | Movement Within |
|-------|----------|--------------|-----------------|
| `region` | Northumbria, Yorkshire | 1000+ km² | Requires ROUTE |
| `settlement` | York, Durham, Whitby | 1-10 km² | Free (~15 min between districts) |
| `district` | York Market, Minster Quarter | 0.1-1 km² | Free (~5 min between buildings) |
| `building` | Merchant's Hall, The Minster | 100-10000 m² | Free (~1 min between rooms) |
| `room` | Back Room, Crypt | 10-500 m² | Instant |

### Scale Rules

```python
SCALE_HIERARCHY = ['region', 'settlement', 'district', 'building', 'room']

def can_contain(parent_scale, child_scale):
    """Check if parent scale can contain child scale."""
    parent_idx = SCALE_HIERARCHY.index(parent_scale)
    child_idx = SCALE_HIERARCHY.index(child_scale)
    return child_idx == parent_idx + 1

# region can contain settlement
# settlement can contain district
# district can contain building
# building can contain room
# room contains nothing
```

---

## Place Types

Types determine map icons:

| Type | Icon | Typical Scale |
|------|------|---------------|
| `city` | ⬡ | settlement |
| `town` | ◆ | settlement |
| `village` | ● | settlement |
| `monastery` | † | settlement/building |
| `hold` | ▲ | settlement/building |
| `crossing` | ═ | settlement |
| `landmark` | ★ | any |
| `market` | ◇ | district |
| `quarter` | □ | district |
| `hall` | ⌂ | building |
| `church` | ✝ | building |
| `tavern` | ⌐ | building |
| `house` | ⌂ | building |

---

## CONTAINS Link (Hierarchy)

Binary relationship — no attributes:

```cypher
(parent:Place)-[:CONTAINS]->(child:Place)
```

### Example Hierarchy

```
place_northumbria (region)
    │
    └── CONTAINS
            │
            ▼
        place_york (settlement)
            │
            ├── CONTAINS → place_york_market (district)
            │                  │
            │                  └── CONTAINS → place_merchants_hall (building)
            │                                     │
            │                                     └── CONTAINS → place_back_room (room)
            │
            └── CONTAINS → place_york_minster (building)
```

### Query: Get Parent

```cypher
MATCH (parent:Place)-[:CONTAINS]->(child:Place {id: $place_id})
RETURN parent
```

### Query: Get Children

```cypher
MATCH (parent:Place {id: $place_id})-[:CONTAINS]->(child:Place)
RETURN child
ORDER BY child.name
```

### Query: Get Full Path

```cypher
MATCH path = (region:Place {scale: 'region'})-[:CONTAINS*]->(place:Place {id: $place_id})
RETURN [node IN nodes(path) | node.name] AS path_names
```

---

## Creating Places

### Validation

```python
def validate_place(place: dict) -> bool:
    """Validate place before creation."""

    # Required fields
    required = ['id', 'name', 'coordinates', 'scale', 'type']
    for field in required:
        if field not in place:
            raise ValueError(f"Missing required field: {field}")

    # ID format
    if not place['id'].startswith('place_'):
        raise ValueError("Place ID must start with 'place_'")

    # Coordinates
    lat, lng = place['coordinates']
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise ValueError("Invalid coordinates")

    # Scale
    if place['scale'] not in SCALE_HIERARCHY:
        raise ValueError(f"Invalid scale: {place['scale']}")

    return True
```

### Cypher: Create Place

```cypher
CREATE (p:Place {
  id: $id,
  name: $name,
  coordinates: $coordinates,
  scale: $scale,
  type: $type,
  detail: $detail
})
RETURN p
```

### Cypher: Add to Hierarchy

```cypher
MATCH (parent:Place {id: $parent_id})
MATCH (child:Place {id: $child_id})
CREATE (parent)-[:CONTAINS]->(child)
```

---

## Example Places

### Region

```yaml
- id: place_northumbria
  name: Northumbria
  coordinates: [54.5, -1.5]
  scale: region
  type: region
  detail: "The great northern kingdom, now under Norman control."
```

### Settlement

```yaml
- id: place_york
  name: York
  coordinates: [53.96, -1.08]
  scale: settlement
  type: city
  detail: "The second city of England. Norman banners fly from its walls."
```

### District

```yaml
- id: place_york_market
  name: York Market
  coordinates: [53.959, -1.082]
  scale: district
  type: market
  detail: "The heart of trade. Stalls crowd the square. Voices in English and Norman."
```

### Building

```yaml
- id: place_merchants_hall
  name: Merchant's Hall
  coordinates: [53.958, -1.081]
  scale: building
  type: hall
  detail: "Stone and timber. The smell of wool and coin."
```

### Room

```yaml
- id: place_back_room
  name: Back Room
  coordinates: [53.958, -1.081]
  scale: room
  type: room
  detail: "Private. A table, two chairs, a locked chest."
```

---

## Coordinate System

### Northern England Bounds

```python
BOUNDS = {
    'north': 55.5,
    'south': 53.0,
    'east': 0.5,
    'west': -3.0
}
```

### Reference Coordinates

| Place | Lat | Lng |
|-------|-----|-----|
| York | 53.96 | -1.08 |
| Durham | 54.78 | -1.57 |
| Scarborough | 54.28 | -0.40 |
| Whitby | 54.49 | -0.61 |
| Ripon | 54.14 | -1.52 |
| Newcastle | 54.97 | -1.61 |

### Rooms Share Parent Coordinates

Rooms within a building use the building's coordinates. No sub-meter precision needed.

```python
def get_display_coordinates(place: Place, graph) -> tuple:
    """Get coordinates for display. Rooms inherit from building."""
    if place.scale == 'room':
        parent = graph.get_parent(place)
        return parent.coordinates
    return place.coordinates
```

---

## Scale-Based Defaults

When Narrator needs movement time within a location:

```python
WITHIN_SCALE_MINUTES = {
    'room': 0,        # Instant
    'building': 1,    # ~1 min between rooms
    'district': 5,    # ~5 min between buildings
    'settlement': 15  # ~15 min between districts
}

def get_movement_within(place: Place) -> int:
    """Default movement time within a place."""
    return WITHIN_SCALE_MINUTES.get(place.scale, 0)
```

---

## Embedding Detail

For semantic search of places by description:

```python
def maybe_embed_detail(place: dict, embed_fn) -> dict:
    """Embed detail if long enough."""
    detail = place.get('detail', '')

    if len(detail) > 20:
        place['detail_embedding'] = embed_fn(detail)

    return place
```

### Query: Find Places by Description

```python
def find_places_by_description(query: str, embed_fn, graph, top_k=5):
    """Semantic search for places."""
    query_embedding = embed_fn(query)

    # Get all places with embeddings
    places = graph.query("""
        MATCH (p:Place)
        WHERE p.detail_embedding IS NOT NULL
        RETURN p.id, p.name, p.detail_embedding
    """)

    # Compute similarities
    scored = []
    for place in places:
        sim = cosine_similarity(query_embedding, place['detail_embedding'])
        scored.append((place, sim))

    # Return top-k
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored[:top_k]]
```

---

## Data File

Places stored in `data/world/places.yaml`:

```yaml
places:
  # Regions
  - id: place_northumbria
    name: Northumbria
    coordinates: [54.5, -1.5]
    scale: region
    type: region
    contains:
      - place_york
      - place_durham
      - place_whitby

  # Settlements
  - id: place_york
    name: York
    coordinates: [53.96, -1.08]
    scale: settlement
    type: city
    detail: "The second city of England."
    contains:
      - place_york_market
      - place_york_minster

  # Districts
  - id: place_york_market
    name: York Market
    coordinates: [53.959, -1.082]
    scale: district
    type: market
    contains:
      - place_merchants_hall
```

---

*"Places nest. Settlements contain districts. Districts contain buildings. The hierarchy is the map."*

---

## Routes

## ROUTE Link Schema

Routes connect settlements and regions. Not used within settlements.

```yaml
ROUTE:
  # Stored (traced input)
  waypoints: float[][]      # [[lat, lng], [lat, lng], ...]
  road_type: string         # roman | track | path | river | none

  # Computed at creation
  distance_km: float
  travel_minutes: int
  difficulty: string        # easy | moderate | hard | dangerous

  # Optional
  detail: string            # "Crosses marshland near Humber"
```

### Field Details

| Field | Source | Notes |
|-------|--------|-------|
| `waypoints` | Traced | Array of [lat, lng] points |
| `road_type` | Manual | Determines speed and difficulty |
| `distance_km` | Computed | Sum of haversine distances |
| `travel_minutes` | Computed | distance / speed |
| `difficulty` | Derived | From road_type |
| `detail` | Optional | For Narrator flavor |

---

## Route Types

| Type | Speed (km/h) | Difficulty | Description |
|------|--------------|------------|-------------|
| `roman` | 5.0 | easy | Paved roads from Roman era |
| `track` | 3.5 | moderate | Unpaved but clear path |
| `path` | 2.5 | hard | Rough trail through terrain |
| `river` | 8.0 | moderate | Downstream by boat |
| `none` | 1.5 | dangerous | Cross-country, no path |

---

## Distance Computation

### Haversine Formula

```python
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1: list, coord2: list) -> float:
    """
    Distance in km between two [lat, lng] points.
    Uses haversine formula for great-circle distance.
    """
    R = 6371  # Earth radius in km

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c
```

### Route Distance

```python
def compute_route_distance(waypoints: list) -> float:
    """Total distance along waypoints in km."""
    total = 0
    for i in range(len(waypoints) - 1):
        total += haversine(waypoints[i], waypoints[i+1])
    return round(total, 2)
```

---

## Travel Time Computation

```python
SPEEDS_KMH = {
    "roman": 5.0,      # Good road, on foot
    "track": 3.5,      # Unpaved but clear
    "path": 2.5,       # Rough trail
    "river": 8.0,      # Downstream by boat
    "none": 1.5        # Cross-country
}

DIFFICULTIES = {
    "roman": "easy",
    "track": "moderate",
    "path": "hard",
    "river": "moderate",
    "none": "dangerous"
}

def compute_travel_time(distance_km: float, road_type: str) -> int:
    """Compute travel time in minutes."""
    speed = SPEEDS_KMH[road_type]
    travel_hours = distance_km / speed
    return int(travel_hours * 60)
```

---

## Creating Routes

```python
def create_route(
    from_place: str,
    to_place: str,
    waypoints: list,
    road_type: str,
    detail: str = None
) -> dict:
    """
    Create a route with computed attributes.

    Args:
        from_place: Starting place ID
        to_place: Destination place ID
        waypoints: List of [lat, lng] coordinates
        road_type: Type of road (roman, track, path, river, none)
        detail: Optional description

    Returns:
        Route dict ready for graph insertion
    """
    distance_km = compute_route_distance(waypoints)
    travel_minutes = compute_travel_time(distance_km, road_type)

    return {
        "from": from_place,
        "to": to_place,
        "waypoints": waypoints,
        "road_type": road_type,
        "distance_km": distance_km,
        "travel_minutes": travel_minutes,
        "difficulty": DIFFICULTIES[road_type],
        "detail": detail
    }
```

### Example

```python
route = create_route(
    from_place="place_york",
    to_place="place_durham",
    waypoints=[
        [53.96, -1.08],   # York
        [54.12, -1.20],   # Waypoint
        [54.35, -1.45],   # Waypoint
        [54.78, -1.57]    # Durham
    ],
    road_type="roman",
    detail="The old Roman road north. Well-maintained."
)

# Result:
# {
#   "from": "place_york",
#   "to": "place_durham",
#   "waypoints": [...],
#   "road_type": "roman",
#   "distance_km": 96.5,
#   "travel_minutes": 1158,  # ~19.3 hours
#   "difficulty": "easy",
#   "detail": "The old Roman road north..."
# }
```

---

## Graph Storage

### Cypher: Create Route

```cypher
MATCH (from:Place {id: $from_id})
MATCH (to:Place {id: $to_id})
CREATE (from)-[r:ROUTE {
  waypoints: $waypoints,
  road_type: $road_type,
  distance_km: $distance_km,
  travel_minutes: $travel_minutes,
  difficulty: $difficulty,
  detail: $detail
}]->(to)
```

### Bidirectional Routes

Most routes work both ways. Create two links:

```python
def create_bidirectional_route(route_data: dict, graph):
    """Create route in both directions."""
    # Forward
    graph.create_route(
        from_place=route_data['from'],
        to_place=route_data['to'],
        **route_data
    )

    # Reverse (swap endpoints, reverse waypoints)
    graph.create_route(
        from_place=route_data['to'],
        to_place=route_data['from'],
        waypoints=list(reversed(route_data['waypoints'])),
        road_type=route_data['road_type'],
        distance_km=route_data['distance_km'],
        travel_minutes=route_data['travel_minutes'],
        difficulty=route_data['difficulty'],
        detail=route_data.get('detail')
    )
```

**Exception: Rivers.** Downstream is faster than upstream.

```python
def create_river_route(route_data: dict, graph):
    """River routes with different upstream/downstream speeds."""
    # Downstream (fast)
    graph.create_route(
        from_place=route_data['from'],
        to_place=route_data['to'],
        road_type='river',
        travel_minutes=route_data['travel_minutes'],
        **route_data
    )

    # Upstream (slower - 3 km/h instead of 8)
    upstream_time = int(route_data['distance_km'] / 3.0 * 60)
    graph.create_route(
        from_place=route_data['to'],
        to_place=route_data['from'],
        waypoints=list(reversed(route_data['waypoints'])),
        road_type='river',
        travel_minutes=upstream_time,
        difficulty='hard',
        detail="Upstream. Slow going."
    )
```

---

## Movement Rules

### Within Same Place

No route needed. Use scale-based defaults:

```python
WITHIN_SCALE_MINUTES = {
    'room': 0,        # Instant
    'building': 1,    # ~1 min between rooms
    'district': 5,    # ~5 min between buildings
    'settlement': 15  # ~15 min between districts
}
```

### Between Different Places

```python
def get_travel_time(from_place: Place, to_place: Place, graph) -> int | None:
    """
    Get travel time between two places.

    Returns:
        Travel time in minutes, or None if no route exists.
    """
    # Same place
    if from_place.id == to_place.id:
        return 0

    # Get parents
    from_parent = graph.get_parent(from_place)
    to_parent = graph.get_parent(to_place)

    # Same parent → use scale-based default
    if from_parent and from_parent.id == to_parent.id:
        return WITHIN_SCALE_MINUTES.get(from_place.scale, 15)

    # Different parents → check for route at settlement level
    from_settlement = graph.get_containing_settlement(from_place)
    to_settlement = graph.get_containing_settlement(to_place)

    if from_settlement.id == to_settlement.id:
        # Same settlement, different districts
        return 15

    # Different settlements → need route
    route = graph.get_route(from_settlement.id, to_settlement.id)
    if route:
        return route['travel_minutes']

    # No direct route
    return None
```

### Finding Containing Settlement

```python
def get_containing_settlement(place: Place, graph) -> Place:
    """Walk up hierarchy to find settlement."""
    current = place

    while current.scale != 'settlement':
        parent = graph.get_parent(current)
        if parent is None:
            return current  # Already at top
        current = parent

    return current
```

---

## Route Queries

### Get Direct Route

```cypher
MATCH (from:Place {id: $from_id})-[r:ROUTE]->(to:Place {id: $to_id})
RETURN r
```

### Get All Routes From Place

```cypher
MATCH (from:Place {id: $place_id})-[r:ROUTE]->(to:Place)
RETURN to.id, to.name, r.travel_minutes, r.difficulty
ORDER BY r.travel_minutes
```

### Find Path (Multi-Hop)

```cypher
MATCH path = shortestPath(
  (from:Place {id: $from_id})-[:ROUTE*..5]->(to:Place {id: $to_id})
)
RETURN [node IN nodes(path) | node.id] AS places,
       [rel IN relationships(path) | rel.travel_minutes] AS times
```

---

## Position Along Route

For showing player/NPC during travel:

```python
def get_position_at_progress(route: dict, progress: float) -> list:
    """
    Get [lat, lng] position along route.

    Args:
        route: Route with waypoints
        progress: 0.0 (start) to 1.0 (end)

    Returns:
        [lat, lng] coordinate
    """
    waypoints = route['waypoints']
    total_dist = route['distance_km']
    target_dist = total_dist * progress

    accumulated = 0
    for i in range(1, len(waypoints)):
        segment_dist = haversine(waypoints[i-1], waypoints[i])

        if accumulated + segment_dist >= target_dist:
            # Interpolate within segment
            t = (target_dist - accumulated) / segment_dist
            lat = waypoints[i-1][0] + (waypoints[i][0] - waypoints[i-1][0]) * t
            lng = waypoints[i-1][1] + (waypoints[i][1] - waypoints[i-1][1]) * t
            return [lat, lng]

        accumulated += segment_dist

    # At end
    return waypoints[-1]
```

---

## Data File

Routes stored in `data/world/routes.yaml`:

```yaml
routes:
  # York to Durham (Roman road)
  - from: place_york
    to: place_durham
    waypoints:
      - [53.96, -1.08]
      - [54.12, -1.20]
      - [54.35, -1.45]
      - [54.78, -1.57]
    road_type: roman
    detail: "The old Roman road north."

  # York to Scarborough (track)
  - from: place_york
    to: place_scarborough
    waypoints:
      - [53.96, -1.08]
      - [54.05, -0.85]
      - [54.15, -0.60]
      - [54.28, -0.40]
    road_type: track
    detail: "East through the wolds."

  # York to Whitby (path through moors)
  - from: place_york
    to: place_whitby
    waypoints:
      - [53.96, -1.08]
      - [54.15, -0.90]
      - [54.30, -0.75]
      - [54.49, -0.61]
    road_type: path
    detail: "Hard going through the North York Moors."
```

---

## Route Tracing Tool

One-time dev tool to trace routes on the map:

```javascript
function RouteTracer({ onSaveRoute }) {
  const [waypoints, setWaypoints] = useState([]);
  const [roadType, setRoadType] = useState('track');
  const [selectedFrom, setSelectedFrom] = useState(null);
  const [selectedTo, setSelectedTo] = useState(null);

  const handleMapClick = (e) => {
    const [lat, lng] = unproject(e.offsetX, e.offsetY, width, height);
    setWaypoints([...waypoints, [lat, lng]]);
  };

  const handleSave = () => {
    if (!selectedFrom || !selectedTo || waypoints.length < 2) return;

    onSaveRoute({
      from: selectedFrom,
      to: selectedTo,
      waypoints,
      road_type: roadType
    });

    // Reset
    setWaypoints([]);
    setSelectedFrom(null);
    setSelectedTo(null);
  };

  const handleUndo = () => {
    setWaypoints(waypoints.slice(0, -1));
  };

  // Render map with click handler and current waypoints
  // ...
}
```

**Usage:**
1. Select "from" place
2. Select "to" place
3. Click map to add waypoints
4. Choose road type
5. Save → exports to YAML

---

*"Routes are real paths, not teleportation. Distance matters. Road type matters. The journey is part of the story."*
