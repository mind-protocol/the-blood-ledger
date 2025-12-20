"""
Blood Ledger — Physics Embedding Helpers

Convenience wrappers so code examples can import `get_embedding` from the
physics package without touching the infrastructure module directly.
"""

from typing import List

from engine.infrastructure.embeddings import get_embedding_service


def get_embedding(text: str) -> List[float]:
    """
    Generate an embedding for the given text.
    """
    return get_embedding_service().embed(text)


def get_embedding_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts.
    """
    return get_embedding_service().embed_batch(texts)

