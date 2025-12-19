# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md
"""
World Builder - LLM service for graph enrichment.

JIT compiler for narrative content. When queries return sparse results,
World Builder generates new characters, places, things, narratives,
and potential moments (thoughts).

Specs:
- docs/infrastructure/world-builder/ALGORITHM_World_Builder.md
"""

import logging
import os
import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Set, Optional

from engine.infrastructure.orchestration.agent_cli import extract_claude_text, run_agent

logger = logging.getLogger(__name__)

# Configuration
ENRICHMENT_CACHE_SECONDS = 60  # Don't re-enrich same query within this window
LLM_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 2048


class WorldBuilder:
    """
    LLM-powered world enrichment service.

    Generates content when graph queries return sparse results.
    Includes caching and recursion prevention.
    """

    def __init__(
        self,
        api_key: str = None,
        working_dir: Optional[str] = None,
        timeout: int = 600,
    ):
        """
        Initialize World Builder.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self._cache: Dict[str, datetime] = {}  # query_hash → last_enriched
        self._enriching: Set[str] = set()  # Prevent recursion
        self.timeout = timeout

        if working_dir:
            self.working_dir = working_dir
        else:
            project_root = Path(__file__).resolve().parents[3]
            self.working_dir = str(project_root / "agents" / "world-builder")

        if self.api_key:
            logger.info("[WorldBuilder] API key detected but CLI is used exclusively")

    async def enrich(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate enrichment content for a sparse query.

        Args:
            query: The sparse query
            context: Dict with char_id, place_id, existing results, sparsity

        Returns:
            Parsed enrichment dict, or None if skipped/failed
        """
        # Create cache key
        query_hash = self._hash_query(query, context.get('char_id'))

        # Skip if recently enriched
        if query_hash in self._cache:
            elapsed = (datetime.now() - self._cache[query_hash]).total_seconds()
            if elapsed < ENRICHMENT_CACHE_SECONDS:
                logger.debug(f"[WorldBuilder] Cache hit for query (enriched {elapsed:.0f}s ago)")
                return None

        # Prevent recursion
        if query_hash in self._enriching:
            logger.debug("[WorldBuilder] Preventing recursive enrichment")
            return None

        self._enriching.add(query_hash)

        try:
            # Build prompt
            from .enrichment import build_enrichment_prompt
            prompt = build_enrichment_prompt(query, context)

            # Call LLM
            response = await self._call_llm(prompt)

            if not response:
                return None

            # Parse YAML from response
            enrichment = self._parse_response(response)

            if enrichment:
                self._cache[query_hash] = datetime.now()
                logger.info(f"[WorldBuilder] Generated enrichment for: {query[:50]}...")

            return enrichment

        except Exception as e:
            logger.error(f"[WorldBuilder] Enrichment failed: {e}")
            return None

        finally:
            self._enriching.discard(query_hash)

    async def _call_llm(self, prompt: str) -> Optional[str]:
        """Call the LLM with the enrichment prompt."""
        try:
            return await self._call_agent_cli(prompt)
        except Exception as e:
            logger.error(f"[WorldBuilder] LLM call failed: {e}")
            return None

    async def _call_agent_cli(self, prompt: str) -> Optional[str]:
        """Call the agent CLI for enrichment text."""
        try:
            result = run_agent(
                prompt,
                working_dir=self.working_dir,
                timeout=self.timeout,
                output_format="json",
                add_dir="../..",
            )
            if result.returncode != 0:
                logger.error(f"[WorldBuilder] Agent CLI failed: {result.stderr}")
                return None
            return extract_claude_text(result.stdout)
        except subprocess.TimeoutExpired:
            logger.error("[WorldBuilder] Agent CLI timed out")
            return None
        except FileNotFoundError:
            logger.error("[WorldBuilder] Agent CLI not found")
            return None
        except Exception as e:
            logger.error(f"[WorldBuilder] Agent CLI call failed: {e}")
            return None

    def _parse_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse YAML from LLM response.

        Extracts YAML block from markdown code fence if present.
        """
        # Try to extract YAML block
        yaml_content = response

        # Check for code fence
        if '```yaml' in response:
            start = response.find('```yaml') + 7
            end = response.find('```', start)
            if end > start:
                yaml_content = response[start:end].strip()
        elif '```' in response:
            start = response.find('```') + 3
            end = response.find('```', start)
            if end > start:
                yaml_content = response[start:end].strip()

        try:
            parsed = yaml.safe_load(yaml_content)
            if isinstance(parsed, dict):
                return parsed
            return None
        except yaml.YAMLError as e:
            logger.warning(f"[WorldBuilder] Failed to parse YAML: {e}")
            return None

    def _hash_query(self, query: str, char_id: Optional[str]) -> str:
        """Create a hash key for caching."""
        return f"{hash(query)}:{char_id or 'none'}"

    def clear_cache(self):
        """Clear the enrichment cache."""
        self._cache.clear()
        logger.debug("[WorldBuilder] Cache cleared")


# Default instance
_default_builder: Optional[WorldBuilder] = None


def get_default_world_builder() -> WorldBuilder:
    """Get or create the default WorldBuilder instance."""
    global _default_builder
    if _default_builder is None:
        _default_builder = WorldBuilder()
    return _default_builder
