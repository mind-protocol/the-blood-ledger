"""
Physics Constants

Game physics constants for Blood Ledger.
Proxy to ngram implementation if available, otherwise use defaults.
"""

import sys
from pathlib import Path

# Try to load from ngram
NGRAM_REPO = Path("/home/mind-protocol/ngram")
MODULE_PATH = "engine/physics/constants.py"
TARGET_FILE = NGRAM_REPO / MODULE_PATH

if TARGET_FILE.exists():
    with open(TARGET_FILE, "r") as f:
        code = f.read()
    exec(code, globals())
else:
    # Fallback defaults if ngram not available

    # Belief propagation
    BELIEF_FLOW_RATE = 0.1
    MAX_PROPAGATION_HOPS = 3
    LINK_FACTORS = {
        'BELIEVES': 1.0,
        'SUPPORTS': 0.8,
        'CONTRADICTS': -0.5,
        'ABOUT': 0.3,
    }

    # Decay
    DECAY_RATE = 0.01
    DECAY_RATE_MIN = 0.001
    DECAY_RATE_MAX = 0.1
    MIN_WEIGHT = 0.01
    CORE_TYPES = {'Character', 'Place', 'Thing'}
    CORE_DECAY_MULTIPLIER = 0.5

    # Tension/Pressure
    BASE_PRESSURE_RATE = 0.05
    DEFAULT_BREAKING_POINT = 0.8
    MAX_CASCADE_DEPTH = 5
    CRITICALITY_TARGET_MIN = 0.7
    CRITICALITY_TARGET_MAX = 0.95
    CRITICALITY_HOT_THRESHOLD = 0.85

    # Energy
    ENERGY_PUMP_RATE = 0.1
    PROXIMITY_FACTOR = 0.5

    # Moments
    DEFAULT_MOMENT_ENERGY = 0.3
    MOMENT_DECAY_RATE = 0.02
