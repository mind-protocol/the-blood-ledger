'use client';

// DOCS: docs/frontend/map/PATTERNS_Interactive_Travel_Map.md

import { useState, useCallback, useEffect } from 'react';
import { MapCanvas } from './MapCanvas';
import { places, routes, sampleVisibility } from '@/data/map-data';
import { Place, PlaceHoverInfo, VisibilityState } from '@/types/map';

export function MapClient() {
  const [selectedPlace, setSelectedPlace] = useState<Place | null>(null);
  const [playerPosition] = useState<string>('place_york');
  const [visibility] = useState<VisibilityState>(sampleVisibility);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  // Update dimensions on resize
  useEffect(() => {
    const updateDimensions = () => {
      // Account for header and padding
      const headerHeight = 80;
      const padding = 32;
      setDimensions({
        width: Math.min(window.innerWidth - padding * 2, 1200),
        height: window.innerHeight - headerHeight - padding * 2,
      });
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const handleSelectPlace = useCallback((place: Place) => {
    setSelectedPlace(place);
  }, []);

  const handleHoverPlace = useCallback((info: PlaceHoverInfo | null) => {
    // Could update status bar or other UI elements
  }, []);

  return (
    <div className="min-h-screen bg-stone-950 flex flex-col">
      {/* Header */}
      <header className="h-16 bg-stone-900/80 border-b border-stone-800 flex items-center justify-between px-6">
        <h1 className="text-xl font-serif text-amber-200/90">
          Northumbria — 1067
        </h1>
        <a
          href="/"
          className="text-sm text-stone-400 hover:text-amber-200 transition-colors"
        >
          Return to Scene
        </a>
      </header>

      {/* Map Container */}
      <main className="flex-1 flex items-center justify-center p-4">
        <div className="relative border border-stone-700 shadow-2xl rounded-lg overflow-hidden">
          <MapCanvas
            places={places}
            routes={routes}
            visibility={visibility}
            playerPosition={playerPosition}
            width={dimensions.width}
            height={dimensions.height}
            onSelectPlace={handleSelectPlace}
            onHoverPlace={handleHoverPlace}
          />
        </div>
      </main>

      {/* Selected Place Panel */}
      {selectedPlace && (
        <aside className="fixed right-4 top-20 w-80 bg-stone-900/95 border border-stone-700 rounded-lg p-4 shadow-xl">
          <div className="flex justify-between items-start mb-3">
            <h2 className="text-lg font-serif text-amber-200">
              {selectedPlace.name}
            </h2>
            <button
              onClick={() => setSelectedPlace(null)}
              className="text-stone-500 hover:text-stone-300 text-xl leading-none"
            >
              &times;
            </button>
          </div>
          <p className="text-sm text-stone-400 mb-3 capitalize">
            {selectedPlace.type}
          </p>
          {selectedPlace.detail && (
            <p className="text-sm text-stone-300 leading-relaxed">
              {selectedPlace.detail}
            </p>
          )}

          {/* Travel button */}
          {selectedPlace.id !== playerPosition && (
            <button
              className="mt-4 w-full py-2 px-4 bg-amber-900/50 hover:bg-amber-800/60
                         border border-amber-700/50 rounded text-amber-200 text-sm
                         transition-colors"
            >
              Travel to {selectedPlace.name}
            </button>
          )}
        </aside>
      )}

      {/* Legend */}
      <footer className="h-12 bg-stone-900/80 border-t border-stone-800 flex items-center justify-center gap-8 text-xs text-stone-500">
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-amber-400 rounded-full" />
          You are here
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-amber-800/70 rounded-full" />
          Familiar
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-amber-800/50 rounded-full" />
          Known
        </span>
        <span className="flex items-center gap-2">
          <span className="w-3 h-3 bg-amber-800/30 rounded-full" />
          Rumored
        </span>
      </footer>
    </div>
  );
}
