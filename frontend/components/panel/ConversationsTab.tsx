'use client';

import { Conversation } from '@/types/game';

interface ConversationsTabProps {
  conversations: Conversation[];
  onSelectConversation: (conversationId: string) => void;
}

export function ConversationsTab({ conversations, onSelectConversation }: ConversationsTabProps) {
  const activeConversation = conversations.find((c) => c.isActive);
  const pastConversations = conversations.filter((c) => !c.isActive);

  return (
    <div className="h-full overflow-y-auto">
      {/* Header */}
      <div className="sticky top-0 bg-stone-900/95 border-b border-stone-700 px-3 py-2">
        <h3 className="text-sm font-bold text-amber-200">Conversations</h3>
      </div>

      <div className="p-3 space-y-4">
        {/* Active conversation */}
        {activeConversation && (
          <div className="space-y-2">
            <div className="text-xs font-bold text-amber-500/70 uppercase tracking-wider">
              Now Speaking
            </div>
            <div className="bg-stone-800/50 rounded-lg p-3 border border-amber-700/30">
              <div className="text-sm font-bold text-amber-100 mb-2">
                {activeConversation.characterName}
              </div>
              <div className="space-y-2">
                {activeConversation.messages.slice(-4).map((msg) => (
                  <div
                    key={msg.id}
                    className={`text-sm ${msg.speaker === 'player' ? 'text-stone-400' : 'text-stone-200'}`}
                  >
                    <span className={`font-bold ${msg.speaker === 'player' ? 'text-stone-500' : 'text-amber-400'}`}>
                      {msg.speaker === 'player' ? 'You' : msg.speaker}:
                    </span>{' '}
                    {msg.content}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Past conversations */}
        {pastConversations.length > 0 && (
          <div className="space-y-2">
            <div className="text-xs font-bold text-stone-500 uppercase tracking-wider">
              Recent
            </div>
            {pastConversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => onSelectConversation(conv.id)}
                className="w-full text-left bg-stone-800/30 hover:bg-stone-800/50 rounded-lg p-2 transition-colors"
              >
                <div className="text-sm font-medium text-stone-300">
                  {conv.characterName}
                </div>
                <div className="text-xs text-stone-500 truncate">
                  {conv.messages[conv.messages.length - 1]?.content || 'No messages'}
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Empty state */}
        {conversations.length === 0 && (
          <div className="text-sm text-stone-500 italic text-center py-4">
            No conversations yet.
          </div>
        )}
      </div>
    </div>
  );
}
