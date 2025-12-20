# PATTERNS: Market Comparison

## Why This Design Exists

This document positions Blood Ledger within the broader market, arguing that it is not a traditional video game but rather a novel type of interactive service. This redefinition is crucial for understanding its unique value proposition, business model, and potential for high Lifetime Value (LTV).

## Not a Game, a Service

Blood Ledger deliberately avoids direct comparison with traditional single-player games like Baldur's Gate 3. Its model is fundamentally different:

| Aspect | BG3 Model | Blood Ledger Model |
|--------|-----------|--------------------|
| Cost | $60 upfront | $0 upfront |
| Content | 100 hours of authored content | Infinite hours of emergent content |
| Play State | Done when finished | Never done |

## Strategic Market Comparisons

### 1. Professional Dungeon Master (DM)
Blood Ledger is best compared to a personalized, professional Dungeon Master, offering a bespoke narrative experience at a fraction of the cost and with infinite availability.

| Service | Cost | What You Get |
|---------|------|--------------|
| Pro DM (in-person) | $20-50/session | Personalized story, 3-4 hours |
| Pro DM (online) | $15-30/session | Same, via Roll20 |
| **Blood Ledger** | **~$5-10/session** | Personalized story, infinite availability |

### 2. AI Character/Companion Services (Character.AI / Replika)
While featuring AI-driven interaction, Blood Ledger offers a significantly richer, world-bound experience than simple AI chatbots, leading to higher ARPU.

| Service | Model | Monthly Revenue/User |
|---------|-------|---------------------|
| Character.AI | $10/month subscription | $10 |
| Replika Pro | $20/month subscription | $20 |
| **Blood Ledger** | PAYG, whale-focused | **$84 ARPU** |

### 3. OnlyFans (Parasocial Economics)
This unconventional comparison highlights Blood Ledger's ability to monetize deep player attachment to fictional entities through narrative payoff, similar to how OnlyFans monetizes parasocial relationships. Players pay for:
*   The feeling of being "known" by characters.
*   Personal consequences for their choices.
*   A world that exists only for them.
*   Investment in persistent relationships.

## Whale Economics (Canonical)

The core economic model is "Whale Economics": simulation is free, monetization occurs when players preserve narrative "Moments." This keeps ARPU high while maintaining strong margins.

### The Core Insight: Simulation Is Free

The simulation engine runs at zero API cost; LLM cost only appears when generating prose Moments. This makes the world rich even when no paid Moments are created.

### Cost Per Moment Type

| Moment Type | Input Tokens | Output Tokens | Cost (Sonnet) | Frequency | Margin @ $0.04 |
|-------------|--------------|---------------|---------------|-----------|----------------|
| **Simple Dialogue** | ~800 | ~150 | $0.0047 | 70% | **88%** |
| **Action/Scene** | ~1,200 | ~250 | $0.0074 | 20% | **81%** |
| **World Building** (Grandmother) | ~2,500 | ~400 | $0.0135 | 8% | **66%** |
| **Major Event** (Flip) | ~3,000 | ~600 | $0.0180 | 2% | **55%** |

*   **Weighted Average Cost:** $0.0062/Moment
*   **Weighted Average Margin:** **84%**

### The "Grandmother Query" Economics

Expensive worldbuilding queries are cached into the graph. After initial generation, future references are cheaper, turning high upfront cost into reusable narrative capital.

### The "Nothing Happening" Subsidy

When a player is AFK, the simulation keeps running for free. The world evolves without LLM costs, and the player returns to meaningful change at no direct cost to the game.

### Margin Defense Table

| Scenario | Player Behavior | Our Cost | Revenue | Margin |
|----------|-----------------|----------|---------|--------|
| **Tourist** | 300 Moments, mostly dialogue | $1.86 | $12.00 | 84% |
| **Regular** | 1,500 Moments, some worldbuilding | $10.50 | $60.00 | 82% |
| **Passionate** | 5,000 Moments, heavy exploration | $40.00 | $200.00 | 80% |
| **Whale** | 15,000 Moments, exhaustive | $135.00 | $600.00 | 77% |

### Worst-Case Stress Test

Even if a player spams expensive worldbuilding queries, caching ensures repeated use drives costs down and keeps the model profitable.

## Lifetime Value (LTV) Comparison

Blood Ledger projects a significantly higher LTV compared to other market offerings due to its unique business model and retention mechanisms.

| Service | Average LTV | Retention | Model |
|---------|-------------|-----------|-------|
| Mobile Game (casual) | $5-15 | 2 months | IAP |
| MMO (WoW) | $150-300 | 1-2 years | Sub |
| Character.AI | $60-120 | 6-12 months | Sub |
| **Blood Ledger (projected)** | **$400-1,200** | **6-18 months** | PAYG |

## Blue Ocean Market Position

Blood Ledger occupies a "blue ocean" market space, avoiding direct competition by offering a fundamentally different product:
*   It's not a game consumed; it's a world that consumes and remembers you.
*   It sells legacy and digital immortality rather than traditional game content.

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Market_Comparison.md
ALGORITHM:       ./ALGORITHM_Semantic_Cache.md
ALGORITHM:       ./ALGORITHM_Hallucination_Defense.md
ALGORITHM:       ./ALGORITHM_World_Scavenger.md
BEHAVIORS:       ./BEHAVIORS_Conversion_Funnel_And_Ledger_Lock.md
BEHAVIORS:       ./BEHAVIORS_Retention_Mechanisms.md
THIS:            ./PATTERNS_Market_Comparison.md
SYNC:            ./SYNC_Business_Model.md
