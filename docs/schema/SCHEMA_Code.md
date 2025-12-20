# SCHEMA: Code Graph

```
CREATED: 2025-12-20
STATUS: Draft
```

## CORE INSIGHT

**Code is a graph.** 
Files are nodes. Dependencies are links.
The "Isomorphic Bridge" maps code artifacts into the same physical space as narrative entities.

- **Weight** = Stability / Importance (Structural depth, established status, centrality). Slow variable.
- **Energy** = Activity (Reads, Writes, Executions). Fast variable.
- **Tension** = Emergent property of conflicting Narratives/Links (NOT a node).

## DESIGN PATTERNS

- **0 Arbitrary Numbers:** Weights and energies emerge from topology and events, not manual assignment.
- **No Constructed Step Processes:** No linear "if-then" workflows. The system is a field of forces.
- **Bottom-Up Only:** High-level behaviors emerge from low-level link interactions.
- **Enable Emergence:** The system is designed for "The Flip"—sudden changes in state when tension breaks.
- **Precise Information Circulation:** While logic is emergent, the *formats* (schemas, protocols, links) are rigid and precise to enable information to flow without friction.

## THE EVOLUTION: DOCTOR TO PHYSICS

The "Doctor" (static checks) is morphing into the "Physics" (dynamic tension).
Static "pathogens" (Monoliths, Stubs, Orphans) are no longer external reports; they are **structural absences or contradictions** represented as Narratives within the graph.

### 1. File
Represents a source code file.

```yaml
File:
  id: file_{path_hash}
  path: "engine/physics/tick.py"
  language: "python"
  line_count: 520
  
  # Physics Properties
  weight: 0.8    # High because it is stable/important (foundational)
  energy: 0.1    # Low because it is not currently active
```

...

### DOCUMENTS (Context)
Connects Code to Narrative.
`File A -[DOCUMENTS]-> Narrative B`
*   Links implementation to intent.
*   **Orphan Detection (Physics):** 
    - A "Rule Narrative" exists: "Foundational code must have documentation."
    - A "Fact Narrative" exists: "file_tick_py has no DOCUMENTS link."
    - These narratives **CONTRADICT**.
    - If `file_tick_py` is stable / important (High Weight), the tension on this contradiction is high.
    - Physics triggers a flip (Refactor/Document Agent) when the system can no longer sustain the lack of context.


### BLAMES (Authorship)
Channel for Energy injection (Writes).
`Developer -[BLAMES {tick: 1234}]-> File`
*   "I touched this."

### TRACES (Execution)
Channel for Energy injection (Runs).
`Test/Runtime -[TRACES {tick: 1234}]-> File`
*   "This code actually ran."

### CONTRADICTS (Tension)
The source of pressure.
`Narrative A -[CONTRADICTS]-> Narrative B`

**Example: The Monolith Tension**
1.  **Narrative A (Ideal):** "Code should be modular (max 500 lines)." (High Weight - System Rule)
2.  **Narrative B (Reality):** "tick.py has 520 lines." (Attached to `file_tick_py`)
3.  **Link:** `Narrative A -[CONTRADICTS]-> Narrative B`
4.  **Result:** Tension emerges between the ideal and the reality. The physics engine detects this contradiction heating up (if `file_tick_py` has high energy) and triggers a flip.

## MECHANICS

### 1. Weight Calculation (Structural)
Weight is NOT arbitrary. It is computed from the `IMPORTS` graph (PageRank-style).
*   **Core Infrastructure:** High In-Degree -> High Weight (Stability / Importance).
*   **Leaf Feature:** Low In-Degree -> Low Weight (Lower Stability/Importance).

*Correction:* A stable core file has **High Weight** (Stable / Important) but **Low Energy** (Cold). It is "Foundation."

### 2. Energy Injection (Granular)
Energy is injected via events, not just commits.
*   **Write (High):** Commit, Edit.
*   **Read (Low):** LSP "Go to Definition", Open File.
*   **Execute (Med):** Unit Test hit, Runtime trace.

### 3. Tension (Emergent)
No explicit "Tension Node". Tension is calculated physics:
`Pressure = (Energy A + Energy B) * Link Strength` on `CONTRADICTS` links.

*   If `file_tick_py` is hot (High Energy), `Narrative B` ("tick.py is big") gets hot.
*   `Narrative A` ("Code should be modular") is always High Weight (Stable Rule).
*   The `CONTRADICTS` link transfers energy, heating both sides.
*   **Break:** The contradiction becomes unsustainable. Flip event -> Refactor Agent.

## SCHEMA EVOLUTION

This schema allows the `ngram` immune system to query the graph:
*   "Show me High Weight (Stable) nodes with Low Documentation." (Foundational debt)
*   "Show me High Energy (Active) nodes involved in Contradictions." (Crisis)