"""
Blood Ledger — Tension Model

Clusters of narratives under pressure that will eventually break.
Based on SCHEMA.md v5.1

TESTS:
    engine/tests/test_models.py::TestTensionModel
    engine/tests/test_behaviors.py::TestTensionAndFlips
    engine/tests/test_implementation.py::TestTensionImplementation (stubs)

VALIDATES:
    V2.5: Tension invariants (id, narratives, pressure, breaking_point)
    V4.5: Tension & flip mechanics (gradual, scheduled, hybrid pressure)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from .base import PressureType, TensionProgression


class Tension(BaseModel):
    """
    TENSION - A cluster of narratives under pressure that will eventually break.

    When pressure >= breaking_point, the tension "flips" and the World Runner
    determines what specifically happened.

    Pressure types:
    - gradual: Slow burn. Pressure ticks up over time. Uncertain when it breaks.
    - scheduled: Deadline. Pressure follows a timeline with cliff jumps.
    - hybrid: Both. Has a floor that rises on schedule, but events can exceed it.
    """
    id: str
    narratives: List[str] = Field(default_factory=list, description="Narrative IDs in tension")
    description: str = Field(default="", description="What this tension is about")
    narrator_notes: str = Field(default="", description="Notes for how to handle the break")

    pressure_type: PressureType = PressureType.GRADUAL

    # Pressure state
    pressure: float = Field(default=0.0, ge=0.0, le=1.0, description="Current pressure level")
    breaking_point: float = Field(default=0.9, ge=0.0, le=1.0)

    # For gradual pressure
    base_rate: float = Field(default=0.001, description="Pressure increase per minute")

    # For scheduled/hybrid pressure
    trigger_at: str = Field(default="", description="When this must break")
    progression: List[TensionProgression] = Field(default_factory=list)

    @property
    def has_flipped(self) -> bool:
        """Check if tension has exceeded breaking point."""
        return self.pressure >= self.breaking_point

    def tick_gradual(self, elapsed_minutes: float, focus: float = 1.0, max_weight: float = 1.0) -> float:
        """
        Tick gradual pressure accumulation.

        Formula: pressure += elapsed_min * base_rate * focus * max_weight

        Args:
            elapsed_minutes: Time elapsed since last tick
            focus: Average focus of narratives in tension
            max_weight: Maximum weight among narratives in tension

        Returns:
            New pressure value
        """
        if self.pressure_type == PressureType.SCHEDULED:
            return self.pressure  # Scheduled doesn't use gradual ticking

        increase = elapsed_minutes * self.base_rate * focus * max_weight
        self.pressure = min(1.0, self.pressure + increase)
        return self.pressure

    def tick_scheduled(self, current_time: str) -> float:
        """
        Update pressure based on scheduled progression.

        Args:
            current_time: Current game time (e.g., "Day 15")

        Returns:
            New pressure value
        """
        if self.pressure_type == PressureType.GRADUAL:
            return self.pressure

        # Find the applicable progression step
        for step in reversed(self.progression):
            # Simple string comparison - in practice would need proper time parsing
            if step.at <= current_time:
                if self.pressure_type == PressureType.SCHEDULED and step.pressure is not None:
                    self.pressure = step.pressure
                elif self.pressure_type == PressureType.HYBRID and step.pressure_floor is not None:
                    # Hybrid: pressure is max of current and floor
                    self.pressure = max(self.pressure, step.pressure_floor)
                break

        return self.pressure

    def add_event_pressure(self, amount: float) -> float:
        """
        Add pressure from an event (for gradual and hybrid types).

        Args:
            amount: Pressure to add (0-1)

        Returns:
            New pressure value
        """
        if self.pressure_type != PressureType.SCHEDULED:
            self.pressure = min(1.0, self.pressure + amount)
        return self.pressure

    def reset(self, new_pressure: float = 0.0) -> None:
        """Reset tension after it breaks (World Runner resolves it)."""
        self.pressure = new_pressure
