# ALGORITHM: Hallucination Defense

## Procedures

The Hallucination Defense is a critical component of the Blood Ledger architecture, designed to prevent Large Language Models (LLMs) from introducing narrative inconsistencies or factual errors into the game's canon. It sacrifices a small portion of potential margin to ensure absolute consistency and player trust.

## The Problem with AI Narrative

Uncontrolled LLM generation can lead to "hallucinations" – output that is factually incorrect or inconsistent with the established game world. This breaks immersion and erodes player trust.

## Our Architecture: Generation vs Canonization

The system separates the act of LLM "generation" (proposing narrative elements) from "canonization" (making it an official part of the game's truth). The LLM acts as an "Actor" that improvises within constraints, while the "Director" (the game's underlying physics engine and graph) holds the ultimate truth and validates all proposals.

## Algorithm Steps

### 1. Narrator Proposes Action
The AI (Narrator) proposes potential narrative actions or dialogue.

```
┌─────────────────────────────────────────────────────────┐
│                     NARRATOR (AI)                        │
│                 "Proposes" potential actions             │
│         "Aldric draws his sword in rage"                 │
└─────────────────────┬───────────────────────────────────┘
```
*   **Cost:** This generation incurs a token cost, even if the proposal is later rejected.

### 2. Physics Engine Validates Proposal
The proposed action is passed to the Physics Engine (driven by `tick.py`), which consults the game's graph and established rules to determine if the action is plausible and consistent with the current state of the world and character motivations.

```
                      │ PROPOSAL (not canon yet)
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   PHYSICS ENGINE                         │
│                  (tick.py — $0.00)                       │
│                                                          │
│  CHECK: Is tension_revenge > 0.9?                        │
│  RESULT: No (0.72)                                       │
│  DECISION: REJECT action                                 │
└─────────────────────┬───────────────────────────────────┘
```
*   **Cost:** This validation step typically costs $0.00 as it relies on internal graph queries and logic.

### 3. Canon Output (Acceptance or Rejection)
*   **If Accepted:** The action becomes canon.
*   **If Rejected:** The rejection itself can become a part of the narrative, explaining *why* something didn't happen, further deepening the story without contradicting established facts.

```
                      │ 
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    CANON OUTPUT                          │
│                                                          │
│  "Aldric's hand twitches toward his hilt.               │
│   But he stops. Not yet. Not here."                      │
│                                                          │
│  (The rejection BECOMES the content)                     │
└─────────────────────────────────────────────────────────┘
```

## The Cost and Value

*   **Cost:** Approximately 15% of the gross margin is spent on generating and validating proposals that may ultimately be rejected. This translates to an overhead token cost (~$0.001 per rejected proposal).
*   **Value:**
    *   **Zero Hallucinations:** Prevents any inconsistent or contradictory information from reaching the player.
    *   **Narrative Integrity:** Ensures characters and events adhere to the established "physics" of the game world.
    *   **Trust Signal:** Builds player trust by demonstrating that the AI is not "dreamy" or "loopy" but grounded in the game's reality.
    *   **Emergent Depth:** Rejected proposals can become compelling narrative moments (e.g., a character almost acting but being held back by their internal state).

## The AI as Actor Model

| Role | System | Responsibility |
|------|--------|----------------|
| **Director** | The Graph (`tick.py`) | Sets constraints, holds truth |
| **Actor** | The AI (Narrator) | Improvises within constraints |
| **Script** | None | There is no script — only physics |

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Whale_Economics.md
THIS:            ./ALGORITHM_Hallucination_Defense.md
SYNC:            ./SYNC_Business_Model.md
