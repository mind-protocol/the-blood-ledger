#!/bin/bash
# SessionEnd hook - mark narrator as stopped

# Read input JSON
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id','unknown'))")
REASON=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('reason','unknown'))")

# State file location
STATE_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/../../playthroughs"
STATE_FILE="$STATE_DIR/narrator_state.json"

# Write state
cat > "$STATE_FILE" << EOF
{
  "running": false,
  "session_id": "$SESSION_ID",
  "stopped_at": "$(date -Iseconds)",
  "reason": "$REASON"
}
EOF

echo "Narrator session ended: $SESSION_ID (reason: $REASON)"
exit 0
