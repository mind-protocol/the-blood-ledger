'use client';

import { Voice } from '@/types/game';

interface VoicesProps {
  voices: Voice[];
}

export function Voices({ voices }: VoicesProps) {
  // Sort by weight descending
  const sortedVoices = [...voices].sort((a, b) => b.weight - a.weight);

  const typeStyles: Record<string, { color: string; icon: string }> = {
    debt: { color: 'text-red-400', icon: '⚖️' },
    oath: { color: 'text-amber-400', icon: '🤝' },
    blood: { color: 'text-rose-500', icon: '🩸' },
    memory: { color: 'text-blue-400', icon: '💭' },
    rumor: { color: 'text-purple-400', icon: '👁️' },
    reputation: { color: 'text-emerald-400', icon: '📜' },
    companion: { color: 'text-sky-400', icon: '🗣️' },
  };

  return (
    <div className="px-4 py-2 space-y-3">
      {sortedVoices.map((voice) => {
        const style = typeStyles[voice.type] || { color: 'text-stone-400', icon: '💬' };
        const opacity = 0.5 + voice.weight * 0.5; // Higher weight = more visible

        return (
          <div
            key={voice.id}
            className="flex gap-3"
            style={{ opacity }}
          >
            <span className="text-sm">{style.icon}</span>
            <div className="flex-1">
              <span className={`text-xs font-bold uppercase tracking-wider ${style.color}`}>
                {voice.source}:
              </span>
              <p className="text-sm text-stone-300 italic mt-0.5">
                "{voice.content}"
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
