'use client';

// DOCS: docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md

import { MapRegion } from '@/types/game';

interface MinimapProps {
  regions: MapRegion[];
  onOpenMap: () => void;
}

export function Minimap({ regions, onOpenMap }: MinimapProps) {
  // Flatten all locations
  const allLocations = regions.flatMap((r) => r.locations);
  const currentLocation = allLocations.find((l) => l.current);
  const discoveredLocations = allLocations.filter((l) => l.discovered);

  return (
    <button
      onClick={onOpenMap}
      className="
        relative w-full aspect-square
        bg-stone-900/90 border border-stone-700
        rounded-lg overflow-hidden
        hover:border-amber-700/50 transition-colors
        group
      "
    >
      {/* Parchment texture */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-950/20 to-stone-900" />

      {/* Locations */}
      {discoveredLocations.map((loc) => (
        <div
          key={loc.id}
          className={`
            absolute w-2 h-2 rounded-full transform -translate-x-1/2 -translate-y-1/2
            ${loc.current
              ? 'bg-amber-400 ring-2 ring-amber-400/50 animate-pulse'
              : 'bg-stone-500'
            }
          `}
          style={{
            left: `${loc.position.x}%`,
            top: `${loc.position.y}%`,
          }}
        />
      ))}

      {/* Connection lines */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        {discoveredLocations.map((loc) =>
          loc.connected
            .map((connId) => {
              const connLoc = allLocations.find((l) => l.id === connId && l.discovered);
              if (!connLoc) return null;
              return (
                <line
                  key={`${loc.id}-${connId}`}
                  x1={`${loc.position.x}%`}
                  y1={`${loc.position.y}%`}
                  x2={`${connLoc.position.x}%`}
                  y2={`${connLoc.position.y}%`}
                  stroke="rgba(120, 113, 108, 0.3)"
                  strokeWidth="1"
                />
              );
            })
        )}
      </svg>

      {/* Current location label */}
      {currentLocation && (
        <div className="absolute bottom-1 left-1 right-1">
          <div className="text-[10px] text-amber-200/80 truncate text-center">
            {currentLocation.name}
          </div>
        </div>
      )}

      {/* Hover overlay */}
      <div className="absolute inset-0 bg-amber-500/0 group-hover:bg-amber-500/5 transition-colors flex items-center justify-center">
        <span className="text-xs text-amber-200/0 group-hover:text-amber-200/70 transition-colors">
          Open Map
        </span>
      </div>
    </button>
  );
}
