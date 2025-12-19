// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md
/**
 * Blood Ledger API Client
 *
 * Connects frontend to the Python backend.
 */

import type { DialogueChunk, GraphMutation, SceneTree } from '@/types/game';
import { showToast } from '@/components/ui/Toast';

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Track if we've shown the backend down toast recently (debounce)
let lastBackendErrorTime = 0;
const TOAST_DEBOUNCE_MS = 5000;

function handleApiError(error: unknown, context: string) {
  const now = Date.now();
  // Only show toast if we haven't shown one recently
  if (now - lastBackendErrorTime > TOAST_DEBOUNCE_MS) {
    lastBackendErrorTime = now;
    showToast('Backend is unavailable. Check if the server is running.', 'error', 6000);
  }
  console.error(`[API] ${context}:`, error);
}

// -----------------------------------------------------------------------------
// Types for API responses
// -----------------------------------------------------------------------------

interface ApiPlace {
  'p.id': string;
  'p.name': string;
  'p.type': string;
  'p.mood'?: string;
}

interface ApiConnection {
  'p1.id': string;
  'p2.id': string;
  'r.path_distance'?: string;
  'r.path_difficulty'?: string;
}

interface ApiCharacter {
  'c.id': string;
  'c.name': string;
  'c.face'?: string;
  'c.voice_tone'?: string;
}

interface ApiNarrative {
  'n.id': string;
  'n.name': string;
  'n.content'?: string;
  'n.type': string;
  'n.weight'?: number;
}

// -----------------------------------------------------------------------------
// API Functions
// -----------------------------------------------------------------------------

export async function createPlaythrough(
  scenarioId: string,
  playerName: string,
  playerGender: string = 'male'
): Promise<{ playthrough_id: string; scenario: string; scene: SceneTree }> {
  try {
    const res = await fetch(`${API_BASE}/api/playthrough/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scenario_id: scenarioId,
        player_name: playerName,
        player_gender: playerGender
      }),
    });
    if (!res.ok) throw new Error(`Failed to create playthrough: ${res.statusText}`);
    return res.json();
  } catch (error) {
    handleApiError(error, 'createPlaythrough');
    throw error;
  }
}

export async function sendMoment(
  playthroughId: string,
  text: string,
  momentType: 'player_freeform' | 'player_click' | 'player_choice' = 'player_freeform'
): Promise<{ status: string; narrator_started: boolean; narrator_running: boolean }> {
  try {
    const res = await fetch(`${API_BASE}/api/moment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playthrough_id: playthroughId,
        text,
        moment_type: momentType,
      }),
    });
    if (!res.ok) throw new Error(`Failed to send moment: ${res.statusText}`);
    return res.json();
  } catch (error) {
    handleApiError(error, 'sendMoment');
    throw error;
  }
}

export async function getPlaythrough(playthroughId: string): Promise<{
  playthrough_id: string;
  has_player_notes: boolean;
  has_story_notes: boolean;
  has_world_injection: boolean;
}> {
  try {
    const res = await fetch(`${API_BASE}/api/playthrough/${playthroughId}`);
    if (!res.ok) throw new Error(`Playthrough not found: ${playthroughId}`);
    return res.json();
  } catch (error) {
    handleApiError(error, 'getPlaythrough');
    throw error;
  }
}

export async function getMap(playthroughId: string): Promise<{
  places: ApiPlace[];
  connections: ApiConnection[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/map`);
  if (!res.ok) throw new Error(`Failed to fetch map: ${res.statusText}`);
  return res.json();
}

export async function getFaces(playthroughId: string): Promise<{
  known_characters: ApiCharacter[];
  companions: ApiCharacter[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/faces`);
  if (!res.ok) throw new Error(`Failed to fetch faces: ${res.statusText}`);
  return res.json();
}

export async function getLedger(playthroughId: string): Promise<{
  items: ApiNarrative[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/ledger`);
  if (!res.ok) throw new Error(`Failed to fetch ledger: ${res.statusText}`);
  return res.json();
}

export async function getChronicle(playthroughId: string): Promise<{
  events: ApiNarrative[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/chronicle`);
  if (!res.ok) throw new Error(`Failed to fetch chronicle: ${res.statusText}`);
  return res.json();
}

export async function semanticQuery(
  playthroughId: string,
  query: string
): Promise<{
  results: Array<{
    id: string;
    name: string;
    type: string;
    content?: string;
    similarity: number;
  }>;
  query: string;
}> {
  const res = await fetch(
    `${API_BASE}/api/${playthroughId}/query?query=${encodeURIComponent(query)}`,
    { method: 'POST' }
  );
  if (!res.ok) throw new Error(`Query failed: ${res.statusText}`);
  return res.json();
}

// -----------------------------------------------------------------------------
// Moment Types
// -----------------------------------------------------------------------------

export interface Moment {
  id: string;
  text: string;
  type: string;
  status: string;
  weight: number;
  tone?: string;
  tick_created?: number;
  tick_spoken?: number;
  speaker?: string;
  clickable_words: string[];
}

export interface MomentTransition {
  from_id: string;
  to_id: string;
  trigger: string;
  require_words: string[];
  weight_transfer: number;
  consumes_origin: boolean;
}

export interface CurrentMomentsResponse {
  moments: Moment[];
  transitions: MomentTransition[];
  active_count: number;
}

export interface ClickMomentResponse {
  status: string;
  traversed: boolean;
  target_moment?: Moment;
  consumed_origin: boolean;
  new_active_moments: Moment[];
}

// SSE event handlers for moment stream
export interface MomentStreamCallbacks {
  onMomentActivated?: (data: { moment_id: string; weight: number; text: string }) => void;
  onMomentSpoken?: (data: { moment_id: string; tick: number }) => void;
  onMomentDecayed?: (data: { moment_id: string }) => void;
  onWeightUpdated?: (data: { moment_id: string; weight: number }) => void;
  onClickTraversed?: (data: { from_moment_id: string; to_moment_id: string; word: string; consumed_origin: boolean }) => void;
  onComplete?: () => void;
  onError?: (error: string) => void;
}

/**
 * Fetch current moments for a location.
 */
export async function fetchCurrentMoments(
  playthroughId: string,
  location: string,
  presentChars?: string[]
): Promise<CurrentMomentsResponse> {
  const params = new URLSearchParams({ location });
  if (presentChars?.length) {
    params.set('present_chars', presentChars.join(','));
  }

  const res = await fetch(`${API_BASE}/api/moments/current/${playthroughId}?${params}`);
  if (!res.ok) throw new Error(`Failed to fetch moments: ${res.statusText}`);
  return res.json();
}

/**
 * Click a word in a moment to traverse.
 */
export async function clickMoment(
  playthroughId: string,
  momentId: string,
  word: string,
  tick: number
): Promise<ClickMomentResponse> {
  const res = await fetch(`${API_BASE}/api/moments/click`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      playthrough_id: playthroughId,
      moment_id: momentId,
      word,
      tick
    }),
  });
  if (!res.ok) throw new Error(`Click failed: ${res.statusText}`);
  return res.json();
}

/**
 * Get moment statistics.
 */
export async function getMomentStats(): Promise<{
  stats: Record<string, number>;
}> {
  const res = await fetch(`${API_BASE}/api/moments/stats`);
  if (!res.ok) throw new Error(`Failed to fetch moment stats: ${res.statusText}`);
  return res.json();
}

/**
 * Subscribe to the moment stream SSE endpoint.
 * Returns a function to close the connection.
 */
export function subscribeToMomentStream(
  playthroughId: string,
  callbacks: MomentStreamCallbacks
): () => void {
  const url = `${API_BASE}/api/moments/stream/${playthroughId}`;
  const eventSource = new EventSource(url);

  eventSource.addEventListener('connected', () => {
    console.log('[SSE] Connected to moment stream');
  });

  eventSource.addEventListener('moment_activated', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onMomentActivated?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse moment_activated event:', e);
    }
  });

  eventSource.addEventListener('moment_spoken', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onMomentSpoken?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse moment_spoken event:', e);
    }
  });

  eventSource.addEventListener('moment_decayed', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onMomentDecayed?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse moment_decayed event:', e);
    }
  });

  eventSource.addEventListener('weight_updated', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onWeightUpdated?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse weight_updated event:', e);
    }
  });

  eventSource.addEventListener('click_traversed', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onClickTraversed?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse click_traversed event:', e);
    }
  });

  eventSource.addEventListener('complete', () => {
    callbacks.onComplete?.();
  });

  eventSource.addEventListener('error', (event) => {
    console.error('[SSE] Stream error:', event);
    callbacks.onError?.('Stream connection error');
  });

  eventSource.addEventListener('ping', () => {
    // Keepalive, do nothing
  });

  // Return close function
  return () => {
    eventSource.close();
  };
}

// -----------------------------------------------------------------------------
// View API (Moment System)
// -----------------------------------------------------------------------------

export interface Place {
  id: string;
  name: string;
  type: string;
}

export interface CurrentView {
  location: Place;
  characters: Array<{
    id: string;
    name: string;
    face?: string;
  }>;
  things: Array<{
    id: string;
    name: string;
  }>;
  moments: Moment[];
  transitions: Array<{
    from: string;
    words: string[];
    to: string;
  }>;
}

/**
 * Get current view for a playthrough (replaces getCurrentScene).
 */
export async function getCurrentView(playthroughId: string): Promise<CurrentView | null> {
  try {
    const res = await fetch(`${API_BASE}/api/view/${playthroughId}`);
    if (!res.ok) {
      if (res.status === 404) return null;
      throw new Error(`Failed to get view: ${res.statusText}`);
    }
    return res.json();
  } catch (error) {
    handleApiError(error, 'getCurrentView');
    return null;
  }
}

// -----------------------------------------------------------------------------
// Health Check
// -----------------------------------------------------------------------------

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}
