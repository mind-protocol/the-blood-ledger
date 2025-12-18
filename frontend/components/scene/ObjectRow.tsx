'use client';

import { Hotspot } from '@/types/game';

interface ObjectRowProps {
  objects: Hotspot[]; // Object-type hotspots
  onObjectClick: (objectId: string) => void;
  selectedObject: string | null;
}

export function ObjectRow({ objects, onObjectClick, selectedObject }: ObjectRowProps) {
  if (objects.length === 0) return null;

  return (
    <div className="px-4 py-3 border-b border-stone-700/50">
      <div className="text-xs text-stone-500 uppercase tracking-wider mb-2">
        Here
      </div>
      <div className="flex gap-2 flex-wrap">
        {objects.map((obj) => (
          <button
            key={obj.id}
            onClick={() => onObjectClick(obj.id)}
            className={`
              flex items-center gap-2 px-3 py-2 rounded-lg
              transition-all duration-200 text-sm
              ${selectedObject === obj.id
                ? 'bg-amber-900/40 ring-1 ring-amber-500/50 text-amber-100'
                : 'bg-stone-800/50 hover:bg-stone-700/50 text-stone-300'
              }
            `}
          >
            <span>{obj.icon}</span>
            <span>{obj.name}</span>
          </button>
        ))}
      </div>

      {/* Selected object actions */}
      {selectedObject && (
        <div className="mt-3 p-2 bg-stone-800/50 rounded-lg">
          {objects
            .filter((o) => o.id === selectedObject)
            .map((obj) => (
              <div key={obj.id}>
                <p className="text-xs text-stone-400 mb-2">{obj.description}</p>
                <div className="flex gap-2 flex-wrap">
                  {obj.actions.map((action) => (
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
