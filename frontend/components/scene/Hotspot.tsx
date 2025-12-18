'use client';

import { useState } from 'react';
import { Hotspot as HotspotType, HotspotAction } from '@/types/game';

interface HotspotProps {
  hotspot: HotspotType;
  onAction: (hotspotId: string, actionId: string) => void;
  isSelected: boolean;
  onSelect: (hotspotId: string | null) => void;
}

export function Hotspot({ hotspot, onAction, isSelected, onSelect }: HotspotProps) {
  const handleClick = () => {
    onSelect(isSelected ? null : hotspot.id);
  };

  const handleAction = (action: HotspotAction) => {
    onAction(hotspot.id, action.id);
    onSelect(null);
  };

  return (
    <div
      className="absolute transform -translate-x-1/2 -translate-y-1/2"
      style={{
        left: `${hotspot.position.x}%`,
        top: `${hotspot.position.y}%`,
      }}
    >
      {/* Hotspot marker */}
      <button
        onClick={handleClick}
        className={`
          relative flex flex-col items-center gap-1 p-2 rounded-lg
          transition-all duration-200 cursor-pointer
          ${isSelected
            ? 'bg-amber-900/60 ring-2 ring-amber-500/50'
            : 'bg-stone-900/40 hover:bg-stone-800/60'
          }
        `}
      >
        <span className="text-2xl">{hotspot.icon}</span>
        <span className="text-xs text-amber-100/80 whitespace-nowrap">
          {hotspot.name}
        </span>
      </button>

      {/* Action dropdown */}
      {isSelected && (
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 z-20">
          <div className="bg-stone-900/95 border border-stone-700 rounded-lg shadow-xl overflow-hidden min-w-[160px]">
            <div className="px-3 py-2 border-b border-stone-700">
              <p className="text-xs text-stone-400">{hotspot.description}</p>
            </div>
            <div className="py-1">
              {hotspot.actions.map((action) => (
                <button
                  key={action.id}
                  onClick={() => handleAction(action)}
                  className="w-full px-3 py-2 text-left text-sm text-amber-100 hover:bg-amber-900/40 transition-colors"
                >
                  <span className="text-amber-400">↳</span> {action.label}
                  {action.description && (
                    <span className="block text-xs text-stone-500 mt-0.5">
                      {action.description}
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
