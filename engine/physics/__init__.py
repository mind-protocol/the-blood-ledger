"""
Blood Ledger — Graph Physics Engine

Energy flow, decay, pressure, and flip detection.
The living world simulation that runs without LLM.

Usage:
    from engine.physics import GraphTick

    tick = GraphTick()
    flips = tick.run(elapsed_minutes=30)

    if flips:
        # Call World Runner for each flip
        for flip in flips:
            print(f"Tension flipped: {flip['id']}")
"""

from .tick import GraphTick
from .constants import *

__all__ = ['GraphTick']
