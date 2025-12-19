# DOCS: docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md
"""
Tempo Controller — Main game loop for moment surfacing.

Manages game speed and coordinates:
- Physics ticking (GraphTick)
- Canon surfacing (CanonHolder)
- SSE broadcasting

Specs:
- docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md
- docs/infrastructure/tempo/BEHAVIORS_Tempo.md
- docs/infrastructure/tempo/VALIDATION_Tempo.md
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Literal, Optional

from engine.physics.graph import GraphQueries
from engine.physics import GraphTick
from engine.infrastructure.canon import CanonHolder

logger = logging.getLogger(__name__)

# Constants
SALIENCE_THRESHOLD = 0.3
MAX_MOMENTS_PER_TICK = 3
BACKPRESSURE_LIMIT = 5

Speed = Literal['pause', '1x', '2x', '3x']


class TempoController:
    """
    Main game loop controller.

    Manages speed settings and moment surfacing:
    - Pause: Player-driven, one moment per input
    - 1x: Real-time presence, all moments display
    - 2x: Fast travel, dialogue + high weight only
    - 3x: Maximum speed, only interrupts display
    """

    def __init__(
        self,
        playthrough_id: str,
        graph_name: str = None,
        host: str = "localhost",
        port: int = 6379
    ):
        from engine.physics.graph.graph_queries import get_playthrough_graph_name

        self.playthrough_id = playthrough_id
        self.graph_name = graph_name or get_playthrough_graph_name(playthrough_id)

        # State
        self.speed: Speed = '1x'
        self.running: bool = True
        self.last_tick: float = 0
        self.tick_count: int = 0
        self.display_queue_size: int = 0  # Tracked for backpressure

        # Components
        self.queries = GraphQueries(graph_name=self.graph_name, host=host, port=port)
        self.physics = GraphTick(graph_name=self.graph_name, host=host, port=port)
        self.canon = CanonHolder(playthrough_id, host=host, port=port)

        # Input event for pause mode
        self._input_event = asyncio.Event()
        self._pending_input: Optional[str] = None

        logger.info(f"[Tempo] Initialized for {playthrough_id} at {self.speed}")

    async def run(self):
        """Main game loop."""
        logger.info(f"[Tempo] Starting main loop for {self.playthrough_id}")

        while self.running:
            try:
                if self.speed == 'pause':
                    await self._wait_for_input()
                else:
                    await self._tick_continuous()
            except asyncio.CancelledError:
                logger.info(f"[Tempo] Loop cancelled for {self.playthrough_id}")
                break
            except Exception as e:
                logger.error(f"[Tempo] Error in main loop: {e}")
                await asyncio.sleep(1.0)  # Prevent tight loop on errors

        logger.info(f"[Tempo] Stopped for {self.playthrough_id}")

    def stop(self):
        """Stop the main loop."""
        if not self.running:
            return

        self.running = False
        self._pending_input = None
        self._input_event.set()  # Wake up if waiting
        logger.info(f"[Tempo] Stop requested for {self.playthrough_id}")

    def set_speed(self, speed: Speed, reason: str = "user"):
        """Change game speed."""
        old_speed = self.speed
        self.speed = speed

        # Broadcast speed change
        self._broadcast_speed_change(speed, reason)

        # Wake up input event if changing from pause
        if old_speed == 'pause' and speed != 'pause':
            self._input_event.set()

        logger.info(f"[Tempo] Speed changed: {old_speed} -> {speed} ({reason})")

    async def on_player_input(self, text: str) -> Dict[str, Any]:
        """
        Handle player input at any speed.

        Returns:
            Dict with moment_id and status
        """
        import uuid

        # Create player moment (status=possible)
        moment_id = f"mom_{uuid.uuid4().hex[:8]}"
        self._create_player_moment(moment_id, text)

        if self.speed == 'pause':
            # Signal input received
            self._pending_input = text
            self._input_event.set()
        elif self.speed == '3x':
            # Player input interrupts 3x
            self.set_speed('1x', 'player_input')

        return {'status': 'ok', 'moment_id': moment_id}

    def update_display_queue_size(self, size: int):
        """Called by frontend to report queue size for backpressure."""
        try:
            normalized = int(size)
        except (TypeError, ValueError):
            logger.warning(f"[Tempo] Invalid queue size: {size}")
            return

        if normalized < 0:
            logger.warning(f"[Tempo] Negative queue size {normalized}; clamping to 0")
            normalized = 0

        if normalized != self.display_queue_size:
            self.display_queue_size = normalized
            logger.debug(f"[Tempo] Queue size updated: {normalized}")

    # -------------------------------------------------------------------------
    # Private: Tick modes
    # -------------------------------------------------------------------------

    async def _wait_for_input(self):
        """Pause mode: wait for player input, then tick once."""
        self._input_event.clear()

        logger.debug(f"[Tempo] Waiting for input (pause mode)")
        await self._input_event.wait()

        if not self.running:
            return

        if self.speed != 'pause':
            # Speed was changed while waiting
            return

        # Tick once
        await self._tick_once()

        # Clear pending input
        self._pending_input = None

    async def _tick_once(self):
        """Single tick cycle (pause mode)."""
        # Run physics
        self.physics.tick()
        self.tick_count += 1

        # Detect ready moments
        ready = self._detect_ready_moments()

        if ready:
            # Process only first (highest salience) in pause mode
            moment = ready[0]
            result = self.canon.record_to_canon(
                moment_id=moment['id'],
                tick=self.tick_count
            )

            if result.get('status') == 'ok':
                logger.debug(f"[Tempo] Recorded moment {moment['id']} (pause mode)")

    async def _tick_continuous(self):
        """Continuous ticking (1x/2x/3x)."""
        interval = self._tick_interval()

        while self.speed != 'pause' and self.running:
            now = time.time()
            elapsed = now - self.last_tick

            if elapsed < interval:
                await asyncio.sleep(0.01)
                continue

            self.last_tick = now

            # Run physics
            self.physics.tick()
            self.tick_count += 1

            # Detect ready moments
            ready = self._detect_ready_moments()

            for moment in ready[:MAX_MOMENTS_PER_TICK]:
                # Record to canon (triggers SSE broadcast inside)
                result = self.canon.record_to_canon(
                    moment_id=moment['id'],
                    tick=self.tick_count
                )

                if result.get('status') != 'ok':
                    continue

                # Check interrupt at 2x/3x
                if self._check_interrupt(moment):
                    self.set_speed('1x', 'interrupt')
                    return  # Exit to main loop

            # Backpressure at 1x
            if self.speed == '1x' and self.display_queue_size > BACKPRESSURE_LIMIT:
                logger.debug(f"[Tempo] Backpressure: queue={self.display_queue_size}")
                await asyncio.sleep(1.0)  # Let frontend catch up

    def _tick_interval(self) -> float:
        """Get tick interval for current speed."""
        return {
            'pause': float('inf'),
            '1x': 1.0,
            '2x': 0.2,
            '3x': 0.01  # Near-instant
        }[self.speed]

    # -------------------------------------------------------------------------
    # Private: Moment detection (Q1 + Q2)
    # -------------------------------------------------------------------------

    def _detect_ready_moments(self) -> List[Dict]:
        """
        Q1 + Q2: Find moments ready to surface.

        Checks salience threshold and presence requirements.
        """
        # Q1: Salience check
        cypher = """
        MATCH (m:Moment)
        WHERE m.status = 'possible'
          AND (m.weight * m.energy) >= $threshold
        RETURN m.id AS id, m.weight AS weight, m.energy AS energy,
               m.type AS type, m.text AS text, m.interrupt AS interrupt
        ORDER BY (m.weight * m.energy) DESC
        """

        try:
            candidates = self.queries.query(cypher, {'threshold': SALIENCE_THRESHOLD})
        except Exception as e:
            logger.warning(f"[Tempo] Failed to query ready moments: {e}")
            return []

        if not candidates:
            return []

        # Get player location for presence check
        player_location = self._get_player_location()

        # Q2: Filter by presence requirements
        ready = []
        for m in candidates:
            if self._check_presence(m['id'], player_location):
                ready.append({
                    'id': m['id'],
                    'weight': m['weight'],
                    'energy': m['energy'],
                    'type': m['type'],
                    'text': m['text'],
                    'interrupt': m.get('interrupt', False)
                })

        return ready

    def _check_presence(self, moment_id: str, player_location: str) -> bool:
        """
        Q2: Check if moment's presence requirements are met.

        A moment is ready if all characters with presence_required=true
        are at the same location as the player.
        """
        cypher = """
        MATCH (m:Moment {id: $moment_id})-[att:ATTACHED_TO]->(c:Character)
        WHERE att.presence_required = true
        OPTIONAL MATCH (c)-[:AT {present: 1.0}]->(loc:Place)
        RETURN c.id AS char_id, loc.id AS char_location
        """

        try:
            attachments = self.queries.query(cypher, {'moment_id': moment_id})
        except Exception as e:
            logger.warning(f"[Tempo] Presence check failed for {moment_id}: {e}")
            return False

        if not attachments:
            # No presence requirements — always ready
            return True

        # All required characters must be at player location
        for att in attachments:
            if att['char_location'] != player_location:
                return False

        return True

    def _get_player_location(self) -> Optional[str]:
        """Q3: Get player's current location."""
        cypher = """
        MATCH (p:Character {id: 'char_player'})-[:AT {present: 1.0}]->(loc:Place)
        RETURN loc.id AS location_id
        """

        try:
            result = self.queries.query(cypher)
            if result:
                return result[0]['location_id']
        except Exception as e:
            logger.warning(f"[Tempo] Failed to get player location: {e}")

        return None

    # -------------------------------------------------------------------------
    # Private: Interrupt detection
    # -------------------------------------------------------------------------

    def _check_interrupt(self, moment: Dict) -> bool:
        """
        Check if moment should interrupt 2x/3x.

        Interrupts force snap back to 1x.
        """
        if self.speed == '1x':
            return False  # Already at 1x

        # Check moment's interrupt flag
        if moment.get('interrupt'):
            return True

        # Additional interrupt conditions could be checked here:
        # - Combat initiated
        # - Major arrival
        # - Decision point (CAN_LEAD_TO links)

        return False

    # -------------------------------------------------------------------------
    # Private: Player moment creation
    # -------------------------------------------------------------------------

    def _create_player_moment(self, moment_id: str, text: str):
        """Create a player input moment in the graph."""
        player_location = self._get_player_location()

        cypher = """
        CREATE (m:Moment {
            id: $moment_id,
            text: $text,
            type: 'action',
            status: 'possible',
            weight: 1.0,
            energy: 1.0,
            tick_created: $tick,
            player_input: true
        })
        """

        try:
            self.queries.query(cypher, {
                'moment_id': moment_id,
                'text': text,
                'tick': self.tick_count
            })

            # Attach to player location if known
            if player_location:
                attach_cypher = """
                MATCH (m:Moment {id: $moment_id}), (p:Place {id: $place_id})
                MERGE (m)-[:ATTACHED_TO {presence_required: false, persistent: false}]->(p)
                """
                self.queries.query(attach_cypher, {
                    'moment_id': moment_id,
                    'place_id': player_location
                })

            logger.debug(f"[Tempo] Created player moment: {moment_id}")

        except Exception as e:
            logger.warning(f"[Tempo] Failed to create player moment: {e}")

    # -------------------------------------------------------------------------
    # Private: SSE broadcasting
    # -------------------------------------------------------------------------

    def _broadcast_speed_change(self, speed: Speed, reason: str):
        """Broadcast speed_changed event to frontend."""
        try:
            # Lazy import to avoid circular dependency
            from engine.infrastructure.api.sse_broadcast import broadcast_moment_event

            broadcast_moment_event(
                self.playthrough_id,
                "speed_changed",
                {'speed': speed, 'reason': reason}
            )
        except Exception as e:
            logger.warning(f"[Tempo] Failed to broadcast speed change: {e}")
