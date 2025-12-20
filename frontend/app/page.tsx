// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md
'use client';

import { useState, useEffect } from 'react';
import { GameClient } from '@/components/GameClient';
import gameStateData from '@/data/game-state.json';
import { GameState } from '@/types/game';

export default function Home() {
  const [playthroughId, setPlaythroughId] = useState<string | undefined>(undefined);

  // Read playthrough ID from session storage on mount
  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      const stored = sessionStorage.getItem('playthroughId');
      if (stored) {
        setPlaythroughId(stored);
      }
    });

    return () => cancelAnimationFrame(raf);
  }, []);

  // Static data as fallback when backend unavailable
  const fallbackState = gameStateData as GameState;

  return <GameClient fallbackState={fallbackState} playthroughId={playthroughId} />;
}
