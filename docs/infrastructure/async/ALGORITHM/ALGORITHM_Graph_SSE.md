# Async Architecture - Algorithm: Graph SSE

**Purpose:** Graph SSE events and frontend consumption.

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Async_Architecture.md
BEHAVIORS:      ../BEHAVIORS_Travel_Experience.md
VALIDATION:     ../VALIDATION_Async_Architecture.md
IMPLEMENTATION: ../IMPLEMENTATION_Async_Architecture.md
OVERVIEW:       ALGORITHM_Overview.md
THIS:           ALGORITHM_Graph_SSE.md (you are here)
SYNC:           ../SYNC_Async_Architecture.md
```

---

## Graph SSE

**Purpose:** How the graph streams state changes to the frontend in real-time.

### Principle

Graph streams **location and image events only**.
- `position_update` - player moved
- `image_ready` - place image generated

NOT every graph write. Just these two event types.
Frontend subscribes once, receives what it needs for real-time map/image updates.

### Connection

Frontend establishes SSE connection on load:

```javascript
const eventSource = new EventSource('/api/graph/stream?playthrough=default');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleGraphEvent(data);
};
```

### Event Types

**position_update**

Trigger: Runner updates player position in graph

```json
{
  "type": "position_update",
  "player_id": "char_rolf",
  "current_place": "place_humber_crossing"
}
```

Frontend Action: Update current location display, animate if map exists

**image_ready**

Trigger: Image generation completes for place; frontend updates the left panel if the place matches the current location.

### Backend Implementation

**Position Update**

When Runner updates player position:

```python
def update_player_position(player_id, place_id):
    # Write to graph
    graph.set_property(player_id, "current_place", place_id)

    # Emit SSE
    sse_manager.broadcast({
        "type": "position_update",
        "player_id": player_id,
        "current_place": place_id
    })
```

**Image Ready**

When image generation completes:

```python
def on_image_generated(place_id, image_url):
    # Update graph
    graph.set_property(place_id, "image_url", image_url)

    # Emit SSE
    sse_manager.broadcast({
        "type": "image_ready",
        "place_id": place_id,
        "image_url": image_url
    })
```

**SSE Manager**

Maintain a per-playthrough subscriber list and broadcast JSON events to connected clients.

### Frontend Handling

Dispatch `position_update` to the map/position UI and `image_ready` to the left panel when it matches the current place.

### Connection Management

**Reconnection**

```javascript
eventSource.onerror = () => {
  eventSource.close();
  setTimeout(() => {
    reconnectSSE();
  }, 1000);
};
```

**Cleanup**

```javascript
// On unmount
eventSource.close();
```

### Performance Considerations

Keep payloads small, maintain one connection per client, and debounce rapid updates on the frontend.
