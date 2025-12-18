"""
Blood Ledger — World Runner Service

Calls Claude CLI to resolve flips (tension breaks).
Stateless - no --continue, each call is independent.
"""

import subprocess
import json
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class WorldRunnerService:
    """
    Service for calling the World Runner agent via Claude CLI.
    """

    def __init__(
        self,
        working_dir: str = None,
        timeout: int = 600  # 10 minutes
    ):
        self.working_dir = working_dir or str(Path.cwd())
        self.timeout = timeout

        logger.info("[WorldRunnerService] Initialized")

    def process_flips(
        self,
        flips: List[Dict[str, Any]],
        graph_context: Dict[str, Any],
        player_context: Dict[str, Any],
        time_span: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Process flipped tensions and determine what happened.

        Args:
            flips: List of flipped tensions
            graph_context: Relevant narratives and character info
            player_context: Player location and state
            time_span: Time span being processed

        Returns:
            WorldRunnerOutput dict with graph_mutations and world_injection
        """
        # Build prompt
        prompt = self._build_prompt(flips, graph_context, player_context, time_span)

        # Call Claude CLI (stateless, no --continue)
        result = self._call_claude(prompt)

        return result

    def _build_prompt(
        self,
        flips: List[Dict[str, Any]],
        graph_context: Dict[str, Any],
        player_context: Dict[str, Any],
        time_span: str
    ) -> str:
        """Build the world runner prompt."""
        import yaml

        parts = [
            "WORLD RUNNER INSTRUCTION",
            "=" * 24,
            "",
            f"TIME_SPAN: {time_span}",
            "",
            "FLIPS:",
            yaml.dump(flips, default_flow_style=False),
            "",
            "GRAPH_CONTEXT:",
            yaml.dump(graph_context, default_flow_style=False),
            "",
            "PLAYER_CONTEXT:",
            yaml.dump(player_context, default_flow_style=False),
            "",
            "Determine what happened during this time span.",
            "For each flip, determine:",
            "1. What specifically occurred",
            "2. Who witnessed it",
            "3. What new narratives emerge",
            "4. How beliefs change",
            "5. Any cascading effects",
            "",
            "Output JSON matching WorldRunnerOutput schema.",
        ]

        return "\n".join(parts)

    def _call_claude(self, prompt: str) -> Dict[str, Any]:
        """Call Claude CLI and parse response."""
        # Stateless - no --continue
        cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions", "--output-format", "json", "--verbose"]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.working_dir
            )

            if result.returncode != 0:
                logger.error(f"[WorldRunnerService] Claude CLI failed: {result.stderr}")
                return self._fallback_response()

            # Parse JSON response
            response_text = result.stdout.strip()

            # Handle potential markdown code blocks
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])

            return json.loads(response_text)

        except subprocess.TimeoutExpired:
            logger.error("[WorldRunnerService] Claude CLI timed out")
            return self._fallback_response()
        except json.JSONDecodeError as e:
            logger.error(f"[WorldRunnerService] Failed to parse response: {e}")
            return self._fallback_response()
        except FileNotFoundError:
            logger.error("[WorldRunnerService] Claude CLI not found")
            return self._fallback_response()

    def _fallback_response(self) -> Dict[str, Any]:
        """Return a minimal fallback response."""
        return {
            "thinking": "Fallback response - World Runner unavailable",
            "graph_mutations": {
                "new_narratives": [],
                "new_beliefs": [],
                "tension_updates": [],
                "new_tensions": [],
                "character_movements": [],
                "modifier_changes": []
            },
            "world_injection": {
                "time_since_last": "unknown",
                "breaks": [],
                "news_arrived": [],
                "tension_changes": {},
                "interruption": None,
                "atmosphere_shift": None,
                "narrator_notes": "World Runner unavailable - minimal response"
            }
        }
