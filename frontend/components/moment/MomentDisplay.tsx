'use client';

import type { Moment } from '@/types/moment';
import { ClickableText } from './ClickableText';

/**
 * Props for MomentDisplay component.
 */
interface MomentDisplayProps {
  /** The moment to display */
  moment: Moment;
  /** Called when a clickable word is clicked */
  onWordClick?: (word: string) => void;
  /** Is this the latest moment (for animation) */
  isLatest?: boolean;
  /** Show debug info (weight, status) */
  showDebug?: boolean;
}

/** Derive character image path from speaker name */
function getCharacterImageUrl(speaker: string): string {
  const charId = `char_${speaker.toLowerCase().replace(/\s+/g, '_')}`;
  return `/playthroughs/default/images/characters/${charId}.png`;
}

/**
 * Renders a single moment with appropriate styling.
 *
 * Different rendering for:
 * - narration: Italicized, muted color
 * - dialogue: Quoted, with speaker name
 * - player_*: Player's actions/words, amber color
 * - hint: Subtle, smaller text
 *
 * Tone affects color:
 * - bitter/cold: Cool gray
 * - warm/hopeful: Warm amber
 * - defiant/righteous: Bold
 *
 * @example
 * <MomentDisplay
 *   moment={{
 *     id: "moment_1",
 *     text: "Aldric looks at you with cold eyes.",
 *     type: "narration",
 *     status: "active",
 *     weight: 0.8,
 *     tone: "cold",
 *     clickable_words: ["cold", "eyes"]
 *   }}
 *   onWordClick={(word) => handleClick(moment.id, word)}
 * />
 */
export function MomentDisplay({
  moment,
  onWordClick,
  isLatest = false,
  showDebug = false,
}: MomentDisplayProps) {
  const { type, text, speaker, tone, clickable_words, status, weight } = moment;

  // Derive image URL from speaker name
  const imageUrl = speaker ? getCharacterImageUrl(speaker) : null;

  // Determine base styling by type
  const getTypeStyles = () => {
    switch (type) {
      case 'dialogue':
        return 'text-stone-200';
      case 'narration':
        return 'text-stone-400 italic';
      case 'hint':
        return 'text-stone-500 text-sm italic';
      case 'player_click':
      case 'player_freeform':
      case 'player_choice':
        return 'text-amber-100/80';
      case 'action':
        return 'text-stone-300';
      case 'thought':
        return 'text-stone-400 italic opacity-80';
      default:
        return 'text-stone-300';
    }
  };

  // Adjust by tone
  const getToneStyles = () => {
    switch (tone) {
      case 'bitter':
      case 'cold':
        return 'text-slate-300';
      case 'warm':
      case 'hopeful':
        return 'text-amber-200/90';
      case 'defiant':
      case 'righteous':
        return 'font-medium';
      case 'wounded':
      case 'mournful':
        return 'opacity-90';
      case 'guarded':
        return 'opacity-95';
      default:
        return '';
    }
  };

  // Animation for latest moment
  const getAnimationClass = () => {
    if (!isLatest) return '';
    return 'animate-fadeIn';
  };

  // Status badge (for debug)
  const getStatusBadge = () => {
    if (!showDebug) return null;

    const colors = {
      possible: 'bg-blue-500/20 text-blue-300',
      active: 'bg-amber-500/20 text-amber-300',
      spoken: 'bg-green-500/20 text-green-300',
      dormant: 'bg-purple-500/20 text-purple-300',
      decayed: 'bg-stone-500/20 text-stone-400',
    };

    return (
      <span className={`text-xs px-1.5 py-0.5 rounded ${colors[status]}`}>
        {status} ({(weight * 100).toFixed(0)}%)
      </span>
    );
  };

  // Render text with clickable words if interactive
  const renderText = () => {
    if (clickable_words.length > 0 && onWordClick && status === 'active') {
      return (
        <ClickableText
          text={text}
          clickableWords={clickable_words}
          onWordClick={onWordClick}
        />
      );
    }
    return <span>{text}</span>;
  };

  return (
    <div
      className={`
        ${getTypeStyles()}
        ${getToneStyles()}
        ${getAnimationClass()}
        leading-relaxed
      `}
    >
      {showDebug && (
        <div className="flex items-center gap-2 mb-1">
          {getStatusBadge()}
          {tone && (
            <span className="text-xs text-stone-500">
              tone: {tone}
            </span>
          )}
        </div>
      )}

      {type === 'dialogue' && speaker ? (
        <div className="flex items-start gap-3">
          {/* Character avatar */}
          <div className="w-8 h-8 rounded-full overflow-hidden border border-stone-700/50 flex-shrink-0 mt-0.5 bg-stone-800">
            <img
              src={imageUrl!}
              alt={speaker}
              className="w-full h-full object-cover"
              onError={(e) => {
                // Hide broken image, show fallback
                e.currentTarget.style.display = 'none';
              }}
            />
          </div>
          {/* Speaker name and text */}
          <div className="flex-1 min-w-0">
            <span className="text-amber-200/70 text-sm font-medium">
              {speaker}
            </span>
            <p className="text-stone-200 mt-0.5">
              &ldquo;{renderText()}&rdquo;
            </p>
          </div>
        </div>
      ) : type.startsWith('player_') ? (
        <span className="text-yellow-300 italic text-lg">&ldquo;{renderText()}&rdquo;</span>
      ) : (
        renderText()
      )}
    </div>
  );
}

export default MomentDisplay;
