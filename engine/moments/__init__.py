# DOCS: docs/engine/moments/PATTERNS_Moments.md
"""
Moment Graph module.

This stub exists to anchor the documentation chain and future implementation.

Docs:
- docs/engine/moments/PATTERNS_Moments.md — design rationale
- docs/engine/moments/SYNC_Moments.md — current state
- docs/schema/SCHEMA_Moments.md — schema contract
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
