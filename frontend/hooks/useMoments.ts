'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  fetchCurrentMoments,
  clickMoment,
  subscribeToMomentStream,
  type Moment,
  type MomentTransition,
  type CurrentMomentsResponse,
  type ClickMomentResponse,
} from '@/lib/api';

/**
 * State returned by useMoments hook.
 */
interface MomentsState {
  /** Spoken moments (history) */
  spokenMoments: Moment[];
  /** Currently active moments */
  activeMoments: Moment[];
  /** All available transitions */
  transitions: MomentTransition[];
  /** Is a traversal in progress */
  isLoading: boolean;
  /** Last error, if any */
  error: string | null;
}

/**
 * Actions returned by useMoments hook.
 */
interface MomentsActions {
  /** Handle a word click in a moment */
  clickWord: (momentId: string, word: string) => Promise<void>;
  /** Refresh current moments from API */
  refresh: () => Promise<void>;
  /** Clear error state */
  clearError: () => void;
}

/**
 * Hook for managing moment state.
 *
 * Connects to the moment API and SSE stream for real-time updates.
 * Handles click traversal and state management.
 *
 * @example
 * const { spokenMoments, activeMoments, clickWord, isLoading } = useMoments({
 *   playthroughId: 'pt_abc123',
 *   location: 'place_camp',
 *   tick: 1234
 * });
 */
export function useMoments({
  playthroughId,
  location,
  tick,
  autoConnect = true,
}: {
  playthroughId: string;
  location?: string;
  tick: number;
  autoConnect?: boolean;
}): MomentsState & MomentsActions {
  const [spokenMoments, setSpokenMoments] = useState<Moment[]>([]);
  const [activeMoments, setActiveMoments] = useState<Moment[]>([]);
  const [transitions, setTransitions] = useState<MomentTransition[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch current moments from API
  const fetchMoments = useCallback(async () => {
    if (!playthroughId || !location) return;

    try {
      const data = await fetchCurrentMoments(playthroughId, location);

      // Separate spoken and active
      const spoken = data.moments.filter(m => m.status === 'spoken');
      const active = data.moments.filter(m =>
        m.status === 'active' || m.status === 'possible'
      );

      setSpokenMoments(spoken);
      setActiveMoments(active);
      setTransitions(data.transitions);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch moments:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
  }, [playthroughId, location]);

  // Handle word click
  const handleClickWord = useCallback(
    async (momentId: string, word: string) => {
      if (isLoading) return;

      setIsLoading(true);
      setError(null);

      try {
        const data = await clickMoment(playthroughId, momentId, word, tick);

        if (data.traversed && data.target_moment) {
          // Move origin to spoken (if consumed)
          if (data.consumed_origin) {
            setActiveMoments(prev => {
              const origin = prev.find(m => m.id === momentId);
              if (origin) {
                setSpokenMoments(s => [...s, { ...origin, status: 'spoken' }]);
              }
              return prev.filter(m => m.id !== momentId);
            });
          }

          // Add new active moments
          setActiveMoments(prev => [...prev, ...data.new_active_moments]);
        }
      } catch (err) {
        console.error('Click failed:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    },
    [playthroughId, tick, isLoading]
  );

  // Connect to SSE stream for real-time updates
  useEffect(() => {
    if (!autoConnect || !playthroughId) return;

    // Connect to moment stream using API function
    const close = subscribeToMomentStream(playthroughId, {
      onMomentActivated: (data) => {
        setActiveMoments(prev => {
          // Avoid duplicates
          if (prev.some(m => m.id === data.moment_id)) return prev;
          // Create minimal moment from event data
          return [...prev, {
            id: data.moment_id,
            text: data.text,
            type: 'narration',
            status: 'active',
            weight: data.weight,
            clickable_words: [],
          }];
        });
      },
      onMomentSpoken: (data) => {
        // Move from active to spoken
        setActiveMoments(prev => {
          const moment = prev.find(m => m.id === data.moment_id);
          if (moment) {
            setSpokenMoments(s => [...s, { ...moment, status: 'spoken' }]);
          }
          return prev.filter(m => m.id !== data.moment_id);
        });
      },
      onWeightUpdated: (data) => {
        setActiveMoments(prev =>
          prev.map(m =>
            m.id === data.moment_id ? { ...m, weight: data.weight } : m
          )
        );
      },
      onError: (error) => {
        console.error('[useMoments] SSE error:', error);
        setError('Connection lost. Reconnecting...');
      }
    });

    return () => {
      close();
    };
  }, [autoConnect, playthroughId]);

  // Initial fetch
  useEffect(() => {
    fetchMoments();
  }, [fetchMoments]);

  return {
    spokenMoments,
    activeMoments,
    transitions,
    isLoading,
    error,
    clickWord: handleClickWord,
    refresh: fetchMoments,
    clearError: () => setError(null),
  };
}

export default useMoments;
