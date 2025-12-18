'use client';

import { Hotspot } from '@/types/game';

interface CharacterRowProps {
  characters: Hotspot[]; // Person-type hotspots
  onCharacterClick: (characterId: string) => void;
  selectedCharacter: string | null;
}

export function CharacterRow({ characters, onCharacterClick, selectedCharacter }: CharacterRowProps) {
  if (characters.length === 0) return null;

  return (
    <div className="px-4 py-3 border-b border-stone-700/50">
      <div className="text-xs text-stone-500 uppercase tracking-wider mb-2">
        Present
      </div>
      <div className="flex gap-3 flex-wrap">
        {characters.map((char) => (
          <button
            key={char.id}
            onClick={() => onCharacterClick(char.id)}
            className={`
              flex flex-col items-center gap-1 p-2 rounded-lg
              transition-all duration-200
              ${selectedCharacter === char.id
                ? 'bg-amber-900/40 ring-2 ring-amber-500/50'
                : 'bg-stone-800/50 hover:bg-stone-700/50'
              }
            `}
          >
            {/* Portrait placeholder - will be image later */}
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-stone-700 to-stone-800 flex items-center justify-center text-xl border-2 border-stone-600">
              {char.icon}
            </div>
            <span className="text-xs text-amber-100/80">{char.name}</span>
          </button>
        ))}
      </div>

      {/* Selected character actions */}
      {selectedCharacter && (
        <div className="mt-3 p-2 bg-stone-800/50 rounded-lg">
          {characters
            .filter((c) => c.id === selectedCharacter)
            .map((char) => (
              <div key={char.id}>
                <p className="text-xs text-stone-400 mb-2">{char.description}</p>
                <div className="flex gap-2 flex-wrap">
                  {char.actions.map((action) => (
                    <button
                      key={action.id}
                      className="px-3 py-1 text-xs bg-stone-700/50 hover:bg-amber-900/40 rounded border border-stone-600 hover:border-amber-700 text-amber-100 transition-colors"
                    >
                      {action.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
