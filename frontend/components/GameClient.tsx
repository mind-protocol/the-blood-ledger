'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useGameState } from '@/hooks/useGameState';
import { useTempo } from '@/hooks/useTempo';
import { GameLayout } from '@/components/GameLayout';
import { GameState } from '@/types/game';

interface GameClientProps {
  fallbackState: GameState;
  playthroughId?: string;
}

// Immersive loading messages (generic, not plot-specific)
const LOADING_MESSAGES = [
  "The fire crackles in the darkness...",
  "Shadows dance at the edge of vision...",
  "The wind carries distant voices...",
  "Memory stirs in the silence...",
  "The world holds its breath...",
];

export function GameClient({ fallbackState, playthroughId: propPlaythroughId }: GameClientProps) {
  const router = useRouter();
  const { gameState, playthroughId, isLoading, error, isConnected, needsOpening, loadingMessage, sendAction } = useGameState(propPlaythroughId);
  const { speed, tick } = useTempo(playthroughId);

  // Redirect to start screen if no scene exists
  useEffect(() => {
    if (needsOpening && !isLoading) {
      router.replace('/start');
    }
  }, [needsOpening, isLoading, router]);

  // Handle player actions (free input)
  const handleAction = async (action: string) => {
    console.log('Action:', action);
    await sendAction(action);
  };

  // Show immersive loading state (also while redirecting to opening)
  if (isLoading || needsOpening) {
    const message = loadingMessage || LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)];

    return (
      <div className="flex items-center justify-center min-h-screen bg-stone-950">
        <div className="max-w-lg text-center px-8">
          {/* Atmospheric glow */}
          <div className="relative mb-8">
            <div className="absolute inset-0 blur-3xl bg-amber-900/20 rounded-full" />
            <div className="relative text-6xl animate-pulse">🔥</div>
          </div>

          {/* Loading message */}
          <p className="text-stone-400 text-lg italic leading-relaxed mb-6">
            {message}
          </p>

          {/* Subtle progress indicator */}
          <div className="flex justify-center gap-1">
            <div className="w-2 h-2 rounded-full bg-stone-600 animate-pulse" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 rounded-full bg-stone-600 animate-pulse" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 rounded-full bg-stone-600 animate-pulse" style={{ animationDelay: '300ms' }} />
          </div>

          {/* Connection status */}
          <p className="text-stone-600 text-xs mt-8">
            {isConnected ? 'Connected to the world...' : 'Awakening the Narrator...'}
          </p>
        </div>
      </div>
    );
  }

  // Use live data if connected, fallback otherwise
  const state = isConnected && gameState ? gameState : fallbackState;

  return (
    <>
      {/* Top right: Connection status */}
      <div className="fixed top-2 right-2 z-50">
        <div
          className={`px-2 py-1 rounded text-xs ${
            isConnected
              ? 'bg-green-900/50 text-green-300'
              : 'bg-amber-900/50 text-amber-300'
          }`}
        >
          {isConnected ? '● Live' : '○ Static'}
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div className="fixed top-2 left-2 right-16 z-50 bg-red-900/80 text-red-200 px-3 py-1 rounded text-sm">
          {error}
        </div>
      )}

      <GameLayout
        initialState={state}
        playthroughId={playthroughId}
        onAction={handleAction}
        tick={tick}
        speed={speed}
      />
    </>
  );
}
