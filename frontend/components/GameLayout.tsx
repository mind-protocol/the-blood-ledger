'use client';

import { useCallback } from 'react';
import { GameState } from '@/types/game';
import { SettingStrip } from './scene/SettingStrip';
import { CenterStage } from './scene/CenterStage';
import { ChroniclePanel } from './chronicle/ChroniclePanel';
import { Minimap } from './minimap/Minimap';
import { DebugPanel } from './debug/DebugPanel';

type Speed = 'pause' | '1x' | '2x' | '3x';

interface GameLayoutProps {
  initialState: GameState;
  playthroughId?: string;
  onAction?: (action: string) => Promise<void>;
  tick?: number;  // World tick for moment system
  speed?: Speed;  // Current game speed
}

export function GameLayout({ initialState: gameState, playthroughId, onAction, tick = 0, speed = '1x' }: GameLayoutProps) {
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

      {/* Right: Minimap + Chronicle (1/4) */}
      <div className="w-1/4 flex-shrink-0 relative flex flex-col">
        {/* Minimap with Sun Arc */}
        {gameState.map && gameState.map.length > 0 && (
          <div className={`
            p-2 border-b border-stone-800 flex-shrink-0
            transition-all duration-300
            ${speed === '3x' ? 'flex-grow max-h-[50%]' : ''}
            ${speed === '2x' ? 'pb-4' : ''}
          `}>
            <Minimap
              regions={gameState.map}
              onOpenMap={() => window.location.href = '/map'}
              tick={tick}
              speed={speed}
            />
          </div>
        )}

        {/* Chronicle */}
        <div className="flex-1 min-h-0">
          <ChroniclePanel
            chronicle={gameState.chronicle}
            player={gameState.player}
            onWrite={handleWrite}
            playthroughId={playthroughId}
          />
        </div>
      </div>

      {/* Debug panel for graph mutations */}
      <DebugPanel collapsed={false} playthroughId={playthroughId} />
    </div>
  );
}
