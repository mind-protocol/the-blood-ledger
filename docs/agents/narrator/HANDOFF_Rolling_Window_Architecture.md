# Handoff — Rolling Window Architecture

```
CREATED: 2024-12-16
STATUS: Decision made, awaiting implementation
FOR: Backend developer
```

---

## The Problem

Pre-generating 2 layers of clickable responses creates combinatorial explosion:

```
Root scene: 5 clickables
Layer 1:    5 × 5 = 25 responses
Layer 2:    25 × 5 = 125 responses
```

125+ scene packages per generation is too expensive and slow.

---

## The Solution: Rolling Window

Generate **1 layer ahead**. As player clicks, generate next layer in background and push to frontend.

```
┌─────────────────────────────────────────────────────────────────┐
│                         ROLLING WINDOW                          │
│                                                                 │
│  1. Scene loads with layer 1 pre-generated (5 responses)       │
│  2. Player clicks "blade"                                       │
│  3. Frontend shows "blade" response immediately (cached)        │
│  4. Backend starts generating layer 2 for new clickables        │
│  5. Backend pushes updates via SSE when ready                   │
│  6. Frontend patches scene tree                                 │
│  7. Player never waits                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why SSE (Not WebSocket)

| Requirement | SSE | WebSocket |
|-------------|-----|-----------|
| Server → Client push | ✓ | ✓ |
| Client → Server | Not needed (use HTTP POST) | ✓ (overkill) |
| Complexity | Low | Higher |
| Auto-reconnect | Built-in | Manual |
| HTTP/2 compatible | Yes | Separate protocol |

**Decision: Use SSE for scene updates.**

Player actions (clicks) go through normal HTTP. Scene tree updates push via SSE.

---

## API Design

### Click Action (HTTP POST)

```
POST /api/scene/click
Content-Type: application/json

{
  "scene_id": "camp_night",
  "word": "blade",
  "path": ["root"]  // breadcrumb to current position in tree
}
```

**Response:**

```json
{
  "status": "ok",
  "response_cached": true,
  "generation_queued": true
}
```

- `response_cached: true` — Frontend can show response immediately
- `generation_queued: true` — Backend is generating next layer

### Scene Updates (SSE)

```
GET /api/scene/stream
Accept: text/event-stream
```

**Events:**

```
event: scene_update
data: {
  "scene_id": "camp_night",
  "path": ["root", "blade"],
  "clickables": {
    "Wulfric": {
      "speaks": "Who was Wulfric?",
      "intent": "ask_about_family",
      "response": { ... }
    },
    "hands": {
      "speaks": "Your hands stopped.",
      "intent": "observation",
      "response": { ... }
    }
  }
}

event: generation_complete
data: {
  "scene_id": "camp_night",
  "path": ["root", "blade"],
  "depth": 1
}
```

### Scene State (HTTP GET)

For initial load or reconnection:

```
GET /api/scene/{scene_id}
```

Returns full scene tree with all currently-generated responses.

---

## Frontend Responsibilities

1. **On scene load:** Connect to SSE stream, fetch initial scene state
2. **On click:**
   - Immediately render cached response (optimistic)
   - POST click to backend
   - If `response_cached: false`, show brief loading state
3. **On SSE `scene_update`:** Patch scene tree at specified path
4. **On disconnect:** Reconnect SSE, fetch current state to sync

---

## Backend Responsibilities

1. **Scene generation:** Call narrator with `--continue`, parse JSON output
2. **Caching:** Store scene trees in memory/Redis, keyed by `scene_id`
3. **Background generation:** Queue layer 2 generation on click
4. **SSE broadcast:** Push updates to connected clients for that scene
5. **Graph tick:** After `time_elapsed`, run graph tick, check for flips

---

## Generation Queue

Use a simple job queue (Redis, or in-memory for MVP):

```python
@on_click(scene_id, word, path)
def handle_click():
    # 1. Return cached response immediately
    response = cache.get(scene_id, path + [word])

    # 2. Queue generation for new clickables
    for clickable in response.clickables:
        if not cache.has(scene_id, path + [word, clickable]):
            queue.enqueue(generate_response, scene_id, path + [word, clickable])

    return response

@worker
def generate_response(scene_id, path):
    # 1. Call narrator
    response = narrator.generate(scene_id, path)

    # 2. Cache it
    cache.set(scene_id, path, response)

    # 3. Push to frontend
    sse.broadcast(scene_id, {
        "event": "scene_update",
        "path": path[:-1],  # parent path
        "clickables": { path[-1]: response }
    })
```

---

## Edge Cases

### Player clicks before generation completes

Show brief loading indicator ("Aldric considers..."). SSE will push response when ready.

```
event: generation_started
data: { "path": ["root", "blade", "Wulfric"], "eta_ms": 2000 }
```

### Player clicks rapidly (skips ahead)

Each click queues generation. Later clicks may arrive before earlier ones complete. Frontend should handle out-of-order updates gracefully (patch by path).

### Reconnection

On SSE reconnect, frontend should:
1. Fetch current scene state via HTTP GET
2. Diff against local state
3. Patch any missing responses

---

## Narrator Prompt Implications

The narrator CLAUDE.md has been updated to reflect:

- **Layer 1:** Always generate (every clickable has a response)
- **Layer 2:** Rolling window — generated in background

The narrator doesn't need to know about SSE/HTTP. It just generates scene packages on demand.

---

## Open Questions

1. **Prioritization:** If player is clicking fast, which paths to generate first? (Suggest: most recent click path)

2. **TTL:** How long to cache scene trees? (Suggest: per-session, cleared on scene change or graph flip)

3. **Prefetch heuristics:** Should we predict likely clicks and pre-generate? (Suggest: defer to V2)

---

## Files Changed

- `agents/narrator/CLAUDE.md` — Updated depth strategy to rolling window
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` — This file

---

## Next Steps

1. [ ] Implement SSE endpoint (`/api/scene/stream`)
2. [ ] Implement click handler (`POST /api/scene/click`)
3. [ ] Implement generation queue (Redis or in-memory)
4. [ ] Frontend: SSE client + scene tree patching
5. [ ] Frontend: Loading state for uncached responses

---

*"The player never waits. The narrator works ahead. The backend orchestrates."*
