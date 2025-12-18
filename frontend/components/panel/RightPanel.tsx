'use client';

import { useState } from 'react';
import { ChronicleEntry, Conversation, LedgerEntry, Player } from '@/types/game';
import { ChronicleTab } from './ChronicleTab';
import { ConversationsTab } from './ConversationsTab';
import { LedgerTab } from './LedgerTab';

type TabType = 'chronicle' | 'conversations' | 'ledger';

interface RightPanelProps {
  player: Player;
  chronicle: ChronicleEntry[];
  conversations: Conversation[];
  ledger: LedgerEntry[];
  onSelectConversation: (conversationId: string) => void;
}

export function RightPanel({
  player,
  chronicle,
  conversations,
  ledger,
  onSelectConversation,
}: RightPanelProps) {
  const [activeTab, setActiveTab] = useState<TabType>('chronicle');

  const tabs: { id: TabType; label: string; shortLabel: string }[] = [
    { id: 'chronicle', label: 'Chronicle', shortLabel: 'CHRON' },
    { id: 'conversations', label: 'Conversations', shortLabel: 'TALK' },
    { id: 'ledger', label: 'Ledger', shortLabel: 'LEDG' },
  ];

  return (
    <div className="h-full flex flex-col bg-stone-900 border-l border-stone-700">
      {/* Tabs */}
      <div className="flex border-b border-stone-700">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`
              flex-1 px-2 py-2 text-xs font-bold uppercase tracking-wider
              transition-colors
              ${activeTab === tab.id
                ? 'bg-stone-800 text-amber-200 border-b-2 border-amber-500'
                : 'text-stone-500 hover:text-stone-300 hover:bg-stone-800/50'
              }
            `}
          >
            {tab.shortLabel}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'chronicle' && (
          <ChronicleTab entries={chronicle} player={player} />
        )}
        {activeTab === 'conversations' && (
          <ConversationsTab
            conversations={conversations}
            onSelectConversation={onSelectConversation}
          />
        )}
        {activeTab === 'ledger' && <LedgerTab entries={ledger} />}
      </div>
    </div>
  );
}
