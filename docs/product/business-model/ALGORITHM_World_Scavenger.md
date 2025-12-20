# ALGORITHM: World Scavenger

## Procedures

The World Scavenger algorithm is a long-term margin protection strategy that shifts the paradigm of content generation. Instead of always generating new narrative content from scratch, the system prioritizes "scavenging" (reusing and adapting) content from other players' worlds. This approach leads to an inverse cost curve: the system becomes cheaper to operate as the player base grows and the content cache becomes richer.

## Paradigm Shift: Scavenge Before Generate

The fundamental principle is that the `WorldBuilder` primarily acts as a scavenger, and only as a last resort generates fresh content.

## The Scavenger Priority Stack

When a request for new narrative content (e.g., character backstory, location history) arises, the system follows a hierarchical process:

1.  **FIND exact cluster match:** Cost: $0.00. The most efficient method, reusing content that perfectly fits.
2.  **GHOST INJECT similar NPC:** Cost: $0.0001 (vector search). Finds and adapts existing NPCs from other worlds that are semantically similar to the current need.
3.  **STEAL rumors from feed:** Cost: $0.00. Integrates existing rumors or unconfirmed events from the "Bleed-Through" feed.
4.  **SYNTHESIZE from fragments:** Cost: $0.005. Combines smaller, pre-existing narrative fragments to create new content.
5.  **GENERATE fresh (last resort):** Cost: $0.02+. Only if all other methods fail, the system resorts to full LLM generation.

## Three Scavenging Systems

### 1. Village Cache
*   **Function:** Copies fully-explored topologies and narratives from other worlds (e.g., descriptions of a small village, its inhabitants, and local histories).
*   **Cost:** $0.00.

### 2. Ghost Injection
*   **Function:** Utilizes vector search to find matching NPCs from other players' worlds who fit a specific thematic or role requirement. These "ghosts" are then integrated into the local world (see `ALGORITHM_Transposition_Pipeline.md` for integration logic).
*   **Cost:** $0.0001 per search (extremely low).

### 3. Shadow Feed
*   **Function:** Imports distant events and narrative fragments as rumors from the Bleed-Through network, enriching the local world's background without directly impacting its canon (see `ALGORITHM_Transposition_Pipeline.md` for fuzzing logic).
*   **Cost:** $0.00.

## Inverse Cost Curve

The cost per player per month decreases significantly as the player base grows due to increased cache hit rates.

| Players | Cache Hit Rate | Cost/Player/Month |
|---------|----------------|-------------------|
| 100 | 20% | $5.00 |
| 1,000 | 60% | $1.50 |
| 10,000 | 85% | $0.30 |
| 100,000 | 95% | $0.05 |

## Advantages of Scavenging

*   **Cost Efficiency:** Dramatically reduces the reliance on expensive LLM generation, leading to substantial cost savings at scale.
*   **Higher Quality Content:** Scavenged NPCs and narratives often have "lived" experiences from actual gameplay (50+ turns). This means they bring proven voice, tone, and emergent quirks that are more authentic than 0-shot LLM prompts. This is "player-validated quality."
*   **Narrative Moat:** The first few players actively "build" the world. Subsequent players inherit a rich, pre-generated universe. Every exploration makes the global cache richer, making the system inherently cheaper and more robust as it grows.

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Whale_Economics.md
THIS:            ./ALGORITHM_World_Scavenger.md
SYNC:            ./SYNC_Business_Model.md
