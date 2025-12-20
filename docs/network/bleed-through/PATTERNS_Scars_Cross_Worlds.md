# PATTERNS: Scars Cross Worlds

## Why This Design Exists

"The Bleed-Through" is a foundational narrative and technical pattern in Blood Ledger. It defines how elements from one player's single-player world (characters, events, rumors) can manifest in other players' worlds. This isn't merely content reuse; it's designed to create a sense of persistent legacy, explain subjective realities, and act as a powerful engine for emergent narrative and player retention.

## Core Insight: AI as Actor, Not Author

The Bleed-Through pattern reinforces the core principle that the game's AI acts as an "Actor" within constraints set by "The Graph" (the game's underlying physics and canon), not as an arbitrary "Author." This ensures narrative integrity and prevents hallucinations, as the graph is the sole source of truth.

## Strategic Position and Rationale

The Bleed-Through is not merely an underlying system; it is a highlighted, assumed, and owned feature with significant strategic benefits:

*   **Validates Player Investment:** Whales (high-spending players) pay for "significance." If their actions and characters can appear in other worlds, their perceived Return on Investment (ROI) in the game skyrockets, offering "digital immortality."
    *   **Pitch:** "You aren't just playing a game. You're leaving scars on the multiverse."
*   **Explains Subjective Truth:** This pattern provides an in-fiction explanation for how NPCs might hold conflicting beliefs or possess fragmented memories. What might appear as an "AI bug" becomes a rich "fog of war" – a character's trauma from another world bleeding through.
*   **Solves the Content Treadmill:** By making players the engine of content generation, the Bleed-Through promises an infinite game where "no two playthroughs are alike because the wounds of other worlds keep bleeding into yours."

## Public Features of Bleed-Through

These are the player-facing manifestations of the Bleed-Through mechanism:

*   **Living Ghosts:** NPCs are not generic; some "bled through" from other players' worlds, carrying unique histories and scars. "The stranger in the tavern isn't a random generation. He bled through from a world that burned."
*   **The Rumor Bleed:** News and stories (not all true) can travel between worlds, adding layers of intrigue and making players question what is fact and what is fiction. "News bleeds between worlds. Not all of it is true."
*   **Your Scars Spread:** Players are made aware that their own actions within their world have ripple effects, manifesting in other players' experiences. "Your wounds ripple into worlds you'll never see."

## Marketing and Vocabulary

The language used to describe the Bleed-Through is carefully chosen to emphasize its narrative and philosophical depth, while avoiding technical jargon:

*   **Use These Terms:** Bleed-Through, Ghost, Bleed, Bleed Report, The Rumor Bleed, Living Scars.
*   **Never Use These Terms:** Caching, Scavenging, Vector search, Echo System, Topology, Transposition (these sound like cost-saving measures and break immersion).

This frames a technical necessity (content reuse) as a profound narrative feature, transforming "We save money by reusing data" into "Some stories bleed through the walls between worlds."

## Maturity

STATUS: CANONICAL

---

## CHAIN

BEHAVIORS:       ./BEHAVIORS_Bleed_Reports.md
THIS:            ./PATTERNS_Scars_Cross_Worlds.md
SYNC:            ./SYNC_Bleed_Through.md