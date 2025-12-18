'use client';

import { useRef, useEffect, useCallback, useState } from 'react';
import {
  Place,
  Route,
  VisibilityState,
  VisibilityLevel,
  MapProps,
  PlaceHoverInfo,
} from '@/types/map';
import { project, haversine } from '@/lib/map';
import { seededRandom, hashString } from '@/lib/map';
import { coastlinePoints } from '@/data/map-data';

// =============================================================================
// CONSTANTS
// =============================================================================

const PLACE_COLORS: Record<VisibilityLevel, string> = {
  unknown: 'transparent',
  rumored: 'rgba(139, 90, 43, 0.4)',
  known: 'rgba(139, 90, 43, 0.7)',
  familiar: 'rgba(180, 120, 60, 1)',
};

const ROUTE_COLORS: Record<VisibilityLevel, string> = {
  unknown: 'transparent',
  rumored: 'rgba(90, 60, 40, 0.5)',
  known: 'rgba(80, 50, 30, 0.7)',
  familiar: 'rgba(70, 40, 20, 0.9)',
};

const PLACE_SIZES: Record<string, number> = {
  city: 12,
  town: 8,
  village: 5,
  monastery: 7,
  hold: 9,
  crossing: 4,
  landmark: 6,
  region: 0, // Regions don't render as points
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getPlaceVisibility(
  placeId: string,
  visibility: VisibilityState
): VisibilityLevel {
  return visibility.places[placeId]?.level || 'unknown';
}

function getRouteVisibility(
  routeId: string,
  visibility: VisibilityState
): VisibilityLevel {
  return visibility.routes[routeId]?.level || 'unknown';
}

function wobblePoint(
  x: number,
  y: number,
  random: () => number,
  amount: number = 2
): [number, number] {
  return [x + (random() - 0.5) * amount, y + (random() - 0.5) * amount];
}

// =============================================================================
// RENDERING LAYERS
// =============================================================================

function drawParchmentLayer(
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number
) {
  // Base parchment color
  const gradient = ctx.createRadialGradient(
    width / 2,
    height / 2,
    0,
    width / 2,
    height / 2,
    Math.max(width, height) * 0.7
  );
  gradient.addColorStop(0, '#d4c4a8');
  gradient.addColorStop(0.5, '#c9b896');
  gradient.addColorStop(1, '#b8a682');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);

  // Add subtle noise texture
  const random = seededRandom(42);
  ctx.fillStyle = 'rgba(80, 60, 40, 0.03)';
  for (let i = 0; i < 1000; i++) {
    const x = random() * width;
    const y = random() * height;
    const size = random() * 3 + 1;
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fill();
  }

  // Edge darkening (vignette)
  const edgeGradient = ctx.createRadialGradient(
    width / 2,
    height / 2,
    Math.min(width, height) * 0.3,
    width / 2,
    height / 2,
    Math.max(width, height) * 0.7
  );
  edgeGradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
  edgeGradient.addColorStop(1, 'rgba(60, 40, 20, 0.15)');
  ctx.fillStyle = edgeGradient;
  ctx.fillRect(0, 0, width, height);
}

// Terrain data - rivers and uplands
const RIVERS: { name: string; points: [number, number][] }[] = [
  {
    name: 'Ouse',
    points: [
      [54.02, -1.08], // Near York
      [53.96, -1.08], // York
      [53.85, -1.05],
      [53.75, -0.95],
    ],
  },
  {
    name: 'Derwent',
    points: [
      [54.10, -0.95],
      [54.00, -0.91], // Stamford Bridge
      [53.92, -0.88],
    ],
  },
  {
    name: 'Tees',
    points: [
      [54.52, -1.55], // Darlington
      [54.55, -1.30],
      [54.58, -1.10],
      [54.62, -0.90],
    ],
  },
  {
    name: 'Swale',
    points: [
      [54.40, -1.74], // Richmond
      [54.35, -1.60],
      [54.30, -1.45],
      [54.25, -1.30],
    ],
  },
];

const UPLANDS: { name: string; center: [number, number]; radius: number }[] = [
  { name: 'North York Moors', center: [54.35, -0.85], radius: 0.35 },
  { name: 'Pennines', center: [54.45, -2.10], radius: 0.4 },
  { name: 'Cleveland Hills', center: [54.42, -1.15], radius: 0.2 },
];

function drawTerrainLayer(
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number
) {
  const random = seededRandom(hashString('terrain'));

  // Draw upland/moorland areas with stippling
  UPLANDS.forEach((upland) => {
    const [cx, cy] = project(upland.center[0], upland.center[1], width, height);
    const radiusPx = (upland.radius / 2.5) * width; // Scale radius to pixels

    // Subtle fill for moorland
    const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, radiusPx);
    gradient.addColorStop(0, 'rgba(120, 100, 70, 0.15)');
    gradient.addColorStop(0.7, 'rgba(110, 95, 65, 0.1)');
    gradient.addColorStop(1, 'rgba(100, 90, 60, 0)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(cx, cy, radiusPx, 0, Math.PI * 2);
    ctx.fill();

    // Hill hachures/stippling
    ctx.fillStyle = 'rgba(80, 60, 40, 0.2)';
    for (let i = 0; i < 60; i++) {
      const angle = random() * Math.PI * 2;
      const dist = random() * radiusPx * 0.8;
      const x = cx + Math.cos(angle) * dist;
      const y = cy + Math.sin(angle) * dist;

      // Small hatches pointing downhill (away from center)
      const hatchAngle = Math.atan2(y - cy, x - cx);
      const len = 3 + random() * 4;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + Math.cos(hatchAngle) * len, y + Math.sin(hatchAngle) * len);
      ctx.strokeStyle = 'rgba(80, 60, 40, 0.25)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  });

  // Draw rivers
  ctx.strokeStyle = 'rgba(70, 100, 130, 0.4)';
  ctx.lineWidth = 2;
  ctx.setLineDash([]);

  RIVERS.forEach((river) => {
    const riverRandom = seededRandom(hashString(river.name));
    ctx.beginPath();
    river.points.forEach((point, i) => {
      const [x, y] = project(point[0], point[1], width, height);
      const [wx, wy] = wobblePoint(x, y, riverRandom, 2);
      if (i === 0) {
        ctx.moveTo(wx, wy);
      } else {
        // Curved river using quadratic bezier
        const prevPoint = river.points[i - 1];
        const [px, py] = project(prevPoint[0], prevPoint[1], width, height);
        const [pwx, pwy] = wobblePoint(px, py, riverRandom, 2);
        const cpx = (pwx + wx) / 2 + (riverRandom() - 0.5) * 15;
        const cpy = (pwy + wy) / 2 + (riverRandom() - 0.5) * 15;
        ctx.quadraticCurveTo(cpx, cpy, wx, wy);
      }
    });
    ctx.stroke();
  });
}

function drawCoastlineLayer(
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number
) {
  const random = seededRandom(hashString('coastline'));

  // Draw sea area (everything to the east)
  ctx.fillStyle = 'rgba(70, 100, 120, 0.2)';
  ctx.beginPath();

  // Start from top-right corner
  ctx.moveTo(width, 0);

  // Draw along coastline
  coastlinePoints.forEach((point, i) => {
    const [x, y] = project(point[0], point[1], width, height);
    const [wx, wy] = wobblePoint(x, y, random, 3);
    if (i === 0) {
      ctx.lineTo(wx, wy);
    } else {
      ctx.lineTo(wx, wy);
    }
  });

  // Complete the sea area
  ctx.lineTo(width, height);
  ctx.lineTo(width, 0);
  ctx.closePath();
  ctx.fill();

  // Draw coastline itself
  ctx.strokeStyle = 'rgba(60, 80, 95, 0.6)';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([]);
  ctx.beginPath();

  coastlinePoints.forEach((point, i) => {
    const [x, y] = project(point[0], point[1], width, height);
    const [wx, wy] = wobblePoint(x, y, random, 2);
    if (i === 0) {
      ctx.moveTo(wx, wy);
    } else {
      ctx.lineTo(wx, wy);
    }
  });
  ctx.stroke();

  // Draw wave marks
  ctx.strokeStyle = 'rgba(70, 90, 100, 0.25)';
  ctx.lineWidth = 1;
  for (let i = 0; i < coastlinePoints.length - 1; i++) {
    const p1 = coastlinePoints[i];
    const p2 = coastlinePoints[i + 1];
    const [x1, y1] = project(p1[0], p1[1], width, height);
    const [x2, y2] = project(p2[0], p2[1], width, height);

    // Multiple wave marks
    for (let w = 0; w < 3; w++) {
      const offset = 10 + w * 8;
      const midX = (x1 + x2) / 2 + offset;
      const midY = (y1 + y2) / 2;
      ctx.beginPath();
      ctx.arc(midX, midY, 3 + w, 0, Math.PI, false);
      ctx.stroke();
    }
  }
}

function drawRoutesLayer(
  ctx: CanvasRenderingContext2D,
  routes: Route[],
  visibility: VisibilityState,
  width: number,
  height: number
) {
  routes.forEach((route) => {
    const level = getRouteVisibility(route.id, visibility);
    if (level === 'unknown') return;

    const random = seededRandom(hashString(route.id));
    ctx.strokeStyle = ROUTE_COLORS[level];

    // Style based on road type
    switch (route.roadType) {
      case 'roman':
        ctx.lineWidth = 3;
        ctx.setLineDash([]);
        break;
      case 'track':
        ctx.lineWidth = 2;
        ctx.setLineDash([8, 4]);
        break;
      case 'path':
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        break;
      default:
        ctx.lineWidth = 1;
        ctx.setLineDash([2, 6]);
    }

    ctx.beginPath();
    route.waypoints.forEach((point, i) => {
      const [x, y] = project(point[0], point[1], width, height);
      const [wx, wy] = wobblePoint(x, y, random, 1.5);
      if (i === 0) {
        ctx.moveTo(wx, wy);
      } else {
        ctx.lineTo(wx, wy);
      }
    });
    ctx.stroke();
  });

  ctx.setLineDash([]);
}

function drawFogLayer(
  ctx: CanvasRenderingContext2D,
  places: Place[],
  visibility: VisibilityState,
  width: number,
  height: number
) {
  // Create offscreen canvas for fog
  const fogCanvas = document.createElement('canvas');
  fogCanvas.width = width;
  fogCanvas.height = height;
  const fogCtx = fogCanvas.getContext('2d');
  if (!fogCtx) return;

  // Fill with fog color
  fogCtx.fillStyle = 'rgba(160, 145, 125, 0.75)';
  fogCtx.fillRect(0, 0, width, height);

  // Cut out revealed areas around known places
  fogCtx.globalCompositeOperation = 'destination-out';

  places.forEach((place) => {
    const level = getPlaceVisibility(place.id, visibility);
    if (level === 'unknown') return;

    const [x, y] = project(place.coordinates[0], place.coordinates[1], width, height);

    // Radius based on visibility level
    let radius: number;
    switch (level) {
      case 'familiar':
        radius = 100;
        break;
      case 'known':
        radius = 65;
        break;
      case 'rumored':
        radius = 40;
        break;
      default:
        radius = 0;
    }

    if (radius > 0) {
      const gradient = fogCtx.createRadialGradient(x, y, 0, x, y, radius);
      gradient.addColorStop(0, 'rgba(0, 0, 0, 1)');
      gradient.addColorStop(0.6, 'rgba(0, 0, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      fogCtx.fillStyle = gradient;
      fogCtx.beginPath();
      fogCtx.arc(x, y, radius, 0, Math.PI * 2);
      fogCtx.fill();
    }
  });

  // Draw the fog layer onto main canvas
  ctx.drawImage(fogCanvas, 0, 0);
}

function drawPlacesLayer(
  ctx: CanvasRenderingContext2D,
  places: Place[],
  visibility: VisibilityState,
  width: number,
  height: number,
  hoveredPlace: Place | null
) {
  places.forEach((place) => {
    if (place.scale === 'region') return; // Don't render regions as points

    const level = getPlaceVisibility(place.id, visibility);
    if (level === 'unknown') return;

    const [x, y] = project(place.coordinates[0], place.coordinates[1], width, height);
    const size = PLACE_SIZES[place.type] || 5;
    const isHovered = hoveredPlace?.id === place.id;

    // Draw place marker
    ctx.fillStyle = isHovered ? 'rgba(200, 150, 80, 1)' : PLACE_COLORS[level];
    ctx.strokeStyle = 'rgba(60, 40, 20, 0.6)';
    ctx.lineWidth = 1;

    // Different shapes for different types
    ctx.beginPath();
    switch (place.type) {
      case 'city':
        // Square with inner square
        ctx.rect(x - size / 2, y - size / 2, size, size);
        ctx.fill();
        ctx.stroke();
        ctx.strokeRect(x - size / 4, y - size / 4, size / 2, size / 2);
        break;
      case 'hold':
        // Triangle (castle)
        ctx.moveTo(x, y - size / 2);
        ctx.lineTo(x + size / 2, y + size / 2);
        ctx.lineTo(x - size / 2, y + size / 2);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        break;
      case 'monastery':
        // Cross
        ctx.moveTo(x, y - size / 2);
        ctx.lineTo(x, y + size / 2);
        ctx.moveTo(x - size / 3, y - size / 4);
        ctx.lineTo(x + size / 3, y - size / 4);
        ctx.strokeStyle = PLACE_COLORS[level];
        ctx.lineWidth = 2;
        ctx.stroke();
        break;
      case 'crossing':
        // X mark
        ctx.moveTo(x - size / 2, y - size / 2);
        ctx.lineTo(x + size / 2, y + size / 2);
        ctx.moveTo(x + size / 2, y - size / 2);
        ctx.lineTo(x - size / 2, y + size / 2);
        ctx.strokeStyle = PLACE_COLORS[level];
        ctx.lineWidth = 2;
        ctx.stroke();
        break;
      default:
        // Circle for towns, villages, etc.
        ctx.arc(x, y, size / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    }

    // Draw label for familiar/known places
    if (level === 'familiar' || level === 'known') {
      ctx.font = level === 'familiar' ? 'bold 11px serif' : '10px serif';
      ctx.fillStyle = 'rgba(40, 30, 20, 0.9)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      ctx.fillText(place.name, x, y + size / 2 + 4);
    }
  });
}

function drawMarkersLayer(
  ctx: CanvasRenderingContext2D,
  playerPosition: string | [number, number],
  places: Place[],
  width: number,
  height: number
) {
  // Get player coordinates
  let playerCoords: [number, number];
  if (typeof playerPosition === 'string') {
    const playerPlace = places.find((p) => p.id === playerPosition);
    if (!playerPlace) return;
    playerCoords = playerPlace.coordinates;
  } else {
    playerCoords = playerPosition;
  }

  const [x, y] = project(playerCoords[0], playerCoords[1], width, height);

  // Pulsing glow
  const time = Date.now() / 1000;
  const pulse = Math.sin(time * 2) * 0.3 + 0.7;

  // Outer glow
  ctx.fillStyle = `rgba(220, 180, 100, ${pulse * 0.3})`;
  ctx.beginPath();
  ctx.arc(x, y, 18, 0, Math.PI * 2);
  ctx.fill();

  // Inner glow
  ctx.fillStyle = `rgba(240, 200, 120, ${pulse * 0.5})`;
  ctx.beginPath();
  ctx.arc(x, y, 12, 0, Math.PI * 2);
  ctx.fill();

  // Player marker
  ctx.fillStyle = '#e8c864';
  ctx.strokeStyle = '#8b5a2b';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(x, y, 7, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
}

function drawUILayer(
  ctx: CanvasRenderingContext2D,
  hoverInfo: PlaceHoverInfo | null,
  width: number,
  height: number
) {
  if (!hoverInfo) return;

  const { place, visibility, travelMinutes } = hoverInfo;
  const [x, y] = project(place.coordinates[0], place.coordinates[1], width, height);

  // Tooltip box
  const padding = 8;
  const lineHeight = 16;
  const lines = [place.name];
  if (place.detail && visibility !== 'rumored') {
    lines.push(place.detail);
  }
  if (travelMinutes) {
    const hours = Math.floor(travelMinutes / 60);
    const mins = travelMinutes % 60;
    lines.push(`~${hours}h ${mins}m travel`);
  }

  ctx.font = '12px serif';
  const maxWidth = Math.max(...lines.map((l) => ctx.measureText(l).width));
  const boxWidth = maxWidth + padding * 2;
  const boxHeight = lines.length * lineHeight + padding * 2;

  // Position tooltip above the place
  let tooltipX = x - boxWidth / 2;
  let tooltipY = y - boxHeight - 15;

  // Keep within bounds
  tooltipX = Math.max(5, Math.min(width - boxWidth - 5, tooltipX));
  tooltipY = Math.max(5, tooltipY);

  // Draw tooltip background
  ctx.fillStyle = 'rgba(40, 30, 20, 0.9)';
  ctx.strokeStyle = 'rgba(180, 140, 80, 0.8)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(tooltipX, tooltipY, boxWidth, boxHeight, 4);
  ctx.fill();
  ctx.stroke();

  // Draw text
  ctx.fillStyle = '#d4c4a8';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
  lines.forEach((line, i) => {
    ctx.font = i === 0 ? 'bold 12px serif' : '11px serif';
    ctx.fillText(line, tooltipX + padding, tooltipY + padding + i * lineHeight);
  });
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function MapCanvas({
  places,
  routes,
  visibility,
  playerPosition,
  width,
  height,
  onSelectPlace,
  onHoverPlace,
}: MapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoveredPlace, setHoveredPlace] = useState<Place | null>(null);
  const hoveredPlaceRef = useRef<Place | null>(null);
  const renderRequestRef = useRef<boolean>(false);

  // Find place at coordinates
  const findPlaceAtPoint = useCallback(
    (canvasX: number, canvasY: number): Place | null => {
      for (const place of places) {
        if (place.scale === 'region') continue;
        const level = getPlaceVisibility(place.id, visibility);
        if (level === 'unknown') continue;

        const [px, py] = project(
          place.coordinates[0],
          place.coordinates[1],
          width,
          height
        );
        const size = PLACE_SIZES[place.type] || 5;
        const hitRadius = Math.max(size, 10);

        const dx = canvasX - px;
        const dy = canvasY - py;
        if (dx * dx + dy * dy < hitRadius * hitRadius) {
          return place;
        }
      }
      return null;
    },
    [places, visibility, width, height]
  );

  // Calculate travel time from player to place
  const calculateTravelMinutes = useCallback(
    (place: Place): number | undefined => {
      // Find a route from player to this place
      let playerPlaceId: string;
      if (typeof playerPosition === 'string') {
        playerPlaceId = playerPosition;
      } else {
        // Find nearest place to player coordinates
        let nearest: Place | null = null;
        let nearestDist = Infinity;
        for (const p of places) {
          if (p.scale === 'region') continue;
          const dist = haversine(playerPosition, p.coordinates);
          if (dist < nearestDist) {
            nearestDist = dist;
            nearest = p;
          }
        }
        if (!nearest) return undefined;
        playerPlaceId = nearest.id;
      }

      // Find direct route
      const route = routes.find(
        (r) =>
          (r.from === playerPlaceId && r.to === place.id) ||
          (r.to === playerPlaceId && r.from === place.id)
      );

      return route?.travelMinutes;
    },
    [playerPosition, places, routes]
  );

  // Mouse move handler
  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const place = findPlaceAtPoint(x, y);
      setHoveredPlace(place);

      if (place) {
        const level = getPlaceVisibility(place.id, visibility);
        onHoverPlace?.({
          place,
          visibility: level,
          travelMinutes: calculateTravelMinutes(place),
        });
      } else {
        onHoverPlace?.(null);
      }
    },
    [findPlaceAtPoint, visibility, onHoverPlace, calculateTravelMinutes]
  );

  // Click handler
  const handleClick = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const place = findPlaceAtPoint(x, y);
      if (place) {
        onSelectPlace?.(place);
      }
    },
    [findPlaceAtPoint, onSelectPlace]
  );

  // Keep ref in sync with state
  useEffect(() => {
    hoveredPlaceRef.current = hoveredPlace;
    renderRequestRef.current = true;
  }, [hoveredPlace]);

  // Render function (uses refs to avoid dependency issues)
  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const currentHovered = hoveredPlaceRef.current;

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Draw layers in order
    drawParchmentLayer(ctx, width, height);
    drawTerrainLayer(ctx, width, height);
    drawCoastlineLayer(ctx, width, height);
    drawRoutesLayer(ctx, routes, visibility, width, height);
    drawFogLayer(ctx, places, visibility, width, height);
    drawPlacesLayer(ctx, places, visibility, width, height, currentHovered);
    drawMarkersLayer(ctx, playerPosition, places, width, height);

    // Build hover info for UI layer
    let hoverInfo: PlaceHoverInfo | null = null;
    if (currentHovered) {
      hoverInfo = {
        place: currentHovered,
        visibility: getPlaceVisibility(currentHovered.id, visibility),
        travelMinutes: calculateTravelMinutes(currentHovered),
      };
    }
    drawUILayer(ctx, hoverInfo, width, height);
  }, [
    width,
    height,
    places,
    routes,
    visibility,
    playerPosition,
    calculateTravelMinutes,
  ]);

  // Render on mount and when dependencies change
  useEffect(() => {
    render();
  }, [render]);

  // Slow animation for pulsing player marker
  useEffect(() => {
    const intervalId = setInterval(() => {
      render();
    }, 150); // ~7fps for pulse animation

    return () => {
      clearInterval(intervalId);
    };
  }, [render]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      onMouseMove={handleMouseMove}
      onClick={handleClick}
      className="cursor-crosshair"
      style={{
        imageRendering: 'auto',
      }}
    />
  );
}
