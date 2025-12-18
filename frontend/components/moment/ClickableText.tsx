'use client';

import { useMemo, useCallback } from 'react';

/**
 * Props for ClickableText component.
 */
interface ClickableTextProps {
  /** The text to render */
  text: string;
  /** Words that should be clickable (case-insensitive matching) */
  clickableWords: string[];
  /** Called when a clickable word is clicked */
  onWordClick: (word: string) => void;
  /** Disable clicks (e.g., during traversal) */
  disabled?: boolean;
  /** Additional class names */
  className?: string;
}

/**
 * Renders text with clickable words highlighted.
 *
 * Words in `clickableWords` are rendered as interactive spans
 * with visual feedback (underline, hover glow, cursor pointer).
 *
 * @example
 * <ClickableText
 *   text="Aldric's eyes darken when you mention Edmund's name."
 *   clickableWords={["Edmund", "eyes", "name"]}
 *   onWordClick={(word) => handleClick(word)}
 * />
 */
export function ClickableText({
  text,
  clickableWords,
  onWordClick,
  disabled = false,
  className = '',
}: ClickableTextProps) {
  // Build regex for matching clickable words
  const wordPattern = useMemo(() => {
    if (clickableWords.length === 0) return null;

    // Escape special regex characters and join with |
    const escaped = clickableWords.map(w =>
      w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    );
    // Match whole words only (with word boundaries)
    return new RegExp(`\\b(${escaped.join('|')})\\b`, 'gi');
  }, [clickableWords]);

  // Split text into segments (clickable and non-clickable)
  const segments = useMemo(() => {
    if (!wordPattern) {
      return [{ text, clickable: false }];
    }

    const result: Array<{ text: string; clickable: boolean; word?: string }> = [];
    let lastIndex = 0;

    // Find all matches
    let match;
    while ((match = wordPattern.exec(text)) !== null) {
      // Add text before match
      if (match.index > lastIndex) {
        result.push({
          text: text.slice(lastIndex, match.index),
          clickable: false,
        });
      }

      // Add the match
      result.push({
        text: match[0],
        clickable: true,
        word: match[0],
      });

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      result.push({
        text: text.slice(lastIndex),
        clickable: false,
      });
    }

    return result;
  }, [text, wordPattern]);

  // Handle click on a word
  const handleClick = useCallback(
    (word: string) => {
      if (!disabled) {
        onWordClick(word);
      }
    },
    [disabled, onWordClick]
  );

  return (
    <span className={className}>
      {segments.map((segment, index) =>
        segment.clickable ? (
          <span
            key={index}
            onClick={() => handleClick(segment.word!)}
            className={`
              text-amber-200 underline decoration-amber-400/50 underline-offset-2
              cursor-pointer transition-all duration-150
              ${disabled
                ? 'opacity-50 cursor-not-allowed'
                : 'hover:text-amber-100 hover:decoration-amber-300 hover:shadow-[0_0_8px_rgba(217,119,6,0.3)]'
              }
            `}
            role="button"
            tabIndex={disabled ? -1 : 0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                handleClick(segment.word!);
              }
            }}
          >
            {segment.text}
          </span>
        ) : (
          <span key={index}>{segment.text}</span>
        )
      )}
    </span>
  );
}

export default ClickableText;
