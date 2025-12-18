# Graph SSE — Algorithm

**Purpose:** How the graph streams state changes to the frontend in real-time.

---

## Principle

Graph streams **location and image events only**.
- `position_update` — player moved
- `image_ready` — place image generated

NOT every graph write. Just these two event types.
Frontend subscribes once, receives what it needs for real-time map/image updates.

---

## Connection

Frontend establishes SSE connection on load:

```javascript
const eventSource = new EventSource('/api/graph/stream?playthrough=default');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleGraphEvent(data);
};
```

---

## Event Types

### position_update

**Trigger:** Runner updates player position in graph

```json
{
  "type": "position_update",
  "player_id": "char_rolf",
  "current_place": "place_humber_crossing"
}
```

**Frontend Action:** Update current location display, animate if map exists

---

### image_ready

**Trigger:** Image generation completes for place

```json
{
  "type": "image_ready",
  "place_id": "place_humber_crossing",
  "image_url": "/images/places/place_humber_crossing.png"
}
```

**Frontend Action:** Update left panel if current place, cache image

---

## Backend Implementation

### Position Update

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

### Image Ready

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

### SSE Manager

```python
class SSEManager:
    def __init__(self):
        self.clients = {}  # playthrough_id -> list of response objects

    def subscribe(self, playthrough_id, response):
        if playthrough_id not in self.clients:
            self.clients[playthrough_id] = []
        self.clients[playthrough_id].append(response)

    def broadcast(self, playthrough_id, event):
        for client in self.clients.get(playthrough_id, []):
            client.send(json.dumps(event))
```

---

## Frontend Handling

```javascript
function handleGraphEvent(event) {
  switch (event.type) {
    case 'position_update':
      updateCurrentPlace(event.current_place);
      break;

    case 'image_ready':
      if (event.place_id === currentPlace) {
        updateLeftPanel(event.image_url);
      }
      break;
  }
}
```

---

## Connection Management

### Reconnection

```javascript
eventSource.onerror = () => {
  eventSource.close();
  setTimeout(() => {
    reconnectSSE();
  }, 1000);
};
```

### Cleanup

```javascript
// On unmount
eventSource.close();
```

---

## Performance Considerations

- Events are small JSON payloads
- One connection per client (not per event type)
- Server buffers events during disconnect, replays on reconnect
- Frontend debounces rapid position updates for smooth animation
