'use client';

import { useCallback } from 'react';
import { GameState } from '@/types/game';
import { SettingStrip } from './scene/SettingStrip';
import { CenterStage } from './scene/CenterStage';
import { ChroniclePanel } from './chronicle/ChroniclePanel';
import { DebugPanel } from './debug/DebugPanel';

interface GameLayoutProps {
  initialState: GameState;
  playthroughId?: string;
  onAction?: (action: string) => Promise<void>;
  tick?: number;  // World tick for moment system
}

export function GameLayout({ initialState: gameState, playthroughId, onAction, tick = 0 }: GameLayoutProps) {
  const currentScene = gameState.currentScene;
  const people = currentScene.hotspots.filter((h) => h.type === 'person');

  const handleEndConversation = useCallback(() => {
    // No-op for now
  }, []);

  const handleWrite = useCallback((text: string) => {
    if (onAction) {
      onAction(text);
    }
  }, [onAction]);

  return (
    <div className="h-screen w-screen bg-stone-950 flex overflow-hidden">
      {/* Left: Setting strip (1/4) */}
      <div className="w-1/4 flex-shrink-0">
        <SettingStrip scene={currentScene} />
      </div>

      {/* Center: Conversation/Interaction (1/2) */}
      <div className="w-1/2 flex-shrink-0 border-x border-stone-800">
        <CenterStage
          scene={currentScene}
          people={people}
          onEndConversation={handleEndConversation}
          playthroughId={playthroughId || ''}
          location={currentScene.id}
          tick={tick}
        />
      </div>

      {/* Right: Chronicle (1/4) */}
      <div className="w-1/4 flex-shrink-0 relative">
        <ChroniclePanel
          chronicle={gameState.chronicle}
          player={gameState.player}
          onWrite={handleWrite}
        />
      </div>

      {/* Debug panel for graph mutations */}
      <DebugPanel collapsed={false} playthroughId={playthroughId} />
    </div>
  );
}
