'use client';

// DOCS: docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md

import { useState, useRef } from 'react';
import { SpeedControl } from '@/components/SpeedControl';
import { ChronicleEntry, Player } from '@/types/game';

interface ChroniclePanelProps {
  chronicle: ChronicleEntry[];
  player: Player;
  onWrite: (text: string) => void;
  playthroughId?: string;
}

export function ChroniclePanel({ chronicle, player, onWrite, playthroughId }: ChroniclePanelProps) {
  const [writeText, setWriteText] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  const handleSubmit = () => {
    if (writeText.trim()) {
      onWrite(writeText.trim());
      setWriteText('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div
      className="h-full flex flex-col"
      style={{
        background: 'linear-gradient(135deg, #2a2520 0%, #1f1b18 50%, #252119 100%)',
      }}
    >
      {/* Parchment texture overlay */}
      <div
        className="absolute inset-0 pointer-events-none opacity-10"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Header */}
      <div className="px-5 py-4 border-b border-amber-900/30 relative">
        <h2 className="text-sm text-amber-700/80 uppercase tracking-[0.2em]">
          Chronicle
        </h2>
        <p className="text-xs text-amber-900/60 mt-1 italic">
          Day {player.day} · {player.location}
        </p>
      </div>

      {/* Scrollable entries */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-4 relative">
        <div className="space-y-6">
          {chronicle.map((entry, index) => (
            <div key={entry.id} className="relative">
              {/* Day marker - like a margin note */}
              <div className="absolute -left-1 top-0 text-xs text-amber-800/50 font-medium">
                {entry.day}
              </div>

              {/* Entry content */}
              <div className="pl-6">
                <p className="text-xs text-amber-600/70 mb-1">
                  {entry.location}
                </p>
                <p
                  className={`text-sm leading-relaxed ${
                    entry.isPlayerWritten
                      ? 'text-amber-100 italic'
                      : 'text-stone-300'
                  }`}
                  style={{ fontFamily: 'Georgia, serif' }}
                >
                  {entry.content}
                </p>
              </div>

              {/* Decorative line between entries */}
              {index < chronicle.length - 1 && (
                <div className="mt-4 border-b border-amber-900/20" />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Write input - like writing in the journal */}
      <div className="px-5 py-4 border-t border-amber-900/30 relative">
        <div className="relative">
          <textarea
            value={writeText}
            onChange={(e) => setWriteText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Write in your journal..."
            rows={2}
            className="w-full bg-transparent text-amber-200/80 text-sm placeholder-amber-900/40 resize-none outline-none italic"
            style={{ fontFamily: 'Georgia, serif' }}
          />
          {writeText.trim() && (
            <button
              onClick={handleSubmit}
              className="absolute bottom-1 right-0 text-xs text-amber-700/60 hover:text-amber-600 transition-colors"
            >
              [write]
            </button>
          )}
        </div>
        {playthroughId && (
          <div className="mt-3 flex flex-wrap gap-2">
            <SpeedControl playthroughId={playthroughId} />
          </div>
        )}
      </div>
    </div>
  );
}
