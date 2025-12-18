// =============================================================================
// MAP SYSTEM TYPES
// =============================================================================

// -----------------------------------------------------------------------------
// Place Types
// -----------------------------------------------------------------------------

export type PlaceScale = 'region' | 'settlement' | 'district' | 'building' | 'room';

export type PlaceType =
  | 'city'
  | 'town'
  | 'village'
  | 'monastery'
  | 'hold'
  | 'crossing'
  | 'landmark'
  | 'market'
  | 'quarter'
  | 'hall'
  | 'church'
  | 'tavern'
  | 'house'
  | 'room'
  | 'region';

export interface Place {
  id: string;
  name: string;
  coordinates: [number, number]; // [lat, lng]
  scale: PlaceScale;
  type: PlaceType;
  detail?: string;
  parentId?: string; // For hierarchy
}

// -----------------------------------------------------------------------------
// Route Types
// -----------------------------------------------------------------------------

export type RoadType = 'roman' | 'track' | 'path' | 'river' | 'none';

export type Difficulty = 'easy' | 'moderate' | 'hard' | 'dangerous';

export interface Route {
  id: string;
  from: string; // Place ID
  to: string; // Place ID
  waypoints: [number, number][]; // [[lat, lng], ...]
  roadType: RoadType;
  distanceKm: number;
  travelMinutes: number;
  difficulty: Difficulty;
  detail?: string;
}

// -----------------------------------------------------------------------------
// Visibility Types
// -----------------------------------------------------------------------------

export type VisibilityLevel = 'unknown' | 'rumored' | 'known' | 'familiar';

export interface PlaceVisibility {
  level: VisibilityLevel;
  discoveredAt?: number; // Game tick
  visitedAt?: number; // Game tick
}

export interface RouteVisibility {
  level: VisibilityLevel;
  discoveredAt?: number;
}

export type VisibilityState = {
  places: Record<string, PlaceVisibility>;
  routes: Record<string, RouteVisibility>;
};

// -----------------------------------------------------------------------------
// Dynamic State Types
// -----------------------------------------------------------------------------

export interface NPCMovement {
  characterId: string;
  characterName: string;
  routeId: string;
  progress: number; // 0-1
}

export interface TensionMarker {
  placeId: string;
  level: number; // 0-1
}

// -----------------------------------------------------------------------------
// Interaction Types
// -----------------------------------------------------------------------------

export interface PlaceHoverInfo {
  place: Place;
  visibility: VisibilityLevel;
  travelMinutes?: number;
}

export interface MapClickEvent {
  type: 'place' | 'route' | 'empty';
  place?: Place;
  route?: Route;
  coordinates?: [number, number];
}

// -----------------------------------------------------------------------------
// Map Props
// -----------------------------------------------------------------------------

export interface MapProps {
  // Data
  places: Place[];
  routes: Route[];
  visibility: VisibilityState;

  // Player state
  playerPosition: string | [number, number]; // Place ID or [lat, lng]
  playerDestination?: string;
  travelProgress?: number;

  // Dynamic elements
  npcsMoving?: NPCMovement[];
  tensions?: TensionMarker[];

  // Dimensions
  width: number;
  height: number;

  // Callbacks
  onSelectPlace?: (place: Place) => void;
  onHoverPlace?: (info: PlaceHoverInfo | null) => void;
  onRequestTravel?: (from: string, to: string) => void;
}

// -----------------------------------------------------------------------------
// Bounds
// -----------------------------------------------------------------------------

export const MAP_BOUNDS = {
  north: 55.5,
  south: 53.0,
  east: 0.5,
  west: -3.0,
} as const;
