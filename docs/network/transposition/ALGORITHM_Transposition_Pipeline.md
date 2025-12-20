# ALGORITHM: Transposition Pipeline

## Procedures

The Transposition Pipeline is a structured, multi-step algorithm designed to safely and intelligently integrate "Imported Entities" (characters, narratives, events from other players' Chronicles) into a "Local World" without violating its established "Ground Truth Canon." This pipeline transforms potential narrative conflicts into emergent story hooks, preserving the integrity and unique nature of each player's experience.

## 2. The Transposition Pipeline: An Overview

To ensure narrative integrity, the transposition process follows these steps:

1.  **Entity Selection & Data Packaging:** An entity (e.g., a character and their core beliefs) is selected from a source Chronicle and packaged as a portable data object for import.
2.  **Conflict Detection:** The packaged entity's core attributes, roles, and subjective beliefs are compared against the Local World's Ground Truth Canon to identify semantic and factual conflicts.
3.  **Conflict Resolution:** A cascade of resolution strategies is applied to intelligently modify the imported entity until it no longer conflicts with the established local canon.
4.  **Integration & Canonization:** The fully resolved and modified entity is written into the Local World's graph, becoming a new, coherent part of its evolving story.

The first critical stage in this pipeline is the conflict detection algorithm, which serves as the system's primary defense against narrative paradoxes.

## 3. Algorithm: Conflict Detection

Conflict detection is the critical first step in preventing the introduction of narrative paradoxes. The system employs semantic and factual analysis to compare the roles and histories of imported entities with those already established as Ground Truth in the Local World.

### 3.1. Semantic Role Comparison

This ensures an imported character's core identity or role does not create a contradiction with a high-status character in the Local World.

*   **Step 1: Identify Core Role:** Isolate the primary title or function of the imported entity (e.g., "Reeve of Thornwick").
*   **Step 2: Query Local Equivalents:** Search the Local World's graph for semantically similar high-status roles, especially location-tied.
*   **Step 3: Semantic Comparison:** Use vector embeddings to compare the semantic meaning of imported and local roles (e.g., `cosine_similarity("Reeve of Thornwick", "Reeve of Thornwick")` returns 1.0).
*   **Step 4: Flag Conflict:** If similarity exceeds a predefined threshold (e.g., > 0.9), a direct role conflict is flagged.

### 3.2. Historical Fact Comparison

Verifies that an imported entity's core beliefs do not contradict the established history of the Local World. This is a nuanced comparison of subjective belief against objective Ground Truth, creating "I was wrong" moments.

*   **Step 1: Extract Core Beliefs:** Identify high-focus narrative nodes that the imported character believes (e.g., Aldric believing `narr_edmund_betrayal` with intensity 0.6).
*   **Step 2: Query Local Canon:** Retrieve the `truth` property of the same narrative node in the Local World's graph (e.g., `narr_edmund_betrayal` has `truth: 0.0` in Local World).
*   **Step 3: Identify Contradiction:** A conflict is flagged if a high-intensity imported belief contradicts a high-certainty local fact.

Once a conflict is flagged, the system proceeds to the resolution stage.

## 4. Algorithm: Conflict Resolution Strategies

Conflict resolution is a narrative design tool. Its purpose is to transform potential canon violations into sources of mystery, unreliable history, and emergent story hooks, reinforcing the "Discovery, not revelation" principle. The system employs a hierarchy of strategies to resolve flagged conflicts, turning paradoxes into narrative depth.

### 4.1. Strategy 1: Renaming

*   **Trigger:** Semantic role conflict detected (e.g., Imported "Reeve of Thornwick" vs. Local "Reeve of Thornwick").
*   **Action:** Semantically searches for a similar but non-conflicting title (e.g., "Warden," "Steward," "Bailiff").
*   **Result:** Imported character is integrated with a new title (e.g., "Edmund, a Warden from a Distant Land").
*   **Narrative Design Goal:** Create 'fallen royalty' or 'pretender' archetypes.

### 4.2. Strategy 2: Relocation

*   **Trigger:** Historical conflict detected (e.g., character's defining moment in "York" contradicts Local World's "York" history).
*   **Action:** Identifies a distant, undefined region; generates a new placeholder location (e.g., "Old York" in Northern Wastes); remaps imported memories to this new location.
*   **Result:** Character's past remains intact but is now associated with a remote, possibly forgotten, place.
*   **Narrative Design Goal:** Generate 'lost history' and a sense of a wider, unknown world.

### 4.3. Strategy 3: Fuzzing

*   **Trigger:** An imported belief is too central to local canon to be Renamed or Relocated (e.g., Imported `narr_edmund_betrayal` is `truth: 1.0`, but Local World's canon has Edmund as loyal).
*   **Action:** Converts the imported "Ground Truth" fact into a "Rumor" in the Local World. Creates a new `NARRATIVE` node with `narrative_type: rumor`, sets `truth: 0.4`, and alters content (e.g., "They say Edmund had a hand in the old Thane's death.").
*   **Result:** The imported fact becomes part of "The Rumor Bleed," adding subjective truth and intrigue without overriding established history.
*   **Narrative Design Goal:** Implement 'The Rumor Bleed' and populate the world with unreliable narrators.

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Local_Canon_Primary.md
VALIDATION:      ./VALIDATION_Transposition_Invariants.md
THIS:            ./ALGORITHM_Transposition_Pipeline.md
SYNC:            ./SYNC_Transposition_Logic.md
