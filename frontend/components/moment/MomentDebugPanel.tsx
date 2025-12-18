'use client';

import { useState } from 'react';
import type { Moment, MomentTransition } from '@/types/moment';

/**
 * Props for MomentDebugPanel component.
 */
interface MomentDebugPanelProps {
  /** All moments (possible, active, spoken) */
  moments: Moment[];
  /** Transitions between moments */
  transitions: MomentTransition[];
  /** Whether to show the panel */
  isOpen?: boolean;
  /** Called when panel is toggled */
  onToggle?: () => void;
}

/**
 * Debug visualization for moment graph state.
 *
 * Shows:
 * - All moments with their weights (visual bars)
 * - Status badges
 * - CAN_LEAD_TO links between moments
 * - Filtering by status
 *
 * @example
 * <MomentDebugPanel
 *   moments={allMoments}
 *   transitions={allTransitions}
 *   isOpen={debugMode}
 *   onToggle={() => setDebugMode(!debugMode)}
 * />
 */
export function MomentDebugPanel({
  moments,
  transitions,
  isOpen = false,
  onToggle,
}: MomentDebugPanelProps) {
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed bottom-4 right-4 px-3 py-1.5 bg-stone-800 text-stone-300 text-xs rounded-md hover:bg-stone-700 transition-colors"
      >
        Debug Moments
      </button>
    );
  }

  // Filter moments by status
  const filteredMoments = statusFilter
    ? moments.filter(m => m.status === statusFilter)
    : moments;

  // Count by status
  const statusCounts = moments.reduce((acc, m) => {
    acc[m.status] = (acc[m.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Get transitions for a moment
  const getTransitionsFrom = (momentId: string) =>
    transitions.filter(t => t.from_id === momentId);

  const getTransitionsTo = (momentId: string) =>
    transitions.filter(t => t.to_id === momentId);

  return (
    <div className="fixed bottom-4 right-4 w-96 max-h-[70vh] bg-stone-900/95 border border-stone-700 rounded-lg shadow-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-stone-800 border-b border-stone-700">
        <h3 className="text-sm font-medium text-stone-200">
          Moment Graph Debug
        </h3>
        <button
          onClick={onToggle}
          className="text-stone-400 hover:text-stone-200"
        >
          ✕
        </button>
      </div>

      {/* Status filter tabs */}
      <div className="flex gap-1 p-2 border-b border-stone-800">
        <button
          onClick={() => setStatusFilter(null)}
          className={`px-2 py-1 text-xs rounded ${
            statusFilter === null
              ? 'bg-amber-500/20 text-amber-300'
              : 'text-stone-400 hover:text-stone-200'
          }`}
        >
          All ({moments.length})
        </button>
        {Object.entries(statusCounts).map(([status, count]) => (
          <button
            key={status}
            onClick={() => setStatusFilter(status)}
            className={`px-2 py-1 text-xs rounded ${
              statusFilter === status
                ? 'bg-amber-500/20 text-amber-300'
                : 'text-stone-400 hover:text-stone-200'
            }`}
          >
            {status} ({count})
          </button>
        ))}
      </div>

      {/* Moments list */}
      <div className="overflow-y-auto max-h-[50vh] p-2 space-y-2">
        {filteredMoments.map(moment => (
          <div
            key={moment.id}
            className="p-2 bg-stone-800/50 rounded border border-stone-700/50"
          >
            {/* Header with status and weight */}
            <div className="flex items-center justify-between mb-1">
              <StatusBadge status={moment.status} />
              <WeightBar weight={moment.weight} />
            </div>

            {/* ID and type */}
            <div className="text-xs text-stone-500 mb-1">
              {moment.id} • {moment.type}
              {moment.tone && ` • ${moment.tone}`}
            </div>

            {/* Text preview */}
            <p className="text-xs text-stone-300 truncate">
              {moment.text.slice(0, 100)}
              {moment.text.length > 100 && '...'}
            </p>

            {/* Clickable words */}
            {moment.clickable_words.length > 0 && (
              <div className="mt-1 flex flex-wrap gap-1">
                {moment.clickable_words.map(word => (
                  <span
                    key={word}
                    className="px-1.5 py-0.5 text-xs bg-amber-500/20 text-amber-300 rounded"
                  >
                    {word}
                  </span>
                ))}
              </div>
            )}

            {/* Transitions */}
            <div className="mt-2 text-xs">
              {getTransitionsFrom(moment.id).map(t => (
                <div key={`${t.from_id}-${t.to_id}`} className="text-stone-500">
                  → {t.to_id.slice(0, 30)}
                  <span className="text-stone-600 ml-1">
                    ({t.trigger}, w:{t.weight_transfer})
                  </span>
                </div>
              ))}
              {getTransitionsTo(moment.id).map(t => (
                <div key={`${t.from_id}-${t.to_id}`} className="text-stone-600">
                  ← {t.from_id.slice(0, 30)}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * Status badge with color coding.
 */
function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    possible: 'bg-blue-500/20 text-blue-300',
    active: 'bg-amber-500/20 text-amber-300',
    spoken: 'bg-green-500/20 text-green-300',
    dormant: 'bg-purple-500/20 text-purple-300',
    decayed: 'bg-stone-500/20 text-stone-400',
  };

  return (
    <span className={`px-1.5 py-0.5 text-xs rounded ${colors[status] || 'text-stone-400'}`}>
      {status}
    </span>
  );
}

/**
 * Visual weight bar (0-1).
 */
function WeightBar({ weight }: { weight: number }) {
  const percentage = Math.round(weight * 100);
  const color =
    weight >= 0.8 ? 'bg-amber-500' :
    weight >= 0.5 ? 'bg-amber-600' :
    weight >= 0.3 ? 'bg-stone-500' :
    'bg-stone-600';

  return (
    <div className="flex items-center gap-1">
      <div className="w-16 h-1.5 bg-stone-700 rounded-full overflow-hidden">
        <div
          className={`h-full ${color} transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-xs text-stone-500">{percentage}%</span>
    </div>
  );
}

export default MomentDebugPanel;
