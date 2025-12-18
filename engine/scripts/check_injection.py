#!/usr/bin/env python3
"""
Hook script for Claude Code PostToolUse.
Checks injection_queue.jsonl for pending interruptions.
Returns injection to Narrator via additionalContext.
"""

import json
import os
import sys

# Path relative to script location (works from any directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
INJECTION_FILE = os.path.join(PROJECT_ROOT, "playthroughs/default/injection_queue.jsonl")


def main():
    if not os.path.exists(INJECTION_FILE):
        # No file, no injection
        print(json.dumps({"decision": None}))
        return

    with open(INJECTION_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        # Empty file, no injection
        print(json.dumps({"decision": None}))
        return

    # Take first injection (FIFO)
    injection = json.loads(lines[0].strip())

    # Rewrite file with remaining injections
    with open(INJECTION_FILE, "w") as f:
        f.writelines(lines[1:])

    # Return to Claude Code with injection in additionalContext
    print(json.dumps({
        "decision": None,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": json.dumps(injection)
        }
    }))


if __name__ == "__main__":
    main()
