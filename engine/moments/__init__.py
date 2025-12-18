"""
Moment Graph module.

This stub exists to anchor the documentation chain and future implementation.

Docs:
- docs/engine/moments/PATTERNS_Moments.md — philosophy and context
- docs/engine/moments/BEHAVIORS_Moments.md — observable effects
- docs/engine/moments/ALGORITHM_*.md — procedures for queries/transitions/lifecycle
- docs/engine/moments/SCHEMA_Moments.md — graph schema contract
- docs/engine/moments/API_Moments.md — API surface to satisfy
- docs/engine/moments/VALIDATION_Moments.md — invariants/tests
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Moment:
    """Minimal placeholder representation used until the real graph-backed model lands."""
    id: str
    text: str
    type: str = "narration"
    status: str = "possible"
    weight: float = 0.8
    speaker: Optional[str] = None


def not_implemented(*_, **__):
    """Helper that reminds implementers to wire actual graph operations."""
    raise NotImplementedError(
        "Moment graph not implemented yet. See docs/engine/moments/PATTERNS_Moments.md"
    )

