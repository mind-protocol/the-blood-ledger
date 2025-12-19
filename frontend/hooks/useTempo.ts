'use client';

// DOCS: docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md

import { useState, useEffect, useCallback } from 'react';
import { API_BASE } from '@/lib/api';

type Speed = 'pause' | '1x' | '2x' | '3x';

interface TempoState {
  speed: Speed;
  tick: number;
  running: boolean;
}

interface UseTempoReturn {
  speed: Speed;
  tick: number;
  running: boolean;
  setSpeed: (speed: Speed) => Promise<void>;
}

/**
 * Hook to track tempo state (speed, tick) from backend.
 *
 * Listens to SSE events for speed_changed and tick updates.
 */
export function useTempo(
  playthroughId: string | undefined,
  apiBase: string = API_BASE
): UseTempoReturn {
  const [state, setState] = useState<TempoState>({
    speed: '1x',
    tick: 0,
    running: false,
  });

  // Fetch initial state
  useEffect(() => {
    if (!playthroughId) return;

    const fetchState = async () => {
      try {
        const res = await fetch(`${apiBase}/api/tempo/${playthroughId}`);
        if (res.ok) {
          const data = await res.json();
          setState({
            speed: data.speed,
            tick: data.tick,
            running: data.running,
          });
        }
      } catch (err) {
        console.error('Failed to fetch tempo state:', err);
      }
    };

    fetchState();
  }, [playthroughId, apiBase]);

  // Listen for SSE events
  useEffect(() => {
    if (!playthroughId) return;

    const eventSource = new EventSource(`${apiBase}/api/moments/stream/${playthroughId}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'speed_changed') {
          setState((prev) => ({
            ...prev,
            speed: data.payload.speed,
          }));
        }

        // Track tick from moment_spoken events
        if (data.type === 'moment_spoken' && data.payload?.tick !== undefined) {
          setState((prev) => ({
            ...prev,
            tick: data.payload.tick,
          }));
        }
      } catch (err) {
        // Ignore parse errors
      }
    };

    return () => eventSource.close();
  }, [playthroughId, apiBase]);

  const setSpeed = useCallback(async (speed: Speed) => {
    if (!playthroughId) return;

    try {
      const res = await fetch(`${apiBase}/api/tempo/speed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playthrough_id: playthroughId, speed }),
      });

      if (res.ok) {
        setState((prev) => ({ ...prev, speed }));
      }
    } catch (err) {
      console.error('Failed to set speed:', err);
    }
  }, [playthroughId, apiBase]);

  return {
    speed: state.speed,
    tick: state.tick,
    running: state.running,
    setSpeed,
  };
}
