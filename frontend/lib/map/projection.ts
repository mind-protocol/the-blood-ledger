// DOCS: docs/frontend/map/PATTERNS_Interactive_Travel_Map.md
/**
 * Map projection utilities for Northern England
 * Simple equirectangular projection
 */

import { MAP_BOUNDS } from '@/types/map';

/**
 * Convert [lat, lng] to [x, y] canvas coordinates
 */
export function project(
  lat: number,
  lng: number,
  width: number,
  height: number
): [number, number] {
  const x = ((lng - MAP_BOUNDS.west) / (MAP_BOUNDS.east - MAP_BOUNDS.west)) * width;
  const y = ((MAP_BOUNDS.north - lat) / (MAP_BOUNDS.north - MAP_BOUNDS.south)) * height;
  return [x, y];
}

/**
 * Convert [x, y] canvas coordinates to [lat, lng]
 */
export function unproject(
  x: number,
  y: number,
  width: number,
  height: number
): [number, number] {
  const lng = (x / width) * (MAP_BOUNDS.east - MAP_BOUNDS.west) + MAP_BOUNDS.west;
  const lat = MAP_BOUNDS.north - (y / height) * (MAP_BOUNDS.north - MAP_BOUNDS.south);
  return [lat, lng];
}

/**
 * Calculate distance in km between two [lat, lng] points using haversine formula
 */
export function haversine(
  coord1: [number, number],
  coord2: [number, number]
): number {
  const R = 6371; // Earth radius in km

  const lat1 = (coord1[0] * Math.PI) / 180;
  const lon1 = (coord1[1] * Math.PI) / 180;
  const lat2 = (coord2[0] * Math.PI) / 180;
  const lon2 = (coord2[1] * Math.PI) / 180;

  const dlat = lat2 - lat1;
  const dlon = lon2 - lon1;

  const a =
    Math.sin(dlat / 2) ** 2 +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
}

/**
 * Calculate total distance along waypoints
 */
export function routeDistance(waypoints: [number, number][]): number {
  let total = 0;
  for (let i = 1; i < waypoints.length; i++) {
    total += haversine(waypoints[i - 1], waypoints[i]);
  }
  return total;
}

/**
 * Get position along a route at given progress (0-1)
 */
export function getPositionAtProgress(
  waypoints: [number, number][],
  totalDistanceKm: number,
  progress: number
): [number, number] {
  const targetDist = totalDistanceKm * progress;
  let accumulated = 0;

  for (let i = 1; i < waypoints.length; i++) {
    const segmentDist = haversine(waypoints[i - 1], waypoints[i]);

    if (accumulated + segmentDist >= targetDist) {
      const t = (targetDist - accumulated) / segmentDist;
      const lat = waypoints[i - 1][0] + (waypoints[i][0] - waypoints[i - 1][0]) * t;
      const lng = waypoints[i - 1][1] + (waypoints[i][1] - waypoints[i - 1][1]) * t;
      return [lat, lng];
    }

    accumulated += segmentDist;
  }

  return waypoints[waypoints.length - 1];
}
