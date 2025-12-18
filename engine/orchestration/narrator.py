"""
Blood Ledger — Narrator Service

Calls Claude CLI to generate scenes.
Uses --continue for persistent session across playthrough.
"""

import subprocess
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class NarratorService:
    """
    Service for calling the Narrator agent via Claude CLI.
    Runs from agents/narrator/ directory where CLAUDE.md is located.
    """

    def __init__(
        self,
        working_dir: str = None,
        timeout: int = 600  # 10 minutes for complex scene generation
    ):
        # Default to agents/narrator relative to project root
        if working_dir:
            self.working_dir = working_dir
        else:
            # Find project root (parent of engine/)
            project_root = Path(__file__).parent.parent.parent
            self.working_dir = str(project_root / "agents" / "narrator")

        self.timeout = timeout
        self.session_started = False

        logger.info(f"[NarratorService] Initialized, working_dir={self.working_dir}")

    def generate(
        self,
        scene_context: Dict[str, Any],
        world_injection: Dict[str, Any] = None,
        instruction: str = None
    ) -> Dict[str, Any]:
        """
        Generate a scene using the Narrator.

        Args:
            scene_context: Current scene context (location, characters, narratives)
            world_injection: Optional injection from World Runner
            instruction: Optional specific instruction

        Returns:
            NarratorOutput dict with scene, time_elapsed, mutations, seeds
        """
        # Build prompt
        prompt = self._build_prompt(scene_context, world_injection, instruction)

        # Call Claude CLI
        result = self._call_claude(prompt)

        return result

    def _build_prompt(
        self,
        scene_context: Dict[str, Any],
        world_injection: Dict[str, Any] = None,
        instruction: str = None
    ) -> str:
        """Build the narrator prompt."""
        import yaml

        parts = [
            "NARRATOR INSTRUCTION",
            "=" * 20,
            "",
            "SCENE_CONTEXT:",
            yaml.dump(scene_context, default_flow_style=False),
        ]

        if world_injection:
            parts.extend([
                "",
                "WORLD_INJECTION:",
                yaml.dump(world_injection, default_flow_style=False),
            ])

        if instruction:
            parts.extend([
                "",
                "GENERATION_INSTRUCTION:",
                instruction,
            ])
        else:
            parts.extend([
                "",
                "GENERATION_INSTRUCTION:",
                "Generate a scene for this moment.",
                "Include narration, speech (if appropriate), voices, and clickables.",
                "Estimate time_elapsed for this scene.",
            ])

        parts.extend([
            "",
            "Output JSON matching NarratorOutput schema.",
            "Include time_elapsed estimate.",
        ])

        return "\n".join(parts)

    def _call_claude(self, prompt: str) -> Dict[str, Any]:
        """Call Claude CLI and parse response."""
        # Use -c to continue conversation (persistent session)
        # --dangerously-skip-permissions for non-interactive execution
        # --add-dir ../../ to include project context
        base_flags = [
            "--dangerously-skip-permissions",
            "--output-format", "json",
            "--verbose",
            "--add-dir", "../.."
        ]

        if self.session_started:
            cmd = ["claude", "-c", "-p", prompt] + base_flags
        else:
            cmd = ["claude", "-p", prompt] + base_flags
            self.session_started = True

        logger.info(f"[NarratorService] Calling Claude from {self.working_dir}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.working_dir
            )

            if result.returncode != 0:
                logger.error(f"[NarratorService] Claude CLI failed: {result.stderr}")
                return self._fallback_response()

            # Parse JSON response - Claude CLI wraps result in envelope
            response_text = result.stdout.strip()
            logger.debug(f"[NarratorService] Raw response: {response_text[:500]}...")

            try:
                envelope = json.loads(response_text)

                # Extract actual result from envelope
                if isinstance(envelope, dict) and 'result' in envelope:
                    actual_result = envelope['result']

                    # Handle markdown code blocks in result
                    if isinstance(actual_result, str):
                        if actual_result.startswith("```json"):
                            lines = actual_result.split("\n")
                            actual_result = "\n".join(lines[1:-1])
                        elif actual_result.startswith("```"):
                            lines = actual_result.split("\n")
                            actual_result = "\n".join(lines[1:-1])

                        return json.loads(actual_result)
                    return actual_result
                else:
                    # Direct response (no envelope)
                    return envelope

            except json.JSONDecodeError:
                # Maybe it's a plain text response, try to extract JSON
                if "```json" in response_text:
                    start = response_text.find("```json") + 7
                    end = response_text.find("```", start)
                    if end > start:
                        return json.loads(response_text[start:end].strip())
                raise

        except subprocess.TimeoutExpired:
            logger.error("[NarratorService] Claude CLI timed out")
            return self._fallback_response()
        except json.JSONDecodeError as e:
            logger.error(f"[NarratorService] Failed to parse response: {e}")
            logger.error(f"[NarratorService] Response was: {result.stdout[:500] if result else 'None'}")
            return self._fallback_response()
        except FileNotFoundError:
            logger.error("[NarratorService] Claude CLI not found")
            return self._fallback_response()
        except Exception as e:
            logger.error(f"[NarratorService] Unexpected error: {e}")
            return self._fallback_response()

    def _fallback_response(self) -> Dict[str, Any]:
        """Return a minimal fallback response using SceneTree schema."""
        return {
            "scene": {
                "id": "scene_fallback",
                "location": {
                    "place": "place_unknown",
                    "name": "Unknown",
                    "region": "Somewhere in England",
                    "time": "unknown"
                },
                "present": [],
                "atmosphere": ["The fire has burned low.", "Cold seeps through your cloak."],
                "narration": [
                    {
                        "text": "The moment stretches in silence.",
                        "clickable": {}
                    }
                ],
                "voices": [],
                "freeInput": {
                    "enabled": True,
                    "handler": "narrator",
                    "context": []
                }
            },
            "time_elapsed": "1 minute",
            "mutations": [],
            "seeds": []
        }

    def reset_session(self):
        """Reset the narrator session (for new playthrough)."""
        self.session_started = False
        logger.info("[NarratorService] Session reset")
