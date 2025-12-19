# Async Architecture - Archive (2024-12)

```
CREATED: 2024-12-19
PURPOSE: Archive verbose documentation content removed from active docs.
SOURCE: docs/infrastructure/async/ALGORITHM/ALGORITHM_Discussion_Trees.md (archived from pre-split file)
```

---

## Discussion Trees (Archived Detail)

### Principle

Each companion has discussion trees - pre-generated conversation topics.
Generated in background. Deleted when used. Regenerated when low.
Companions feel alive even when nothing's happening.

### Lifecycle

**Generation**

Trigger: Character becomes companion OR remaining branches < 5

Method: Subagent in background bash task

```python
bash(
    command='''
        cd agents/discussion_generator && \
        claude -p "Generate discussion trees for char_aldric" \
        --allowedTools "Write,Read" \
        --add-dir ../../
    ''',
    run_in_background=true
)
```

Output: 5-10 topics, 3-4 depth each

Storage: `playthroughs/default/discussion_trees/{char_id}.json`

**Usage**

| Trigger | Action |
|---------|--------|
| Player clicks portrait | Shows topic list |
| Player selects topic | Tree activates, narration begins |
| 10+ seconds idle during travel | Companion initiates (if content exists) |
| Branch explored | Branch DELETED immediately |

**Regeneration**

Trigger: Remaining unexplored branches < 5

Method: Same subagent, background bash

Timing: Automatic - runs when threshold crossed

Note: Old trees deleted on use, new trees generated fresh

### Tree Structure

```json
{
  "topic": {
    "id": "aldric_past_battles",
    "name": "Past Battles",
    "opener": {
      "narrator": "Aldric stares into the fire, lost in memory.",
      "clickable": {
        "fire": {
          "speaks": "What are you thinking about?",
          "response": {
            "speaker": "char_aldric",
            "text": "Old fights. Men I killed. Men I couldn't save.",
            "clickable": {
              "killed": {
                "speaks": "Tell me about the fights.",
                "response": {
                  "speaker": "char_aldric",
                  "text": "At Stamford Bridge, I stood in the shield wall..."
                }
              },
              "save": {
                "speaks": "Who couldn't you save?",
                "response": {
                  "beat": "His jaw tightens.",
                  "speaker": "char_aldric",
                  "text": "My brother. He was right beside me when the arrow took him."
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Player Triggered

1. Player clicks companion portrait
2. Frontend shows topic list:
   ```
   - Past Battles
   - His Family
   - What He Thinks of Normans
   - A Question for You
   ```
3. Player clicks topic
4. Narrator activates tree, streams narration
5. Each branch explored is deleted

### Idle Triggered

**Conditions:**
- Traveling (not in scene)
- No player input for 10+ seconds
- No injection pending
- Unexplored content exists

**Detection:** Frontend responsibility. Frontend tracks idle time and triggers initiation.

**Presentation:**
```
[silence]
Aldric clears his throat.
"Can I ask you something?"
[tree activates]
```

**Dismissal:**
- Player ignores -> silence
- "Not now" -> companion respects
- Topic remains available (until used elsewhere)

### Generation Prompt

File: `/prompts/discussion_generator.md`

**Inputs:**
- `character.backstory`
- `character.beliefs`
- `character.relationship_to_player`
- Current narrative context
- Topics already explored (to avoid)

**Outputs:**
- Topic list with full trees
- Each topic 3-4 layers deep
- Natural conversation flow
- Seeds for future payoffs

### File Format

`playthroughs/default/discussion_trees/char_aldric.json`:

```json
{
  "topics": [
    {
      "id": "aldric_past_battles",
      "name": "Past Battles",
      "opener": { ... }
    },
    {
      "id": "aldric_family",
      "name": "His Family",
      "opener": { ... }
    }
  ]
}
```

### Deletion on Use

When a branch is explored:

```python
def on_branch_explored(char_id, topic_id, branch_path):
    tree_file = f"playthroughs/default/discussion_trees/{char_id}.md"
    tree = load_tree(tree_file)

    # Delete the explored branch
    delete_branch(tree, topic_id, branch_path)

    # Save updated tree
    save_tree(tree_file, tree)

    # Check if regeneration needed
    if count_unexplored_branches(tree) < 5:
        trigger_regeneration(char_id)
```

---

## Data Flow Diagram (Archived Detail)

```
┌─────────────────────────────────────────────────────────────┐
│                         GRAPH                               │
│                   (source of truth)                         │
│                                                             │
│   places ─── characters ─── narratives ─── tensions         │
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │ SSE stream  │    │ write API   │    │ read API    │    │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
└──────────┼──────────────────┼──────────────────┼────────────┘
           │                  │                  │
           ▼                  │                  │
┌─────────────────┐           │                  │
│    FRONTEND     │           │                  │
│                 │           │                  │
│  map ← position │           │                  │
│  fog ← visibility           │                  │
│  img ← place.image          │                  │
│        │                    │                  │
│        └──────── writes ────┼──→ injection_queue.jsonl
└─────────────────┘           │                  │
                              │                  │
                ┌─────────────┘                  │
                │                                │
                ▼                                │
         ┌─────────────┐                         │
         │   RUNNER    │                         │
         │ (background)│                         │
         │             │                         │
         │  creates    │                         │
         │  places     │─────writes─────────────→│
         │  ticks      │                         │
         └──────┬──────┘                         │
                │                                │
                │ (main output)                  │
                ▼                                │
         ┌─────────────┐                         │
         │ TaskOutput  │                         │
         │ (on system  │                         │
         │  reminder)  │                         │
         └──────┬──────┘                         │
                │                                │
                ▼                                │
         ┌─────────────────┐                     │
         │    NARRATOR     │←───reads────────────┘
         │                 │
         │  streams        │←─── PostToolUse Hook
         │  responds       │     (interruptions only)
         │  spawns Runner  │
         └─────────────────┘
```
