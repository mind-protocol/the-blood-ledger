'use client';

// DOCS: docs/frontend/scene/PATTERNS_Scene.md

import { Scene, Voice } from '@/types/game';
import { SceneHeader } from './SceneHeader';
import { SceneBanner } from './SceneBanner';

interface SceneViewProps {
  scene: Scene;
  voices?: Voice[];
  onTalk?: (personId: string) => void;
  onTravel?: () => void;
  onWrite?: () => void;
}

export function SceneView({
  scene,
  voices = [],
  onTalk,
  onTravel,
  onWrite,
}: SceneViewProps) {
  // Get people from hotspots (only type === 'person')
  const people = scene.hotspots.filter((h) => h.type === 'person');

  return (
    <div className="flex flex-col h-full bg-stone-900">
      {/* Header */}
      <SceneHeader scene={scene} />

      {/* Banner image */}
      <SceneBanner scene={scene} />

      {/* People present */}
      {people.length > 0 && (
        <div className="px-4 py-3 border-b border-stone-800">
          <div className="flex gap-4">
            {people.map((person) => (
              <div key={person.id} className="flex items-start gap-3">
                {/* Portrait */}
                <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 bg-stone-800">
                  {person.imageUrl ? (
                    <img
                      src={person.imageUrl}
                      alt={person.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-2xl">
                      {person.icon}
                    </div>
                  )}
                </div>
                {/* Name and description */}
                <div className="flex-1 min-w-0">
                  <h3 className="text-amber-200 font-medium text-sm">{person.name}</h3>
                  <p className="text-stone-400 text-xs leading-relaxed mt-0.5">
                    {person.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Voices */}
      {voices.length > 0 && (
        <div className="px-4 py-3 flex-1">
          <h4 className="text-stone-500 text-xs uppercase tracking-wider mb-2">Voices</h4>
          <div className="space-y-2">
            {voices
              .sort((a, b) => b.weight - a.weight)
              .slice(0, 4)
              .map((voice) => (
                <p
                  key={voice.id}
                  className="text-stone-300 text-sm italic"
                  style={{ opacity: 0.5 + voice.weight * 0.5 }}
                >
                  "{voice.content}"
                </p>
              ))}
          </div>
        </div>
      )}

      {/* Three actions */}
      <div className="px-4 py-3 border-t border-stone-800 mt-auto">
        <div className="flex gap-3">
          {/* Talk - one button per person */}
          {people.map((person) => (
            <button
              key={person.id}
              onClick={() => onTalk?.(person.id)}
              className="flex-1 px-4 py-2.5 bg-amber-900/30 hover:bg-amber-900/50 border border-amber-700/50 hover:border-amber-600 rounded-lg text-amber-100 text-sm font-medium transition-colors"
            >
              Talk to {person.name}
            </button>
          ))}

          {/* Travel */}
          <button
            onClick={onTravel}
            className="px-4 py-2.5 bg-stone-800 hover:bg-stone-700 border border-stone-600 hover:border-stone-500 rounded-lg text-stone-200 text-sm font-medium transition-colors"
          >
            Travel
          </button>

          {/* Write */}
          <button
            onClick={onWrite}
            className="px-4 py-2.5 bg-stone-800 hover:bg-stone-700 border border-stone-600 hover:border-stone-500 rounded-lg text-stone-200 text-sm font-medium transition-colors"
          >
            Write
          </button>
        </div>
      </div>
    </div>
  );
}
