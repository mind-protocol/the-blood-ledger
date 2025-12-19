// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md
// =============================================================================
// GAME STATE TYPES
// =============================================================================

// -----------------------------------------------------------------------------
// Scene Types
// -----------------------------------------------------------------------------

export type SceneType =
  | 'CAMP'
  | 'ROAD'
  | 'HALL'
  | 'HOLD'
  | 'VILLAGE'
  | 'FOREST'
  | 'CHURCH'
  | 'BATTLEFIELD'
  | 'TAVERN'
  | 'GATE';

export type TimeOfDay = 'DAWN' | 'DAY' | 'DUSK' | 'NIGHT';

export type Weather = 'CLEAR' | 'CLOUDY' | 'RAIN' | 'STORM' | 'FOG' | 'SNOW';

export interface HotspotAction {
  id: string;
  label: string;
  description?: string;
}

export interface Hotspot {
  id: string;
  type: 'object' | 'person';
  name: string;
  description: string;
  position: { x: number; y: number }; // percentage position in scene
  icon: string; // emoji or icon key
  imageUrl?: string | null; // path to square image
  actions: HotspotAction[];
}

export interface SceneAction {
  id: string;
  label: string;
  description?: string;
}

export interface Scene {
  id: string;
  placeId?: string;  // Graph place ID for image lookup
  type: SceneType;
  name: string;
  location: string;
  timeOfDay: TimeOfDay;
  weather: Weather;
  atmosphere: string[]; // 2-3 lines
  hotspots: Hotspot[];
  actions: SceneAction[];
  bannerImage?: string | null; // path to 16:9 banner image
}

// -----------------------------------------------------------------------------
// Character Types
// -----------------------------------------------------------------------------

export interface Character {
  id: string;
  name: string;
  title?: string | null;
  description: string;
  face?: string | null; // image URL or placeholder
  location: string;
  isCompanion: boolean;
  isPresent: boolean; // in current scene
}

// -----------------------------------------------------------------------------
// Narrative Types (Voices)
// -----------------------------------------------------------------------------

export type NarrativeType =
  | 'debt'
  | 'oath'
  | 'blood'
  | 'memory'
  | 'rumor'
  | 'reputation'
  | 'companion';

export interface Voice {
  id: string;
  type: NarrativeType;
  source: string; // who/what is speaking (e.g., "THE DEBT TO EDMUND", "ALDRIC")
  content: string; // what they say
  weight: number; // 0-1, determines prominence
}

// -----------------------------------------------------------------------------
// Chronicle Types
// -----------------------------------------------------------------------------

export interface ChronicleEntry {
  id: string;
  day: number;
  location: string;
  content: string;
  isPlayerWritten: boolean;
}

// -----------------------------------------------------------------------------
// Ledger Types
// -----------------------------------------------------------------------------

export interface LedgerEntry {
  id: string;
  type: 'debt' | 'oath' | 'blood';
  subject: string; // who it's about
  content: string;
  resolved: boolean;
}

// -----------------------------------------------------------------------------
// Conversation Types
// -----------------------------------------------------------------------------

export interface ConversationMessage {
  id: string;
  speaker: string; // character name or 'player'
  content: string;
  timestamp: number;
}

export interface Conversation {
  id: string;
  characterId: string;
  characterName: string;
  messages: ConversationMessage[];
  isActive: boolean;
}

// -----------------------------------------------------------------------------
// Map Types
// -----------------------------------------------------------------------------

export interface MapLocation {
  id: string;
  name: string;
  type: SceneType;
  position: { x: number; y: number };
  discovered: boolean;
  current: boolean;
  connected: string[]; // IDs of connected locations
}

export interface MapRegion {
  id: string;
  name: string;
  locations: MapLocation[];
}

// -----------------------------------------------------------------------------
// Player State
// -----------------------------------------------------------------------------

export interface Player {
  name: string;
  title?: string | null;
  day: number;
  location: string;
}

// -----------------------------------------------------------------------------
// Dialogue Types (Streaming Narrator Output)
// -----------------------------------------------------------------------------

// A single chunk of streamed dialogue
export interface DialogueChunk {
  speaker?: string;          // Character ID if dialogue, omit for narration
  text: string;              // The content
}

// Graph mutation from narrator
export interface GraphMutation {
  type: 'new_character' | 'new_edge' | 'new_narrative' | 'update_belief' | 'adjust_focus';
  payload: Record<string, unknown>;
}

// Full narrator output (new format)
export interface NarratorOutput {
  dialogue: DialogueChunk[];        // Streamed response chunks
  mutations: GraphMutation[];       // Changes invented during generation
  scene: SceneTree | Record<string, never>;  // Full scene OR empty {} for conversational
  time_elapsed?: string;            // Only for significant actions (≥5 min)
  seeds?: Array<{
    setup: string;
    intended_payoff: string;
  }>;
}

// SSE event types for streaming
export type DialogueSSEEventType = 'dialogue' | 'mutation' | 'scene' | 'time' | 'complete' | 'error';

export interface DialogueSSEEvent {
  type: DialogueSSEEventType;
  data: DialogueChunk | GraphMutation | SceneTree | { time_elapsed: string } | { status: string } | { error: string };
}

// -----------------------------------------------------------------------------
// Scene Tree Types (Pre-Baked Narrator Output)
// -----------------------------------------------------------------------------

// A clickable word with its response tree
export interface SceneTreeClickable {
  speaks: string;           // What player says when clicking
  name: string;             // Name for tracking
  response?: SceneTreeResponse;
  waitingMessage?: string;  // Immersive message shown while LLM generates response (when no pre-baked response)
}

// A response to a click - can be narration, speech, or both
export interface SceneTreeResponse {
  type?: 'narration';       // Optional - defaults to speech if speaker present
  speaker?: string;         // Character speaking (if dialogue)
  text: string;             // The response text
  then?: SceneTreeNarration; // Follow-up narration with more clickables
  clickable?: Record<string, SceneTreeClickable>; // New clickables in response
}

// A piece of narration with clickable words
export interface SceneTreeNarration {
  text: string;
  speaker?: string;         // If this is dialogue
  clickable?: Record<string, SceneTreeClickable>;
  freeform_acknowledgment?: SceneTreeFreeformAck;  // Pre-written response to free text input
}

// Pre-written acknowledgment after player free text input (nests)
export interface SceneTreeFreeformAck {
  speaker?: string;         // Character speaking (if dialogue)
  text: string;             // The acknowledgment text
  then?: SceneTreeNarration[];  // Continue with more narration (nests)
}

// A voice (internal thought) with clickable concepts
export interface SceneTreeVoice {
  source: string;           // Narrative ID from graph
  text: string;             // What the voice says
  weight: number;           // How loud (0-1)
  clickable?: Record<string, SceneTreeClickable>;
}

// Free input configuration
export interface SceneTreeFreeInput {
  enabled: boolean;
  handler: string;          // Which LLM handler to use
  context: string[];        // Graph nodes to include in context
}

// Scene exits (travel/wait options)
export interface SceneTreeExit {
  speaks: string;           // What player says
  destinations?: string[];  // For travel: places available
  advances_time?: boolean;  // For wait: does time pass
  next_scene?: string;      // For wait: which scene loads next
}

// Full scene tree structure
export interface SceneTree {
  id: string;
  location: {
    place: string;          // Graph place ID
    name: string;           // Display name
    region: string;         // Location description
    time: string;           // Time of day
  };
  characters: string[];     // Character IDs present in scene
  atmosphere: string[];     // Atmospheric text lines
  narration: SceneTreeNarration[];
  voices: SceneTreeVoice[];
  freeInput?: SceneTreeFreeInput;
  exits?: {
    travel?: SceneTreeExit;
    wait?: SceneTreeExit;
  };
}

// Conversation state - tracks current position in tree
export interface ConversationState {
  sceneTreeId: string;
  currentNarration: SceneTreeNarration[];  // Current narration being shown
  currentVoices: SceneTreeVoice[];         // Current voices being shown
  history: {
    spoken: string;           // What player said
    response: SceneTreeResponse; // Response received
  }[];
}

// -----------------------------------------------------------------------------
// Full Game State
// -----------------------------------------------------------------------------

export interface GameState {
  player: Player;
  currentScene: Scene;
  sceneTree?: SceneTree;  // Raw Narrator response with clickables
  characters: Character[];
  voices: Voice[];
  chronicle: ChronicleEntry[];
  ledger: LedgerEntry[];
  conversations: Conversation[];
  map: MapRegion[];
}
