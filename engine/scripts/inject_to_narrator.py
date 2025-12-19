#!/usr/bin/env python3
"""
Inject a message to the narrator.

If narrator is running: writes to injection_queue.json
If narrator is not running: calls narrator directly with claude -p

DOCS: docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md

Usage:
    python inject_to_narrator.py <playthrough_id> <message>
    python inject_to_narrator.py pt_abc123 "Aldric wants to say something"
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
PLAYTHROUGHS_DIR = PROJECT_ROOT / "playthroughs"
NARRATOR_STATE_FILE = PLAYTHROUGHS_DIR / "narrator_state.json"


def is_narrator_running() -> bool:
    """Check if narrator session is currently active."""
    if not NARRATOR_STATE_FILE.exists():
        return False

    try:
        state = json.loads(NARRATOR_STATE_FILE.read_text())
        return state.get("running", False)
    except (json.JSONDecodeError, IOError):
        return False


def inject_via_queue(playthrough_id: str, message: str) -> dict:
    """Write to injection_queue.json for running narrator to pick up."""
    playthrough_dir = PLAYTHROUGHS_DIR / playthrough_id
    queue_file = playthrough_dir / "injection_queue.json"

    # Read existing queue
    queue = []
    if queue_file.exists():
        try:
            queue = json.loads(queue_file.read_text())
        except json.JSONDecodeError:
            queue = []

    # Add new injection
    injection = {
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "world_runner"
    }
    queue.append(injection)

    # Write back
    queue_file.write_text(json.dumps(queue, indent=2))

    return {"method": "queue", "injection": injection}


def inject_via_direct_call(playthrough_id: str, message: str) -> dict:
    """Call narrator directly with claude -p when no session is running."""
    narrator_dir = PROJECT_ROOT / "agents" / "narrator"

    # Build the prompt for the narrator
    prompt = f"""INJECTION from World Runner:
Playthrough: {playthrough_id}

{message}

Process this injection and update the scene if needed."""

    try:
        # Call claude in the narrator directory
        result = subprocess.run(
            ["claude", "-p", prompt, "--dangerously-skip-permissions"],
            cwd=str(narrator_dir),
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            "method": "direct",
            "exit_code": result.returncode,
            "stdout": result.stdout[:500] if result.stdout else "",
            "stderr": result.stderr[:500] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        return {"method": "direct", "error": "timeout"}
    except Exception as e:
        return {"method": "direct", "error": str(e)}


def inject(playthrough_id: str, message: str) -> dict:
    """
    Inject a message to the narrator.

    Automatically chooses the right method based on narrator state.
    """
    if is_narrator_running():
        return inject_via_queue(playthrough_id, message)
    else:
        return inject_via_direct_call(playthrough_id, message)


def main():
    if len(sys.argv) < 3:
        print("Usage: python inject_to_narrator.py <playthrough_id> <message>")
        sys.exit(1)

    playthrough_id = sys.argv[1]
    message = " ".join(sys.argv[2:])

    result = inject(playthrough_id, message)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
