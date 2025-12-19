# Map System — Algorithm: Rendering

```
CREATED: 2024-12-16
STATUS: Canonical
```

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
