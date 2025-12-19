#!/usr/bin/env python3
"""
Seed a minimal Moment Graph sample into FalkorDB.

Usage:
    python engine/scripts/seed_moment_sample.py \
        --graph blood_ledger --db-host localhost --db-port 6379 \
        --sample data/samples/moment_sample.yaml

DOCS: docs/infrastructure/ops-scripts/PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from engine.physics.graph import GraphOps  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Seed sample moments into FalkorDB")
    parser.add_argument("--graph", default="blood_ledger", help="Graph name")
    parser.add_argument("--db-host", default="localhost", help="FalkorDB host")
    parser.add_argument("--db-port", type=int, default=6379, help="FalkorDB port")
    parser.add_argument(
        "--sample",
        default="data/samples/moment_sample.yaml",
        help="Path to sample YAML file"
    )
    parser.add_argument(
        "--playthrough",
        default="sample",
        help="Playthrough folder name (affects asset paths)"
    )
    args = parser.parse_args()

    sample_path = (PROJECT_ROOT / args.sample).resolve()
    if not sample_path.exists():
        raise SystemExit(f"Sample file not found: {sample_path}")

    ops = GraphOps(graph_name=args.graph, host=args.db_host, port=args.db_port)
    result = ops.apply(path=str(sample_path), playthrough=args.playthrough)

    print("Seed complete:")
    print(f"  Persisted: {len(result.persisted)} items")
    if result.duplicates:
        print(f"  Duplicates skipped: {len(result.duplicates)}")
    if result.errors:
        print("  Errors encountered:")
        for err in result.errors:
            print(f"    - {err['item']}: {err['message']}")


if __name__ == "__main__":
    main()
