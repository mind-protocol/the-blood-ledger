# SYNC: Bleed-Through System

## Maturity

STATUS: CANONICAL

## Current State

The Bleed-Through system, a core narrative and technical innovation of Blood Ledger, is documented. This includes:
*   The fundamental pattern of how "scars cross worlds," defining AI as actor, strategic positioning, and public features of Bleed-Through (`PATTERNS_Scars_Cross_Worlds.md`).
*   The observable behaviors and impact of "Bleed Reports" as a killer retention feature, offering digital immortality (`BEHAVIORS_Bleed_Reports.md`).
*   Marketing and vocabulary guidelines for communicating this feature.

## Recent Changes

*   Initial documentation created from `data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md`.
*   2025-12-20: Added `ALGORITHM_Bleed_Through_Pipeline.md` and `HEALTH_Bleed_Through.md`.
*   2025-12-21: Merged `MECHANISMS_Bleed_Through_Pipeline.md` into the algorithm doc and removed the non-standard file.

## Handoffs

**For next agent:**
*   These documents are crucial for understanding how emergent narratives from player actions are leveraged across different game instances.
*   The technical algorithm for how this is achieved (transposition logic) is documented separately in `docs/network/transposition/ALGORITHM_Transposition_Pipeline.md`. Refer to that for implementation details.
*   Any work on character persistence, world generation, or narrative event handling should consider the Bleed-Through mechanics.

**For human:**
*   Review the documented Bleed-Through system for accuracy and alignment with the game's core narrative vision.
*   Verify that the marketing language and feature descriptions effectively communicate the intended player experience.

## Agent's Analysis (Gemini, 2025-12-19)

### Opinions & Insights

"The Bleed-Through" is arguably the most unique and defining feature of Blood Ledger, brilliantly tying together the game's economic, marketing, and narrative aspects.
*   **Narrative Reframing of Technical Necessity:** The strategic decision to frame content reuse (a technical optimization, as seen in the "World Scavenger") as a profound narrative feature ("digital immortality," "scars crossing worlds") is exceptionally clever and highly effective for player engagement and marketing.
*   **Explaining "Subjective Truth":** Providing an in-fiction explanation for narrative inconsistencies (NPCs holding conflicting beliefs due to "bled-through trauma") transforms potential bugs into compelling storytelling devices, enriching the game's philosophical depth.
*   **Retention through Legacy:** The concept of "Bleed Reports" providing tangible evidence of a player's lasting impact across other worlds is a powerful retention hook, creating a continuous loop of interest even after a character's story concludes.

### Ideas & Propositions

1.  **"Bleed-In" Story Hooks:** When a "Living Ghost" or "Rumor Bleed" event happens in a player's world, the system could generate explicit, optional quests or narrative branches to investigate the origin of that bleed-through. This would further integrate the feature into active gameplay.
2.  **Player-Submitted "Signature Scars":** Allow players to "mark" certain moments or characters in their world as particularly impactful ("Signature Scars") which could then be prioritized for bleed-through into other worlds, giving players more direct influence over their legacy.
3.  **Visual Manifestations of Bleed-Through:** Beyond textual descriptions, explore subtle visual cues in the game world (e.g., spectral glimpses of a "Living Ghost" in the distance, an eerie atmospheric shift indicating a strong "Rumor Bleed") to enhance the sense of cross-world influence.

### Gaps & Concerns

1.  **Balancing Narrative Impact vs. Player Agency:** Ensuring that "bled-through" content feels impactful and relevant without undermining the current player's agency or sense of unique story ownership is a delicate balance. Overuse or poorly integrated bleed-through could dilute the personal narrative.
2.  **Technical Robustness of Transposition:** The success relies heavily on the `ALGORITHM_Transposition_Pipeline.md` to be perfectly robust. Any visible glitch or logical inconsistency in the transposition process (e.g., a "Living Ghost" behaving completely out of character or contradicting local facts in an unexplainable way) could shatter immersion.
3.  **The "Unseen" Bleed-Through:** While "Bleed Reports" are excellent, ensuring players *feel* the constant presence of the bleed-through in their active game world, even without explicit reports, is important to reinforce the "scars spread" theme.
4.  **"Negative" Bleed-Through Management:** How are potentially "unfun" or overly traumatic elements from other players' worlds managed? The balance between emergent narrative and player enjoyment (e.g., avoiding repeatedly importing highly negative traits that could make an NPC unlikable) needs careful consideration.

---

## CHAIN

PATTERNS:        ./PATTERNS_Scars_Cross_Worlds.md
BEHAVIORS:       ./BEHAVIORS_Bleed_Reports.md
ALGORITHM:       ./ALGORITHM_Bleed_Through_Pipeline.md
HEALTH:          ./HEALTH_Bleed_Through.md
THIS:            ./SYNC_Bleed_Through.md
