# Narrator — Patterns: World Building Through Pre-Generation

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## The Core Insight

**Pre-generation isn't optimization. It's world-building.**

The narrator generates responses the player may never see. But those responses become real. They exist. They're canon.

The world becomes real whether you look or not.

---

## What This Creates

### Consistency

Aldric's answer about Thornwick exists — even if you never clicked "Thornwick."

If you ask in scene 5 instead of scene 2, the answer already exists. Same answer. Same Aldric. The system doesn't generate fresh — it retrieves what was already true.

### Depth on Demand

Later scene. You finally ask about his grandmother. The answer is there. It connects to Thornwick. It connects to why he won't look at burned villages.

It feels like he was always this deep.

Because he was.

### Graph Enrichment

Generated responses write back to the graph:

```
Player never asked about grandmother.
But narrator generated:

"She died before the Harrying. At least she didn't see what they did to Thornwick."

→ New narrative node created:
  narr_aldric_grandmother {
    summary: "Aldric's grandmother died before the Harrying",
    content: "Wulfhild died in her sleep, the winter before.
              Aldric says 'at least' when he speaks of it.",
    truth: 1.0,
    connections: [narr_aldric_thornwick, narr_harrying_memory]
  }

→ Exists now. Forever. Waiting.
```

### The Narrator Discovers

By generating ahead, the narrator finds connections the author didn't plan.

"Oh, Aldric's grandmother died before Thornwick burned. That's why he says 'at least.' That's why he prays sometimes — he's grateful she didn't see."

The system discovers the world by exploring it.

---

## The World Thickens

Every scene:
- Narrator generates 2-3 layers of responses
- Most are never seen
- All of them become canon

The graph grows. Characters deepen. Connections multiply.

By hour 10:
- Aldric has a hundred unseen answers
- All consistent
- All waiting
- All real

---

## The Player Feels This

They don't know why Aldric feels real.

They just know:
- He has answers to questions they haven't asked
- His answers connect to each other
- His past has texture they can discover
- He feels like a person, not a character

**Because the narrator made him real before anyone asked.**

---

## Graph Enrichment Protocol

When generating responses, the narrator can:

### 1. Discover New Narratives

```typescript
interface GeneratedInsight {
  type: 'new_narrative';
  content: {
    summary: string;
    detail: string;
    connections: string[];  // IDs of related narratives
  };
  source: {
    scene: string;
    clickable: string;
    generated_for: string;  // Character whose response revealed this
  };
}
```

### 2. Deepen Existing Narratives

```typescript
interface NarrativeEnrichment {
  type: 'enrichment';
  narrative_id: string;
  additions: {
    detail?: string;        // More specific information
    emotion?: string;       // How the character feels about this
    connection?: string;    // Newly discovered link
  };
}
```

### 3. Record Character Knowledge

```typescript
interface CharacterKnowledge {
  type: 'knowledge';
  character_id: string;
  knows: {
    about: string;          // What they know about
    detail: string;         // What specifically
    certainty: number;      // How sure they are
    source: string;         // How they know
  };
}
```

---

## The Accumulation Effect

Session 1:
- Player talks to Aldric about York
- Narrator generates responses about Thornwick (not clicked)
- Aldric's grandmother is mentioned in one response
- → Graph now has narr_aldric_grandmother

Session 2:
- Player asks about Aldric's family
- Response includes grandmother detail (from graph)
- Player never knew this was generated in session 1
- → "He's always been this detailed"

Session 5:
- Player visits Thornwick
- Aldric's reaction draws from: grandmother, brother, the Harrying
- All these details exist because they were pre-generated
- → Character feels like he has a real past

---

## What Gets Written Back

| Generated Content | Write to Graph? |
|-------------------|-----------------|
| Character backstory details | Yes |
| Character emotional states | Yes |
| New narrative connections | Yes |
| Factual details (places, events) | Yes |
| Conversational filler | No |
| Generic responses | No |

**Rule:** If it could be referenced later, it's canon. Write it to the graph.

---

## The Narrator as Archeologist

The narrator doesn't just generate responses. The narrator discovers who these people are.

Each generation is a dig:
- What would Aldric say about his grandmother?
- Oh, she died before the Harrying.
- Oh, he's grateful for that.
- Oh, that's why he prays.

The narrator unearths the truth by asking questions the player might never ask.

---

## Why This Matters for Engagement

**Drive 5 (Social Influence):** Characters feel like real people with real pasts.

**Drive 7 (Unpredictability):** You can always discover more. There's always depth.

**Drive 4 (Ownership):** You're building a relationship with someone who exists.

**The success metric:** "You know them well enough to predict them."

This works because they're real. They have consistent histories. They have answers you haven't heard yet.

---

## Implementation Note

The narrator must:
1. Generate responses
2. Extract insights from responses
3. Write insights to graph
4. Ensure future generations read from enriched graph

The graph is both input and output. Each generation makes the world more real.

---

*"Aldric isn't written. He's discovered. The narrator just keeps digging until there's a whole person there."*
