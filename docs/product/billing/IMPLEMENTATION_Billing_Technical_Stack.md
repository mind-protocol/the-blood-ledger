# IMPLEMENTATION: Billing Technical Stack

## Code Architecture

The billing system integrates several components to track player usage and process payments based on the "Moments saved" model.

## Stack

```
┌─────────────────────────────────────────────────────────┐
│                    PLAYER CLIENT                        │
│                  (Steam + Electron)                     │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   GAME SERVER                           │
│         (Python — engine/physics/embeddings.py, narrator, etc.)              │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              USAGE TRACKER                       │   │
│  │  - Counts interactions per player               │   │
│  │  - Tags interaction type (dialogue/action/etc)  │   │
│  │  - Batches to billing service every 5 min       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 STRIPE BILLING                          │
│                                                         │
│  - Customer records (CC on file)                      
```

## Components

### Player Client
*   **Platform:** Steam and Electron.
*   **Role:** Handles the player-facing game interface.

### Game Server
*   **Platform:** Python (e.g., `engine/physics/embeddings.py`, narrator services).
*   **Usage Tracker:**
    *   Counts every "Moment" generated or saved by the player.
    *   Tags each interaction with its type (e.g., dialogue, action, world-building).
    *   Batches usage data to the billing service every 5 minutes to ensure near real-time tracking.

### Stripe Billing
*   **Role:** Manages customer records, payment methods (credit cards on file), and the invoicing process.
*   **Integration (Partial Content):** The provided document was truncated, so the full details of Stripe integration are not available here. It is assumed to handle the processing of batched usage data into billable units and generating monthly invoices.

## Maturity

STATUS: DESIGNING
(Marked as DESIGNING due to the truncation of the source document, indicating incomplete information about the full Stripe integration details.)

---

## CHAIN

PATTERNS:        ./PATTERNS_Pay_To_Preserve_History.md
THIS:            ./IMPLEMENTATION_Billing_Technical_Stack.md
SYNC:            ./SYNC_Billing_System.md
