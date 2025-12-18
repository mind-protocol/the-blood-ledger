'use client';

import { SceneAction } from '@/types/game';

interface SceneActionsProps {
  actions: SceneAction[];
  onAction: (actionId: string) => void;
}

export function SceneActions({ actions, onAction }: SceneActionsProps) {
  return (
    <div className="px-4 py-3 flex flex-wrap gap-2">
      {actions.map((action) => (
        <button
          key={action.id}
          onClick={() => onAction(action.id)}
          className="
            px-4 py-2
            bg-stone-800/80 hover:bg-amber-900/50
            border border-stone-600 hover:border-amber-700
            rounded-md
            text-sm text-amber-100
            transition-all duration-200
            hover:shadow-lg hover:shadow-amber-900/20
          "
          title={action.description}
        >
          [ {action.label} ]
        </button>
      ))}
    </div>
  );
}
