# SYNC: Transposition Logic

## Maturity

STATUS: CANONICAL

## Current State

The algorithmic details governing Character and Narrative Transposition (the technical implementation of the "Bleed-Through" feature) are documented. This includes:
*   The fundamental pattern emphasizing the "Primacy of Local Canon" for maintaining narrative integrity (`PATTERNS_Local_Canon_Primary.md`).
*   The multi-step "Transposition Pipeline," covering entity selection, conflict detection (semantic and historical), and conflict resolution strategies (renaming, relocation, fuzzing) (`ALGORITHM_Transposition_Pipeline.md`).
*   The "Safety Locks on Ground Truth" which define non-negotiable invariants to protect player experience (`VALIDATION_Transposition_Invariants.md`).

## Recent Changes

*   Initial documentation created from `data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md`.

## Handoffs

**For next agent:**
*   These documents are essential for any development related to importing content from other worlds or ensuring narrative consistency in emergent gameplay.
*   The details provided in `ALGORITHM_Transposition_Pipeline.md` are quite granular and directly inform the implementation of the transposition process.

**For human:**
*   Review the documented algorithms and invariants to ensure they align with the desired behavior and narrative integrity goals for the "Bleed-Through" feature.
*   Confirm the specific thresholds (e.g., for semantic similarity or belief intensity) used in conflict detection and resolution are appropriate.

## Agent's Analysis (Gemini, 2025-12-19)

### Opinions & Insights

The Transposition Logic, rooted in the "Local Canon Primary" pattern, is absolutely critical to the Blood Ledger's core promise of a coherent, emergent, yet deeply personal narrative.
*   **Robustness through Layers:** The multi-stage pipeline with distinct phases for Selection, Detection, Resolution, and Integration, capped by "Safety Locks," demonstrates a highly robust approach to handling external narrative elements. This layered defense against paradoxes is crucial for player immersion.
*   **Narrative Flexibility from Resolution:** The conflict resolution strategies (Renaming, Relocation, Fuzzing) are ingeniously designed. They don't just prevent errors; they actively *generate* new narrative hooks and elements of mystery, unreliable history, and wider worldbuilding. This turns potential clashes into sources of richness.
*   **"Truth" as a Technical Moat:** The explicit definition of "Ground Truth Canon" and the role of the `Canon Holder` as the ultimate arbiter is a strong technical and narrative foundation, distinguishing this system from simpler generative AI approaches.

### Ideas & Propositions

1.  **"Fuzzing" as a Player Choice:** In certain high-impact conflict resolution scenarios, the system could present the player with a choice: "This character's memory of X contradicts your world's history. Do you accept their version as a persistent rumor (Fuzz), or completely dismiss it?" This would deepen player agency over the evolving canon.
2.  **Visualization of Transposition Impact:** For debug or developer tools, visualize how an Imported Entity is transformed by the pipeline (e.g., show original data, then highlight Renamed titles, Relocated events, or Fuzzed beliefs). This would aid in understanding and tuning the algorithm.
3.  **Cross-Referencing with World Scavenger:** Ensure tight integration and feedback loops with the `ALGORITHM_World_Scavenger.md`. "Fuzzed" rumors or "Relocated" events could become prime candidates for the World Scavenger to re-inject into other worlds, closing a meta-narrative loop.

### Gaps & Concerns

1.  **Performance of Conflict Detection:** The "semantic and factual analysis" for conflict detection (especially graph queries for "semantically similar high-status roles" and "high-intensity imported beliefs") could be computationally intensive. Performance benchmarks and optimization strategies will be critical, especially as the graph size grows.
2.  **Threshold Tuning:** The "predefined threshold" for semantic similarity in conflict detection, and the intensity/certainty thresholds for historical fact comparison, will require extensive tuning and testing to ensure natural and satisfying outcomes. What feels like a compelling "rumor" vs. a frustrating contradiction?
3.  **Edge Cases for "Defer to Local Canon":** While "Lock 2: Defer to Local Canon" is a robust safety net, consistently hitting this "graceful failure" could lead to a feeling of less dynamic bleed-through content. Clear guidelines or alternative "fuzzing" options for fundamental conflicts might be needed.
4.  **Player Awareness of Resolution:** While the goal is seamless integration, making players subtly aware of *why* an imported entity feels "off" or "altered" (e.g., a renamed character being introduced with a slight air of mystery about their past) could reinforce the deep systemic workings.

---

## CHAIN

PATTERNS:        ./PATTERNS_Local_Canon_Primary.md
ALGORITHM:       ./ALGORITHM_Transposition_Pipeline.md
VALIDATION:      ./VALIDATION_Transposition_Invariants.md
THIS:            ./SYNC_Transposition_Logic.md