"""
Canon Holder — Records moments to canon (spoken status).

DOCS: docs/infrastructure/canon/IMPLEMENTATION_Canon.md

This is the single gatekeeper. No moment reaches the player without passing through here.

Responsibilities:
1. Flip moment status: active → spoken
2. Set tick_spoken
3. Apply energy cost (60%)
4. Create THEN link to previous moment
5. Broadcast SSE event

See docs/infrastructure/canon/ALGORITHM_Canon_Holder.md for full spec.
"""

import logging
from typing import Optional, Dict, Any, List

from engine.physics.graph import GraphQueries, get_playthrough_graph_name
from .speaker import determine_speaker, get_moment_type

logger = logging.getLogger(__name__)

# Configuration
ACTUALIZATION_COST = 0.6  # 60% energy cost when speaking
MAX_MOMENTS_PER_TICK = 3  # Maximum moments to record per tick


class CanonHolder:
    """
    Canon Holder service for a specific playthrough.

    Handles recording moments to canon (spoken status) and
    broadcasting SSE events.
    """

    def __init__(
        self,
        playthrough_id: str,
        host: str = "localhost",
        port: int = 6379
    ):
        self.playthrough_id = playthrough_id
        self.host = host
        self.port = port
        self.graph_name = get_playthrough_graph_name(playthrough_id)
        self._queries = GraphQueries(
            graph_name=self.graph_name,
            host=host,
            port=port
        )

    def record_to_canon(
        self,
        moment_id: str,
        speaker_id: Optional[str] = None,
        previous_moment_id: Optional[str] = None,
        tick: int = 0,
        player_caused: bool = False
    ) -> Dict[str, Any]:
        """
        Record a moment to canon. This is THE function.

        Steps:
        1. Validate moment is active (not already spoken)
        2. Update status to 'spoken'
        3. Set tick_spoken
        4. Set speaker (if provided)
        5. Apply energy cost
        6. Create THEN link to previous
        7. Broadcast SSE

        Args:
            moment_id: The moment to record
            speaker_id: Who speaks it (None for narration)
            previous_moment_id: Previous moment for THEN link
            tick: Current game tick
            player_caused: Whether player action triggered this

        Returns:
            Dict with status, moment_id, and any errors
        """
        # 1. Get moment and validate
        moment = self._get_moment(moment_id)
        if not moment:
            logger.warning(f"[Canon] Moment not found: {moment_id}")
            return {"status": "error", "error": "moment_not_found"}

        if moment.get("status") == "spoken":
            logger.debug(f"[Canon] Moment already spoken: {moment_id}")
            return {"status": "already_spoken", "moment_id": moment_id}

        # 2. For dialogue, verify speaker
        moment_type = moment.get("type", "narration")
        if moment_type == "dialogue" and not speaker_id:
            # Try to find speaker
            speaker_id = determine_speaker(
                self.playthrough_id, moment_id,
                host=self.host, port=self.port
            )
            if not speaker_id:
                logger.debug(f"[Canon] No speaker for dialogue moment: {moment_id}")
                return {"status": "no_speaker", "moment_id": moment_id}

        # 3. Update moment in graph (Q6 Step 1)
        # Note: Speaker is NOT stored on moment - derived from SAID link
        old_energy = moment.get("energy", 1.0)
        new_energy = old_energy * (1 - ACTUALIZATION_COST)

        cypher_update = """
        MATCH (m:Moment {id: $moment_id})
        SET m.status = 'spoken',
            m.tick_spoken = $tick,
            m.energy = m.energy * 0.4
        RETURN m.text
        """
        results = self._queries.query(cypher_update, {
            "moment_id": moment_id,
            "tick": tick
        })

        text = results[0].get("m.text", "") if results else moment.get("text", "")

        # 4. Create SAID link if speaker (Q6 Step 2)
        if speaker_id:
            self._create_said_link(speaker_id, moment_id, tick)

        # 5. Create THEN link to previous moment (Q6 Step 3)
        if previous_moment_id:
            self._create_then_link(previous_moment_id, moment_id, tick, player_caused)

        # 6. Broadcast SSE event (lazy import to avoid circular dependency)
        from engine.infrastructure.api.sse_broadcast import broadcast_moment_event
        broadcast_moment_event(self.playthrough_id, "moment_spoken", {
            "moment_id": moment_id,
            "text": text,
            "speaker": speaker_id,
            "tick": tick,
            "type": moment_type
        })

        logger.info(f"[Canon] Recorded {moment_id} to canon (speaker={speaker_id}, tick={tick})")

        return {
            "status": "ok",
            "moment_id": moment_id,
            "speaker": speaker_id,
            "tick": tick,
            "energy_cost": old_energy - new_energy
        }

    def process_ready_moments(
        self,
        ready_moments: List[Dict[str, Any]],
        tick: int,
        player_caused: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Process multiple ready moments in salience order.

        Args:
            ready_moments: List of moments to potentially record
            tick: Current game tick
            player_caused: Whether player action triggered this

        Returns:
            List of recording results
        """
        # Sort by salience (weight * energy)
        sorted_moments = sorted(
            ready_moments,
            key=lambda m: m.get("weight", 0.5) * m.get("energy", 1.0),
            reverse=True
        )

        results = []
        previous_id = self._get_last_spoken_moment_id()

        for moment in sorted_moments[:MAX_MOMENTS_PER_TICK]:
            moment_id = moment.get("id")
            if not moment_id:
                continue

            # For dialogue, find speaker
            speaker_id = None
            if moment.get("type") == "dialogue":
                speaker_id = determine_speaker(
                    self.playthrough_id, moment_id,
                    host=self.host, port=self.port
                )
                if not speaker_id:
                    logger.debug(f"[Canon] Skipping dialogue {moment_id} - no speaker")
                    continue

            result = self.record_to_canon(
                moment_id=moment_id,
                speaker_id=speaker_id,
                previous_moment_id=previous_id,
                tick=tick,
                player_caused=player_caused
            )

            results.append(result)

            if result.get("status") == "ok":
                previous_id = moment_id

        return results

    def _get_moment(self, moment_id: str) -> Optional[Dict[str, Any]]:
        """Get a moment by ID."""
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        RETURN m.id AS id, m.text AS text, m.type AS type,
               m.status AS status, m.weight AS weight, m.energy AS energy
        """
        results = self._queries.query(cypher, {"moment_id": moment_id})
        return results[0] if results else None

    def _create_said_link(
        self,
        speaker_id: str,
        moment_id: str,
        tick: int
    ):
        """Create SAID link from character to moment (Q6 Step 2)."""
        cypher = """
        MATCH (c:Character {id: $speaker_id})
        MATCH (m:Moment {id: $moment_id})
        CREATE (c)-[:SAID {tick: $tick}]->(m)
        """
        try:
            self._queries.query(cypher, {
                "speaker_id": speaker_id,
                "moment_id": moment_id,
                "tick": tick
            })
            logger.debug(f"[Canon] Created SAID link: {speaker_id} -> {moment_id}")
        except Exception as e:
            logger.warning(f"[Canon] Failed to create SAID link: {e}")

    def _create_then_link(
        self,
        from_id: str,
        to_id: str,
        tick: int,
        player_caused: bool
    ):
        """Create THEN link between moments (Q6 Step 3)."""
        cypher = """
        MATCH (from:Moment {id: $from_id})
        MATCH (to:Moment {id: $to_id})
        MERGE (from)-[r:THEN]->(to)
        SET r.tick = $tick,
            r.player_caused = $player_caused
        """
        try:
            self._queries.query(cypher, {
                "from_id": from_id,
                "to_id": to_id,
                "tick": tick,
                "player_caused": player_caused
            })
            logger.debug(f"[Canon] Created THEN link: {from_id} -> {to_id}")
        except Exception as e:
            logger.warning(f"[Canon] Failed to create THEN link: {e}")

    def _get_last_spoken_moment_id(self) -> Optional[str]:
        """Get the most recently spoken moment."""
        cypher = """
        MATCH (m:Moment {status: 'spoken'})
        RETURN m.id
        ORDER BY m.tick_spoken DESC
        LIMIT 1
        """
        results = self._queries.query(cypher)
        return results[0].get("m.id") if results else None


# Convenience function for direct use
def record_to_canon(
    playthrough_id: str,
    moment_id: str,
    speaker_id: Optional[str] = None,
    previous_moment_id: Optional[str] = None,
    tick: int = 0,
    player_caused: bool = False,
    host: str = "localhost",
    port: int = 6379
) -> Dict[str, Any]:
    """
    Record a moment to canon.

    Convenience function that creates CanonHolder and calls record_to_canon.

    Args:
        playthrough_id: The playthrough ID
        moment_id: The moment to record
        speaker_id: Who speaks it (None for narration)
        previous_moment_id: Previous moment for THEN link
        tick: Current game tick
        player_caused: Whether player action triggered this
        host: FalkorDB host
        port: FalkorDB port

    Returns:
        Dict with status and details
    """
    holder = CanonHolder(playthrough_id, host=host, port=port)
    return holder.record_to_canon(
        moment_id=moment_id,
        speaker_id=speaker_id,
        previous_moment_id=previous_moment_id,
        tick=tick,
        player_caused=player_caused
    )
