# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md
"""
Semantic sparsity detection for World Builder.

Determines when query results are too thin and enrichment is needed.
Uses embedding-based measures, not type-based rules.

Specs:
- docs/infrastructure/world-builder/ALGORITHM/ALGORITHM_Overview.md
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import numpy as np

logger = logging.getLogger(__name__)

# Configuration
SPARSITY_PROXIMITY_THRESHOLD = 0.6  # Min embedding similarity
SPARSITY_MIN_CLUSTER = 2            # Min results for non-sparse
SPARSITY_MIN_DIVERSITY = 0.3        # Min result variety
SPARSITY_MIN_CONNECTEDNESS = 1.5    # Min avg links per result


@dataclass
class SparsityResult:
    """Result of sparsity analysis."""
    sparse: bool
    proximity: float       # 0-1, how close results match query
    cluster_size: int      # Number of results
    diversity: float       # 0-1, how varied results are
    connectedness: float   # Avg links per result node
    reason: Optional[str] = None


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    if a is None or b is None:
        return 0.0
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def node_to_text(node: Dict[str, Any]) -> str:
    """
    Convert a node to text for embedding.

    Uses 'detail' field if present, otherwise 'name' or 'text'.
    """
    # Try detail first (rich description)
    if 'detail' in node and node['detail']:
        return str(node['detail'])

    # Try name (for characters, places)
    if 'name' in node and node['name']:
        return str(node['name'])

    # Try text (for moments, narratives)
    if 'text' in node and node['text']:
        return str(node['text'])

    # Try content (for narratives)
    if 'content' in node and node['content']:
        return str(node['content'])

    # Fallback to id
    return str(node.get('id', ''))


def is_sparse(
    query_text: str,
    results: List[Dict[str, Any]],
    embed_fn: callable = None,
    count_links_fn: callable = None
) -> SparsityResult:
    """
    Semantic sparsity detection.

    Measures result quality across multiple dimensions:
    - Proximity: Are results semantically close to query?
    - Cluster size: How many results?
    - Diversity: Are results varied or all the same?
    - Connectedness: Do results link to other things?

    Args:
        query_text: The query string
        results: List of result nodes
        embed_fn: Function to embed text (returns np.ndarray)
        count_links_fn: Function to count links for a node id

    Returns:
        SparsityResult with sparse flag and metrics
    """
    # No results = definitely sparse
    if not results:
        return SparsityResult(
            sparse=True,
            proximity=0.0,
            cluster_size=0,
            diversity=0.0,
            connectedness=0.0,
            reason='no_results'
        )

    # Default embed function (returns None if not provided)
    if embed_fn is None:
        embed_fn = _default_embed

    # Default link count function
    if count_links_fn is None:
        count_links_fn = lambda node_id: 0

    # Embed query
    query_emb = embed_fn(query_text)

    # Embed results
    result_texts = [node_to_text(r) for r in results]
    result_embs = [embed_fn(text) for text in result_texts]

    # Filter out None embeddings
    valid_embs = [(emb, r) for emb, r in zip(result_embs, results) if emb is not None]

    if not valid_embs and query_emb is None:
        # Can't compute embeddings, use simple heuristics
        return SparsityResult(
            sparse=len(results) < SPARSITY_MIN_CLUSTER,
            proximity=0.5,  # Unknown
            cluster_size=len(results),
            diversity=0.5,  # Unknown
            connectedness=0.0,
            reason='no_embeddings'
        )

    # Proximity: best match to query
    if query_emb is not None and valid_embs:
        proximities = [cosine_similarity(query_emb, emb) for emb, _ in valid_embs]
        proximity = max(proximities) if proximities else 0.0
    else:
        proximity = 0.5  # Unknown

    # Cluster size
    cluster_size = len(results)

    # Diversity: average pairwise distance
    if len(valid_embs) > 1:
        distances = []
        for i, (e1, _) in enumerate(valid_embs):
            for e2, _ in valid_embs[i+1:]:
                distances.append(1 - cosine_similarity(e1, e2))
        diversity = sum(distances) / len(distances) if distances else 0.0
    else:
        diversity = 0.0

    # Connectedness: average outgoing links
    link_counts = [count_links_fn(r.get('id', '')) for r in results]
    connectedness = sum(link_counts) / len(results) if results else 0.0

    # Determine sparsity - sparse if ANY dimension is weak
    reasons = []
    if proximity < SPARSITY_PROXIMITY_THRESHOLD:
        reasons.append(f'proximity={proximity:.2f}<{SPARSITY_PROXIMITY_THRESHOLD}')
    if cluster_size < SPARSITY_MIN_CLUSTER:
        reasons.append(f'cluster_size={cluster_size}<{SPARSITY_MIN_CLUSTER}')
    if diversity < SPARSITY_MIN_DIVERSITY and cluster_size > 1:
        reasons.append(f'diversity={diversity:.2f}<{SPARSITY_MIN_DIVERSITY}')
    if connectedness < SPARSITY_MIN_CONNECTEDNESS:
        reasons.append(f'connectedness={connectedness:.2f}<{SPARSITY_MIN_CONNECTEDNESS}')

    sparse = len(reasons) > 0
    reason = ', '.join(reasons) if reasons else None

    logger.debug(
        f"[Sparsity] query='{query_text[:50]}...' sparse={sparse} "
        f"proximity={proximity:.2f} cluster={cluster_size} "
        f"diversity={diversity:.2f} connected={connectedness:.2f}"
    )

    return SparsityResult(
        sparse=sparse,
        proximity=proximity,
        cluster_size=cluster_size,
        diversity=diversity,
        connectedness=connectedness,
        reason=reason
    )


def _default_embed(text: str) -> Optional[np.ndarray]:
    """
    Default embedding function.

    Returns None - actual embedding should be injected.
    In production, use sentence-transformers or similar.
    """
    # Lazy import to check if embeddings module exists
    try:
        from engine.infrastructure.embeddings import get_embedding
        return get_embedding(text)
    except ImportError:
        logger.debug("[Sparsity] No embedding module available")
        return None
