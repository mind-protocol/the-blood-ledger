# Narrator — Algorithm: The Thread

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## The Thread

Single persistent conversation with the narrator. Never reset.

```
[System Prompt]
[Scene 1 generation]
[Scene 1 output]
[Scene 2 generation]
[Scene 2 output]
...continuing indefinitely with --continue
```

**The narrator remembers everything it authored.**

---

## Why Continuity Matters

### Foreshadowing

Scene 2: Narrator writes "Aldric's hand rests on his blade. Old habit."

Scene 7: Player finally asks about the habit. Narrator remembers it planted this seed. Pays it off coherently.

### Consistency

Scene 3: Aldric says "Keeps my hands busy."

Scene 12: Similar situation. Narrator remembers Aldric's voice, his patterns. Same character, evolved.

### Accumulated Knowledge

By scene 20, the narrator knows:
- Every seed it planted
- Every response it authored (seen or unseen)
- Every character detail it created
- Every tension it's been building

Fresh context each time would lose all of this.

---

## The Implementation

Using Claude Code's `--continue` flag:

```bash
# First scene
claude -p "Generate scene: Camp Night" --output-format json

# Subsequent scenes (same conversation)
claude --continue -p "Generate scene: Road to York" --output-format json

# Continue indefinitely
claude --continue -p "Generate scene: York Gate" --output-format json
```

Each call builds on the previous. The narrator accumulates.

---

## Thread State

The thread implicitly contains:

```
THREAD STATE (in narrator's memory)
├── All scenes generated
├── All clickables authored
├── All responses written (seen or not)
├── Character voice patterns established
├── Seeds planted
├── Setups awaiting payoff
└── Accumulated understanding of the world
```

This isn't stored explicitly — it's in the conversation history.

---

## When to Start Fresh

The thread should be continuous within a playthrough. But:

**New playthrough** = New thread
- Different player character
- Different starting narratives
- Fresh authorial space

**Same playthrough** = Same thread
- Continue from where we left off
- Narrator remembers everything

---

## Thread Management

### Session Boundaries

Player closes game, returns later:
- Thread persists (Claude Code conversation continues)
- On resume, narrator has full context

### Thread Too Long

If thread exceeds context window:
- Summarize earlier portions
- Keep recent scenes in full
- Narrator loses detail on early scenes but keeps patterns

```
[System Prompt]
[Summary: Scenes 1-10]
[Full: Scenes 11-15]
[Current generation]
```

### Backup/Restore

Thread state should be recoverable:
- Store conversation ID
- Can resume from any point
- Consider periodic state snapshots

---

## Generation Flow

```
1. Read graph state (what's true now)
2. Read thread (what's been authored)
3. Generate scene package
4. Narrator remembers what it just wrote
5. Return output
6. Graph receives mutations
7. Player receives scene
8. Wait for next generation request
```

The thread grows with each generation. The narrator accumulates.

---

## The Narrator's Memory

What the narrator remembers through the thread:

| Memory Type | Example | Why It Matters |
|-------------|---------|----------------|
| Seeds planted | "Old habit" in scene 2 | Can pay off later |
| Character patterns | Aldric's terse speech | Consistency |
| Responses written | Grandmother answer | World depth |
| Emotional arcs | Aldric opening up slowly | Character development |
| Player tendencies | Asks about past often | Personalization |

---

## Thread vs Graph

| Thread | Graph |
|--------|-------|
| What was authored | What's true |
| Narrator's memory | World's memory |
| Voice and style | Facts and connections |
| Seeds and setups | Narratives and beliefs |
| Implicit in conversation | Explicit in data |

Both are needed. Graph without thread = inconsistent voice. Thread without graph = no persistent world state.

---

## Error Handling

### Thread Lost

If conversation can't continue:
1. Start new thread
2. Load recent graph state
3. Generate summary of recent scenes for narrator context
4. Mark discontinuity in logs
5. Continue (some consistency loss acceptable)

### Thread Corrupted

If output is inconsistent with earlier:
1. Narrator self-corrects with graph as source of truth
2. Graph mutations take precedence
3. Log the correction

---

*"The thread is the narrator's memory. It knows what it wrote. It builds on its own work. It never forgets."*
