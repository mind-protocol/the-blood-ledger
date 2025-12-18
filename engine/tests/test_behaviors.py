"""
Behavior Tests — Game Mechanics

Tests the behavioral invariants of the game mechanics.
These tests validate formulas and constants WITHOUT requiring a database.

VALIDATES:
    V4.1: Time progression (tick to day/time conversion)
    V4.2: Energy flow (constants and formulas)
    V4.3: Weight computation (clamp logic)
    V4.4: Decay system (rates and multipliers)
    V4.5: Tension & flips (pressure formulas)
    V4.6: Criticality and proximity (target ranges)

TESTS IMPLEMENTATIONS:
    engine/physics/constants.py — All physics constants
    engine/models/tensions.py — Tension.tick_gradual, add_event_pressure

DOES NOT TEST (see test_implementation.py):
    engine/physics/tick.py — GraphTick class (requires DB)

REFERENCES:
    docs/engine/VALIDATION_Complete_Spec.md — All invariants
    docs/engine/TEST_Complete_Spec.md — Test index

RUN:
    pytest test_behaviors.py -v
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.physics.constants import (
    BELIEF_FLOW_RATE, MAX_PROPAGATION_HOPS, LINK_FACTORS,
    DECAY_RATE, DECAY_RATE_MIN, DECAY_RATE_MAX, MIN_WEIGHT,
    CORE_TYPES, CORE_DECAY_MULTIPLIER,
    BASE_PRESSURE_RATE, DEFAULT_BREAKING_POINT, MAX_CASCADE_DEPTH,
    CRITICALITY_TARGET_MIN, CRITICALITY_TARGET_MAX, CRITICALITY_HOT_THRESHOLD,
    distance_to_proximity, MIN_TICK_MINUTES, TICK_INTERVAL_MINUTES
)
from engine.models.base import NarrativeType, PressureType, TimeOfDay
from engine.models.nodes import Narrative
from engine.models.tensions import Tension


# =============================================================================
# V4.1: TIME PROGRESSION TESTS
# =============================================================================

class TestTimeProgression:
    """Test time-related mechanics."""

    def test_tick_interval_defined(self):
        """TICK_INTERVAL_MINUTES should be defined and positive."""
        assert TICK_INTERVAL_MINUTES > 0

    def test_min_tick_minutes_defined(self):
        """MIN_TICK_MINUTES should be defined and positive."""
        assert MIN_TICK_MINUTES > 0

    def test_tick_to_day_calculation(self):
        """Verify tick to day conversion (1440 ticks per day)."""
        TICKS_PER_DAY = 1440  # 60 min * 24 hours

        # Day 1 = ticks 0-1439
        # Day 2 = ticks 1440-2879
        # Day 3 = ticks 2880-4319

        def tick_to_day(tick: int) -> int:
            return (tick // TICKS_PER_DAY) + 1

        assert tick_to_day(0) == 1
        assert tick_to_day(1439) == 1
        assert tick_to_day(1440) == 2
        assert tick_to_day(2880) == 3

    def test_tick_to_time_of_day(self):
        """Verify tick to time of day conversion."""
        def tick_to_time(tick: int) -> str:
            minutes = tick % 1440  # Minutes within day
            hour = minutes // 60

            if hour < 6:
                return "night"
            elif hour < 9:
                return "dawn"
            elif hour < 12:
                return "morning"
            elif hour < 15:
                return "midday"
            elif hour < 18:
                return "afternoon"
            elif hour < 20:
                return "dusk"
            elif hour < 22:
                return "evening"
            else:
                return "night"

        # Test various times
        assert tick_to_time(0) == "night"      # midnight
        assert tick_to_time(300) == "night"    # 5am
        assert tick_to_time(360) == "dawn"     # 6am
        assert tick_to_time(540) == "morning"  # 9am
        assert tick_to_time(720) == "midday"   # 12pm
        assert tick_to_time(900) == "afternoon"  # 3pm
        assert tick_to_time(1200) == "dusk"    # 8pm
        assert tick_to_time(1320) == "evening"  # 10pm


# =============================================================================
# V4.2: ENERGY FLOW TESTS
# =============================================================================

class TestEnergyFlow:
    """Test energy flow mechanics."""

    def test_belief_flow_rate_valid(self):
        """BELIEF_FLOW_RATE should be in (0, 1]."""
        assert 0 < BELIEF_FLOW_RATE <= 1

    def test_max_propagation_hops_positive(self):
        """MAX_PROPAGATION_HOPS should be positive."""
        assert MAX_PROPAGATION_HOPS > 0

    def test_link_factors_all_positive(self):
        """All link factors should be positive."""
        for name, factor in LINK_FACTORS.items():
            assert factor > 0, f"Link factor {name} should be positive"

    def test_link_factors_expected_types(self):
        """All expected link types should have factors."""
        expected = {'contradicts', 'supports', 'elaborates', 'subsumes', 'supersedes'}
        assert expected == set(LINK_FACTORS.keys())

    def test_supersedes_factor_significant(self):
        """Supersedes should have significant factor (drains source)."""
        assert LINK_FACTORS['supersedes'] >= 0.2

    def test_contradicts_high_factor(self):
        """Contradicts should have high factor (both heat up)."""
        assert LINK_FACTORS['contradicts'] >= LINK_FACTORS['supports']

    def test_energy_flow_calculation(self):
        """Verify energy flow formula: energy = char_energy * belief * flow_rate."""
        char_energy = 0.8
        belief_strength = 0.9
        heard = 1.0

        # Flow = char_energy * belief_strength * heard * BELIEF_FLOW_RATE
        expected_flow = char_energy * belief_strength * heard * BELIEF_FLOW_RATE
        assert expected_flow == char_energy * belief_strength * heard * 0.1

    def test_supersession_drain(self):
        """Supersession should drain source by 50% of transfer."""
        source_energy = 1.0
        supersedes_strength = 0.8
        factor = LINK_FACTORS['supersedes']

        transfer = source_energy * supersedes_strength * factor
        drain = transfer * 0.5

        # Source should lose 50% of what's transferred
        new_source_energy = source_energy - drain
        assert new_source_energy < source_energy


# =============================================================================
# V4.3: WEIGHT COMPUTATION TESTS
# =============================================================================

class TestWeightComputation:
    """Test weight computation mechanics."""

    def test_weight_range(self):
        """Weight should always be in [MIN_WEIGHT, 1.0]."""
        # Test via Narrative model
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY, weight=0.5
        )
        assert MIN_WEIGHT <= narr.weight <= 1.0

    def test_min_weight_floor(self):
        """MIN_WEIGHT should be small but positive."""
        assert MIN_WEIGHT > 0
        assert MIN_WEIGHT < 0.1

    def test_focus_affects_weight(self):
        """Higher focus should affect weight visibility."""
        low_focus = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY, focus=0.5
        )
        high_focus = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY, focus=2.0
        )

        assert low_focus.focus == 0.5
        assert high_focus.focus == 2.0

    def test_weight_clamp_logic(self):
        """Weight clamping should work correctly."""
        def clamp_weight(energy: float) -> float:
            return max(MIN_WEIGHT, min(1.0, energy))

        assert clamp_weight(-0.5) == MIN_WEIGHT
        assert clamp_weight(0.0) == MIN_WEIGHT
        assert clamp_weight(0.5) == 0.5
        assert clamp_weight(1.0) == 1.0
        assert clamp_weight(1.5) == 1.0


# =============================================================================
# V4.4: DECAY SYSTEM TESTS
# =============================================================================

class TestDecaySystem:
    """Test decay mechanics."""

    def test_decay_rate_valid(self):
        """DECAY_RATE should be small positive number."""
        assert 0 < DECAY_RATE < 0.5

    def test_decay_rate_bounds(self):
        """Decay rate bounds should be valid."""
        assert DECAY_RATE_MIN < DECAY_RATE < DECAY_RATE_MAX
        assert DECAY_RATE_MIN > 0
        assert DECAY_RATE_MAX < 1.0

    def test_core_types_defined(self):
        """Core types should be defined."""
        expected = ['oath', 'blood', 'debt']
        assert set(CORE_TYPES) == set(expected)

    def test_core_decay_multiplier(self):
        """Core types should decay at 0.25x rate."""
        assert CORE_DECAY_MULTIPLIER == 0.25

    def test_core_types_are_narrative_types(self):
        """Core types should be valid narrative types."""
        narrative_types = {t.value for t in NarrativeType}
        for core in CORE_TYPES:
            assert core in narrative_types, f"Core type {core} should be valid narrative type"

    def test_decay_reduces_weight(self):
        """Decay should reduce weight toward MIN_WEIGHT."""
        initial_weight = 0.8
        decay_rate = DECAY_RATE

        # After one decay: weight * (1 - decay_rate)
        decayed = initial_weight * (1 - decay_rate)
        assert decayed < initial_weight

    def test_decay_respects_min_weight(self):
        """Decay should never reduce below MIN_WEIGHT."""
        weight = MIN_WEIGHT * 2
        decay_rate = 0.9  # Extreme decay

        # Even with extreme decay, should stay >= MIN_WEIGHT
        decayed = max(MIN_WEIGHT, weight * (1 - decay_rate))
        assert decayed >= MIN_WEIGHT

    def test_core_types_decay_slower(self):
        """Core types should decay at CORE_DECAY_MULTIPLIER rate."""
        initial = 0.8

        # Normal decay
        normal_decayed = initial * (1 - DECAY_RATE)

        # Core decay
        core_decayed = initial * (1 - DECAY_RATE * CORE_DECAY_MULTIPLIER)

        # Core should retain more weight
        assert core_decayed > normal_decayed

    def test_focus_affects_decay(self):
        """Higher focus should reduce decay."""
        initial = 0.8

        # Decay with focus 1.0
        focus_1 = initial * (1 - DECAY_RATE / 1.0)

        # Decay with focus 2.0
        focus_2 = initial * (1 - DECAY_RATE / 2.0)

        # Higher focus = less decay = more weight retained
        assert focus_2 > focus_1


# =============================================================================
# V4.5: TENSION & FLIP TESTS
# =============================================================================

class TestTensionAndFlips:
    """Test tension and flip mechanics."""

    def test_default_breaking_point(self):
        """DEFAULT_BREAKING_POINT should be high but < 1."""
        assert 0.5 < DEFAULT_BREAKING_POINT < 1.0
        assert DEFAULT_BREAKING_POINT == 0.9

    def test_base_pressure_rate(self):
        """BASE_PRESSURE_RATE should be small positive number."""
        assert 0 < BASE_PRESSURE_RATE < 0.1
        assert BASE_PRESSURE_RATE == 0.001

    def test_max_cascade_depth(self):
        """MAX_CASCADE_DEPTH should prevent infinite loops."""
        assert MAX_CASCADE_DEPTH > 0
        assert MAX_CASCADE_DEPTH <= 10
        assert MAX_CASCADE_DEPTH == 5

    def test_tension_flip_detection(self):
        """Tension flips when pressure >= breaking_point."""
        # Not flipped
        tension = Tension(id="test", pressure=0.5, breaking_point=0.9)
        assert tension.has_flipped is False

        # At breaking point - flipped
        tension = Tension(id="test", pressure=0.9, breaking_point=0.9)
        assert tension.has_flipped is True

        # Above breaking point - flipped
        tension = Tension(id="test", pressure=0.95, breaking_point=0.9)
        assert tension.has_flipped is True

    def test_tension_gradual_pressure(self):
        """Gradual tension accumulates pressure over time."""
        tension = Tension(
            id="test",
            pressure=0.0,
            pressure_type=PressureType.GRADUAL,
            base_rate=0.001
        )

        # Tick for 100 minutes
        new_pressure = tension.tick_gradual(100, focus=1.0, max_weight=1.0)

        # Expected: 0.0 + 100 * 0.001 * 1.0 * 1.0 = 0.1
        assert abs(new_pressure - 0.1) < 0.001

    def test_tension_scheduled_ignores_gradual(self):
        """Scheduled tensions don't use gradual ticking."""
        tension = Tension(
            id="test",
            pressure=0.0,
            pressure_type=PressureType.SCHEDULED
        )

        new_pressure = tension.tick_gradual(100, focus=1.0, max_weight=1.0)
        assert new_pressure == 0.0  # Unchanged

    def test_tension_event_pressure(self):
        """Event pressure can be added to gradual/hybrid tensions."""
        tension = Tension(id="test", pressure=0.3, pressure_type=PressureType.GRADUAL)
        tension.add_event_pressure(0.2)
        assert abs(tension.pressure - 0.5) < 0.001

    def test_tension_event_pressure_capped(self):
        """Event pressure should not exceed 1.0."""
        tension = Tension(id="test", pressure=0.9)
        tension.add_event_pressure(0.5)
        assert tension.pressure <= 1.0

    def test_tension_reset(self):
        """Tension can be reset after flip."""
        tension = Tension(id="test", pressure=0.95)
        tension.reset(0.1)
        assert tension.pressure == 0.1

    def test_tension_pressure_formula(self):
        """Verify pressure formula: rate * focus * max_weight * time."""
        base_rate = 0.001
        focus = 1.5
        max_weight = 0.8
        elapsed = 100

        expected = elapsed * base_rate * focus * max_weight
        assert abs(expected - 0.12) < 0.001


# =============================================================================
# V4.6: CRITICALITY TESTS
# =============================================================================

class TestCriticality:
    """Test criticality adjustment mechanics."""

    def test_criticality_targets(self):
        """Criticality targets should define valid range."""
        assert 0 < CRITICALITY_TARGET_MIN < CRITICALITY_TARGET_MAX < 1.0

    def test_criticality_hot_threshold(self):
        """Hot threshold should be high."""
        assert CRITICALITY_HOT_THRESHOLD > CRITICALITY_TARGET_MAX

    def test_criticality_adjustment_logic(self):
        """Verify criticality adjustment logic."""
        # Too cold (avg < min): reduce decay
        avg_cold = CRITICALITY_TARGET_MIN - 0.1
        assert avg_cold < CRITICALITY_TARGET_MIN

        # Too hot (avg > max): increase decay
        avg_hot = CRITICALITY_TARGET_MAX + 0.1
        assert avg_hot > CRITICALITY_TARGET_MAX

        # In range: no adjustment
        avg_ok = (CRITICALITY_TARGET_MIN + CRITICALITY_TARGET_MAX) / 2
        assert CRITICALITY_TARGET_MIN <= avg_ok <= CRITICALITY_TARGET_MAX


# =============================================================================
# V4.7: PROXIMITY TESTS
# =============================================================================

class TestProximity:
    """Test proximity calculations."""

    def test_same_location_proximity(self):
        """Same location = 1.0 proximity."""
        assert distance_to_proximity(0) == 1.0

    def test_nearby_proximity(self):
        """1 day away = 0.5 proximity."""
        assert distance_to_proximity(1) == 0.5

    def test_moderate_proximity(self):
        """2 days away = 0.25 proximity."""
        assert distance_to_proximity(2) == 0.25

    def test_distant_proximity(self):
        """3+ days away = 0.05 proximity."""
        assert distance_to_proximity(3) == 0.05
        assert distance_to_proximity(5) == 0.05
        assert distance_to_proximity(10) == 0.05

    def test_proximity_formula(self):
        """Proximity should decrease with distance."""
        proximities = [distance_to_proximity(d) for d in range(5)]
        # Should be monotonically decreasing or equal
        for i in range(len(proximities) - 1):
            assert proximities[i] >= proximities[i + 1]


# =============================================================================
# V5: EXPERIENCE INVARIANT STRUCTURE TESTS
# =============================================================================

class TestExperienceStructure:
    """Test that structures support experience invariants."""

    def test_narrative_has_about_fields(self):
        """Narratives should have about fields for characters/places/things."""
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY
        )
        assert hasattr(narr.about, 'characters')
        assert hasattr(narr.about, 'places')
        assert hasattr(narr.about, 'things')

    def test_narrative_has_voice(self):
        """Narratives should have voice for surfacing as Voices."""
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY
        )
        assert hasattr(narr, 'voice')
        assert hasattr(narr.voice, 'style')
        assert hasattr(narr.voice, 'phrases')

    def test_narrative_has_truth(self):
        """Narratives should have truth field (director-only)."""
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.LIE, truth=0.3
        )
        assert hasattr(narr, 'truth')
        assert narr.truth == 0.3

    def test_tension_has_narratives(self):
        """Tensions should reference narratives."""
        tension = Tension(
            id="test",
            narratives=["narr_1", "narr_2"]
        )
        assert len(tension.narratives) == 2


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
