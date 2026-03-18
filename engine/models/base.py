"""
Engine Models — Base Types

Proxy to ngram implementation.
"""

import sys
from pathlib import Path

# Proxy to ngram implementation
NGRAM_REPO = Path("/home/mind-protocol/ngram")
MODULE_PATH = "engine/models/base.py"
TARGET_FILE = NGRAM_REPO / MODULE_PATH

if not TARGET_FILE.exists():
    raise ImportError(f"Cannot find {TARGET_FILE}")

with open(TARGET_FILE, "r") as f:
    code = f.read()

exec(code, globals())
