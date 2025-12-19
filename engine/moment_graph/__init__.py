"""
Blood Ledger — Moment Graph Engine

Core mechanics for instant-response dialogue traversal.
No LLM on hot path. Pure graph operations.

DOCS: docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md

Phase 1 MVP:
- Click traversal (<50ms)
- Weight-based surfacing
- Presence gating
- Persistence (dormant/reactivate)
- Speaker resolution
"""

from .traversal import MomentTraversal
from .queries import MomentQueries
from .surface import MomentSurface

__all__ = ['MomentTraversal', 'MomentQueries', 'MomentSurface']
