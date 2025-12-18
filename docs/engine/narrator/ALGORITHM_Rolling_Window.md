# Narrator — Algorithm: Rolling Window Generation

```
CREATED: 2024-12-16
STATUS: Canonical
SUPERSEDES: Full pre-generation approach
```

---

## The Model

**Generate current + N layers ahead. As player clicks, generate next layer in background.**

Player never waits. The narrator stays ahead.

```
Time →

Player sees:     [Layer 0]
Already exists:  [Layer 0] [Layer 1] [Layer 2]
                     ↑
                  player is here

Player clicks → Layer 1 becomes Layer 0
Background:     Generate new Layer 2
```

---

## The Window

```typescript
interface RollingWindow {
  current: SceneState;           // What player sees now
  depth1: Map<string, SceneState>;  // Responses to current clickables
  depth2: Map<string, SceneState>;  // Responses to depth1 clickables
  generating: Set<string>;       // Currently being generated
}
```

**Window size: 2 layers ahead**
- Current: rendered
- Depth 1: instant on click
- Depth 2: ready when depth 1 becomes current

---

## On Scene Load

1. Check if scene tree exists in cache
2. If yes: load current + depth 1 + depth 2
3. If no: generate current, then depth 1, then depth 2
4. Render current immediately (even before depth 2 ready)

```typescript
async function loadScene(sceneId: string): Promise<RollingWindow> {
  // Try cache first
  const cached = await cache.get(sceneId);
  if (cached && cached.depth2) {
    return cached;
  }

  // Generate progressively
  const current = await generateSceneState(sceneId);
  render(current); // Show immediately

  const depth1 = await generateResponses(current.clickable);

  // Background: don't block
  generateDepth2(depth1).then(d2 => {
    window.depth2 = d2;
  });

  return { current, depth1, depth2: new Map() };
}
```

---

## On Click

Player clicks a word. Response is instant (from depth 1).

```typescript
async function handleClick(word: string): Promise<void> {
  const response = window.depth1.get(word);

  // Instant: swap in response
  window.current = response;
  window.depth1 = window.depth2.get(word) || new Map();
  render(window.current);

  // Background: generate new depth 2
  generateDepth2(window.depth1).then(d2 => {
    window.depth2 = d2;
  });
}
```

**Player experience: instant.** Generation happens after render.

---

## Generation Priority

When generating depth 2, prioritize by:

1. **Weight** — Higher weight clickables first (player more likely to click)
2. **Position** — Words earlier in text first (eye tracking)
3. **Type** — Voices before narration (more emotionally relevant)

```typescript
function prioritizeClickables(clickables: Clickable[]): Clickable[] {
  return clickables.sort((a, b) => {
    // Voices first
    if (a.source === 'voice' && b.source !== 'voice') return -1;
    // Then by weight
    return b.weight - a.weight;
  });
}
```

---

## Handling Slow Generation

If player clicks before depth 2 is ready:

```typescript
async function handleClick(word: string): Promise<void> {
  const response = window.depth1.get(word);

  window.current = response;
  render(window.current);

  // Check if depth 2 ready
  if (!window.depth2.has(word)) {
    // Show subtle indicator while generating
    showThinkingIndicator();

    // Generate just what we need
    const newDepth1 = await generateResponses(response.clickable);
    window.depth1 = newDepth1;

    hideThinkingIndicator();
  } else {
    window.depth1 = window.depth2.get(word);
  }

  // Continue background generation
  generateDepth2(window.depth1);
}
```

**Thinking indicator:** Subtle, not blocking. "..." or slight dim. Player can still read.

---

## Scene Transitions

When a click leads to a new scene:

```typescript
interface SceneTransition {
  type: 'transition';
  next: string;           // Scene ID
  narration?: string;     // "You stand. The cold hits."
}

async function handleTransition(transition: SceneTransition): Promise<void> {
  // Show transition narration
  if (transition.narration) {
    render({ narration: transition.narration });
    await delay(1500); // Let player read
  }

  // Pre-fetch was hopefully running
  const nextScene = await loadScene(transition.next);
  render(nextScene.current);
}
```

**Predictive pre-fetch:** When player enters a scene, start loading likely next scenes in background.

---

## Caching Strategy

```typescript
interface SceneCache {
  // Full trees for visited scenes
  visited: Map<string, SceneTree>;

  // Partial trees for likely scenes
  prefetched: Map<string, RollingWindow>;

  // Generation queue
  queue: PriorityQueue<GenerationJob>;
}
```

**Cache lifetime:**
- Visited scenes: keep until session ends
- Prefetched scenes: keep 5 most likely
- Evict LRU when memory pressure

---

## Background Worker

Dedicated worker for generation:

```typescript
const generationWorker = {
  queue: new PriorityQueue(),

  async run() {
    while (true) {
      const job = await this.queue.pop();

      if (job.type === 'depth2') {
        await generateDepth2(job.clickables);
      } else if (job.type === 'prefetch') {
        await prefetchScene(job.sceneId);
      }
    }
  },

  prioritize(job: GenerationJob) {
    // Current scene depth > prefetch
    // Higher weight clickables > lower
    return job.priority;
  }
};
```

---

## Metrics to Track

| Metric | Target | Meaning |
|--------|--------|---------|
| Click-to-render | < 50ms | Instant feel |
| Depth 2 ready % | > 95% | Rarely wait |
| Generation time | < 2s | Fast enough to stay ahead |
| Cache hit rate | > 80% | Efficient reuse |

---

## Example Flow

```
1. Player enters Camp Night scene
   - Render current immediately
   - Background: generate depth 1 (3 clickables × 1 response each)
   - Background: generate depth 2 (3 × 3 = 9 responses)

2. Player clicks "Thornwick"
   - Instant: show response from depth 1
   - New current has 4 clickables
   - Background: generate new depth 2 (4 × 3 = 12 responses)

3. Player clicks "Harrying"
   - Instant: show response from depth 2 (now depth 1)
   - Background: continue generating

4. Player types free input
   - On-demand LLM call
   - Show "Aldric considers..." (500ms-2s)
   - Render response
   - Background: generate responses to new state
```

---

## Free Input Handling

Free input breaks the pre-generation model. Handle gracefully:

```typescript
async function handleFreeInput(text: string): Promise<void> {
  showThinkingIndicator("Aldric considers...");

  const response = await generateFreeResponse({
    input: text,
    character: currentCharacter,
    context: getConversationContext(),
    graphContext: getRelevantNarratives()
  });

  hideThinkingIndicator();

  // Insert into current state
  window.current = {
    narration: response.narration,
    speech: response.speech,
    voices: window.current.voices, // Keep voices
    clickable: response.clickable
  };

  render(window.current);

  // Generate ahead from new state
  generateDepth1And2(window.current);
}
```

---

*"The narrator runs ahead, always one step beyond where you are. You never catch up. You never have to wait."*
