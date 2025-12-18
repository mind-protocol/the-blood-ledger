'use client';

import { ChronicleEntry, Player } from '@/types/game';

interface ChronicleTabProps {
  entries: ChronicleEntry[];
  player: Player;
}

export function ChronicleTab({ entries, player }: ChronicleTabProps) {
  // Sort by day descending (most recent first)
  const sortedEntries = [...entries].sort((a, b) => b.day - a.day);

  return (
    <div className="h-full overflow-y-auto">
      {/* Header */}
      <div className="sticky top-0 bg-stone-900/95 border-b border-stone-700 px-3 py-2">
        <h3 className="text-sm font-bold text-amber-200">The Chronicle</h3>
        <p className="text-xs text-stone-500">Day {player.day} · {player.location}</p>
      </div>

      {/* Entries */}
      <div className="p-3 space-y-4">
        {sortedEntries.map((entry) => (
          <div
            key={entry.id}
            className={`
              text-sm
              ${entry.day === player.day ? 'text-stone-200' : 'text-stone-400'}
            `}
          >
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-bold text-amber-500/70">
                Day {entry.day}
              </span>
              <span className="text-xs text-stone-600">·</span>
              <span className="text-xs text-stone-500">{entry.location}</span>
            </div>
            <p className={`
              leading-relaxed
              ${entry.isPlayerWritten ? 'italic border-l-2 border-amber-700/50 pl-2' : ''}
            `}>
              {entry.content}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
