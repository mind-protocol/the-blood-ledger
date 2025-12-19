# DOCS: docs/infrastructure/canon/IMPLEMENTATION_Canon.md
"""
Canon Holder — Records moments to canon (spoken status).

Usage:
    from engine.infrastructure.canon import record_to_canon, determine_speaker

    # Record a moment
    record_to_canon(
        playthrough_id="pt_abc123",
        moment_id="mom_xyz",
        speaker_id="char_aldric",  # or None for narration
        previous_moment_id="mom_prev",
        tick=42,
        player_caused=True
    )

    # Find who should speak a moment
    speaker = determine_speaker(playthrough_id, moment_id)

See docs/infrastructure/canon/ for full documentation chain.
"""

from .canon_holder import record_to_canon, CanonHolder
from .speaker import determine_speaker

__all__ = [
    'record_to_canon',
    'CanonHolder',
    'determine_speaker',
]
