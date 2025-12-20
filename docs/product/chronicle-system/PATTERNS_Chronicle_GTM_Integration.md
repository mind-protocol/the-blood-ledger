# PATTERNS: Chronicle Go-To-Market Integration

## Why This Design Exists

The Blood Chronicle is not just a feature; it's the game's core acquisition strategy. This pattern outlines how the Chronicle system is integrated into the Go-To-Market (GTM) strategy to drive user acquisition and reduce Customer Acquisition Cost (CAC) through a self-sustaining viral loop.

## The Acquisition Flywheel

The Chronicle model fundamentally shifts traditional marketing:
```
                    ┌─────────────────────┐
                    │   CHRONICLES ON     │
                    │     YOUTUBE         │◄────────────┐
                    └──────────┬──────────┘             │
                               │                        │
                    Viewers discover                    │
                               │                        │
                    ┌──────────▼──────────┐             │
                    │   CLICK TO PLAY     │             │
                    │   blood-ledger.com  │             │
                    └──────────┬──────────┘             │
                               │                        │
                    Download + Demo                     │
                               │                        │
                    ┌──────────▼──────────┐             │
                    │   LEDGER LOCK       │             │
                    │   (conversion)      │             │
                    └──────────┬──────────┘             │
                               │                        │
                    15% convert, pay                    │
                               │                        │
                    ┌──────────▼──────────┐             │
                    │   PLAY + CREATE     │             │
                    │   THEIR CHRONICLE   │             │
                    └──────────┬──────────┘             │
                               │                        │
                    Upload to channel                   │
                               │                        │
                    └──────────────────────────────────┘
```

## Chronicle as CAC Reducer

The system aims for significantly lower CAC compared to traditional methods:
*   **Chronicle Viral:** Targets ~$0.05 CAC, with unlimited scalability.
*   **Math:** Illustrates how 100 players uploading Chronicles can lead to ~4 new paying players, and how this flywheel accelerates.

## Seeding Strategy (Initial Launch)

To kickstart the flywheel before a large player base:
1.  **Developer Chronicles:** Developers play and upload their own Chronicles to demonstrate the game's potential.
2.  **Content Creator Keys:** Provide beta keys to content creators, positioning the game as one that "makes the video for you."
3.  **Early Curation:** Manually review and feature the best early player Chronicles to maintain quality and attract attention.

## Viral Hooks in Chronicle Design

Chronicles are designed with specific narrative and emotional hooks to encourage sharing:
*   **Tragedy Porn:** Playlists like "The Shortest Lives" appeal to morbid curiosity.
*   **Justice:** Showcasing revenge narratives ("The Betrayals").
*   **Mystery:** "The Shadow" teases future events.
*   **Relatability:** Moments where small actions have large consequences ("I made a tiny lie...").
*   **Worldbuilding:** Deep lore reveals in Life Chronicles.
*   **Competition:** Fastest death, longest life.

## Email Integration

Automated email digests (e.g., "Your week in blood — and theirs") are used to re-engage players and promote both their own Chronicles and popular community Chronicles.

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
BEHAVIORS:       ./BEHAVIORS_Chronicle_Types_And_Structure.md
THIS:            ./PATTERNS_Chronicle_GTM_Integration.md
SYNC:            ./SYNC_Chronicle_System.md
