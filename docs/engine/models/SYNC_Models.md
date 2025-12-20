# Data Models — Sync: Current State

```
STATUS: DRAFT
UPDATED: 2025-12-20
```

## MATURITY

STATUS: DRAFT

What's canonical (v1):
- The Pydantic models for nodes, links, and tensions are defined in `engine/models/`.
- Basic type enforcement and field validation are in place.

## CURRENT STATE

The `engine/models/` module provides the core data structures for the game. All major node, link, and tension types are defined using Pydantic, ensuring type safety and basic data validation. This module acts as the authoritative source for the game's graph schema.

## RECENT CHANGES

### 2025-12-20: Initial Ngram Documentation Creation

- **What:** Created `PATTERNS_Models.md`, `BEHAVIORS_Models.md`, `ALGORITHM_Models.md`, `VALIDATION_Models.md`, `IMPLEMENTATION_Models.md`, `HEALTH_Models.md`, and `SYNC_Models.md` for the `engine/models` module.
- **Why:** To align with the `ngram` framework and provide comprehensive documentation for the data models.
- **Impact:** The `engine/models` module is now documented with a complete `ngram` documentation chain.

## IN PROGRESS

- Currently, no active code development is ongoing for the `engine/models` module. The focus is on completing and refining the documentation chain.

## KNOWN ISSUES

- The `embeddable_text` methods across models (e.g., `Character`, `Place`, `Thing`, `Narrative`) in `nodes.py` do not fully align with the `detail > 20, fallback to name` logic specified in `PATTERNS_Embeddings.md`.
- Custom validation for mutually exclusive fields (e.g., `Narrative.source` vs. `Narrative.detail`) is not yet implemented.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code for any changes to the data models or their validation logic. Ensure that any new models or field updates are reflected across the entire documentation chain. Prioritize addressing the `embeddable_text` inconsistency.

## HANDOFF: FOR HUMAN

The core data models are well-defined and documented. Key areas for review involve aligning `embeddable_text` logic with embedding patterns and considering custom validators for complex field relationships.

## TODO

- [ ] Add `engine/models` mapping to `modules.yaml` (already done in previous step).
- [ ] Implement unit tests for all Pydantic models, covering validation, defaults, and properties.
- [ ] Refactor the `embeddable_text` methods across models in `nodes.py` to be consistent with the `PATTERNS_Embeddings.md` rules (detail > 20, fallback to name).

## CONSCIOUSNESS TRACE

Confidence in the model definitions themselves is high, as Pydantic handles much of the core validation. The remaining work is primarily about ensuring consistency with related modules (embeddings) and enhancing validation for complex narrative-specific constraints.

## POINTERS

- `docs/engine/models/PATTERNS_Models.md` for the Pydantic design philosophy.
- `engine/models/` for the Python implementation of the data models.

## CHAIN

```
THIS:            SYNC_Models.md (you are here)
PATTERNS:        ./PATTERNS_Models.md
BEHAVIORS:       ./BEHAVIORS_Models.md
ALGORITHM:       ./ALGORITHM_Models.md
VALIDATION:      ./VALIDATION_Models.md
IMPLEMENTATION:  ./IMPLEMENTATION_Models.md
HEALTH:          ./HEALTH_Models.md
```