'use client';

// DOCS: docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md

import { useState, useEffect, useCallback } from 'react';
import { API_BASE } from '@/lib/api';

type Speed = 'pause' | '1x' | '2x' | '3x';

interface SpeedControlProps {
  playthroughId: string;
  apiBase?: string;
}

const SPEED_CONFIG: Record<Speed, { icon: string; label: string; title: string }> = {
  pause: { icon: '⏸', label: 'Pause', title: 'Turn-based: waits for your input' },
  '1x': { icon: '🗣️', label: '1x', title: 'Present: real-time conversation' },
  '2x': { icon: '🚶', label: '2x', title: 'Travel: time passes, dialogue persists' },
  '3x': { icon: '⏩', label: '3x', title: 'Skip: fast-forward until drama' },
};

const SPEEDS: Speed[] = ['pause', '1x', '2x', '3x'];

export function SpeedControl({ playthroughId, apiBase = API_BASE }: SpeedControlProps) {
  const [currentSpeed, setCurrentSpeed] = useState<Speed>('1x');
  const [isLoading, setIsLoading] = useState(false);

  // Fetch current speed on mount
  useEffect(() => {
    const fetchSpeed = async () => {
      try {
        const res = await fetch(`${apiBase}/api/tempo/${playthroughId}`);
        if (res.ok) {
          const data = await res.json();
          setCurrentSpeed(data.speed);
        }
      } catch (err) {
        console.error('Failed to fetch tempo state:', err);
      }
    };

    fetchSpeed();
  }, [playthroughId, apiBase]);

  // Listen for speed_changed SSE events
  useEffect(() => {
    const eventSource = new EventSource(`${apiBase}/api/moments/stream/${playthroughId}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'speed_changed') {
          setCurrentSpeed(data.payload.speed);
        }
      } catch (err) {
        // Ignore parse errors
      }
    };

    return () => eventSource.close();
  }, [playthroughId, apiBase]);

  const setSpeed = useCallback(async (speed: Speed) => {
    if (speed === currentSpeed || isLoading) return;

    setIsLoading(true);
    try {
      const res = await fetch(`${apiBase}/api/tempo/speed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playthrough_id: playthroughId, speed }),
      });

      if (res.ok) {
        setCurrentSpeed(speed);
      }
    } catch (err) {
      console.error('Failed to set speed:', err);
    } finally {
      setIsLoading(false);
    }
  }, [playthroughId, apiBase, currentSpeed, isLoading]);

  return (
    <div className="flex flex-wrap items-center gap-1 bg-stone-900/80 backdrop-blur-sm rounded-lg px-2 py-1 border border-stone-700 max-w-full">
      {SPEEDS.map((speed) => {
        const config = SPEED_CONFIG[speed];
        const isActive = speed === currentSpeed;

        return (
          <button
            key={speed}
            onClick={() => setSpeed(speed)}
            disabled={isLoading}
            title={config.title}
            className={`
              px-2 py-1 rounded text-sm font-medium transition-all duration-150
              ${isActive
                ? 'bg-amber-900/60 text-amber-200 border border-amber-700'
                : 'text-stone-400 hover:text-stone-200 hover:bg-stone-800 border border-transparent'
              }
              ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            <span className="mr-1">{config.icon}</span>
            <span className="hidden sm:inline">{config.label}</span>
          </button>
        );
      })}
    </div>
  );
}
