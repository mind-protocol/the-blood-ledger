# Narrator — Patterns: Why This Design

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## The Core Insight

**The narrator is a persistent creative intelligence maintaining a world. Not a stateless function that generates text on demand.**

It has continuity. It remembers what it authored. It builds on its own work.

---

## The Five Principles

### 1. Authored, Not Generated

The narrator doesn't "generate content." It authors a play. Every word, every clickable, every seed is intentional. The narrator knows what's being set up, what will pay off, what's being withheld.

### 2. The World Is Real Before Being Observed

Pre-generation isn't caching. It's ontology. Aldric's answer about his grandmother exists whether asked or not. The world has depth that exceeds any single playthrough.

### 3. Graph Is Memory, Narrator Is Voice

The graph stores what's true. The narrator decides what speaks, when, how. Same graph, different narrator = different game. The narrator is authorial style.

### 4. Continuity Over Context

Using `--continue` means the narrator accumulates. It knows what it wrote three scenes ago. It can foreshadow, callback, develop. A fresh context window each time would lose this.

### 5. Click Is Lookup, Not Generation

Every click is instant because the response already exists. The narrator worked ahead.

---

## The Authorial Model

The narrator is not a responder. The narrator is a playwright who:

1. **Plants seeds** — Every clickable word is intentional
2. **Controls pacing** — Some clicks advance, some deepen, some plant for later
3. **Shapes discovery** — What can be clicked determines what can be found
4. **Maintains voice** — Character responses are authored, not improvised

The LLM is a tool the narrator uses to generate content — but the narrator controls what gets generated, when, and how it connects.

---

## Pre-Baked Scene Trees

A scene is not generated on-demand. It arrives pre-baked:

```
Scene: Camp Night
├── click "fire" → response A
│   ├── click "alone" → response A1
│   └── click "cold" → response A2
├── click "blade" → response B
│   ├── click "steady" → response B1
│   └── click "holding" → response B2
├── click "York" → response C
│   └── ...
└── click "Thornwick" → response D
    ├── click "family" → response D1
    └── click "Harrying" → response D2
```

**On scene load:** Everything for this moment already exists
**On click:** Swap in the pre-baked response
**No LLM call on click**

---

## Generation Strategy

### Option A: Full Pre-Generation
Generate entire conversation tree before player arrives.
- Works for bounded scenes
- Complete authorial control
- Higher upfront cost

### Option B: Rolling Window
Generate current + 2 layers ahead. As player clicks, generate next layer in background.
- Player never waits
- Lower upfront cost
- Works for deep conversations

### Option C: Hybrid (Recommended)
- Key scenes (story beats) fully pre-generated
- Minor scenes use rolling window
- Free input is on-demand with "thinking" indicator

---

## The Schema

```json
{
  "current": {
    "narration": "He looks at you across the fire.",
    "speech": {
      "speaker": "Aldric",
      "text": "Can't sleep either?"
    },
    "voices": [
      "Three days to York. He's close now."
    ],
    "clickable": {
      "fire": {
        "speaks": "Let me gather wood.",
        "response": {
          "narration": "You stand. The cold hits immediately.",
          "speech": { "speaker": "Aldric", "text": "I'll come." },
          "voices": ["He doesn't want to be alone either."],
          "clickable": { ... }
        }
      }
    }
  }
}
```

Each response contains:
- **narration** — What happens (italic, scene-setting)
- **speech** — What they say (quoted dialogue)
- **voices** — What you think (the internal chorus)
- **clickable** — Next layer of seeds

---

## What the Narrator Controls

| Element | Authored by Narrator |
|---------|---------------------|
| Narration text | Yes |
| Which words are clickable | Yes |
| What player says when clicking | Yes |
| Character response | Yes |
| New clickables after response | Yes |
| Voice content | Yes (from graph) |
| Pacing and depth | Yes |

The narrator decides everything. The LLM executes under narrator control.

---

## Free Input: The Exception

The text box "Say something to Aldric" is the one on-demand moment:

- Player opted in by typing
- Show "Aldric considers..." while generating
- LLM generates within constrained context
- Most players click, not type

Free input is escape valve, not primary interaction.

---

## The Narrator's Workflow

Before player reaches scene:

1. **Query graph** — Who's present? What narratives are active? What tensions exist?
2. **Generate narration** — The scene text with clickable seeds
3. **Generate responses** — For each clickable, what happens when clicked
4. **Recurse** — Generate 2-3 layers deep
5. **Store the tree** — Ready for instant delivery

Player arrives → scene loads instantly → clicks are lookups.

---

## Why This Matters

**For the player:**
- Instant response to every click
- Feels authored, not generated
- Consistent character voices
- No "AI thinking" breaks immersion

**For the experience:**
- Every clickable is intentional
- Seeds can be planted that pay off later
- Pacing is controlled
- The game feels written, not computed

**For development:**
- Can review and edit generated content
- Quality control before player sees it
- Debug specific conversation paths
- A/B test different authored approaches

---

## Connection to Graph

The narrator reads from the graph to generate:

- **Present characters** → Who can speak
- **Active narratives** → What voices say
- **Character backstory** → How they respond
- **Tensions** → What's ready to break
- **Player history** → What they've done

The graph is truth. The narrator is interpretation. The scene tree is presentation.

---

*"The narrator works while you sleep. When you click, you're reading what was already written."*
