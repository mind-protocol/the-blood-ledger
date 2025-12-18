'use client';

import { Hotspot } from '@/types/game';

interface HotspotRowProps {
  hotspots: Hotspot[];
  onHotspotClick: (hotspotId: string) => void;
  selectedHotspot: string | null;
}

export function HotspotRow({ hotspots, onHotspotClick, selectedHotspot }: HotspotRowProps) {
  if (hotspots.length === 0) return null;

  // Sort: people first, then objects
  const sortedHotspots = [...hotspots].sort((a, b) => {
    if (a.type === 'person' && b.type !== 'person') return -1;
    if (a.type !== 'person' && b.type === 'person') return 1;
    return 0;
  });

  const selectedItem = hotspots.find((h) => h.id === selectedHotspot);

  return (
    <div className="p-3">
      {/* Horizontal scrollable row of hotspots */}
      <div className="flex gap-3 overflow-x-auto pb-2">
        {sortedHotspots.map((hotspot) => (
          <button
            key={hotspot.id}
            onClick={() => onHotspotClick(hotspot.id)}
            className={`
              relative flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden
              transition-all duration-200
              ${selectedHotspot === hotspot.id
                ? 'ring-2 ring-amber-500/70'
                : 'hover:ring-1 hover:ring-stone-500/50'
              }
            `}
          >
            {hotspot.imageUrl ? (
              <img
                src={hotspot.imageUrl}
                alt={hotspot.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full bg-stone-800 flex items-center justify-center text-2xl">
                {hotspot.icon}
              </div>
            )}
            {/* Name overlay */}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent px-1 py-0.5">
              <span className={`text-[10px] font-medium leading-tight block truncate ${hotspot.type === 'person' ? 'text-amber-200' : 'text-stone-200'}`}>
                {hotspot.name}
              </span>
            </div>
          </button>
        ))}
      </div>

      {/* Selected hotspot actions */}
      {selectedItem && (
        <div className="mt-3 p-3 bg-stone-800/50 rounded-lg">
          <p className="text-xs text-stone-400 mb-2">{selectedItem.description}</p>
          <div className="flex gap-2 flex-wrap">
            {selectedItem.actions.map((action) => (
              <button
                key={action.id}
                className="px-3 py-1 text-xs bg-stone-700/50 hover:bg-amber-900/40 rounded border border-stone-600 hover:border-amber-700 text-amber-100 transition-colors"
              >
                {action.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
