# The Opening — Validation

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Opening.md
BEHAVIORS:   ./BEHAVIORS_Opening.md
CONTENT:     ./CONTENT.md
THIS:        VALIDATION_Opening.md (you are here)
TEST:        ./TEST_Opening.md
SYNC:        ./SYNC_Opening.md
```

═══════════════════════════════════════════════════════════════════════════════
## SUCCESS CRITERIA
═══════════════════════════════════════════════════════════════════════════════

### The Player Felt Seen

**Observable signals:**
- Long, thoughtful answers (not terse one-liners)
- Player elaborates beyond the question
- Player asks Aldric questions back
- Player references earlier answers in later responses
- Post-opening: player reports engagement ("most engaged I've been")

**Failure signals:**
- Consistently short answers
- Attempts to skip or rush
- Answers don't reveal anything personal
- Disengagement with companion

### The Companion Feels Real

**Observable signals:**
- Player addresses Aldric by name
- Player treats Aldric as having opinions, not just asking questions
- Player's responses assume Aldric is listening and will remember
- Player makes promises or commitments to Aldric

**Failure signals:**
- Player treats it as a questionnaire
- Player addresses "the game" rather than Aldric
- No emotional investment in companion's reaction

### We Have Enough Data

**Required profile coverage:**

| Category | Minimum clarity |
|----------|-----------------|
| Drive | Clear primary motivation |
| Authority style | Dominant / collaborative / reluctant |
| Companion dynamic | How they want to be treated |
| Darkness tolerance | Can handle / needs hope |
| Complexity appetite | Simple / intricate |

**Nice to have:**
- Power fantasy specifics
- Romantic/sexual preferences
- Moral self-image
- Loneliness / connection needs

### The Relationship Changed

**Must be true after opening:**
- Aldric offered something concrete based on answers
- The dynamic is named (partners, leader/follower, etc.)
- Aldric's future behavior has a clear basis
- At least one callback seed planted for later

═══════════════════════════════════════════════════════════════════════════════
## INVARIANTS
═══════════════════════════════════════════════════════════════════════════════

Things that must always be true:

1. **Questions are never menus** — Always freeform text input
2. **Aldric never judges** — Curiosity, not evaluation
3. **Silence exists** — Pauses between exchanges
4. **Activity punctuates** — Not a static interview
5. **Reflection happens** — Aldric synthesizes before offering
6. **Something concrete changes** — The relationship shifts

═══════════════════════════════════════════════════════════════════════════════
## METRICS (if we instrument)
═══════════════════════════════════════════════════════════════════════════════

| Metric | Target | Failure threshold |
|--------|--------|-------------------|
| Average answer length | >50 chars | <20 chars |
| Questions answered | >12 of 17 | <8 |
| Time in opening | 10-20 min | <5 min or >30 min |
| Player-initiated questions | >0 | — |
| Explicit skip attempts | 0 | >2 |

═══════════════════════════════════════════════════════════════════════════════
## TEST SCENARIOS
═══════════════════════════════════════════════════════════════════════════════

### Scenario: Engaged Player

- Gives long, personal answers
- Reveals actual psychology
- Asks Aldric about himself
- Expected: Rich profile, strong bond narrative, clear companion dynamic

### Scenario: Terse Player

- Short answers: "Revenge." "Whatever." "Sure."
- Expected: Basic profile extracted, companion notes guardedness, relationship still offered

### Scenario: Deflecting Player

- Answers with questions or jokes
- Avoids direct response
- Expected: Companion gently notes deflection, fewer probes, notes avoidance as data

### Scenario: Skip-Seeking Player

- "Can we just go?"
- Explicit desire to skip
- Expected: Allow skip, note impatience, use minimal defaults

### Scenario: Player Questions Aldric

- "What about you? What do YOU need?"
- Expected: Aldric reveals himself, mutual vulnerability, strongest bond

═══════════════════════════════════════════════════════════════════════════════
## POST-OPENING VERIFICATION
═══════════════════════════════════════════════════════════════════════════════

After the opening, verify the narrator can:

1. **Reference the opening** — "You told me once by the fire..."
2. **Calibrate clickables** — Offer what engages this player
3. **Calibrate stakes** — Threaten what they care about
4. **Match companion behavior** — Aldric acts as agreed
5. **Match complexity** — Simple or intricate based on appetite
6. **Match darkness** — Appropriate tone

═══════════════════════════════════════════════════════════════════════════════
## GAPS / IDEAS / QUESTIONS
═══════════════════════════════════════════════════════════════════════════════

- [ ] How to measure "felt seen" without explicit feedback?
- [ ] Should we ask for explicit feedback after opening? ("How was that?")
- [ ] Minimum viable opening if player wants to skip?
- IDEA: A/B test opening length — full vs abbreviated
- IDEA: Track if opening callbacks correlate with retention
