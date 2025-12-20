# BEHAVIORS: Retention Mechanisms

## Observable Effects

This document describes the design features and system responses intended to drive long-term player retention in Blood Ledger, addressing the "Month 2 Problem" where novelty might wear off. The game aims for extended engagement by creating deep personal investment and offering continuous discovery.

## Retention Mechanism 1: The Growing Graph

*   **Behavior:** As a player invests time, their personal "Graph" of relationships, events, and lore expands significantly. This graph is treated as a unique, valuable asset built by the player.
*   **System Response:** The game displays the increasing complexity and detail of this graph (e.g., from 50 nodes to 3,000+ nodes, encompassing regional history, political factions, and multi-generational family trees).
*   **Player Psychology:** Leaving the game means abandoning this highly personalized and detailed world-state, akin to a sunk cost, making retention significantly higher.

## Retention Mechanism 2: The Chronicle Promise

*   **Behavior:** Every hour of gameplay contributes to the player's eventual "Life Chronicle" (a death/ending montage).
*   **System Response:** The game implicitly and explicitly links continued play to the richness and length of this ultimate narrative artifact.
*   **Player Psychology:** Players are motivated to continue playing to see what their full "Life Chronicle" will look like after many hours, or how their character will ultimately die, creating a goal they build towards from minute one.

## Retention Mechanism 3: The Multi-Life Model

*   **Behavior:** Upon character death or story completion, players can start a new life in the *same persistent world*, often as a descendant.
*   **System Response:** The world remembers previous lives. NPCs react based on the legacy of previous characters, and past actions (lies, debts) become starting conditions for the new playthrough.
*   **Player Psychology:** Each life offers a fresh perspective and new challenges within an evolving, familiar world, providing infinite replayability and continuous discovery.

## Retention Mechanism 4: The "Missed Events" Drive

*   **Behavior:** Chronicles (especially Life Chronicles) reveal significant off-screen events that occurred during the player's absence or in parallel.
*   **System Response:** The game uses these revelations to demonstrate the world's persistence and complexity.
*   **Player Psychology:** This generates curiosity and a desire to explore more, understand what else was missed, and engage more deeply with the world.

## Churn Prevention Triggers

The system monitors player behavior and intervenes with targeted nudges to prevent churn.

| Signal | Detection | Intervention |
|--------|-----------|--------------|
| Session frequency drops | <2 sessions in 7 days | Email: "The world moved while you were away. Wulfric made a decision." |
| Average session shortens | <20 mins for 3 sessions | In-game: Voice whispers something intriguing they haven't explored |
| Graph exploration slows | Same 5 NPCs for 10 sessions | Introduce mystery: "A stranger arrived asking about you by name." |
| Payment declines | CC failed | 7-day grace period, "read-only" mode, save their world |

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Whale_Economics.md
ALGORITHM:       ./ALGORITHM_Semantic_Cache.md
ALGORITHM:       ./ALGORITHM_Hallucination_Defense.md
ALGORITHM:       ./ALGORITHM_World_Scavenger.md
BEHAVIORS:       ./BEHAVIORS_Conversion_Funnel_And_Ledger_Lock.md
PATTERNS:        ./PATTERNS_Market_Comparison.md
THIS:            ./BEHAVIORS_Retention_Mechanisms.md
SYNC:            ./SYNC_Business_Model.md
