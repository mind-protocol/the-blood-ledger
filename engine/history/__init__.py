"""
Blood Ledger — History Module

History is distributed, not centralized. The past exists as narratives + beliefs,
not as an event log. Every query about the past filters through what characters know.

Two sources of history:
- Player-experienced: Conversation threads are the primary record, narratives index them
- World-generated: Narratives carry their own detail field

NOTE: occurred_where creates an OCCURRED_AT link to Place, not a node attribute.

Usage:
    from engine.history import HistoryService

    history = HistoryService(graph_queries, conversations_dir="playthroughs/{id}/conversations")

    # Query what a character knows about the past
    memories = history.query_history("player", about_person="char_aldric")

    # Record player-experienced history (with conversation)
    history.record_player_history(
        content="Aldric told me about his brother",
        conversation_text="Aldric: My brother held the bridge...",
        character_id="char_aldric",
        witnesses=["player", "char_aldric"],
        occurred_at="Day 4, night",
        occurred_where="place_camp"
    )

    # Record world-generated history (no conversation)
    history.record_world_history(
        content="Saxon thegns seized York",
        detail="The rebellion began at dawn...",
        occurred_at="Day 12, dawn",
        occurred_where="place_york",
        witnesses=["char_malet"]
    )
"""

from .service import HistoryService
from .conversations import ConversationThread

__all__ = ["HistoryService", "ConversationThread"]
