'use client';

import { Scene } from '@/types/game';

interface SceneHeaderProps {
  scene: Scene;
}

export function SceneHeader({ scene }: SceneHeaderProps) {
  const timeDisplay = {
    DAWN: 'Dawn',
    DAY: 'Day',
    DUSK: 'Dusk',
    NIGHT: 'Night',
  };

  const weatherDisplay = {
    CLEAR: '',
    CLOUDY: 'Overcast',
    RAIN: 'Rain',
    STORM: 'Storm',
    FOG: 'Fog',
    SNOW: 'Snow',
  };

  const weatherText = weatherDisplay[scene.weather];
  const timeText = timeDisplay[scene.timeOfDay];
  const conditionText = weatherText ? `${weatherText} · ${timeText}` : timeText;

  return (
    <div className="flex items-center justify-between px-4 py-2 border-b border-stone-700">
      <h1 className="text-xl font-serif font-bold text-amber-100 tracking-wide">
        {scene.name}
      </h1>
      <div className="flex items-center gap-2 text-sm text-stone-400">
        <span>{scene.location}</span>
        <span className="text-stone-600">·</span>
        <span className="text-amber-200/70">[{conditionText}]</span>
      </div>
    </div>
  );
}
