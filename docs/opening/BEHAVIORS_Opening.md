# The Opening — Behaviors: Player Experience

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Opening.md
THIS:        BEHAVIORS_Opening.md (you are here)
ALGORITHM:   ./ALGORITHM_Opening.md
CONTENT:     ./CONTENT.md
VALIDATION:  ./VALIDATION_Opening.md
TEST:        ./TEST_Opening.md
SYNC:        ./SYNC_Opening.md
```

═══════════════════════════════════════════════════════════════════════════════
## WHAT THE PLAYER EXPERIENCES
═══════════════════════════════════════════════════════════════════════════════

### The Setup

Night. A fire. The player and one companion (Aldric) alone.
Three days into a journey. Destination: York. Target: Edmund.

No action. No danger. Just two people and the weight of what's coming.

### The Arc

```
OPENING     Companion's uncertainty — "Haven't decided about you yet"
    ↓
PROBING     Questions that matter — drive, authority, darkness, intimacy
    ↓
REFLECTION  Companion mirrors back — "You're not what I expected"
    ↓
CONNECTION  Companion finds themselves — "I've never fit either"
    ↓
OFFER       Something concrete changes — "I'll translate for you"
    ↓
CLOSE       Relationship crystallizes — "Partners"
```

### The Rhythm

Not all at once. Spread across:
- Firelight conversation
- Walking in silence
- Crossing a stream
- Night when neither can sleep
- Dawn before breaking camp

Each beat has a different mood. Questions match the moment.

═══════════════════════════════════════════════════════════════════════════════
## INPUT / OUTPUT
═══════════════════════════════════════════════════════════════════════════════

### Input

Player's freeform text responses to companion questions.

No clicks. No menus. Pure conversation.

### Output

**Player Profile** — extracted from their answers:

| Dimension | What we learn |
|-----------|---------------|
| Drive | What moves them (vengeance, duty, idealism, survival) |
| Authority style | Dominant, collaborative, reluctant |
| Focus | Survival, strategy, intrigue, relationships, action |
| Fantasy | What "winning" looks like to them |
| Companion dynamic | How they want to be treated |
| Power fantasy | Powerful, clever, moral, feared, loved, *understood* |
| Darkness tolerance | How bleak can it get |
| Emotional range | Vulnerability, intimacy, or stoic distance |
| Conflict style | Violence, cunning, diplomacy, avoidance |
| Stakes preference | People, honor, possessions, goals |
| Mortality comfort | At risk or invincible |
| Trust/betrayal | Suspicious or trusting, loyal or opportunistic |
| Pacing | Savor moments or push momentum |
| Detail appetite | Rich description or sparse |
| Secret desires | What they want but won't admit |
| Historical literacy | Know the period or need context |
| Complexity appetite | Simple drama or intricate webs |
| Competence fantasy | Earned wins or effortless power |
| Social status | How much status matters |
| Sexual/romantic | Engage, deflect, or pursue |
| Moral self-image | Need to be good, or comfortable gray |
| Loneliness | Connection or solitude |
| Control vs chaos | Planner or adapter |

**Companion State** — initialized based on what was revealed:

- How Aldric will behave going forward
- What he'll remember
- What he offered (e.g., "I'll translate")
- The relationship dynamic (equals, mentor, etc.)

**Initial Narratives** — seeded into the graph:

- Bond narrative between player and companion
- Player's stated drive as active narrative
- Any promises made during conversation

═══════════════════════════════════════════════════════════════════════════════
## OBSERVABLE BEHAVIORS
═══════════════════════════════════════════════════════════════════════════════

### During Opening

1. Companion asks question
2. Player types freeform response
3. Companion pauses (silence has weight)
4. Companion reflects on answer
5. Activity transition (fire, walking, etc.)
6. Next question in new context

### After Opening

1. Companion behavior reflects what was learned
2. Clickables calibrated to player's interests
3. Stakes threaten what player cares about
4. Complexity matches player's appetite
5. Companion references opening conversation later

═══════════════════════════════════════════════════════════════════════════════
## EDGE CASES
═══════════════════════════════════════════════════════════════════════════════

| Case | Handling |
|------|----------|
| Terse answers | Companion can probe once, then move on |
| Player wants to skip | Allow, but note disengagement as data |
| Contradictory answers | Companion might gently note it |
| Player asks companion questions | Companion answers — reveals themselves too |
| Player refuses to engage | Companion notices: "You don't like talking about yourself" |

═══════════════════════════════════════════════════════════════════════════════
## GAPS / IDEAS / QUESTIONS
═══════════════════════════════════════════════════════════════════════════════

- [ ] Minimum viable profile — what if player answers 3 questions then skips?
- [ ] Should opening have a "skip" option or is commitment required?
- [ ] How to surface the companion's own answers when player asks back?
- IDEA: Track engagement level as meta-signal (long answers = invested)
