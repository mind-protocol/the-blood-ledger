'use client';

import { LedgerEntry } from '@/types/game';

interface LedgerTabProps {
  entries: LedgerEntry[];
}

export function LedgerTab({ entries }: LedgerTabProps) {
  const debts = entries.filter((e) => e.type === 'debt' && !e.resolved);
  const oaths = entries.filter((e) => e.type === 'oath' && !e.resolved);
  const blood = entries.filter((e) => e.type === 'blood' && !e.resolved);

  const typeStyles = {
    debt: { icon: '⚖️', color: 'text-red-400', borderColor: 'border-red-900/50' },
    oath: { icon: '🤝', color: 'text-amber-400', borderColor: 'border-amber-900/50' },
    blood: { icon: '🩸', color: 'text-rose-500', borderColor: 'border-rose-900/50' },
  };

  const renderSection = (title: string, items: LedgerEntry[], type: 'debt' | 'oath' | 'blood') => {
    if (items.length === 0) return null;
    const style = typeStyles[type];

    return (
      <div className="space-y-2">
        <div className={`text-xs font-bold uppercase tracking-wider ${style.color}`}>
          {style.icon} {title}
        </div>
        {items.map((entry) => (
          <div
            key={entry.id}
            className={`text-sm bg-stone-800/30 rounded p-2 border-l-2 ${style.borderColor}`}
          >
            <div className="font-medium text-stone-200">{entry.subject}</div>
            <div className="text-stone-400 text-xs mt-1">{entry.content}</div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="h-full overflow-y-auto">
      {/* Header */}
      <div className="sticky top-0 bg-stone-900/95 border-b border-stone-700 px-3 py-2">
        <h3 className="text-sm font-bold text-amber-200">The Blood Ledger</h3>
        <p className="text-xs text-stone-500">What&apos;s owed. What&apos;s sworn. What&apos;s blood.</p>
      </div>

      {/* Content */}
      <div className="p-3 space-y-4">
        {renderSection('Debts', debts, 'debt')}
        {renderSection('Oaths', oaths, 'oath')}
        {renderSection('Blood', blood, 'blood')}

        {entries.length === 0 && (
          <div className="text-sm text-stone-500 italic text-center py-4">
            The ledger is empty.
          </div>
        )}
      </div>
    </div>
  );
}
