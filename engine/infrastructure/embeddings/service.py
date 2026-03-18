# DOCS: docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md
"""
Embedding service facade.

Uses sentence-transformers when available, otherwise falls back to a deterministic
hash-based vectorizer to keep the system functional without external deps.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Iterable, List, Optional


DEFAULT_MODEL_NAME = "all-mpnet-base-v2"
DEFAULT_DIMENSIONS = 768


def _normalize(vec: List[float]) -> List[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def _hash_vector(text: str, dims: int) -> List[float]:
    """Deterministic fallback embedding without external dependencies."""
    vector = [0.0] * dims
    for token in text.lower().split():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for i in range(0, len(digest), 2):
            idx = (digest[i] << 8 | digest[i + 1]) % dims
            vector[idx] += 1.0
    return _normalize(vector)


@dataclass
class EmbeddingService:
    model_name: str = DEFAULT_MODEL_NAME
    dimensions: int = DEFAULT_DIMENSIONS
    model: Optional[object] = None

    def _load_model(self) -> None:
        if self.model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
        except Exception:
            self.model = None
            return
        self.model = SentenceTransformer(self.model_name)

    def embed(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self.dimensions
        self._load_model()
        if self.model is None:
            return _hash_vector(text, self.dimensions)
        vector = self.model.encode([text], normalize_embeddings=True)[0]
        return [float(v) for v in vector]

    def embed_many(self, texts: Iterable[str]) -> List[List[float]]:
        self._load_model()
        texts_list = list(texts)
        if not texts_list:
            return []
        if self.model is None:
            return [_hash_vector(text, self.dimensions) for text in texts_list]
        vectors = self.model.encode(texts_list, normalize_embeddings=True)
        return [[float(v) for v in vector] for vector in vectors]

    def similarity(self, vec_a: Iterable[float], vec_b: Iterable[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    global _service
    if _service is None:
        _service = EmbeddingService()
    return _service


def get_embedding(text: str) -> List[float]:
    return get_embedding_service().embed(text)
