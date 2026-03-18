# DOCS: docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md
"""
Agent CLI wrapper used by orchestration services.

This module provides a thin subprocess wrapper so engine code can invoke the
local CLI (e.g., `claude`) without hardcoding tool flags in each caller.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class AgentCliResult:
    returncode: int
    stdout: str
    stderr: str


def _build_command(
    prompt: str,
    output_format: Optional[str],
    add_dir: Optional[str],
    allowed_tools: Optional[Iterable[str]],
    skip_permissions: bool,
) -> list[str]:
    cli_bin = os.environ.get("NGRAM_AGENT_CLI_CMD", "claude")
    cmd = [cli_bin, "-p", prompt]

    format_flag = os.environ.get("NGRAM_AGENT_CLI_FORMAT_FLAG", "--format").strip()
    if output_format and format_flag:
        cmd.extend([format_flag, output_format])

    if add_dir:
        cmd.extend(["--add-dir", add_dir])

    if allowed_tools:
        cmd.extend(["--allowedTools", ",".join(allowed_tools)])

    if skip_permissions or os.environ.get("NGRAM_AGENT_CLI_SKIP_PERMISSIONS") == "1":
        cmd.append("--dangerously-skip-permissions")

    extra_args = os.environ.get("NGRAM_AGENT_CLI_EXTRA_ARGS")
    if extra_args:
        cmd.extend(extra_args.split())

    return cmd


def run_agent(
    prompt: str,
    working_dir: Optional[str] = None,
    timeout: int = 600,
    output_format: Optional[str] = None,
    add_dir: Optional[str] = None,
    allowed_tools: Optional[Iterable[str]] = None,
    skip_permissions: bool = False,
) -> AgentCliResult:
    """
    Invoke the configured agent CLI and return stdout/stderr.

    The CLI binary can be configured via `NGRAM_AGENT_CLI_CMD`.
    """
    cmd = _build_command(
        prompt=prompt,
        output_format=output_format,
        add_dir=add_dir,
        allowed_tools=allowed_tools,
        skip_permissions=skip_permissions,
    )

    completed = subprocess.run(
        cmd,
        cwd=working_dir,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return AgentCliResult(
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def extract_claude_text(stdout: str) -> str:
    """
    Extract plain text from CLI output.

    Supports raw text or Claude-style JSON payloads.
    """
    raw = stdout.strip()
    if not raw:
        return ""

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw

    if isinstance(payload, dict):
        if "content" in payload and isinstance(payload["content"], list):
            parts = []
            for entry in payload["content"]:
                if isinstance(entry, dict) and "text" in entry:
                    parts.append(entry["text"])
            if parts:
                return "".join(parts).strip()
        if "text" in payload and isinstance(payload["text"], str):
            return payload["text"].strip()

    return raw
