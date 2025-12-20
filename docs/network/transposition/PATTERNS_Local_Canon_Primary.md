# PATTERNS: Local Canon Primary

## Why This Design Exists

The "Local Canon Primary" pattern is fundamental to maintaining narrative integrity within each player's single-player world, especially in the context of the "Bleed-Through" feature. It establishes that the receiving player's current game state (the "Local World") is the absolute source of truth, and all incoming information (from "Imported Entities") must be reconciled with it. This pattern ensures that player choices feel impactful and that the immediate game experience remains coherent and believable.

## Core Principle: The Primacy of Local Canon

*   **Single Source of Truth:** Each Local World's history is absolute and serves as the foundational layer. Any incoming information that contradicts this foundation threatens the player's sense of presence and the weight of their choices.
*   **The Canon Holder as Arbiter:** The `Canon Holder` system, through its `record_to_canon()` function, is the single point of truth for "Ground Truth." It acts as the final gatekeeper of reality within the Local World.
*   **Immutability of History:** "Ground Truth" nodes and their chronological connections (`THEN` links) are inviolable. Imported entities cannot overwrite, alter, or erase any part of this recorded past. This preserves the player's unique history.
*   **Presence as Fact:** A character's physical location, defined by `CHARACTER -[AT]-> PLACE` links and recorded by the `Canon Holder`, is a protected fact. An imported character cannot manifest in a way that contradicts this established physical presence, enforcing the "Presence, not observation" design pillar.

## The Bleed-Through Mandate

The primary directive for the Bleed-Through feature is to achieve transposition of characters, stories, and events without violating the established canon of the local, receiving world. This pattern outlines the critical algorithms for conflict detection, resolution, and system-level safety checks that are designed to preserve narrative coherence and integrity.

## Foundational Terms

*   **Local World:** The receiving player's current game state, including its established history, character relationships, and physical layout.
*   **Imported Entity:** Any character, narrative, event, or relationship being brought into the Local World from an external player's Chronicle.
*   **Ground Truth Canon:** Facts and events that have been officially recorded in the Local World's history by the Canon Holder system. These are represented as immutable graph nodes and chronological `THEN` links.

## Maturity

STATUS: CANONICAL

---

## CHAIN

ALGORITHM:       ./ALGORITHM_Transposition_Pipeline.md
VALIDATION:      ./VALIDATION_Transposition_Invariants.md
THIS:            ./PATTERNS_Local_Canon_Primary.md
SYNC:            ./SYNC_Transposition_Logic.md