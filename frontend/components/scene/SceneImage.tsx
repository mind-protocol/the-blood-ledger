'use client';

import { useState } from 'react';
import { Scene } from '@/types/game';
import { Hotspot } from './Hotspot';

// Pre-computed star positions to avoid hydration mismatch
const STAR_POSITIONS = [
  { x: 12, y: 8, delay: 0.2 },
  { x: 28, y: 15, delay: 1.1 },
  { x: 45, y: 5, delay: 0.7 },
  { x: 62, y: 22, delay: 1.5 },
  { x: 78, y: 12, delay: 0.3 },
  { x: 91, y: 28, delay: 1.8 },
  { x: 8, y: 32, delay: 0.9 },
  { x: 35, y: 25, delay: 1.3 },
  { x: 55, y: 18, delay: 0.5 },
  { x: 72, y: 35, delay: 1.7 },
  { x: 88, y: 8, delay: 0.1 },
  { x: 15, y: 20, delay: 1.4 },
  { x: 42, y: 30, delay: 0.6 },
  { x: 68, y: 10, delay: 1.2 },
  { x: 82, y: 25, delay: 0.4 },
  { x: 5, y: 15, delay: 1.6 },
  { x: 25, y: 38, delay: 0.8 },
  { x: 50, y: 12, delay: 1.0 },
  { x: 75, y: 30, delay: 1.9 },
  { x: 95, y: 18, delay: 0.2 },
];

interface SceneImageProps {
  scene: Scene;
  onHotspotAction: (hotspotId: string, actionId: string) => void;
}

export function SceneImage({ scene, onHotspotAction }: SceneImageProps) {
  const [selectedHotspot, setSelectedHotspot] = useState<string | null>(null);

  // Background gradients based on time of day
  const timeBackgrounds = {
    DAWN: 'from-indigo-900 via-rose-900/30 to-amber-900/20',
    DAY: 'from-sky-900 via-stone-800 to-stone-900',
    DUSK: 'from-orange-900/40 via-purple-900/30 to-stone-900',
    NIGHT: 'from-slate-950 via-stone-900 to-slate-950',
  };

  const handleBackgroundClick = () => {
    setSelectedHotspot(null);
  };

  return (
    <div
      className={`
        relative w-full aspect-[16/9] rounded-lg overflow-hidden
        bg-gradient-to-b ${timeBackgrounds[scene.timeOfDay]}
        border border-stone-700/50
      `}
      onClick={handleBackgroundClick}
    >
      {/* Atmospheric overlay */}
      <div className="absolute inset-0 bg-[url('/noise.png')] opacity-5" />

      {/* Stars for night - deterministic positions */}
      {scene.timeOfDay === 'NIGHT' && (
        <div className="absolute inset-0">
          {STAR_POSITIONS.map((star, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white/60 rounded-full animate-pulse"
              style={{
                left: `${star.x}%`,
                top: `${star.y}%`,
                animationDelay: `${star.delay}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Ground/horizon line */}
      <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-stone-950/80 to-transparent" />

      {/* Hotspots */}
      {scene.hotspots.map((hotspot) => (
        <Hotspot
          key={hotspot.id}
          hotspot={hotspot}
          onAction={onHotspotAction}
          isSelected={selectedHotspot === hotspot.id}
          onSelect={(id) => {
            setSelectedHotspot(id);
          }}
        />
      ))}

      {/* Scene type indicator */}
      <div className="absolute top-3 left-3 px-2 py-1 bg-stone-900/60 rounded text-xs text-stone-400 font-mono">
        {scene.type}
      </div>
    </div>
  );
}
