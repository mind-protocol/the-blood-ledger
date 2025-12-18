'use client';

import { Scene } from '@/types/game';

interface SettingStripProps {
  scene: Scene;
}

export function SettingStrip({ scene }: SettingStripProps) {
  // Use bannerImage if set, otherwise infer from place ID
  const imageUrl = scene.bannerImage || (scene.placeId ? `/playthroughs/default/images/places/${scene.placeId}.png` : null);

  return (
    <div className="h-full relative overflow-hidden">
      {/* Background image - cropped tall */}
      {imageUrl && (
        <img
          src={imageUrl}
          alt={scene.name}
          className="absolute inset-0 w-full h-full object-cover"
          style={{ objectPosition: 'center' }}
          onError={(e) => {
            // Hide image on error, show gradient fallback
            e.currentTarget.style.display = 'none';
          }}
        />
      )}
      {/* Gradient fallback (always rendered behind image) */}
      <div className="absolute inset-0 bg-gradient-to-b from-stone-800 via-stone-900 to-stone-950 -z-10" />

      {/* Gradient overlays for atmosphere */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent to-stone-950/60" />
      <div className="absolute inset-0 bg-gradient-to-t from-stone-950/80 via-transparent to-stone-950/40" />

      {/* Scene info at bottom */}
      <div className="absolute bottom-0 left-0 right-0 p-4">
        <h1 className="text-lg font-semibold text-amber-100 drop-shadow-lg">
          {scene.name}
        </h1>
        <p className="text-xs text-stone-300 mt-1 drop-shadow">
          {scene.location}
        </p>
        <p className="text-xs text-stone-400 drop-shadow">
          {scene.timeOfDay.toLowerCase()}
        </p>
      </div>

      {/* Atmosphere text - subtle */}
      <div className="absolute top-4 left-4 right-4">
        {scene.atmosphere.slice(0, 2).map((line, i) => (
          <p
            key={i}
            className="text-xs text-stone-400/70 italic leading-relaxed drop-shadow"
          >
            {line}
          </p>
        ))}
      </div>
    </div>
  );
}
