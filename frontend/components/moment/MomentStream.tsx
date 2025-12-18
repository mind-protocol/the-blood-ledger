'use client';

import { useEffect, useRef } from 'react';
import type { Moment } from '@/types/moment';
import { MomentDisplay } from './MomentDisplay';

/**
 * Props for MomentStream component.
 */
interface MomentStreamProps {
  /** Spoken moments (history), ordered by tick_spoken */
  moments: Moment[];
  /** Currently active/possible moments */
  activeMoments: Moment[];
  /** Called when a word is clicked in an active moment */
  onWordClick: (momentId: string, word: string) => void;
  /** Is a traversal in progress */
  isLoading?: boolean;
  /** Show debug info */
  showDebug?: boolean;
}

/**
 * Displays a stream of moments (spoken history + active).
 *
 * Replaces DialogueStream with moment-aware rendering:
 * - Spoken moments are rendered as history (non-interactive)
 * - Active moments are interactive (clickable words)
 * - Auto-scrolls to latest moment
 *
 * @example
 * <MomentStream
 *   moments={spokenMoments}
 *   activeMoments={activeMoments}
 *   onWordClick={(id, word) => handleClick(id, word)}
 *   isLoading={isTraversing}
 * />
 */
export function MomentStream({
  moments,
  activeMoments,
  onWordClick,
  isLoading = false,
  showDebug = false,
}: MomentStreamProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new moments arrive
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [moments.length, activeMoments.length]);

  // Handle word click - pass both moment ID and word
  const handleWordClick = (momentId: string) => (word: string) => {
    if (!isLoading) {
      onWordClick(momentId, word);
    }
  };

  // If nothing to show
  if (moments.length === 0 && activeMoments.length === 0) {
    return null;
  }

  return (
    <div
      ref={containerRef}
      className="space-y-3 overflow-y-auto max-h-[60vh]"
    >
      {/* Spoken moments (history) */}
      {moments.map((moment, index) => (
        <MomentDisplay
          key={moment.id}
          moment={moment}
          showDebug={showDebug}
        />
      ))}

      {/* Divider between history and active */}
      {moments.length > 0 && activeMoments.length > 0 && (
        <div className="border-t border-stone-800/30 pt-4" />
      )}

      {/* Active moments (interactive) */}
      {activeMoments.map((moment, index) => (
        <MomentDisplay
          key={moment.id}
          moment={moment}
          onWordClick={handleWordClick(moment.id)}
          isLatest={index === activeMoments.length - 1}
          showDebug={showDebug}
        />
      ))}

      {/* Loading indicator - subtle */}
      {isLoading && (
        <div className="flex items-center gap-1 py-2 opacity-40">
          <span
            className="w-1.5 h-1.5 bg-stone-500 rounded-full animate-pulse"
            style={{ animationDelay: '0ms' }}
          />
          <span
            className="w-1.5 h-1.5 bg-stone-500 rounded-full animate-pulse"
            style={{ animationDelay: '200ms' }}
          />
          <span
            className="w-1.5 h-1.5 bg-stone-500 rounded-full animate-pulse"
            style={{ animationDelay: '400ms' }}
          />
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={bottomRef} />
    </div>
  );
}

export default MomentStream;
