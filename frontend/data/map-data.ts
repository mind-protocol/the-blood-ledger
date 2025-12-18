import { Place, Route, VisibilityState } from '@/types/map';

// =============================================================================
// PLACES
// =============================================================================

export const places: Place[] = [
  // Region
  {
    id: 'place_northumbria',
    name: 'Northumbria',
    coordinates: [54.5, -1.5],
    scale: 'region',
    type: 'region',
    detail: 'The great northern kingdom, now under Norman control.',
  },

  // Settlements
  {
    id: 'place_york',
    name: 'York',
    coordinates: [53.96, -1.08],
    scale: 'settlement',
    type: 'city',
    detail: 'The second city of England. Norman banners fly from its walls.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_durham',
    name: 'Durham',
    coordinates: [54.78, -1.57],
    scale: 'settlement',
    type: 'city',
    detail: 'A great cathedral rises above the river. The bishop holds power here.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_scarborough',
    name: 'Scarborough',
    coordinates: [54.28, -0.40],
    scale: 'settlement',
    type: 'town',
    detail: 'A coastal town, clinging to the cliffs above the sea.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_whitby',
    name: 'Whitby',
    coordinates: [54.49, -0.61],
    scale: 'settlement',
    type: 'monastery',
    detail: 'The abbey watches over the harbor. Fishermen and monks share the town.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_ripon',
    name: 'Ripon',
    coordinates: [54.14, -1.52],
    scale: 'settlement',
    type: 'town',
    detail: 'A market town around an ancient minster.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_thirsk',
    name: 'Thirsk',
    coordinates: [54.23, -1.34],
    scale: 'settlement',
    type: 'village',
    detail: 'A quiet village at a crossroads.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_helmsley',
    name: 'Helmsley',
    coordinates: [54.25, -1.06],
    scale: 'settlement',
    type: 'hold',
    detail: 'A Norman castle commands the vale.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_pickering',
    name: 'Pickering',
    coordinates: [54.24, -0.78],
    scale: 'settlement',
    type: 'town',
    detail: 'Gateway to the moors. Hunters gather here.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_northallerton',
    name: 'Northallerton',
    coordinates: [54.34, -1.43],
    scale: 'settlement',
    type: 'village',
    detail: 'The road north passes through here.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_richmond',
    name: 'Richmond',
    coordinates: [54.40, -1.74],
    scale: 'settlement',
    type: 'hold',
    detail: 'A mighty castle overlooks the dale.',
    parentId: 'place_northumbria',
  },
  {
    id: 'place_darlington',
    name: 'Darlington',
    coordinates: [54.52, -1.55],
    scale: 'settlement',
    type: 'village',
    detail: 'A river crossing on the way to Durham.',
    parentId: 'place_northumbria',
  },

  // Landmarks / Crossings
  {
    id: 'place_stamford_bridge',
    name: 'Stamford Bridge',
    coordinates: [53.99, -0.91],
    scale: 'settlement',
    type: 'crossing',
    detail: 'Where Harald Hardrada fell. The river still runs red in memory.',
    parentId: 'place_northumbria',
  },
];

// =============================================================================
// COASTLINE (North Sea)
// =============================================================================

export const coastlinePoints: [number, number][] = [
  [55.5, -1.45],
  [55.3, -1.40],
  [55.1, -1.35],
  [54.97, -1.42],
  [54.78, -1.20],
  [54.65, -0.95],
  [54.49, -0.58], // Whitby
  [54.35, -0.35],
  [54.28, -0.38], // Scarborough
  [54.10, -0.20],
  [53.95, -0.10],
  [53.75, 0.00],
  [53.50, 0.10],
  [53.00, 0.20],
];

// =============================================================================
// ROUTES
// =============================================================================

export const routes: Route[] = [
  // York to Durham (Roman road north)
  {
    id: 'route_york_durham',
    from: 'place_york',
    to: 'place_durham',
    waypoints: [
      [53.96, -1.08],
      [54.14, -1.35],
      [54.34, -1.43],
      [54.52, -1.55],
      [54.78, -1.57],
    ],
    roadType: 'roman',
    distanceKm: 96,
    travelMinutes: 1152, // ~19 hours
    difficulty: 'easy',
    detail: 'The old Roman road north. Well-maintained.',
  },

  // York to Scarborough
  {
    id: 'route_york_scarborough',
    from: 'place_york',
    to: 'place_scarborough',
    waypoints: [
      [53.96, -1.08],
      [54.05, -0.85],
      [54.15, -0.60],
      [54.28, -0.40],
    ],
    roadType: 'track',
    distanceKm: 65,
    travelMinutes: 1114, // ~18.5 hours
    difficulty: 'moderate',
    detail: 'East through the wolds to the coast.',
  },

  // York to Whitby
  {
    id: 'route_york_whitby',
    from: 'place_york',
    to: 'place_whitby',
    waypoints: [
      [53.96, -1.08],
      [54.10, -0.95],
      [54.25, -0.78],
      [54.35, -0.68],
      [54.49, -0.61],
    ],
    roadType: 'path',
    distanceKm: 72,
    travelMinutes: 1728, // ~29 hours
    difficulty: 'hard',
    detail: 'Through the North York Moors. Difficult terrain.',
  },

  // York to Ripon
  {
    id: 'route_york_ripon',
    from: 'place_york',
    to: 'place_ripon',
    waypoints: [
      [53.96, -1.08],
      [54.05, -1.30],
      [54.14, -1.52],
    ],
    roadType: 'roman',
    distanceKm: 40,
    travelMinutes: 480, // 8 hours
    difficulty: 'easy',
    detail: 'Roman road northwest.',
  },

  // York to Stamford Bridge
  {
    id: 'route_york_stamford',
    from: 'place_york',
    to: 'place_stamford_bridge',
    waypoints: [
      [53.96, -1.08],
      [53.99, -0.91],
    ],
    roadType: 'roman',
    distanceKm: 12,
    travelMinutes: 144, // 2.4 hours
    difficulty: 'easy',
    detail: 'Short journey east along the river.',
  },

  // Ripon to Richmond
  {
    id: 'route_ripon_richmond',
    from: 'place_ripon',
    to: 'place_richmond',
    waypoints: [
      [54.14, -1.52],
      [54.27, -1.63],
      [54.40, -1.74],
    ],
    roadType: 'track',
    distanceKm: 35,
    travelMinutes: 600, // 10 hours
    difficulty: 'moderate',
    detail: 'Northwest into the dales.',
  },

  // Durham to Darlington
  {
    id: 'route_durham_darlington',
    from: 'place_durham',
    to: 'place_darlington',
    waypoints: [
      [54.78, -1.57],
      [54.65, -1.56],
      [54.52, -1.55],
    ],
    roadType: 'roman',
    distanceKm: 30,
    travelMinutes: 360, // 6 hours
    difficulty: 'easy',
  },

  // Thirsk to Northallerton
  {
    id: 'route_thirsk_northallerton',
    from: 'place_thirsk',
    to: 'place_northallerton',
    waypoints: [
      [54.23, -1.34],
      [54.34, -1.43],
    ],
    roadType: 'track',
    distanceKm: 15,
    travelMinutes: 257, // ~4 hours
    difficulty: 'moderate',
  },

  // Pickering to Scarborough
  {
    id: 'route_pickering_scarborough',
    from: 'place_pickering',
    to: 'place_scarborough',
    waypoints: [
      [54.24, -0.78],
      [54.26, -0.59],
      [54.28, -0.40],
    ],
    roadType: 'track',
    distanceKm: 28,
    travelMinutes: 480, // 8 hours
    difficulty: 'moderate',
  },

  // Pickering to Whitby
  {
    id: 'route_pickering_whitby',
    from: 'place_pickering',
    to: 'place_whitby',
    waypoints: [
      [54.24, -0.78],
      [54.35, -0.70],
      [54.49, -0.61],
    ],
    roadType: 'path',
    distanceKm: 35,
    travelMinutes: 840, // 14 hours
    difficulty: 'hard',
    detail: 'Over the moors to the abbey.',
  },

  // Helmsley to Pickering
  {
    id: 'route_helmsley_pickering',
    from: 'place_helmsley',
    to: 'place_pickering',
    waypoints: [
      [54.25, -1.06],
      [54.24, -0.78],
    ],
    roadType: 'track',
    distanceKm: 20,
    travelMinutes: 343, // ~6 hours
    difficulty: 'moderate',
  },
];

// =============================================================================
// SAMPLE VISIBILITY STATE
// =============================================================================

export const sampleVisibility: VisibilityState = {
  places: {
    place_york: { level: 'familiar', discoveredAt: 0, visitedAt: 0 },
    place_stamford_bridge: { level: 'known', discoveredAt: 100 },
    place_ripon: { level: 'rumored', discoveredAt: 500 },
    place_durham: { level: 'rumored', discoveredAt: 800 },
    place_scarborough: { level: 'known', discoveredAt: 300 },
    place_thirsk: { level: 'rumored', discoveredAt: 600 },
    place_helmsley: { level: 'known', discoveredAt: 400 },
    place_pickering: { level: 'known', discoveredAt: 450 },
    place_whitby: { level: 'rumored', discoveredAt: 700 },
  },
  routes: {
    route_york_stamford: { level: 'familiar', discoveredAt: 100 },
    route_york_scarborough: { level: 'known', discoveredAt: 300 },
    route_york_ripon: { level: 'rumored', discoveredAt: 500 },
    route_york_durham: { level: 'rumored', discoveredAt: 800 },
    route_helmsley_pickering: { level: 'known', discoveredAt: 450 },
  },
};
