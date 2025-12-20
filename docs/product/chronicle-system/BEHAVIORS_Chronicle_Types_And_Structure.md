# BEHAVIORS: Chronicle Types and Structure

```
STATUS: CANONICAL
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Chronicle System.md
```

## Observable Effects

The Blood Chronicle system generates distinct video narratives of player gameplay, varying in length and purpose. These Chronicles are highly structured and designed for maximum shareability and engagement.

## Chronicle Types

### 1. Session Chronicle (60-90 seconds)
*   **Trigger:** End of any play session (manual or auto after 30 min idle).
*   **Purpose:** Quick recap, highly shareable, low commitment to watch.
*   **Structure:**
    *   `[0:00-0:08] COLD OPEN`: Striking image + dramatic line.
    *   `[0:08-0:25] THE WEIGHT`: 2-3 growing Ledger entries, narrator summarizes tensions.
    *   `[0:25-0:55] THE MOMENT`: Single most significant choice/event, character reaction, consequence.
    *   `[0:55-1:15] THE SHADOW`: 1 off-screen event, tease future impact.
    *   `[1:15-1:25] END CARD`: Player name (optional), session number, CTA.

### 2. Weekly Chronicle (3-5 minutes)
*   **Trigger:** 7 days since last Weekly, OR major story arc completes.
*   **Purpose:** Longer narrative for invested viewers, YouTube algorithm friendly.
*   **Structure:**
    *   `[0:00-0:20] TITLE SEQUENCE`.
    *   `[0:20-1:30] PREVIOUSLY`: Montage of prior sessions, key relationships.
    *   `[1:30-3:30] THIS WEEK`: 3-4 major scenes (setup, moment, consequence).
    *   `[3:30-4:30] THE WORLD MOVED`: 2-3 off-screen events, simulation working.
    *   `[4:30-5:00] NEXT WEEK'S WEIGHT`: Teaser of mounting tensions, cliffhanger, end card.

### 3. Life Chronicle (8-15 minutes)
*   **Trigger:** Character death OR player chooses "Close This Chapter".
*   **Purpose:** The full story, emotional closure, maximum shareability.
*   **Structure:**
    *   `[0:00-0:30] EPITAPH`.
    *   `[0:30-2:00] ACT I — ARRIVAL`: How journey began, first relationships, lies/oaths.
    *   `[2:00-5:00] ACT II — THE WEIGHT BUILDS`: 3-5 major turning points, debts, secrets, alliances, subtle graph visualization.
    *   `[5:00-8:00] ACT III — WHAT YOU DIDN'T SEE`: Full reveal of off-screen events, parallel storylines, cascade of consequences.
    *   `[8:00-11:00] ACT IV — THE BREAKING`: Final sequence leading to death/ending, detailed factors.
    *   `[11:00-13:00] EPILOGUE — WHAT REMAINS`: World after player, legacy, unpaid debts.
    *   `[13:00-14:00] THE GRAPH REVEAL (Optional)`.
    *   `[14:00-15:00] END`: Final stats, invitation to new life.

## Behavior Contracts

### B1: Session chronicle generated after play

```
GIVEN:  a session ends
WHEN:   chronicle generation runs
THEN:   a 60–90 second session chronicle is produced
```

### B2: Weekly chronicle summarizes arc

```
GIVEN:  7 days or major arc completion
WHEN:   weekly generation runs
THEN:   a 3–5 minute chronicle is produced
```

### B3: Life chronicle on death

```
GIVEN:  player character dies
WHEN:   life chronicle generation runs
THEN:   an 8–15 minute chronicle is produced
```

## Inputs / Outputs

### Primary Function: `generate_chronicle()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| chronicle_buffer | object | Events and snapshots |
| chronicle_type | string | session/weekly/life |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| video_file | string | Rendered MP4 path |

**Side Effects:**

- Saves MP4, thumbnail, metadata
- Optional upload to YouTube

## Sharing & Distribution Behaviors

### Director Mode (Player as Filmmaker)
*   **Problem Addressed:** Raw gameplay is often uninteresting; players are not natural content creators.
*   **Solution:** System identifies key moments, and player makes creative choices (which moments to include, narrative tone, thumbnail). This transforms "sharing gameplay" into "directing a film."
*   **Psychology:** Promotes creative ownership, leading to pride-driven sharing and higher engagement.

### Standard In-Game Flow
*   Provides options to watch, edit, upload, download, and share Chronicles directly from within the game interface.
*   Includes settings for auto-uploading and player attribution.

### YouTube Channel Structure
*   **"Blood Ledger Chronicles"** channel with auto-generated playlists (e.g., Today's Chronicles, This Week's Best, The Long Lives, The Betrayals) based on criteria.
*   **Auto-generated metadata** (title, description, tags) for discoverability and SEO.

### Social Sharing Templates
*   Pre-formatted messages for Twitter, Reddit, and Discord, designed to maximize impact and engagement.

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
MECHANISMS:      ./MECHANISMS_Chronicle_Pipeline.md
VALIDATION:      ./VALIDATION_Chronicle_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Chronicle_System.md
TEST:            ./TEST_Chronicle_System.md
THIS:            ./BEHAVIORS_Chronicle_Types_And_Structure.md
SYNC:            ./SYNC_Chronicle_System.md

---

## EDGE CASES

### E1: No significant events

```
GIVEN:  low activity session
THEN:   chronicle focuses on "shadow" events or skips upload
```

### E2: Upload failure

```
GIVEN:  YouTube upload fails
THEN:   store MP4 locally and retry later
```

---

## ANTI-BEHAVIORS

### A1: Raw gameplay dump

```
GIVEN:   chronicle generation
WHEN:    output is produced
MUST NOT: output a raw log
INSTEAD: produce a cinematic narrative
```

### A2: Player forced to upload

```
GIVEN:   chronicle generated
WHEN:    upload choice appears
MUST NOT: auto-upload without consent
INSTEAD: require explicit opt-in
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define consent flow for auto-upload
- [ ] Define default sharing settings
- IDEA: Add chronicle preview and trim tools
