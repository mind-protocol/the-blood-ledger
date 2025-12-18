'use client';

import { useState, useMemo, useEffect } from 'react';
import { Scene, Hotspot } from '@/types/game';
import { useMoments } from '@/hooks/useMoments';
import { type Moment } from '@/lib/api';

// =============================================================================
// Reading Time Calculator
// =============================================================================

const CHAR_READ_TIME_MS = 40;
const MIN_LINE_DELAY_MS = 800;
const MAX_LINE_DELAY_MS = 4000;

function calculateReadTime(text: string): number {
  const charCount = text.length;
  const readTime = charCount * CHAR_READ_TIME_MS;
  return Math.min(Math.max(readTime, MIN_LINE_DELAY_MS), MAX_LINE_DELAY_MS);
}

// =============================================================================
// Animated Line Component
// =============================================================================

interface AnimatedLineProps {
  children: React.ReactNode;
  isVisible: boolean;
}

function AnimatedLine({ children, isVisible }: AnimatedLineProps) {
  return (
    <div
      className={`
        transform transition-all duration-1000 ease-[cubic-bezier(0.16,1,0.3,1)]
        ${isVisible
          ? 'opacity-100 translate-y-0 max-h-96'
          : 'opacity-0 translate-y-4 max-h-0 overflow-hidden'
        }
      `}
    >
      {children}
    </div>
  );
}

// =============================================================================
// Typing Indicator
// =============================================================================

function TypingIndicator() {
  return (
    <div className="py-1 flex gap-1 opacity-40">
      <span className="w-1.5 h-1.5 bg-stone-500 rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
      <span className="w-1.5 h-1.5 bg-stone-500 rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
      <span className="w-1.5 h-1.5 bg-stone-500 rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
    </div>
  );
}

// =============================================================================
// Clickable Word Component
// =============================================================================

interface ClickableWordProps {
  word: string;
  momentId: string;
  onClick: (momentId: string, word: string) => void;
  variant?: 'narration' | 'dialogue';
}

function ClickableWord({ word, momentId, onClick, variant = 'narration' }: ClickableWordProps) {
  const colorClass = variant === 'dialogue'
    ? 'text-amber-300/90 hover:text-amber-200'
    : 'text-stone-400 hover:text-amber-200';

  return (
    <button
      onClick={() => onClick(momentId, word)}
      className={`${colorClass} hover:underline decoration-amber-600/40 underline-offset-2 transition-colors cursor-pointer`}
    >
      {word}
    </button>
  );
}

// =============================================================================
// Moment Text Renderer
// =============================================================================

interface MomentTextProps {
  moment: Moment;
  onClickWord: (momentId: string, word: string) => void;
  variant?: 'narration' | 'dialogue';
}

function MomentText({ moment, onClickWord, variant = 'narration' }: MomentTextProps) {
  const tokens = moment.text.split(/(\s+)/);
  const clickableSet = new Set(moment.clickable_words || []);

  return (
    <>
      {tokens.map((token, i) => {
        const cleanToken = token.replace(/^["""']+|[.,!?"""']+$/g, '');

        if (clickableSet.has(cleanToken)) {
          const leadingMatch = token.match(/^["""']+/);
          const trailingMatch = token.match(/[.,!?"""']+$/);
          const leading = leadingMatch ? leadingMatch[0] : '';
          const trailing = trailingMatch ? trailingMatch[0] : '';

          return (
            <span key={i}>
              {leading}
              <ClickableWord
                word={cleanToken}
                momentId={moment.id}
                onClick={onClickWord}
                variant={variant}
              />
              {trailing}
            </span>
          );
        }

        return <span key={i}>{token}</span>;
      })}
    </>
  );
}

// =============================================================================
// Moment Block Component
// =============================================================================

interface MomentBlockProps {
  moment: Moment;
  onClickWord: (momentId: string, word: string) => void;
  characters?: { name: string; imageUrl?: string; icon?: string }[];
}

function MomentBlock({ moment, onClickWord, characters = [] }: MomentBlockProps) {
  const character = moment.speaker
    ? characters.find(c => c.name.toLowerCase() === moment.speaker?.toLowerCase())
    : null;

  // Dialogue moment with speaker
  if (moment.speaker || moment.type === 'dialogue') {
    return (
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full overflow-hidden border border-stone-700/50 flex-shrink-0 mt-0.5">
          {character?.imageUrl ? (
            <img
              src={character.imageUrl}
              alt={moment.speaker || 'Speaker'}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-stone-800 flex items-center justify-center text-sm">
              {character?.icon || '👤'}
            </div>
          )}
        </div>
        <div className="flex-1 min-w-0">
          {moment.speaker && (
            <span className="text-amber-200/70 text-sm font-medium">
              {moment.speaker}
            </span>
          )}
          <p className="text-stone-200 mt-0.5">
            <MomentText moment={moment} onClickWord={onClickWord} variant="dialogue" />
          </p>
        </div>
      </div>
    );
  }

  // Narration moment
  return (
    <p className="text-stone-500 leading-relaxed italic">
      <MomentText moment={moment} onClickWord={onClickWord} variant="narration" />
    </p>
  );
}

// =============================================================================
// Reveal Animation Hook
// =============================================================================

function useRevealAnimation(
  items: unknown[],
  getReadTime: (item: unknown) => number,
  resetKey: string
) {
  const [visibleCount, setVisibleCount] = useState(0);

  useEffect(() => {
    setVisibleCount(0);
  }, [resetKey]);

  useEffect(() => {
    if (visibleCount >= items.length) return;

    const delay = visibleCount === 0
      ? 300
      : getReadTime(items[visibleCount - 1]);

    const timer = setTimeout(() => {
      setVisibleCount(prev => prev + 1);
    }, delay);

    return () => clearTimeout(timer);
  }, [visibleCount, items.length, getReadTime, items]);

  return {
    visibleCount,
    isComplete: visibleCount >= items.length,
  };
}

// =============================================================================
// Center Stage Component
// =============================================================================

interface CenterStageProps {
  scene: Scene;
  people: Hotspot[];
  onEndConversation: () => void;
  playthroughId: string;
  location?: string;
  tick: number;
}

export function CenterStage({
  scene,
  people,
  onEndConversation,
  playthroughId,
  location,
  tick,
}: CenterStageProps) {
  const {
    spokenMoments,
    activeMoments,
    isLoading,
    error,
    clickWord,
    refresh,
  } = useMoments({
    playthroughId,
    location,
    tick,
  });

  const [inputValue, setInputValue] = useState('');
  const [selectedPersonId, setSelectedPersonId] = useState<string | null>(
    people.length > 0 ? people[0].id : null
  );

  const selectedPerson = people.find(p => p.id === selectedPersonId) || people[0] || null;

  // Handle word click
  const handleWordClick = (momentId: string, word: string) => {
    clickWord(momentId, word);
  };

  // Handle free text input (not implemented yet - would need API endpoint)
  const handleSubmit = () => {
    if (inputValue.trim()) {
      console.log('Free input not yet implemented:', inputValue.trim());
      setInputValue('');
    }
  };

  // Sort active moments by weight
  const sortedActiveMoments = useMemo(() => {
    return [...activeMoments].sort((a, b) => (b.weight || 0) - (a.weight || 0));
  }, [activeMoments]);

  // All moments for reveal animation
  const allMoments = useMemo(() => {
    return [...spokenMoments, ...sortedActiveMoments];
  }, [spokenMoments, sortedActiveMoments]);

  // Reveal animation
  const getReadTime = (item: unknown): number => {
    const moment = item as Moment;
    return calculateReadTime(moment.text);
  };

  const resetKey = useMemo(() => {
    return allMoments.map(m => m.id).join(',');
  }, [allMoments]);

  const { visibleCount, isComplete } = useRevealAnimation(
    allMoments,
    getReadTime,
    resetKey
  );

  // Loading state
  if (allMoments.length === 0 && !error) {
    return (
      <div className="h-full flex items-center justify-center text-stone-500">
        <TypingIndicator />
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col p-8 overflow-y-auto">
      {/* Scene header */}
      {scene && (
        <div className="mb-6 pb-4 border-b border-stone-800/50">
          <h2 className="text-amber-200/80 text-lg font-medium">{scene.name}</h2>
          {scene.atmosphere?.[0] && (
            <p className="text-stone-500 text-sm">{scene.atmosphere[0]}</p>
          )}
        </div>
      )}

      {/* Error display */}
      {error && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-800/50 rounded text-red-300 text-sm">
          {error}
          <button onClick={refresh} className="ml-2 underline">
            Retry
          </button>
        </div>
      )}

      {/* Content area */}
      <div className="flex-1 flex flex-col justify-end">
        <div className="max-w-lg mx-auto w-full space-y-4">
          {/* Moments */}
          {allMoments.map((moment, i) => {
            const isVisible = i < visibleCount;
            const isSpoken = spokenMoments.some(m => m.id === moment.id);

            return (
              <AnimatedLine key={moment.id} isVisible={isVisible}>
                <div className={isSpoken ? 'opacity-60' : ''}>
                  <MomentBlock
                    moment={moment}
                    onClickWord={handleWordClick}
                    characters={people.map(p => ({
                      name: p.name,
                      imageUrl: p.imageUrl || undefined,
                      icon: p.icon
                    }))}
                  />
                </div>
              </AnimatedLine>
            );
          })}

          {/* Typing indicator while loading */}
          {(isLoading || !isComplete) && <TypingIndicator />}

          {/* Character selection + free input */}
          {people.length > 0 && (
            <div className={`
              flex gap-4 pt-4 transition-all duration-700 ease-out
              ${isComplete ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}
            `}>
              {/* Character portraits */}
              <div className="flex flex-col gap-2 flex-shrink-0">
                {people.map((person) => (
                  <button
                    key={person.id}
                    onClick={() => setSelectedPersonId(person.id)}
                    className={`
                      flex flex-col items-center p-1 rounded-lg transition-all
                      ${selectedPersonId === person.id
                        ? 'bg-amber-900/30 ring-1 ring-amber-700/50'
                        : 'hover:bg-stone-800/50'
                      }
                    `}
                  >
                    <div className={`
                      w-16 h-16 rounded-full overflow-hidden border-2 shadow-lg transition-all
                      ${selectedPersonId === person.id
                        ? 'border-amber-600/70'
                        : 'border-stone-700/50'
                      }
                    `}>
                      {person.imageUrl ? (
                        <img
                          src={person.imageUrl}
                          alt={person.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full bg-stone-800 flex items-center justify-center text-2xl">
                          {person.icon}
                        </div>
                      )}
                    </div>
                    <span className={`
                      text-xs mt-1 transition-colors
                      ${selectedPersonId === person.id
                        ? 'text-amber-200/90'
                        : 'text-stone-500'
                      }
                    `}>
                      {person.name}
                    </span>
                  </button>
                ))}
              </div>

              {/* Input area */}
              <div className="flex-1 flex flex-col justify-end">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit();
                    }
                  }}
                  placeholder={selectedPerson ? `Say something to ${selectedPerson.name}...` : 'Say something...'}
                  rows={3}
                  className="w-full bg-transparent border border-stone-700/30 focus:border-amber-700/50 rounded-lg text-stone-300 placeholder-stone-600 p-3 outline-none transition-colors resize-none"
                  style={{ minHeight: '80px' }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
