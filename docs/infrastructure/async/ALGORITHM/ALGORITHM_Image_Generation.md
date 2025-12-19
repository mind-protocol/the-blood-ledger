# Async Architecture - Algorithm: Image Generation

**Purpose:** Automatic image generation when places enter the graph.

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Async_Architecture.md
BEHAVIORS:      ../BEHAVIORS_Travel_Experience.md
VALIDATION:     ../VALIDATION_Async_Architecture.md
IMPLEMENTATION: ../IMPLEMENTATION_Async_Architecture.md
OVERVIEW:       ALGORITHM_Overview.md
THIS:           ALGORITHM_Image_Generation.md (you are here)
SYNC:           ../SYNC_Async_Architecture.md
```

---

## Image Generation

**Purpose:** How place images generate automatically.

### Principle

Images generate automatically when places enter graph.
No manual trigger. Graph handles it.
Frontend receives `image_ready` via SSE.

### Trigger

Place node created in graph -> image generation queued

### Process

```
1. Place created in graph
2. Graph queues image generation (background task)
3. Generator creates image from place attributes
4. Image saved to frontend/public/images/places/
5. Graph updates place.image_url
6. Graph SSE broadcasts image_ready
7. Frontend updates if current place
```

### Prompt Construction

**Inputs:**
- `place.type`
- `place.name`
- `place.terrain`
- `place.atmosphere`
- Current `time_of_day`
- Current `weather`

**Format:**
```
Medieval England, 1068. {time_of_day}. {weather}.
{place.type}: {place.name}
{place.terrain}
{place.atmosphere}
Muted colors, atmospheric, painterly.
No people in frame. Landscape only.
```

### Output

| Property | Value |
|----------|-------|
| Format | PNG |
| Aspect | 1:3 (tall, atmospheric) |
| Storage | `frontend/public/images/places/{place_id}.png` |
| URL in graph | `/images/places/{place_id}.png` |

### Implementation

```python
async def generate_place_image(place):
    prompt = build_image_prompt(place)

    # Generate image (async)
    image_data = await image_generator.generate(
        prompt=prompt,
        aspect_ratio="1:3",
        style="painterly"
    )

    # Save to disk
    path = f"frontend/public/images/places/{place['id']}.png"
    save_image(image_data, path)

    # Update graph
    url = f"/images/places/{place['id']}.png"
    graph.set_property(place['id'], "image_url", url)

    # SSE broadcast happens automatically from graph
```

### Graph Hook

When place is created, graph triggers generation:

```python
def on_place_created(place):
    # Broadcast place_created (no image yet)
    sse_manager.broadcast({
        "type": "place_created",
        "place_id": place["id"],
        "name": place["name"],
        "image_url": None
    })

    # Queue image generation
    background_tasks.add(generate_place_image(place))
```

When image is ready:

```python
def on_image_ready(place_id, image_url):
    sse_manager.broadcast({
        "type": "image_ready",
        "place_id": place_id,
        "image_url": image_url
    })
```
