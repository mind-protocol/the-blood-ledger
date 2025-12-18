"""
Blood Ledger — Physics Constants

All constants for the graph physics engine.
From docs/engine/graph/ALGORITHM_Energy_Flow.md

TESTS:
    engine/tests/test_behaviors.py::TestEnergyFlow
    engine/tests/test_behaviors.py::TestWeightComputation
    engine/tests/test_behaviors.py::TestDecaySystem
    engine/tests/test_behaviors.py::TestTensionAndFlips
    engine/tests/test_behaviors.py::TestCriticality
    engine/tests/test_behaviors.py::TestProximity
    engine/tests/test_spec_consistency.py::TestConstantsConsistency

VALIDATES:
    V4.2: Energy flow (BELIEF_FLOW_RATE, MAX_PROPAGATION_HOPS, LINK_FACTORS)
    V4.3: Weight computation (MIN_WEIGHT)
    V4.4: Decay system (DECAY_RATE, CORE_TYPES, CORE_DECAY_MULTIPLIER)
    V4.5: Tension & flips (BASE_PRESSURE_RATE, DEFAULT_BREAKING_POINT, MAX_CASCADE_DEPTH)
    V4.6: Criticality (CRITICALITY_TARGET_*, distance_to_proximity)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

# =============================================================================
# ENERGY FLOW
# =============================================================================

# Rate at which characters pump energy into narratives they believe
BELIEF_FLOW_RATE = 0.1

# Maximum hops for energy propagation between narratives
MAX_PROPAGATION_HOPS = 3

# Link-type propagation factors (how energy flows between narratives)
LINK_FACTORS = {
    'contradicts': 0.30,  # Both heat up
    'supports': 0.20,     # Flows one way
    'elaborates': 0.15,   # Detail flows to general
    'subsumes': 0.10,     # Specific to general
    'supersedes': 0.25,   # Drains source by 50% of transfer
}

# =============================================================================
# DECAY
# =============================================================================

# Base decay rate per tick (dynamic, adjusted for criticality)
DECAY_RATE = 0.02

# Decay rate bounds
DECAY_RATE_MIN = 0.005
DECAY_RATE_MAX = 0.1

# Minimum weight (narratives never decay to zero)
MIN_WEIGHT = 0.01

# Core narrative types that decay slower (0.25x rate)
CORE_TYPES = ['oath', 'blood', 'debt']
CORE_DECAY_MULTIPLIER = 0.25

# =============================================================================
# PRESSURE
# =============================================================================

# Base pressure accumulation rate (per minute)
BASE_PRESSURE_RATE = 0.001

# Default breaking point
DEFAULT_BREAKING_POINT = 0.9

# Maximum cascade depth (prevent infinite loops)
MAX_CASCADE_DEPTH = 5

# =============================================================================
# CRITICALITY
# =============================================================================

# Target average pressure range
CRITICALITY_TARGET_MIN = 0.4
CRITICALITY_TARGET_MAX = 0.6

# At least one tension should be "hot"
CRITICALITY_HOT_THRESHOLD = 0.7

# =============================================================================
# PROXIMITY
# =============================================================================

# Distance-to-proximity conversion
# Same location = 1.0, 1 day = 0.5, 2 days = 0.25, 3+ days = 0.05
def distance_to_proximity(days: float) -> float:
    """Convert travel days to proximity factor."""
    if days <= 0:
        return 1.0
    elif days <= 1:
        return 0.5
    elif days <= 2:
        return 0.25
    else:
        return 0.05

# =============================================================================
# TICK
# =============================================================================

# Minimum time elapsed to trigger a tick
MIN_TICK_MINUTES = 5

# Tick interval in minutes (for scheduled pressure)
TICK_INTERVAL_MINUTES = 5
