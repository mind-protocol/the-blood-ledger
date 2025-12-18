#!/bin/bash
# SessionStart hook - mark narrator as running

# Read input JSON to get session_id
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id','unknown'))")

# State file location
STATE_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/../../playthroughs"
STATE_FILE="$STATE_DIR/narrator_state.json"

# Ensure directory exists
mkdir -p "$STATE_DIR"

# Write state
cat > "$STATE_FILE" << EOF
{
  "running": true,
  "session_id": "$SESSION_ID",
  "started_at": "$(date -Iseconds)",
  "pid": $$
}
EOF

echo "Narrator session started: $SESSION_ID"
exit 0
