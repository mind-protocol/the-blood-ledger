# PATTERNS: Whale Economics

## Why This Design Exists

This document outlines the core economic model of Blood Ledger, centered on "Whale Economics." The simulation is free, but monetization occurs when players choose to preserve their unique narrative "Moments." This model is designed for high average revenue per user (ARPU) and long-term sustainability by leveraging the intrinsic value of player-generated history.

## The Core Insight: Simulation Is Free

The foundational premise is that the game's simulation engine (`tick.py`) operates at **zero API cost**. The complex interplay of graph nodes, tensions, and energy propagation is pure computation, costing nothing. Monetary expenditure is only incurred by the generation of "prose" – the LLM-driven creation of narrative "Moments."

## Cost Per Moment Type

The cost of generating narrative content varies by "Moment Type," reflecting the complexity and LLM token usage.

| Moment Type | Input Tokens | Output Tokens | Cost (Sonnet) | Frequency | Margin @ $0.04 |
|-------------|--------------|---------------|---------------|-----------|----------------|
| **Simple Dialogue** | ~800 | ~150 | $0.0047 | 70% | **88%** |
| **Action/Scene** | ~1,200 | ~250 | $0.0074 | 20% | **81%** |
| **World Building** (Grandmother) | ~2,500 | ~400 | $0.0135 | 8% | **66%** |
| **Major Event** (Flip) | ~3,000 | ~600 | $0.0180 | 2% | **55%** |

*   **Weighted Average Cost:** $0.0062/Moment
*   **Weighted Average Margin:** **84%**

This structure ensures robust margins even with varied player engagement patterns. Expensive WorldBuilder queries are rare but generate permanent, reusable content, while frequent dialogue moments are cheap.

## The "Grandmother Query" Economics

A "Grandmother Query" (e.g., player asking about an NPC's family history) is initially expensive ($0.0135). However, this content is then cached permanently within the game's graph. Future references to this newly established lore cost significantly less (approx. $0.005), making the initial investment highly valuable for narrative depth and consistency.

## The "Nothing Happening" Subsidy

When a player is AFK, the simulation continues to run for free. The game world evolves, NPCs change beliefs, and tensions grow, all without incurring LLM costs. Upon returning, the player encounters a dynamic world with new events, reinforcing the "The world moved" sensation at no additional direct cost to the game's operations. This creates a significant "moat" by providing rich, emergent gameplay for free.

## Margin Defense Table

The business model maintains strong profitability across all player types, from "Tourists" to "Whales."

| Scenario | Player Behavior | Our Cost | Revenue | Margin |
|----------|-----------------|----------|---------|--------|
| **Tourist** | 300 Moments, mostly dialogue | $1.86 | $12.00 | 84% |
| **Regular** | 1,500 Moments, some worldbuilding | $10.50 | $60.00 | 82% |
| **Passionate** | 5,000 Moments, heavy exploration | $40.00 | $200.00 | 80% |
| **Whale** | 15,000 Moments, exhaustive | $135.00 | $600.00 | 77% |

While the percentage margin slightly decreases for "Whales" (who engage in more expensive, complex queries), the absolute profit generated increases massively (e.g., $465 profit from a whale vs. $10 from a tourist).

## Worst-Case Stress Test

Even under an adversarial scenario where a player constantly spams expensive WorldBuilder queries, the model remains profitable. This is mitigated by the permanent caching of generated content; after initial generation, subsequent queries hit the cache at zero cost.

## Maturity

STATUS: CANONICAL

---

## CHAIN

ALGORITHM:       ./ALGORITHM_Semantic_Cache.md
ALGORITHM:       ./ALGORITHM_Hallucination_Defense.md
ALGORITHM:       ./ALGORITHM_World_Scavenger.md
BEHAVIORS:       ./BEHAVIORS_Conversion_Funnel_And_Ledger_Lock.md
BEHAVIORS:       ./BEHAVIORS_Retention_Mechanisms.md
PATTERNS:        ./PATTERNS_Market_Comparison.md
THIS:            ./PATTERNS_Whale_Economics.md
SYNC:            ./SYNC_Business_Model.md