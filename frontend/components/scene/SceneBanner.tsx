'use client';

import { useState, useEffect } from 'react';
import { Scene } from '@/types/game';

interface SceneBannerProps {
  scene: Scene;
}

// Fallback gradient styles when no image is available
const getFallbackStyle = (type: string) => {
  const baseStyles: Record<string, string> = {
    CAMP: 'from-stone-900 via-amber-950/20 to-stone-950',
    ROAD: 'from-slate-800 via-stone-800 to-slate-900',
    HALL: 'from-amber-950/40 via-stone-900 to-stone-950',
    HOLD: 'from-slate-900 via-stone-800 to-slate-950',
    VILLAGE: 'from-emerald-950/30 via-stone-900 to-stone-950',
    FOREST: 'from-emerald-950/40 via-stone-900 to-emerald-950/20',
    CHURCH: 'from-indigo-950/30 via-stone-900 to-stone-950',
    BATTLEFIELD: 'from-red-950/30 via-stone-900 to-stone-950',
    TAVERN: 'from-amber-900/30 via-stone-900 to-stone-950',
    GATE: 'from-slate-800 via-stone-800 to-slate-900',
  };
  return baseStyles[type] || baseStyles.ROAD;
};

export function SceneBanner({ scene }: SceneBannerProps) {
  const [cacheBuster, setCacheBuster] = useState('');

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      setCacheBuster(scene.bannerImage ? `?t=${Date.now()}` : '');
    });

    return () => cancelAnimationFrame(raf);
  }, [scene.bannerImage]);

  const hasBannerImage = scene.bannerImage && scene.bannerImage.length > 0;

  if (hasBannerImage) {
    return (
      <div className="relative w-full aspect-[3/1] overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`${scene.bannerImage}${cacheBuster}`}
          alt={scene.name}
          className="absolute inset-0 w-full h-full object-cover"
        />
        {/* Subtle vignette overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-stone-950/60 via-transparent to-stone-950/20" />
        {/* Location label */}
        <div className="absolute bottom-2 left-3 text-xs text-stone-400 font-mono drop-shadow-lg">
          {scene.type}
        </div>
      </div>
    );
  }

  // Fallback to gradient background
  const gradientStyle = getFallbackStyle(scene.type);

  return (
    <div className={`relative w-full aspect-[3/1] bg-gradient-to-br ${gradientStyle} overflow-hidden`}>
      {/* Vignette */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-stone-950/50" />
      {/* Location label */}
      <div className="absolute bottom-2 left-3 text-xs text-stone-500 font-mono">
        {scene.type}
      </div>
    </div>
  );
}
