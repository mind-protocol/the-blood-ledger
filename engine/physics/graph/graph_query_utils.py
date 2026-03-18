import sys
from pathlib import Path

# Proxy to ngram implementation
NGRAM_REPO = Path("/home/mind-protocol/ngram")
MODULE_PATH = "engine/physics/graph/graph_query_utils.py"
TARGET_FILE = NGRAM_REPO / MODULE_PATH

if not TARGET_FILE.exists():
    raise ImportError(f"Cannot find {TARGET_FILE}")

with open(TARGET_FILE, "r") as f:
    code = f.read()

# Execute the code in the current global namespace
# This ensures relative imports work as expected within the local package
exec(code, globals())
