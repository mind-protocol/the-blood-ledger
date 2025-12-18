// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md

import { GameClient } from '@/components/GameClient';
import gameStateData from '@/data/game-state.json';
import { GameState } from '@/types/game';

export default function Home() {
  // Static data as fallback when backend unavailable
  const fallbackState = gameStateData as GameState;

  return <GameClient fallbackState={fallbackState} />;
}
