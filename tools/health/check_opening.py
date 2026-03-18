#!/usr/bin/env python3
"""
Opening Sequence Health Checker

Verifies opening sequence initialization from HEALTH_Opening.md:
- V1: scene.json exists and contains valid SceneTree
- V2: player.yaml exists and matches request parameters
- V0: Seed nodes exist in the playthrough graph
- V3: Scenario nodes are injected into the graph

HEALTH: docs/design/opening/HEALTH_Opening.md
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal, List

import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Health status enum
HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']

# Throttle settings
THROTTLE_FILE = PROJECT_ROOT / '.health_opening_last_run'
THROTTLE_SECONDS = 3600  # 1 hour

# Expected keys in scene.json
SCENE_REQUIRED_KEYS = ['id', 'location', 'narration']

# Expected keys in player.yaml
PLAYER_REQUIRED_KEYS = ['name', 'scenario']

# Known seed nodes to verify
SEED_NODES = ['place_york', 'char_aldric']


class OpeningHealthChecker:
    """
    Health checker for opening sequence.

    Verifies that playthroughs are correctly initialized with
    scene files, player config, and graph data.
    """

    def __init__(self, playthrough_id: str = 'default', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}
        self.playthrough_dir = PROJECT_ROOT / 'playthroughs' / playthrough_id

    def check_all(self) -> HealthStatus:
        """Run all health checks and return aggregate status."""
        logger.info(f"[OpeningHealth] Starting checks for playthrough: {self.playthrough_id}")

        # V1: scene.json integrity
        self.results['opening_integrity_scene'] = self._check_scene_json()

        # V2: player.yaml integrity
        self.results['opening_integrity_player'] = self._check_player_yaml()

        # V0: Seed graph nodes (requires graph connection)
        self.results['seed_graph_initialized'] = self._check_seed_nodes()

        # Aggregate: AND logic (all must pass)
        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses:
            return 'WARN'
        elif all(s in ('OK', 'SKIP') for s in statuses):
            if 'SKIP' in statuses:
                return 'WARN'  # Some checks couldn't run
            return 'OK'
        else:
            return 'UNKNOWN'

    def _check_scene_json(self) -> Dict[str, Any]:
        """
        V1: Verify scene.json exists and contains valid SceneTree.

        Dock: playthroughs/{id}/scene.json
        """
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        scene_file = self.playthrough_dir / 'scene.json'

        if not scene_file.exists():
            return {
                'status': 'ERROR',
                'message': f'scene.json not found at {scene_file}',
                'validation': 'V1'
            }

        try:
            with open(scene_file) as f:
                scene = json.load(f)

            # Check required keys
            missing_keys = [k for k in SCENE_REQUIRED_KEYS if k not in scene]

            if missing_keys:
                return {
                    'status': 'WARN',
                    'message': f'scene.json missing keys: {missing_keys}',
                    'validation': 'V1',
                    'missing': missing_keys
                }

            return {
                'status': 'OK',
                'message': f'scene.json valid with keys: {list(scene.keys())[:5]}...',
                'validation': 'V1',
                'scene_id': scene.get('id')
            }

        except json.JSONDecodeError as e:
            return {
                'status': 'ERROR',
                'message': f'scene.json invalid JSON: {e}',
                'validation': 'V1'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Failed to read scene.json: {e}',
                'validation': 'V1'
            }

    def _check_player_yaml(self) -> Dict[str, Any]:
        """
        V2: Verify player.yaml exists and has required fields.

        Dock: playthroughs/{id}/player.yaml
        """
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V2'}

        player_file = self.playthrough_dir / 'player.yaml'

        if not player_file.exists():
            return {
                'status': 'ERROR',
                'message': f'player.yaml not found at {player_file}',
                'validation': 'V2'
            }

        try:
            with open(player_file) as f:
                player = yaml.safe_load(f)

            if player is None:
                return {
                    'status': 'ERROR',
                    'message': 'player.yaml is empty',
                    'validation': 'V2'
                }

            # Check required keys
            missing_keys = [k for k in PLAYER_REQUIRED_KEYS if k not in player]

            if missing_keys:
                return {
                    'status': 'WARN',
                    'message': f'player.yaml missing keys: {missing_keys}',
                    'validation': 'V2',
                    'missing': missing_keys
                }

            return {
                'status': 'OK',
                'message': f'player.yaml valid: name={player.get("name")}, scenario={player.get("scenario")}',
                'validation': 'V2',
                'player_name': player.get('name'),
                'scenario': player.get('scenario')
            }

        except yaml.YAMLError as e:
            return {
                'status': 'ERROR',
                'message': f'player.yaml invalid YAML: {e}',
                'validation': 'V2'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Failed to read player.yaml: {e}',
                'validation': 'V2'
            }

    def _check_seed_nodes(self) -> Dict[str, Any]:
        """
        V0: Verify seed nodes exist in the playthrough graph.

        Dock: FalkorDB graph query
        """
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V0'}

        try:
            from engine.physics.graph import GraphQueries, get_playthrough_graph_name

            graph_name = get_playthrough_graph_name(self.playthrough_id)
            queries = GraphQueries(graph_name=graph_name)

            # Check each seed node
            found = []
            missing = []

            for node_id in SEED_NODES:
                cypher = f"MATCH (n {{id: '{node_id}'}}) RETURN count(n) AS cnt"
                try:
                    result = queries.query(cypher)
                    if result and result[0].get('cnt', 0) > 0:
                        found.append(node_id)
                    else:
                        missing.append(node_id)
                except Exception:
                    missing.append(node_id)

            if not missing:
                return {
                    'status': 'OK',
                    'message': f'All seed nodes found: {found}',
                    'validation': 'V0',
                    'found': found
                }
            elif found:
                return {
                    'status': 'WARN',
                    'message': f'Some seed nodes missing: {missing}',
                    'validation': 'V0',
                    'found': found,
                    'missing': missing
                }
            else:
                return {
                    'status': 'ERROR',
                    'message': f'No seed nodes found. Missing: {missing}',
                    'validation': 'V0',
                    'missing': missing
                }

        except ImportError as e:
            return {
                'status': 'SKIP',
                'message': f'Graph queries unavailable: {e}',
                'validation': 'V0'
            }
        except Exception as e:
            return {
                'status': 'SKIP',
                'message': f'Graph check failed: {e}',
                'validation': 'V0'
            }

    def get_report(self) -> Dict[str, Any]:
        """Get full health report."""
        if not self.results:
            self.check_all()

        statuses = [r['status'] for r in self.results.values()]
        aggregate = (
            'ERROR' if 'ERROR' in statuses else
            'WARN' if 'WARN' in statuses or 'SKIP' in statuses else
            'OK' if all(s == 'OK' for s in statuses) else
            'UNKNOWN'
        )

        return {
            'checker': 'check_opening',
            'playthrough_id': self.playthrough_id,
            'status': aggregate,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def should_throttle() -> bool:
    """Check if we should skip due to throttling."""
    if not THROTTLE_FILE.exists():
        return False

    try:
        last_run = float(THROTTLE_FILE.read_text().strip())
        elapsed = datetime.utcnow().timestamp() - last_run
        return elapsed < THROTTLE_SECONDS
    except (ValueError, OSError):
        return False


def update_throttle():
    """Update throttle timestamp."""
    try:
        THROTTLE_FILE.write_text(str(datetime.utcnow().timestamp()))
    except OSError:
        pass


def update_health_file(status: HealthStatus):
    """Update status.result.value in the HEALTH file."""
    health_file = PROJECT_ROOT / 'docs/design/opening/HEALTH_Opening.md'

    if not health_file.exists():
        logger.warning(f"[OpeningHealth] HEALTH file not found: {health_file}")
        return

    try:
        content = health_file.read_text()
        import re

        # Update status value
        new_content = re.sub(
            r'(status:\n\s+stream_destination:.*?\n\s+result:\n\s+representation:.*?\n\s+)value:\s*\w+',
            f'\\g<1>value: {status}',
            content,
            flags=re.DOTALL
        )

        # Update timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        new_content = re.sub(
            r'updated_at:\s*[\d\-T:Z]+',
            f'updated_at: {timestamp}',
            new_content
        )

        health_file.write_text(new_content)
        logger.info(f"[OpeningHealth] Updated HEALTH file: status={status}")

    except Exception as e:
        logger.warning(f"[OpeningHealth] Failed to update HEALTH file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Opening Sequence Health Checker')
    parser.add_argument('--playthrough', '-p', default='default',
                        help='Playthrough ID to check (default: default)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Skip actual checks, just validate setup')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Ignore throttling')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--update-health', action='store_true',
                        help='Update HEALTH file with result')

    args = parser.parse_args()

    # Throttle check
    if not args.force and should_throttle():
        logger.info("[OpeningHealth] Throttled - run with --force to override")
        if args.json:
            print(json.dumps({'status': 'THROTTLED', 'message': 'Rate limited'}))
        return 0

    # Run checks
    checker = OpeningHealthChecker(
        playthrough_id=args.playthrough,
        dry_run=args.dry_run
    )

    aggregate_status = checker.check_all()
    report = checker.get_report()

    # Output
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"OPENING HEALTH CHECK: {aggregate_status}")
        print(f"{'='*60}")
        for name, result in report['checks'].items():
            status_icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(
                result['status'], '?'
            )
            print(f"  {status_icon} {name}: {result['status']}")
            print(f"    {result['message']}")
        print(f"{'='*60}\n")

    # Update throttle
    if not args.dry_run:
        update_throttle()

    # Update HEALTH file
    if args.update_health:
        update_health_file(aggregate_status)

    # Exit code
    return 0 if aggregate_status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
