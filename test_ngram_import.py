import sys
from pathlib import Path

def test_import():
    ngram_root = Path("/home/mind-protocol/ngram")
    if ngram_root.exists():
        sys.path.insert(0, str(ngram_root))
        try:
            from engine.physics.graph.graph_queries import GraphQueries
            print("Successfully imported GraphQueries")
            print(f"GraphQueries members: {dir(GraphQueries)}")
        except ImportError as e:
            print(f"Failed to import GraphQueries: {e}")
    else:
        print("ngram root not found")

if __name__ == "__main__":
    test_import()
