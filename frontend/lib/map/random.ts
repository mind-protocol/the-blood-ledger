// DOCS: docs/frontend/map/PATTERNS_Parchment_Map_View.md
/**
 * Seeded random utilities for consistent "hand-drawn" appearance
 */

/**
 * Linear congruential generator
 * Returns a function that produces deterministic "random" values
 */
export function seededRandom(seed: number): () => number {
  let state = seed;
  return function () {
    state = (state * 1103515245 + 12345) & 0x7fffffff;
    return state / 0x7fffffff;
  };
}

/**
 * Simple string hash for seed generation
 */
export function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}
