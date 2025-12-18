# Implementation Guide: Phase 1 — Core Moment Graph

```
STATUS: Implementation Guide
CREATED: 2024-12-17
PHASE: 1 (MVP)
GOAL: Instant click traversal, no LLM on hot path
```

Phase 1 is the foundation. If click traversal isn't instant (<50ms), nothing else matters.

---

## What Phase 1 Delivers

| Feature | Rating | Player Experience |
|---------|--------|-------------------|
| Click Traversal | 10/10 | Instant response, no waiting |
| Weight-Based Surfacing | 8/10 | Curated without scripted |
| Presence Gating | 9/10 | Context-aware conversations |
| Persistence | 9/10 | NPCs remember mid-conversation |
| Speaker Resolution | 8/10 | Groups feel organic |
| Multiple Entry Points | 9/10 | No "missed content" anxiety |

---

## New Files to Create

### 1. `engine/moment_graph/__init__.py`

```python
"""
Blood Ledger — Moment Graph Engine

Core mechanics for instant-response dialogue traversal.
No LLM on hot path. Pure graph operations.
"""

from .traversal import MomentTraversal
from .queries import MomentQueries
from .surface import MomentSurface

__all__ = ['MomentTraversal', 'MomentQueries', 'MomentSurface']
```

### 2. `engine/moment_graph/queries.py`

```python
"""
Moment Graph — Query Layer

Fast queries for the moment graph. All operations must be <50ms.
"""

import logging
from typing import List, Dict, Any, Optional, Set
from engine.db import GraphQueries

logger = logging.getLogger(__name__)


class MomentQueries:
    """
    Query layer for moment graph operations.

    All methods must be fast (<50ms). No LLM calls.
    """

    def __init__(self, graph_name: str = "blood_ledger"):
        self.read = GraphQueries(graph_name=graph_name)

    def get_current_view(
        self,
        player_id: str,
        location_id: str,
        present_chars: List[str],
        present_things: List[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Get all visible moments for current scene.

        This is THE core query. Must be instant.

        Args:
            player_id: Player character ID
            location_id: Current place ID
            present_chars: Character IDs present
            present_things: Thing IDs present (optional)
            limit: Max moments to return

        Returns:
            {
                "moments": [moment dicts],
                "transitions": [transition dicts],
                "active_count": int
            }
        """
        present_things = present_things or []

        # Build presence set for gating
        present_set = set([player_id, location_id] + present_chars + present_things)

        # Query: Get moments where all presence_required targets are present
        cypher = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']

        // Get all presence-required attachments
        OPTIONAL MATCH (m)-[r:ATTACHED_TO {presence_required: true}]->(target)

        // Collect required targets
        WITH m, collect(target.id) AS required_targets

        // Filter: all required must be in present set
        WHERE ALL(req IN required_targets WHERE req IN $present_set)

        RETURN m.id AS id,
               m.text AS text,
               m.type AS type,
               m.status AS status,
               m.weight AS weight,
               m.tone AS tone,
               required_targets

        ORDER BY m.weight DESC
        LIMIT $limit
        """

        moments = self.read.query(cypher, {
            "present_set": list(present_set),
            "limit": limit
        })

        # Get transitions for active moments
        active_ids = [m['id'] for m in moments if m.get('status') == 'active']
        transitions = self._get_transitions(active_ids) if active_ids else []

        return {
            "moments": moments,
            "transitions": transitions,
            "active_count": len(active_ids)
        }

    def _get_transitions(self, moment_ids: List[str]) -> List[Dict]:
        """Get CAN_LEAD_TO links from given moments."""
        if not moment_ids:
            return []

        cypher = """
        MATCH (m:Moment)-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE m.id IN $ids
        AND next.status IN ['possible', 'active']
        RETURN m.id AS from_id,
               next.id AS to_id,
               r.trigger AS trigger,
               r.require_words AS require_words,
               r.weight_transfer AS weight_transfer,
               r.consumes_origin AS consumes_origin
        """

        return self.read.query(cypher, {"ids": moment_ids})

    def get_moment_by_id(self, moment_id: str) -> Optional[Dict]:
        """Get a single moment by ID."""
        cypher = """
        MATCH (m:Moment {id: $id})
        RETURN m
        """
        results = self.read.query(cypher, {"id": moment_id})
        return results[0] if results else None

    def find_click_targets(
        self,
        moment_id: str,
        word: str
    ) -> List[Dict]:
        """
        Find moments reachable by clicking a word.

        Args:
            moment_id: Current active moment
            word: Word that was clicked

        Returns:
            List of target moments that match the word
        """
        word_lower = word.lower()

        cypher = """
        MATCH (m:Moment {id: $moment_id})-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE r.trigger = 'click'
        AND next.status IN ['possible', 'active']
        RETURN next.id AS id,
               next.text AS text,
               next.type AS type,
               r.require_words AS require_words,
               r.weight_transfer AS weight_transfer,
               r.consumes_origin AS consumes_origin
        """

        candidates = self.read.query(cypher, {"moment_id": moment_id})

        # Filter by word match
        matches = []
        for c in candidates:
            require_words = c.get('require_words', [])
            if isinstance(require_words, str):
                import json
                require_words = json.loads(require_words)

            # Check if clicked word matches any required word
            for req in require_words:
                if req.lower() in word_lower or word_lower in req.lower():
                    matches.append(c)
                    break

        return matches

    def get_speaker_for_moment(
        self,
        moment_id: str,
        present_chars: List[str]
    ) -> Optional[str]:
        """
        Determine who speaks a moment based on CAN_SPEAK weights.

        Args:
            moment_id: The moment to speak
            present_chars: Characters currently present

        Returns:
            Character ID of speaker, or None
        """
        cypher = """
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $moment_id})
        WHERE c.id IN $present
        RETURN c.id AS speaker_id, r.weight AS weight
        ORDER BY r.weight DESC
        LIMIT 1
        """

        results = self.read.query(cypher, {
            "moment_id": moment_id,
            "present": present_chars
        })

        return results[0]['speaker_id'] if results else None

    def get_dormant_moments(
        self,
        location_id: str
    ) -> List[Dict]:
        """Get dormant moments attached to a location."""
        cypher = """
        MATCH (m:Moment {status: 'dormant'})-[:ATTACHED_TO]->(p:Place {id: $loc_id})
        RETURN m.id AS id, m.text AS text, m.weight AS weight
        """
        return self.read.query(cypher, {"loc_id": location_id})

    def get_wait_triggers(
        self,
        tick: int
    ) -> List[Dict]:
        """Get moments that should auto-fire based on wait time."""
        cypher = """
        MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO {trigger: 'wait'}]->(next:Moment)
        WHERE ($tick - m.tick_spoken) >= r.wait_ticks
        AND next.status IN ['possible', 'active']
        RETURN m.id AS from_id,
               next.id AS to_id,
               r.weight_transfer AS weight_transfer,
               r.consumes_origin AS consumes_origin
        """
        return self.read.query(cypher, {"tick": tick})
```

### 3. `engine/moment_graph/traversal.py`

```python
"""
Moment Graph — Traversal Engine

Handles click traversal, weight updates, and moment state transitions.
"""

import logging
from typing import Dict, Any, Optional, List
from engine.db import GraphOps
from .queries import MomentQueries

logger = logging.getLogger(__name__)


class MomentTraversal:
    """
    Handles moment graph traversal.

    Core operations:
    - Click a word -> traverse to linked moment
    - Update weights on traversal
    - Mark moments as spoken
    - Create THEN links for history
    """

    def __init__(self, graph_name: str = "blood_ledger"):
        self.queries = MomentQueries(graph_name=graph_name)
        self.write = GraphOps(graph_name=graph_name)

    def handle_click(
        self,
        moment_id: str,
        word: str,
        tick: int,
        player_id: str = "char_player"
    ) -> Optional[Dict]:
        """
        Handle player clicking a word in a moment.

        This is THE hot path. Must be <50ms total.

        Args:
            moment_id: Current active moment
            word: Word that was clicked
            tick: Current world tick
            player_id: Player character ID

        Returns:
            Target moment dict if found, None otherwise
        """
        # 1. Find matching target
        matches = self.queries.find_click_targets(moment_id, word)
        if not matches:
            logger.debug(f"[Traversal] No match for '{word}' from {moment_id}")
            return None

        # 2. Use first match (highest implicit priority)
        target = matches[0]
        target_id = target['id']

        # 3. Apply weight transfer
        weight_transfer = target.get('weight_transfer', 0.3)
        self.write.boost_moment_weight(target_id, weight_transfer)

        # 4. Consume origin if configured
        if target.get('consumes_origin', True):
            self.write.update_moment_status(moment_id, 'spoken', tick)

        # 5. Activate target
        self.write.update_moment_status(target_id, 'active', tick)

        # 6. Create THEN link (history)
        self._create_then_link(moment_id, target_id, tick, player_caused=True)

        logger.info(f"[Traversal] Click: {moment_id} --[{word}]--> {target_id}")

        return target

    def activate_moment(
        self,
        moment_id: str,
        tick: int
    ) -> None:
        """Activate a moment (make it visible/triggerable)."""
        self.write.update_moment_status(moment_id, 'active', tick)

    def speak_moment(
        self,
        moment_id: str,
        tick: int,
        speaker_id: str = None
    ) -> None:
        """Mark moment as spoken and create SAID link if speaker."""
        self.write.update_moment_status(moment_id, 'spoken', tick)
        if speaker_id:
            self.write.add_said(speaker_id, moment_id)

    def make_dormant(
        self,
        moment_id: str
    ) -> None:
        """Set moment to dormant (waiting for return)."""
        self.write.update_moment_status(moment_id, 'dormant')

    def decay_moment(
        self,
        moment_id: str,
        tick: int
    ) -> None:
        """Mark moment as decayed (pruned)."""
        self.write.update_moment_status(moment_id, 'decayed', tick)

    def reactivate_dormant(
        self,
        location_id: str,
        tick: int
    ) -> List[str]:
        """
        Reactivate dormant moments when player returns to location.

        Args:
            location_id: Place the player arrived at
            tick: Current tick

        Returns:
            List of moment IDs that were reactivated
        """
        dormant = self.queries.get_dormant_moments(location_id)
        reactivated = []

        for m in dormant:
            self.write.update_moment_status(m['id'], 'possible')
            # Restore some weight
            self.write.update_moment_weight(m['id'], max(0.3, m.get('weight', 0.3)))
            reactivated.append(m['id'])

        logger.info(f"[Traversal] Reactivated {len(reactivated)} dormant moments at {location_id}")
        return reactivated

    def _create_then_link(
        self,
        from_id: str,
        to_id: str,
        tick: int,
        player_caused: bool = False
    ) -> None:
        """Create THEN link with tick and causation info."""
        cypher = """
        MATCH (m1:Moment {id: $from_id})
        MATCH (m2:Moment {id: $to_id})
        MERGE (m1)-[r:THEN]->(m2)
        SET r.tick = $tick, r.player_caused = $player_caused
        """
        self.write._query(cypher, {
            "from_id": from_id,
            "to_id": to_id,
            "tick": tick,
            "player_caused": player_caused
        })
```

### 4. `engine/moment_graph/surface.py`

```python
"""
Moment Graph — Surface Engine

Determines which moments should surface (become active).
Handles weight-based activation and decay.
"""

import logging
from typing import Dict, Any, List
from engine.db import GraphOps, GraphQueries

logger = logging.getLogger(__name__)

# Thresholds
ACTIVATION_THRESHOLD = 0.8   # Weight needed to flip possible -> active
DECAY_THRESHOLD = 0.1        # Below this, moment decays
DECAY_RATE = 0.99            # Per-tick weight multiplier


class MomentSurface:
    """
    Manages moment surfacing and decay.

    No LLM. Pure mechanical weight calculations.
    """

    def __init__(self, graph_name: str = "blood_ledger"):
        self.read = GraphQueries(graph_name=graph_name)
        self.write = GraphOps(graph_name=graph_name)

    def check_for_flips(self) -> List[Dict]:
        """
        Check for moments that should flip from possible to active.

        Returns:
            List of moments that flipped
        """
        cypher = """
        MATCH (m:Moment {status: 'possible'})
        WHERE m.weight >= $threshold
        SET m.status = 'active'
        RETURN m.id AS id, m.weight AS weight
        """
        flipped = self.write._query(cypher, {"threshold": ACTIVATION_THRESHOLD})
        if flipped:
            logger.info(f"[Surface] {len(flipped)} moments flipped to active")
        return flipped

    def apply_decay(self, tick: int) -> int:
        """
        Apply weight decay to all possible/active moments.

        Returns:
            Number of moments that decayed below threshold
        """
        # Decay weights
        cypher_decay = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        SET m.weight = m.weight * $decay_rate
        """
        self.write._query(cypher_decay, {"decay_rate": DECAY_RATE})

        # Mark decayed
        cypher_prune = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        AND m.weight < $threshold
        SET m.status = 'decayed', m.tick_decayed = $tick
        RETURN count(m) AS count
        """
        result = self.write._query(cypher_prune, {
            "threshold": DECAY_THRESHOLD,
            "tick": tick
        })
        decayed_count = result[0][0] if result else 0

        if decayed_count > 0:
            logger.info(f"[Surface] {decayed_count} moments decayed")

        return decayed_count

    def tension_to_moments(
        self,
        tension_id: str,
        pressure: float
    ) -> List[str]:
        """
        Flow energy from tension to attached moments.

        Args:
            tension_id: Tension that has pressure
            pressure: Current tension pressure (0-1)

        Returns:
            List of moment IDs that received boost
        """
        # Find attached moments
        cypher = """
        MATCH (m:Moment)-[:ATTACHED_TO]->(t:Tension {id: $tension_id})
        WHERE m.status IN ['possible', 'active']
        SET m.weight = CASE
            WHEN m.weight + ($pressure * 0.2) > 1.0 THEN 1.0
            ELSE m.weight + ($pressure * 0.2)
        END
        RETURN m.id AS id
        """
        boosted = self.write._query(cypher, {
            "tension_id": tension_id,
            "pressure": pressure
        })

        ids = [b[0] for b in boosted] if boosted else []
        if ids:
            logger.debug(f"[Surface] Tension {tension_id} boosted {len(ids)} moments")
        return ids

    def handle_scene_change(
        self,
        old_location: str,
        new_location: str
    ) -> Dict[str, int]:
        """
        Handle moment state changes on scene transition.

        Args:
            old_location: Place player left
            new_location: Place player arrived at

        Returns:
            {"dormant": count, "pruned": count, "reactivated": count}
        """
        stats = {"dormant": 0, "pruned": 0, "reactivated": 0}

        # 1. Dormant persistent moments at old location
        cypher_dormant = """
        MATCH (m:Moment)-[r:ATTACHED_TO {persistent: true}]->(p:Place {id: $old_loc})
        WHERE m.status IN ['possible', 'active']
        SET m.status = 'dormant'
        RETURN count(m) AS count
        """
        result = self.write._query(cypher_dormant, {"old_loc": old_location})
        stats["dormant"] = result[0][0] if result else 0

        # 2. Prune non-persistent moments at old location
        cypher_prune = """
        MATCH (m:Moment)-[r:ATTACHED_TO {persistent: false}]->(p:Place {id: $old_loc})
        WHERE m.status IN ['possible', 'active']
        SET m.status = 'decayed'
        RETURN count(m) AS count
        """
        result = self.write._query(cypher_prune, {"old_loc": old_location})
        stats["pruned"] = result[0][0] if result else 0

        # 3. Reactivate dormant moments at new location
        cypher_reactivate = """
        MATCH (m:Moment {status: 'dormant'})-[:ATTACHED_TO]->(p:Place {id: $new_loc})
        SET m.status = 'possible', m.weight = CASE WHEN m.weight < 0.3 THEN 0.3 ELSE m.weight END
        RETURN count(m) AS count
        """
        result = self.write._query(cypher_reactivate, {"new_loc": new_location})
        stats["reactivated"] = result[0][0] if result else 0

        logger.info(f"[Surface] Scene change: {stats}")
        return stats
```

---

## Integration: Update GraphTick

Add moment surfacing to `engine/physics/tick.py`:

```python
# Add import at top
from engine.moment_graph.surface import MomentSurface

# In GraphTick.__init__:
self.moment_surface = MomentSurface(graph_name=graph_name)

# In GraphTick.run(), after tension processing:

# 9. Apply moment decay
self.moment_surface.apply_decay(current_tick)

# 10. Flow tension energy to moments
for tension in tensions:
    self.moment_surface.tension_to_moments(
        tension_id=tension['id'],
        pressure=tension.get('pressure', 0)
    )

# 11. Check for moment flips
moment_flips = self.moment_surface.check_for_flips()
result.moment_flips = moment_flips
```

---

## Integration: Update MomentProcessor

Modify `engine/memory/moment_processor.py` to set proper status:

```python
# In process_dialogue, process_narration, process_player_action, process_hint:

# Change:
self.ops.add_moment(
    id=moment_id,
    text=text,
    type="dialogue",
    tick=self._current_tick,
    # ... other args
)

# To:
self.ops.add_moment(
    id=moment_id,
    text=text,
    type="dialogue",
    tick=self._current_tick,
    status="spoken",  # Explicitly spoken (transcript moments)
    weight=0.5,
    # ... other args
)
```

---

## API Endpoint (Optional)

If using REST API, add to `engine/api/app.py`:

```python
from engine.moment_graph import MomentTraversal, MomentQueries

moment_queries = MomentQueries()
moment_traversal = MomentTraversal()

@app.get("/moment/view")
def get_moment_view(
    player_id: str,
    location_id: str,
    present_chars: str  # Comma-separated
):
    """Get current visible moments."""
    chars = present_chars.split(",") if present_chars else []
    return moment_queries.get_current_view(player_id, location_id, chars)

@app.post("/moment/click")
def handle_moment_click(
    moment_id: str,
    word: str,
    tick: int,
    player_id: str = "char_player"
):
    """Handle clicking a word in a moment."""
    result = moment_traversal.handle_click(moment_id, word, tick, player_id)
    if result:
        return {"success": True, "target": result}
    return {"success": False, "message": "No matching transition"}
```

---

## Testing Phase 1

### Test 1: Click Traversal Performance

```python
import time
from engine.moment_graph import MomentTraversal, MomentQueries

queries = MomentQueries()
traversal = MomentTraversal()

# Setup: Create test moments
# ... (see mutations/example_moment_graph.yaml)

# Test: Click traversal must be <50ms
start = time.time()
result = traversal.handle_click("moment_aldric_about_brother", "brother", tick=100)
elapsed = (time.time() - start) * 1000

assert elapsed < 50, f"Click traversal too slow: {elapsed}ms"
print(f"Click traversal: {elapsed:.1f}ms")
```

### Test 2: Presence Gating

```python
# Setup: Moment attached to char_aldric with presence_required=True
# ...

# Test: Moment visible when Aldric present
view = queries.get_current_view(
    player_id="char_player",
    location_id="place_camp",
    present_chars=["char_aldric"]
)
assert any(m['id'] == 'moment_aldric_about_brother' for m in view['moments'])

# Test: Moment NOT visible when Aldric absent
view = queries.get_current_view(
    player_id="char_player",
    location_id="place_camp",
    present_chars=[]  # No Aldric
)
assert not any(m['id'] == 'moment_aldric_about_brother' for m in view['moments'])
```

### Test 3: Dormant/Reactivate

```python
from engine.moment_graph import MomentSurface

surface = MomentSurface()

# Setup: Active moment at old location
# ...

# Test: Scene change makes it dormant
stats = surface.handle_scene_change("place_camp", "place_york")
assert stats['dormant'] > 0

# Test: Return reactivates
stats = surface.handle_scene_change("place_york", "place_camp")
assert stats['reactivated'] > 0
```

---

## Phase 1 Checklist

- [ ] `engine/moment_graph/__init__.py` created
- [ ] `engine/moment_graph/queries.py` created with `MomentQueries`
- [ ] `engine/moment_graph/traversal.py` created with `MomentTraversal`
- [ ] `engine/moment_graph/surface.py` created with `MomentSurface`
- [ ] `GraphTick` updated to include moment decay and tension flow
- [ ] `MomentProcessor` updated to set `status="spoken"`
- [ ] Click traversal tested at <50ms
- [ ] Presence gating tested
- [ ] Dormant/reactivate tested

---

## What Phase 1 Does NOT Include

- Semantic matching (Phase 2)
- Citizen/character background generation (Phase 3)
- Social dynamics (Phase 4)
- Natural dynamics (Phase 5)

These require LLM. Phase 1 is pure graph operations.

---

*"Click. Response. Instant. That's the foundation."*
