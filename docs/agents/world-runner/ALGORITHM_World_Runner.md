# World Runner — Algorithm: How It Works

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## Core Principle: Runner Owns the Tick Loop

The Runner advances time in 5-minute ticks, checks for flips, and stops only when the player is affected or time runs out.

```python
def run_world(action, max_minutes, player_context):
    minutes = 0
    world_changes = []
    news = []

    while minutes < max_minutes:
        result = run_graph_tick(elapsed_minutes=5)
        minutes += 5

        for flip in result.flips:
            if affects_player(flip, player_context, minutes):
                event = process_flip_for_player(flip)
                return Injection(
                    interrupted=True,
                    at_minute=minutes,
                    remaining=max_minutes - minutes,
                    event=event,
                    world_changes=world_changes,
                    news_available=news
                )

        for flip in result.flips:
            world_changes.extend(process_flip_background(flip))

        news.extend(propagate_news(minutes))

    return Injection(
        interrupted=False,
        completed=True,
        time_elapsed=max_minutes,
        world_changes=world_changes,
        news_available=news
    )
```

---

## Player Intersection (`affects_player`)

```python
def affects_player(flip, player_context, current_tick):
    player_loc = player_location_at_tick(player_context, current_tick)

    if flip.location == player_loc:
        return True
    if "char_player" in flip.involved_characters:
        return True
    if any(c in player_context.companions for c in flip.involved_characters):
        return True
    if flip.urgency == "critical" and nearby(flip.location, player_loc):
        return True

    return False
```

---

## Algorithm Steps (Condensed)

1. **Tick:** Update tension pressure, narrative weight, and decay.
2. **Detect flips:** Tensions over breaking point become flip candidates.
3. **Process flips:**
   - Player-affecting flip → generate `Event` and return interrupted Injection.
   - Non-player flip → create narratives/beliefs/tensions as background changes.
4. **Propagate news:** News spreads based on time and significance.
5. **Return Injection:** Completed or interrupted with world changes and news.

---

## Stateless Between Calls

Each call is independent. The graph is the memory.

---

## Cluster Context for Flips

For any flip, return a compact cluster of linked nodes (tension, narratives, key characters, and places). Cap total nodes (~30). This gives the Narrator enough context to write the scene without dumping the full graph.

---

## CHAIN

PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
INPUTS:          ./INPUT_REFERENCE.md
TOOLS:           ./TOOL_REFERENCE.md
SYNC:            ./SYNC_World_Runner.md
