// DOCS: docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md
'use client';

import { useState, useEffect, useCallback } from 'react';
import { GameState, MapRegion, Character, LedgerEntry, ChronicleEntry, Scene, Voice, SceneTree } from '@/types/game';
import * as api from '@/lib/api';

// Default playthrough for development
const DEFAULT_PLAYTHROUGH = 'beorn';

// Loading messages that update as we progress
const LOADING_STAGES = [
  "Awakening the Narrator...",
  "The world stirs...",
  "Gathering the threads of your story...",
  "The scene takes shape...",
];

interface UseGameStateResult {
  gameState: GameState | null;
  playthroughId: string;
  isLoading: boolean;
  loadingMessage: string;
  error: string | null;
  isConnected: boolean;
  needsOpening: boolean;  // True if no scene.json or default content
  refresh: () => Promise<void>;
  sendAction: (action: string) => Promise<void>;
  clickWord: (word: string, path?: string[]) => Promise<void>;
}

type CurrentViewWithActiveMoments = api.CurrentView & { active_moments?: api.Moment[] };

export function useGameState(playthroughId: string = DEFAULT_PLAYTHROUGH): UseGameStateResult {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loadingMessage, setLoadingMessage] = useState(LOADING_STAGES[0]);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [needsOpening, setNeedsOpening] = useState(false);

  const fetchGameState = useCallback(
    async (options: { showLoading?: boolean } = {}) => {
      const showLoading = options.showLoading ?? true;
      if (showLoading) {
        setIsLoading(true);
        setLoadingMessage(LOADING_STAGES[0]);
      }
      setError(null);

    try {
      // Check backend health
      const healthy = await api.checkHealth();
      setIsConnected(healthy);

      if (!healthy) {
        setError('Backend not available');
        setIsLoading(false);
        return;
      }

      setLoadingMessage(LOADING_STAGES[1]);

      // Fetch view data in parallel
      const [mapData, facesData, ledgerData, chronicleData] = await Promise.all([
        api.getMap(playthroughId),
        api.getFaces(playthroughId),
        api.getLedger(playthroughId),
        api.getChronicle(playthroughId),
      ]);

      setLoadingMessage(LOADING_STAGES[2]);

      // Try to load current view (moment system)
      let scene: Scene;
      let voices: Voice[] = [];
      let sceneTree: SceneTree | undefined;

      const view = (await api.getCurrentView(playthroughId)) as CurrentViewWithActiveMoments | null;
      const moments = view ? (view.active_moments ?? view.moments ?? []) : [];
      if (view && moments.length > 0) {
        // Normalize view to always have moments field
        const normalizedView = { ...view, moments } as api.CurrentView;
        // Transform view to scene format
        scene = transformViewToScene(normalizedView);
        voices = transformMomentsToVoices(moments);
        // Scene tree is the raw view with clickable moments
        sceneTree = normalizedView as unknown as SceneTree;
        setNeedsOpening(false);
        console.log('Loaded view from moment system');
      } else {
        // No moments yet - redirect to opening
        console.log('No moments found, needs opening');
        setNeedsOpening(true);
        setIsLoading(false);
        return;
      }

      // Transform to GameState format
      const map: MapRegion[] = [{
        id: 'region_north',
        name: 'The North',
        locations: mapData.places.map((p) => ({
          id: p['p.id'],
          name: p['p.name'],
          type: mapPlaceType(p['p.type']),
          position: { x: 50, y: 50 },
          discovered: true,
          current: p['p.id'] === 'place_camp',
          connected: mapData.connections
            .filter((c) => c['p1.id'] === p['p.id'])
            .map((c) => c['p2.id']),
        })),
      }];

      const characters: Character[] = [
        ...facesData.companions.map((c) => ({
          id: c['c.id'],
          name: c['c.name'],
          description: '',
          face: c['c.face'] || null,
          location: 'The Camp',
          isCompanion: true,
          isPresent: true,
        })),
        ...facesData.known_characters.map((c) => ({
          id: c['c.id'],
          name: c['c.name'],
          description: '',
          face: c['c.face'] || null,
          location: 'Unknown',
          isCompanion: false,
          isPresent: false,
        })),
      ];

      const ledger: LedgerEntry[] = ledgerData.items.map((n) => ({
        id: n['n.id'],
        type: (n['n.type'] as 'debt' | 'oath' | 'blood') || 'oath',
        subject: n['n.name'],
        content: n['n.content'] || '',
        resolved: false,
      }));

      const chronicle: ChronicleEntry[] = chronicleData.events.map((e, i) => ({
        id: e['n.id'] || `event_${i}`,
        day: i + 1,
        location: 'The North',
        content: e['n.content'] || e['n.name'],
        isPlayerWritten: false,
      }));

      // Build game state
      const state: GameState = {
        player: {
          name: 'Rolf',
          title: null,
          day: 1,
          location: scene.location,
        },
        currentScene: scene,
        sceneTree,  // Raw Narrator response with clickables
        characters,
        voices,
        chronicle,
        ledger,
        conversations: [],
        map,
      };

      setGameState(state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load game state');
    } finally {
      if (showLoading) {
        setIsLoading(false);
      }
    }
    },
    [playthroughId]
  );

  const sendAction = useCallback(async (action: string) => {
    setLoadingMessage("The world responds...");
    try {
      // Queue the moment - scene updates come via SSE stream
      await api.sendMoment(playthroughId, action, 'player_freeform');
      // Note: Scene updates arrive via SSE, not from this call
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Action failed');
    }
  }, [playthroughId]);

  // Note: clickWord is deprecated - use moment system's clickMoment instead
  const clickWord = useCallback(async (_word: string, _path: string[] = []) => {
    console.warn('[useGameState] clickWord is deprecated. Use moment system instead.');
  }, []);

  useEffect(() => {
    fetchGameState();
  }, [fetchGameState]);

  // SSE subscription for real-time moment updates
  useEffect(() => {
    if (!playthroughId) return;

    console.log('[SSE] Subscribing to moment stream for', playthroughId);

    const unsubscribe = api.subscribeToMomentStream(playthroughId, {
      onMomentActivated: (data) => {
        console.log('[SSE] Moment activated:', data.moment_id);
        // Refresh to get full moment data
        fetchGameState({ showLoading: false });
      },
      onMomentSpoken: (data) => {
        console.log('[SSE] Moment spoken:', data.moment_id);
        // Update moment status in local state if needed
        fetchGameState({ showLoading: false });
      },
      onMomentDecayed: (data) => {
        console.log('[SSE] Moment decayed:', data.moment_id);
        fetchGameState({ showLoading: false });
      },
      onWeightUpdated: (data) => {
        console.log('[SSE] Weight updated:', data.moment_id, data.weight);
        // Could update weight in place, but full refresh is simpler
      },
      onClickTraversed: (data) => {
        console.log('[SSE] Click traversed:', data.word, data.from_moment_id, '->', data.to_moment_id);
        fetchGameState({ showLoading: false });
      },
      onError: (error) => {
        console.warn('[SSE] Stream error (will reconnect):', error);
      }
    });

    return () => {
      console.log('[SSE] Unsubscribing from moment stream');
      unsubscribe();
    };
  }, [playthroughId, fetchGameState]);

  return {
    gameState,
    playthroughId,
    isLoading,
    loadingMessage,
    error,
    isConnected,
    needsOpening,
    refresh: fetchGameState,
    sendAction,
    clickWord,
  };
}

// Helper: Map place type to SceneType
function mapPlaceType(type: string): Scene['type'] {
  const mapping: Record<string, Scene['type']> = {
    camp: 'CAMP',
    city: 'GATE',
    ruin: 'VILLAGE',
    village: 'VILLAGE',
    road: 'ROAD',
    hold: 'HOLD',
    forest: 'FOREST',
    church: 'CHURCH',
  };
  return mapping[type?.toLowerCase()] || 'CAMP';
}

// Helper: Transform Narrator scene response
function transformScene(s: Record<string, unknown>): Scene {
  const location = s.location as Record<string, string> | undefined;
  const characters = s.characters as string[] | undefined;

  // Handle narration - can be {raw, clickables} object or array of {text}
  const narration = s.narration as { raw?: string; clickables?: string[] } | Array<{ text: string }> | undefined;
  let atmosphereText: string[] = [];

  if (s.atmosphere) {
    atmosphereText = s.atmosphere as string[];
  } else if (narration) {
    if ('raw' in narration && typeof narration.raw === 'string') {
      // Narrator format: {raw: "...", clickables: [...]}
      atmosphereText = [narration.raw];
    } else if (Array.isArray(narration)) {
      // Array format: [{text: "..."}, ...]
      atmosphereText = narration.map(n => n.text);
    }
  }

  if (atmosphereText.length === 0) {
    atmosphereText = ['The scene unfolds before you...'];
  }

  // Extract clickables from narration
  const clickables = (narration && 'clickables' in narration)
    ? (narration.clickables as string[]) || []
    : [];

  const placeId = (location?.place as string) || undefined;

  return {
    id: placeId || (s.id as string) || 'scene_generated',
    placeId,
    type: mapPlaceType((location?.place as string) || 'camp'),
    name: (location?.name as string) || 'THE CAMP',
    location: (location?.region as string) || 'The North',
    timeOfDay: ((location?.time as string)?.toUpperCase() || 'NIGHT') as Scene['timeOfDay'],
    weather: 'CLEAR',
    atmosphere: atmosphereText,
    hotspots: [
      // Clickable words from narration
      ...clickables.map((word: string, i: number) => ({
        id: `click_${word}`,
        type: 'object' as const,
        name: word,
        description: `Click to explore: ${word}`,
        position: { x: 20 + (i * 15) % 60, y: 70 + (i % 3) * 10 },
        icon: '👁',
        actions: [
          { id: `click_${word}`, label: word },
        ],
      })),
      // Characters in scene
      ...(characters || []).map((charId: string, i: number) => {
        const charName = charId.replace('char_', '');
        return {
          id: charId,
          type: 'person' as const,
          name: charName.replace(/^\w/, c => c.toUpperCase()),
          description: 'Present in the scene.',
          position: { x: 60 + i * 10, y: 40 + i * 5 },
          icon: '🧍',
          imageUrl: `/playthroughs/default/images/characters/${charId}.png`,
          actions: [
            { id: `talk_${charId}`, label: 'Talk' },
          ],
        };
      }),
    ],
    actions: [
      { id: 'look_around', label: 'Look around' },
      { id: 'wait', label: 'Wait' },
    ],
  };
}

// Helper: Transform Narrator voices
function transformVoices(s: Record<string, unknown>): Voice[] {
  const voices = s.voices as Array<{
    source: string;
    text: string;
    weight: number;
  }> | undefined;

  if (!voices) return [];

  return voices.map((v, i) => ({
    id: `voice_${i}`,
    type: 'memory' as const,
    source: v.source,
    content: v.text,
    weight: v.weight,
  }));
}

// Helper: Transform moment system view to Scene format
function transformViewToScene(view: api.CurrentView): Scene {
  const location = view.location;

  // Get atmosphere from narration moments
  const narrationMoments = view.moments.filter(m => m.type === 'narration' || m.type === 'action');
  const atmosphereText = narrationMoments.map(m => m.text);

  if (atmosphereText.length === 0) {
    atmosphereText.push('The scene unfolds before you...');
  }

  // Build clickable words from transitions
  const clickables: string[] = [];
  for (const t of view.transitions) {
    for (const word of t.words) {
      if (!clickables.includes(word)) {
        clickables.push(word);
      }
    }
  }

  return {
    id: location.id,
    placeId: location.id,
    type: mapPlaceType(location.type),
    name: location.name.toUpperCase(),
    location: 'The North',
    timeOfDay: 'NIGHT',
    weather: 'CLEAR',
    atmosphere: atmosphereText,
    hotspots: [
      // Clickable words from moments
      ...clickables.map((word, i) => ({
        id: `click_${word}`,
        type: 'object' as const,
        name: word,
        description: `Click to explore: ${word}`,
        position: { x: 20 + (i * 15) % 60, y: 70 + (i % 3) * 10 },
        icon: '👁',
        actions: [{ id: `click_${word}`, label: word }],
      })),
      // Characters in scene
      ...view.characters.map((char, i) => ({
        id: char.id,
        type: 'person' as const,
        name: char.name,
        description: 'Present in the scene.',
        position: { x: 60 + i * 10, y: 40 + i * 5 },
        icon: '🧍',
        imageUrl: `/playthroughs/default/images/characters/${char.id}.png`,
        actions: [{ id: `talk_${char.id}`, label: 'Talk' }],
      })),
    ],
    actions: [
      { id: 'look_around', label: 'Look around' },
      { id: 'wait', label: 'Wait' },
    ],
  };
}

// Helper: Transform moments to voices
function transformMomentsToVoices(moments: api.Moment[]): Voice[] {
  // Filter for dialogue moments with speakers
  const dialogueMoments = moments.filter(m => m.type === 'dialogue' && m.speaker);

  return dialogueMoments.map((m, i) => ({
    id: `voice_${m.id || i}`,
    type: 'memory' as const,
    source: m.speaker || 'Unknown',
    content: m.text,
    weight: m.weight,
  }));
}

// Helper: Create fallback scene when Narrator unavailable
function createFallbackScene(
  mapData: { places: Array<{ 'p.id': string; 'p.name': string; 'p.type': string; 'p.mood'?: string }> },
  facesData: { companions: Array<{ 'c.id': string; 'c.name': string }> }
): Scene {
  const camp = mapData.places.find(p => p['p.id'] === 'place_camp');

  return {
    id: 'place_camp',
    placeId: 'place_camp',
    type: 'CAMP',
    name: camp?.['p.name'] || 'THE CAMP',
    location: 'The North',
    timeOfDay: 'NIGHT',
    weather: 'CLEAR',
    atmosphere: [
      'Cold night. Stars visible through bare branches.',
      'The fire crackles, throwing shadows.',
      camp?.['p.mood'] ? `The air feels ${camp['p.mood']}.` : '',
    ].filter(Boolean),
    hotspots: facesData.companions.map((c) => ({
      id: c['c.id'],
      type: 'person' as const,
      name: c['c.name'],
      description: `${c['c.name']} is here.`,
      position: { x: 60, y: 50 },
      icon: '🧍',
      actions: [
        { id: `talk_${c['c.id']}`, label: 'Talk', description: `Speak with ${c['c.name']}` },
      ],
    })),
    actions: [
      { id: 'look_around', label: 'Look around', description: 'Survey the camp' },
      { id: 'rest', label: 'Rest', description: 'Get some sleep' },
    ],
  };
}
