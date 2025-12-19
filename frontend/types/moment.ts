// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md
/**
 * Blood Ledger — Moment Type Definitions
 *
 * Types for the moment graph system.
 * See: docs/engine/UI_API_CHANGES_Moment_Graph.md
 */

/**
 * A moment from the graph.
 */
export interface Moment {
  id: string;
  text: string;
  type: MomentType;
  status: MomentStatus;
  weight: number;
  tone?: string;
  tick_created: number;
  tick_spoken?: number;
  speaker?: string;  // Character ID, from SAID link
  clickable_words: string[];
}

export type MomentType =
  | 'narration'
  | 'dialogue'
  | 'hint'
  | 'player_click'
  | 'player_freeform'
  | 'player_choice'
  | 'action'
  | 'thought';

export type MomentStatus =
  | 'possible'
  | 'active'
  | 'spoken'
  | 'dormant'
  | 'decayed';

/**
 * A CAN_LEAD_TO link between moments.
 */
export interface MomentTransition {
  from_id: string;
  to_id: string;
  trigger: 'click' | 'wait' | 'auto' | 'semantic';
  require_words: string[];
  weight_transfer: number;
  consumes_origin: boolean;
  wait_ticks?: number;
  bidirectional?: boolean;
}

/**
 * Response from GET /api/moments/current
 */
export interface CurrentMomentsResponse {
  moments: Moment[];
  transitions: MomentTransition[];
  active_count: number;
}

/**
 * Request for POST /api/moments/click
 */
export interface ClickRequest {
  playthrough_id: string;
  moment_id: string;
  word: string;
  tick: number;
}

/**
 * Response from POST /api/moments/click
 */
export interface ClickResponse {
  status: 'ok' | 'no_match' | 'error';
  traversed: boolean;
  target_moment?: Moment;
  consumed_origin: boolean;
  new_active_moments: Moment[];
}

/**
 * SSE event types for moment updates.
 */
export type MomentEventType =
  | 'moment_activated'
  | 'moment_spoken'
  | 'moment_decayed'
  | 'weight_updated';

export interface MomentEvent {
  type: MomentEventType;
  moment_id: string;
  data: Partial<Moment>;
}
