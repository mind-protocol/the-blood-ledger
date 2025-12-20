"""
Blood Ledger — Moment Graph Surface Engine

Determines which moments should surface (become active).
Handles weight-based activation and decay.

No LLM. Pure mechanical weight calculations.
"""

import logging
from typing import Dict, Any, List, Optional

from engine.physics.graph.graph_ops import GraphOps
from engine.physics.graph.graph_queries import GraphQueries

logger = logging.getLogger(__name__)

# Thresholds
ACTIVATION_THRESHOLD = 0.8   # Weight needed to flip possible -> active
DECAY_THRESHOLD = 0.1        # Below this, moment decays
DECAY_RATE = 0.99            # Per-tick weight multiplier
MIN_REACTIVATE_WEIGHT = 0.3  # Minimum weight when reactivating dormant moments


class MomentSurface:
    """
    Surfacing logic for flips, decay, and scene transitions.

    Methods are intentionally small to keep runtime costs predictable.
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

    def check_for_flips(
        self,
        threshold: float = ACTIVATION_THRESHOLD
    ) -> List[Dict[str, Any]]:
        """
        Activate possible moments whose weight crosses the activation threshold.
        """
        cypher = """
        MATCH (m:Moment)
        WHERE m.status = 'possible' AND m.weight >= $threshold
        SET m.status = 'active'
        RETURN m.id AS id, m.weight AS weight
        """
        try:
            rows = self.write._query(cypher, {"threshold": threshold})
        except Exception as exc:
            logger.error(f"[MomentSurface] check_for_flips failed: {exc}")
            return []

        flipped = []
        for row in rows:
            if isinstance(row, dict):
                flipped.append({"id": row.get("id"), "weight": row.get("weight")})
            else:
                flipped.append({"id": row[0], "weight": row[1]})
        return flipped

    def apply_decay(
        self,
        decay_rate: float = DECAY_RATE,
        decay_threshold: float = DECAY_THRESHOLD,
        tick: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Apply weight decay and mark moments as decayed below threshold.
        """
        if tick is None:
            tick = self.write._get_current_tick()

        decay_cypher = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        SET m.weight = m.weight * $decay_rate
        RETURN count(m)
        """
        result = self.write._query(decay_cypher, {"decay_rate": decay_rate})
        updated_count = result[0][0] if result and result[0] else 0

        decayed_cypher = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active'] AND m.weight < $threshold
        SET m.status = 'decayed', m.tick_decayed = $tick
        RETURN count(m)
        """
        result = self.write._query(decayed_cypher, {
            "threshold": decay_threshold,
            "tick": tick
        })
        decayed_count = result[0][0] if result and result[0] else 0

        if decayed_count:
            logger.info(f"[MomentSurface] Decay updated {updated_count}, decayed {decayed_count}")

        return {
            "updated_count": updated_count,
            "decayed_count": decayed_count
        }

    def handle_scene_change(
        self,
        old_location_id: Optional[str],
        new_location_id: Optional[str],
        tick: Optional[int] = None,
        min_weight: float = MIN_REACTIVATE_WEIGHT
    ) -> Dict[str, Any]:
        """
        Move moments to dormant/decayed on exit and reactivate on entry.
        """
        if tick is None:
            tick = self.write._get_current_tick()

        dormant_count = 0
        decayed_count = 0
        reactivated_count = 0

        if old_location_id:
            dormant_cypher = """
            MATCH (m:Moment)-[a:ATTACHED_TO]->(p:Place {id: $location_id})
            WHERE a.persistent = true AND m.status IN ['possible', 'active']
            SET m.status = 'dormant'
            RETURN count(m)
            """
            result = self.write._query(dormant_cypher, {"location_id": old_location_id})
            dormant_count = result[0][0] if result and result[0] else 0

            decayed_cypher = """
            MATCH (m:Moment)-[a:ATTACHED_TO]->(p:Place {id: $location_id})
            WHERE a.persistent = false AND m.status IN ['possible', 'active']
            SET m.status = 'decayed', m.tick_decayed = $tick
            RETURN count(m)
            """
            result = self.write._query(decayed_cypher, {
                "location_id": old_location_id,
                "tick": tick
            })
            decayed_count = result[0][0] if result and result[0] else 0

        if new_location_id:
            reactivate_cypher = """
            MATCH (m:Moment)-[:ATTACHED_TO]->(p:Place {id: $location_id})
            WHERE m.status = 'dormant'
            SET m.status = 'possible',
                m.weight = CASE
                    WHEN m.weight < $min_weight THEN $min_weight
                    ELSE m.weight
                END
            RETURN count(m)
            """
            result = self.write._query(reactivate_cypher, {
                "location_id": new_location_id,
                "min_weight": min_weight
            })
            reactivated_count = result[0][0] if result and result[0] else 0

        return {
            "dormant_count": dormant_count,
            "decayed_count": decayed_count,
            "reactivated_count": reactivated_count
        }

    def set_moment_weight(self, moment_id: str, weight: float) -> None:
        """Set moment weight to an explicit value."""
        weight = max(0.0, min(1.0, weight))
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        SET m.weight = $weight
        """
        self.write._query(cypher, {"moment_id": moment_id, "weight": weight})

    def get_surface_stats(self) -> Dict[str, int]:
        """Return counts for each moment status."""
        cypher = """
        MATCH (m:Moment)
        RETURN m.status AS status, count(m) AS count
        """
        rows = self.read.query(cypher)
        stats = {
            "possible": 0,
            "active": 0,
            "spoken": 0,
            "dormant": 0,
            "decayed": 0
        }

        for row in rows:
            if isinstance(row, dict):
                status = row.get("status")
                count = row.get("count", 0)
            else:
                status = row[0]
                count = row[1]
            if status in stats:
                stats[status] = count
        return stats
