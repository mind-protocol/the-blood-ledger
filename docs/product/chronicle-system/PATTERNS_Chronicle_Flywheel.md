# PATTERNS: Chronicle Flywheel

## Why This Design Exists

The Blood Chronicle System is designed as the primary user acquisition and retention engine for Blood Ledger. It transforms every player session into shareable, user-generated video content, leveraging a viral marketing flywheel. Instead of traditional marketing spend, players organically create and distribute promotional material.

## The Flywheel Concept

The core idea is a self-perpetuating loop:
```
Player plays → Chronicle generated → 1-click upload →
YouTube viewers watch → Download game → Play → 
Generate THEIR Chronicle → Upload → More viewers → Loop
```
This model aims for near-zero Customer Acquisition Cost (CAC) and high organic reach.

## Key Design Decisions & Rationale

*   **Player as Content Creator:** Empowering players to "direct their film" rather than just "share gameplay" fosters creative ownership and increases sharing likelihood.
*   **Automated Generation:** Using LLMs, TTS, and video composition tools to automatically generate cinematic recaps minimizes player effort for content creation.
*   **Phased Implementation:** Starting with an MVP (Session Chronicle) and progressively adding features (sharing, polish, viral elements) allows for iterative development and feedback.

## Go-To-Market Integration

The Chronicle system is the GTM engine, not a peripheral feature. The acquisition
loop integrates product, distribution, and conversion:

```
Chronicles on YouTube → Viewer click-through → Download + demo →
Ledger Lock conversion → Player creates Chronicle → Upload → Repeat
```

### CAC Reduction Targets

*   **Chronicle viral goal:** Target ~$0.05 CAC with scalable organic reach.
*   **Flywheel math:** Early cohorts should show that a small set of uploads can
    yield new paid players, accelerating as more players publish.

### Seeding Strategy (Initial Launch)

1.  **Developer Chronicles:** Seed the channel with in-house playthroughs.
2.  **Creator keys:** Give beta access to creators with a "we make the video for you" pitch.
3.  **Early curation:** Manually feature the best early Chronicles to set quality expectations.

### Viral Hooks In Chronicle Design

*   **Tragedy:** Short, brutal lives.
*   **Justice:** Betrayal and revenge arcs.
*   **Mystery:** Teases that hint at deeper lore.
*   **Relatability:** Tiny choices with cascading consequences.
*   **Worldbuilding:** Deep lore reveals in life Chronicles.
*   **Competition:** Fastest death, longest life, most dramatic fall.

### Retention + Re-Engagement

Automated email digests ("your week in blood — and theirs") re-engage players and
promote both personal and community Chronicles.

## What's In Scope

*   Generation of Session, Weekly, and Life Chronicles.
*   Player-guided content selection ("Director Mode").
*   Automated upload and metadata generation for platforms like YouTube.
*   In-game UI for sharing and reviewing Chronicles.
*   Integration with game events to trigger Chronicle generation.

## What's Out of Scope (and Where it Lives Instead)

*   Detailed economic model for monetization (see `docs/product/business-model/PATTERNS_Whale_Economics.md`).
*   Algorithmic details for character and narrative transposition (see `docs/network/transposition/ALGORITHM_Transposition_Pipeline.md`).
*   Specific billing architecture (see `docs/product/billing/PATTERNS_Pay_To_Preserve_History.md`).

## Maturity

STATUS: CANONICAL
(Derived from the initial design document and represents a core, established pattern.)

---

## CHAIN

BEHAVIORS:       ./BEHAVIORS_Chronicle_Types_And_Structure.md
IMPLEMENTATION:  ./IMPLEMENTATION_Chronicle_Technical_Pipeline.md
VALIDATION:      ./VALIDATION_Chronicle_Metrics_And_Success.md
THIS:            ./PATTERNS_Chronicle_Flywheel.md
SYNC:            ./SYNC_Chronicle_System.md
