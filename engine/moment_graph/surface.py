"""
Blood Ledger — Moment Graph Surface Engine

Determines which moments should surface (become active).
Handles weight-based activation and decay.

No LLM. Pure mechanical weight calculations.
"""

import logging
from typing import Dict, Any, List

from engine.db.graph_ops import GraphOps
from engine.db.graph_queries import GraphQueries

logger = logging.getLogger(__name__)

# Thresholds
ACTIVATION_THRESHOLD = 0.8   # Weight needed to flip possible -> active
DECAY_THRESHOLD = 0.1        # Below this, moment decays
DECAY_RATE = 0.99            # Per-tick weight multiplier
TENSION_ENERGY_FACTOR = 0.2  # How much tension pressure transfers to moments


class MomentSurface:
    """
    Manages moment surfacing and decay.

    No LLM. Pure mechanical weight calculations.
    """

    def __init__(
        self,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379
    ):
        self.read = GraphQueries(graph_name=graph_name, host=host, port=port)
        self.write = GraphOps(graph_name=graph_name, host=host, port=port)
        self.graph_name = graph_name

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
        try:
            results = self.write._query(cypher, {"threshold": ACTIVATION_THRESHOLD})
            flipped = [{'id': r[0], 'weight': r[1]} for r in results] if results else []
            if flipped:
                logger.info(f"[Surface] {len(flipped)} moments flipped to active")
            return flipped
        except Exception as e:
            logger.error(f"[Surface] check_for_flips failed: {e}")
            return []

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
        try:
            self.write._query(cypher_decay, {"decay_rate": DECAY_RATE})
        except Exception as e:
            logger.error(f"[Surface] apply_decay (decay step) failed: {e}")
            return 0

        # Mark decayed (those below threshold)
        cypher_prune = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        AND m.weight < $threshold
        SET m.status = 'decayed', m.tick_decayed = $tick
        RETURN count(m) AS count
        """
        try:
            result = self.write._query(cypher_prune, {
                "threshold": DECAY_THRESHOLD,
                "tick": tick
            })
            decayed_count = result[0][0] if result and result[0] else 0
            if decayed_count > 0:
                logger.info(f"[Surface] {decayed_count} moments decayed")
            return decayed_count
        except Exception as e:
            logger.error(f"[Surface] apply_decay (prune step) failed: {e}")
            return 0

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
        boost = pressure * TENSION_ENERGY_FACTOR

        # Find attached moments and boost their weight
        cypher = """
        MATCH (m:Moment)-[:ATTACHED_TO]->(t:Tension {id: $tension_id})
        WHERE m.status IN ['possible', 'active']
        SET m.weight = CASE
            WHEN m.weight + $boost > 1.0 THEN 1.0
            ELSE m.weight + $boost
        END
        RETURN m.id AS id
        """
        try:
            results = self.write._query(cypher, {
                "tension_id": tension_id,
                "boost": boost
            })
            ids = [r[0] for r in results] if results else []
            if ids:
                logger.debug(f"[Surface] Tension {tension_id} boosted {len(ids)} moments by {boost:.3f}")
            return ids
        except Exception as e:
            logger.error(f"[Surface] tension_to_moments failed: {e}")
            return []

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

        # 1. Make persistent moments at old location dormant
        cypher_dormant = """
        MATCH (m:Moment)-[r:ATTACHED_TO]->(p:Place {id: $old_loc})
        WHERE m.status IN ['possible', 'active']
        AND r.persistent = true
        SET m.status = 'dormant'
        RETURN count(m) AS count
        """
        try:
            result = self.write._query(cypher_dormant, {"old_loc": old_location})
            stats["dormant"] = result[0][0] if result and result[0] else 0
        except Exception as e:
            logger.error(f"[Surface] scene_change dormant step failed: {e}")

        # 2. Prune non-persistent moments at old location
        cypher_prune = """
        MATCH (m:Moment)-[r:ATTACHED_TO]->(p:Place {id: $old_loc})
        WHERE m.status IN ['possible', 'active']
        AND (r.persistent = false OR r.persistent IS NULL)
        SET m.status = 'decayed'
        RETURN count(m) AS count
        """
        try:
            result = self.write._query(cypher_prune, {"old_loc": old_location})
            stats["pruned"] = result[0][0] if result and result[0] else 0
        except Exception as e:
            logger.error(f"[Surface] scene_change prune step failed: {e}")

        # 3. Reactivate dormant moments at new location
        cypher_reactivate = """
        MATCH (m:Moment {status: 'dormant'})-[:ATTACHED_TO]->(p:Place {id: $new_loc})
        SET m.status = 'possible',
            m.weight = CASE WHEN m.weight < 0.3 THEN 0.3 ELSE m.weight END
        RETURN count(m) AS count
        """
        try:
            result = self.write._query(cypher_reactivate, {"new_loc": new_location})
            stats["reactivated"] = result[0][0] if result and result[0] else 0
        except Exception as e:
            logger.error(f"[Surface] scene_change reactivate step failed: {e}")

        logger.info(f"[Surface] Scene change {old_location} -> {new_location}: {stats}")
        return stats

    def boost_moment(
        self,
        moment_id: str,
        boost: float
    ) -> None:
        """
        Boost a specific moment's weight.

        Args:
            moment_id: Which moment
            boost: Amount to add (can be negative)
        """
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        SET m.weight = CASE
            WHEN m.weight + $boost > 1.0 THEN 1.0
            WHEN m.weight + $boost < 0.0 THEN 0.0
            ELSE m.weight + $boost
        END
        """
        try:
            self.write._query(cypher, {"moment_id": moment_id, "boost": boost})
        except Exception as e:
            logger.error(f"[Surface] boost_moment failed: {e}")

    def set_moment_weight(
        self,
        moment_id: str,
        weight: float
    ) -> None:
        """
        Set a moment's weight to a specific value.

        Args:
            moment_id: Which moment
            weight: New weight (0-1)
        """
        weight = max(0.0, min(1.0, weight))
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        SET m.weight = $weight
        """
        try:
            self.write._query(cypher, {"moment_id": moment_id, "weight": weight})
        except Exception as e:
            logger.error(f"[Surface] set_moment_weight failed: {e}")

    def get_surface_stats(self) -> Dict[str, int]:
        """Get counts of moments by status."""
        cypher = """
        MATCH (m:Moment)
        RETURN m.status AS status, count(m) AS count
        """
        try:
            results = self.read.query(cypher)
            # Handle both dict and list results from FalkorDB
            if not results:
                return {}
            if isinstance(results[0], dict):
                return {r['status']: r['count'] for r in results if r.get('status')}
            return {r[0]: r[1] for r in results if r[0]}
        except Exception as e:
            logger.error(f"[Surface] get_surface_stats failed: {e}")
            return {}
