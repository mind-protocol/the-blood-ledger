"""
Blood Ledger — Graph Tick

The per-tick algorithm that runs the living world.
No LLM - pure math. Fast enough to run frequently.

DOCS: docs/physics/PATTERNS_Physics.md

Algorithm:
1. Compute character energies
2. Flow energy from characters to narratives
3. Propagate energy between narratives
4. Decay energy
5. Adjust for criticality
6. Tick pressure on tensions
7. Detect flips

TESTS:
    engine/tests/test_implementation.py::TestEnergyFlowImplementation (stubs)
    engine/tests/test_implementation.py::TestDecayImplementation (stubs)
    engine/tests/test_implementation.py::TestTensionImplementation (stubs)

VALIDATES:
    V4.2: Energy flow (_compute_character_energies, _flow_energy_to_narratives, _propagate_energy)
    V4.4: Decay system (_decay_energy)
    V4.5: Tension & flips (_tick_pressures, _detect_flips)
    V4.6: Criticality (_adjust_criticality)

STATUS: PARTIAL IMPLEMENTATION
    Methods exist but require integration testing with FalkorDB.
    Run: pytest test_implementation.py -v -m integration

SEE ALSO:
    engine/physics/constants.py — All physics constants
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

import logging
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass, field

from engine.physics.graph import GraphQueries, GraphOps
from .constants import *

logger = logging.getLogger(__name__)


@dataclass
class TickResult:
    """Result of a graph tick."""
    flips: List[Dict[str, Any]] = field(default_factory=list)
    energy_total: float = 0.0
    avg_pressure: float = 0.0
    decay_rate_used: float = DECAY_RATE
    narratives_updated: int = 0
    tensions_updated: int = 0
    moments_decayed: int = 0  # Phase 5: Moment lifecycle


class GraphTick:
    """
    Graph tick engine - the living world simulation.
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

        # Current decay rate (adjusted for criticality)
        self.decay_rate = DECAY_RATE

        logger.info("[GraphTick] Initialized")

    def run(
        self,
        elapsed_minutes: float,
        player_id: str = "char_player",
        player_location: str = None
    ) -> TickResult:
        """
        Run a graph tick.

        Args:
            elapsed_minutes: Time elapsed since last tick
            player_id: Player character ID (for proximity calculations)
            player_location: Player's current location

        Returns:
            TickResult with flips and stats
        """
        if elapsed_minutes < MIN_TICK_MINUTES:
            logger.debug(f"[GraphTick] Skipping tick ({elapsed_minutes} < {MIN_TICK_MINUTES} min)")
            return TickResult()

        logger.info(f"[GraphTick] Running tick for {elapsed_minutes} minutes")
        result = TickResult()

        # 1. Compute character energies
        char_energies = self._compute_character_energies(player_id, player_location)

        # 2. Flow energy from characters to narratives
        narrative_energies = self._flow_energy_to_narratives(char_energies)

        # 3. Propagate energy between narratives
        narrative_energies = self._propagate_energy(narrative_energies)

        # 4. Decay energy
        narrative_energies = self._decay_energy(narrative_energies)

        # 5. Update narrative weights
        result.narratives_updated = self._update_narrative_weights(narrative_energies)
        result.energy_total = sum(narrative_energies.values())

        # 6. Adjust criticality
        self._adjust_criticality()

        # 7. Tick pressure on tensions
        tensions = self._tick_pressures(elapsed_minutes)
        result.tensions_updated = len(tensions)

        # Calculate average pressure
        if tensions:
            result.avg_pressure = sum(t.get('pressure', 0) for t in tensions) / len(tensions)

        # 8. Detect flips
        result.flips = self._detect_flips(tensions)
        result.decay_rate_used = self.decay_rate

        # 9. Process moment lifecycle (decay, cleanup)
        moment_stats = self._process_moment_tick(elapsed_minutes)
        result.moments_decayed = moment_stats.get('decayed_count', 0)

        logger.info(
            f"[GraphTick] Complete: {len(result.flips)} flips, "
            f"energy={result.energy_total:.2f}, avg_pressure={result.avg_pressure:.2f}, "
            f"moments_decayed={result.moments_decayed}"
        )

        return result

    def _process_moment_tick(self, elapsed_minutes: float) -> Dict[str, Any]:
        """
        Process moment lifecycle on each tick.

        Applies weight decay to possible moments.
        Called every tick (5+ minutes).

        Args:
            elapsed_minutes: Time elapsed since last tick

        Returns:
            Dict with moment lifecycle stats

        Ref: docs/engine/moments/ALGORITHM_Lifecycle.md
        """
        # Calculate number of decay iterations based on elapsed time
        # One decay per 5 minutes
        iterations = max(1, int(elapsed_minutes / 5))

        total_decayed = 0
        total_updated = 0

        for _ in range(iterations):
            result = self.write.decay_moments(
                decay_rate=0.99,      # 1% decay per iteration
                decay_threshold=0.1   # Below 0.1 = decayed
            )
            total_decayed += result.get('decayed_count', 0)
            total_updated += result.get('updated_count', 0)

        return {
            'iterations': iterations,
            'updated_count': total_updated,
            'decayed_count': total_decayed
        }

    def _compute_character_energies(
        self,
        player_id: str,
        player_location: str = None
    ) -> Dict[str, float]:
        """
        Compute energy for each character.

        Energy = relationship_intensity × geographical_proximity
        """
        char_energies = {}

        # Get player location for proximity
        if not player_location:
            player_loc = self._get_character_location(player_id)
            player_location = player_loc

        # Get all characters
        characters = self.read.get_all_characters()

        for char in characters:
            char_id = char.get('id')
            if not char_id:
                continue

            # Relationship intensity: sum of beliefs about this character
            intensity = self._compute_relationship_intensity(char_id)

            # Geographical proximity to player
            proximity = self._compute_proximity(char_id, player_id, player_location)

            char_energies[char_id] = intensity * proximity

        return char_energies

    def _compute_relationship_intensity(self, char_id: str) -> float:
        """
        Compute how intensely narratives involve this character.
        """
        # Get narratives about this character
        narratives = self.read.get_narratives_about(character_id=char_id)

        if not narratives:
            return 0.1  # Base intensity

        # Sum weights of narratives about this character
        total_weight = sum(n.get('weight', 0.5) for n in narratives)
        return min(1.0, total_weight)

    def _compute_proximity(
        self,
        char_id: str,
        player_id: str,
        player_location: str
    ) -> float:
        """
        Compute geographical proximity to player.
        """
        if char_id == player_id:
            return 1.0

        # Get character location
        char_location = self._get_character_location(char_id)
        if not char_location or not player_location:
            return 0.1

        if char_location == player_location:
            return 1.0

        # Get travel distance
        path = self.read.get_path_between(player_location, char_location)
        if not path:
            return 0.05  # Far away

        # Parse distance
        distance_str = path.get('path_distance', '3 days')
        days = self._parse_distance(distance_str)

        return distance_to_proximity(days)

    def _get_character_location(self, char_id: str) -> str:
        """Get character's current location."""
        cypher = f"""
        MATCH (c:Character {{id: '{char_id}'}})-[r:AT]->(p:Place)
        WHERE r.present > 0.5
        RETURN p.id
        """
        try:
            results = self.read.query(cypher)
            return results[0].get('p.id') if results else None
        except:
            return None

    def _parse_distance(self, distance_str: str) -> float:
        """Parse distance string to days."""
        if not distance_str:
            return 1.0

        dist = distance_str.lower()
        if 'adjacent' in dist or 'same' in dist:
            return 0.0
        elif 'hour' in dist:
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1)) / 24.0
            return 0.1
        elif 'day' in dist:
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1))
            return 1.0
        else:
            return 1.0

    def _flow_energy_to_narratives(
        self,
        char_energies: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Flow energy from characters to narratives they believe.
        """
        # Start with current weights of all narratives to allow decay/accumulation
        narrative_energies: Dict[str, float] = {
            n['id']: n.get('weight', MIN_WEIGHT) 
            for n in self.read.get_narratives_about()
        }
        for char_id, char_energy in char_energies.items():
            # Get character's beliefs
            beliefs = self.read.get_character_beliefs(char_id)
            if not beliefs:
                continue

            total_strength = 0.0
            for belief in beliefs:
                total_strength += belief.get('believes', 0) * belief.get('heard', 0)

            if total_strength <= 0:
                continue

            for belief in beliefs:
                narr_id = belief.get('id')
                if not narr_id:
                    continue

                # Energy flow = char_energy × belief_strength × flow_rate
                belief_strength = belief.get('believes', 0) * belief.get('heard', 0)
                if belief_strength <= 0:
                    continue

                energy_flow = (
                    char_energy
                    * (belief_strength / total_strength)
                    * BELIEF_FLOW_RATE
                )

                narrative_energies[narr_id] = narrative_energies.get(narr_id, 0) + energy_flow

        return narrative_energies

    def _propagate_energy(
        self,
        narrative_energies: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Propagate energy between connected narratives.
        """
        # Get narrative links
        for hop in range(MAX_PROPAGATION_HOPS):
            new_energies = dict(narrative_energies)

            for narr_id, energy in narrative_energies.items():
                if energy <= MIN_WEIGHT:
                    continue

                # Get linked narratives
                links = self._get_narrative_links(narr_id)

                for link in links:
                    target_id = link.get('target_id')
                    if not target_id:
                        continue

                    # Determine link type and factor
                    for link_type, factor in LINK_FACTORS.items():
                        link_strength = link.get(link_type, 0)
                        if link_strength > 0:
                            transfer = energy * link_strength * factor

                            new_energies[narr_id] = new_energies.get(narr_id, energy) - transfer

                            # Supersession drains source
                            if link_type == 'supersedes':
                                new_energies[narr_id] -= transfer * 0.5

                            new_energies[target_id] = new_energies.get(target_id, 0) + transfer

            for narr_id, energy in new_energies.items():
                new_energies[narr_id] = max(MIN_WEIGHT, energy)

            narrative_energies = new_energies

        return narrative_energies

    def _get_narrative_links(self, narr_id: str) -> List[Dict[str, Any]]:
        """Get links from a narrative."""
        cypher = f"""
        MATCH (n:Narrative {{id: '{narr_id}'}})-[r:RELATES_TO]->(target:Narrative)
        RETURN target.id AS target_id,
               r.contradicts AS contradicts,
               r.supports AS supports,
               r.elaborates AS elaborates,
               r.subsumes AS subsumes,
               r.supersedes AS supersedes
        """
        try:
            return self.read.query(cypher)
        except:
            return []

    def _decay_energy(
        self,
        narrative_energies: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Apply decay to narrative energies.
        """
        decayed = {}

        for narr_id, energy in narrative_energies.items():
            # Get narrative type for decay rate
            narr = self.read.get_narrative(narr_id)
            narr_type = narr.get('type', '') if narr else ''
            focus = narr.get('focus', 1.0) if narr else 1.0

            # Core types decay slower
            if narr_type in CORE_TYPES:
                decay_mult = CORE_DECAY_MULTIPLIER
            else:
                decay_mult = 1.0

            # Higher focus = slower decay
            focus_mult = 1.0 / focus if focus > 0 else 1.0

            # Apply decay
            effective_decay = self.decay_rate * decay_mult * focus_mult
            new_energy = max(MIN_WEIGHT, energy * (1 - effective_decay))

            decayed[narr_id] = new_energy

        return decayed

    def _update_narrative_weights(
        self,
        narrative_energies: Dict[str, float]
    ) -> int:
        """
        Update narrative weights in the graph.
        """
        updated = 0

        for narr_id, energy in narrative_energies.items():
            # Clamp to 0-1
            weight = max(MIN_WEIGHT, min(1.0, energy))

            cypher = f"""
            MATCH (n:Narrative {{id: '{narr_id}'}})
            SET n.weight = {weight}
            """
            try:
                self.write._query(cypher)
                updated += 1
            except:
                pass

        return updated

    def _adjust_criticality(self):
        """
        Adjust decay rate to maintain system near critical threshold.
        """
        tensions = self.read.get_all_tensions()
        if not tensions:
            return

        avg_pressure = sum(t.get('pressure', 0) for t in tensions) / len(tensions)
        max_pressure = max(t.get('pressure', 0) for t in tensions)

        # Too cold: reduce decay
        if avg_pressure < CRITICALITY_TARGET_MIN:
            self.decay_rate = max(DECAY_RATE_MIN, self.decay_rate * 0.9)
        # Too hot: increase decay
        elif avg_pressure > CRITICALITY_TARGET_MAX:
            self.decay_rate = min(DECAY_RATE_MAX, self.decay_rate * 1.1)

        # Need at least one hot tension
        if max_pressure < CRITICALITY_HOT_THRESHOLD:
            self.decay_rate = max(DECAY_RATE_MIN, self.decay_rate * 0.95)

    def _tick_pressures(self, elapsed_minutes: float) -> List[Dict[str, Any]]:
        """
        Tick pressure accumulation on all tensions.
        """
        tensions = self.read.get_all_tensions()
        updated_tensions = []

        for tension in tensions:
            tension_id = tension.get('id')
            pressure_type = tension.get('pressure_type', 'gradual')
            current_pressure = tension.get('pressure', 0)
            base_rate = tension.get('base_rate', BASE_PRESSURE_RATE)
            breaking_point = tension.get('breaking_point', DEFAULT_BREAKING_POINT)

            # Get max weight of narratives in tension
            narrative_ids = tension.get('narratives', [])
            if isinstance(narrative_ids, str):
                import json
                narrative_ids = json.loads(narrative_ids)

            max_weight = 0.5
            avg_focus = 1.0
            for narr_id in narrative_ids:
                narr = self.read.get_narrative(narr_id)
                if narr:
                    max_weight = max(max_weight, narr.get('weight', 0.5))
                    avg_focus = (avg_focus + narr.get('focus', 1.0)) / 2

            # Calculate new pressure
            if pressure_type in ['gradual', 'hybrid']:
                increase = elapsed_minutes * base_rate * avg_focus * max_weight
                new_pressure = min(1.0, current_pressure + increase)
            else:
                new_pressure = current_pressure

            # Update tension
            if new_pressure != current_pressure:
                cypher = f"""
                MATCH (t:Tension {{id: '{tension_id}'}})
                SET t.pressure = {new_pressure}
                """
                try:
                    self.write._query(cypher)
                except:
                    pass

            updated_tensions.append({
                'id': tension_id,
                'pressure': new_pressure,
                'breaking_point': breaking_point,
                'pressure_type': pressure_type,
                'narratives': narrative_ids
            })

        return updated_tensions

    def _detect_flips(self, tensions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect tensions that have exceeded their breaking point.
        """
        flips = []

        for tension in tensions:
            pressure = tension.get('pressure', 0)
            breaking_point = tension.get('breaking_point', DEFAULT_BREAKING_POINT)

            if pressure >= breaking_point:
                flips.append({
                    'tension_id': tension.get('id'),
                    'pressure': pressure,
                    'breaking_point': breaking_point,
                    'trigger_reason': f"Pressure {pressure:.2f} >= breaking_point {breaking_point:.2f}",
                    'narratives': tension.get('narratives', [])
                })

                logger.info(f"[GraphTick] FLIP detected: {tension.get('id')} at {pressure:.2f}")

        return flips
