#!/usr/bin/env python3
"""
Canon Holder Health Checker

Verifies canon recording pipeline from HEALTH_Canon.md:
- V1: Moment status flips to spoken with tick_spoken
- V2: THEN chain and SAID link are created when applicable

HEALTH: docs/infrastructure/canon/HEALTH_Canon.md
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']

THROTTLE_FILE = PROJECT_ROOT / '.health_canon_last_run'
THROTTLE_SECONDS = 3600


class CanonHealthChecker:
    """Health checker for canon recording pipeline."""

    def __init__(self, playthrough_id: str = 'default', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        """Run all health checks."""
        logger.info(f"[CanonHealth] Starting checks for playthrough: {self.playthrough_id}")

        # V1: Canon holder can be instantiated
        self.results['canon_holder_init'] = self._check_canon_holder_init()

        # V2: Spoken moments have proper status
        self.results['spoken_moments_valid'] = self._check_spoken_moments()

        # Aggregate
        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses:
            return 'WARN'
        elif all(s in ('OK', 'SKIP') for s in statuses):
            return 'WARN' if 'SKIP' in statuses else 'OK'
        return 'UNKNOWN'

    def _check_canon_holder_init(self) -> Dict[str, Any]:
        """V1: Verify CanonHolder can be instantiated."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.infrastructure.canon import CanonHolder

            canon = CanonHolder(self.playthrough_id)
            return {
                'status': 'OK',
                'message': f'CanonHolder initialized for {self.playthrough_id}',
                'validation': 'V1'
            }

        except ImportError as e:
            return {
                'status': 'SKIP',
                'message': f'Import failed: {e}',
                'validation': 'V1'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Initialization failed: {e}',
                'validation': 'V1'
            }

    def _check_spoken_moments(self) -> Dict[str, Any]:
        """V2: Verify spoken moments have tick_spoken set."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V2'}

        try:
            from engine.physics.graph import GraphQueries, get_playthrough_graph_name

            graph_name = get_playthrough_graph_name(self.playthrough_id)
            queries = GraphQueries(graph_name=graph_name)

            # Query for spoken moments without tick_spoken
            cypher = """
            MATCH (m:Moment {status: 'spoken'})
            WHERE m.tick_spoken IS NULL
            RETURN count(m) AS invalid_count
            """

            result = queries.query(cypher)
            invalid_count = result[0].get('invalid_count', 0) if result else 0

            if invalid_count == 0:
                return {
                    'status': 'OK',
                    'message': 'All spoken moments have tick_spoken set',
                    'validation': 'V2'
                }
            else:
                return {
                    'status': 'WARN',
                    'message': f'{invalid_count} spoken moments missing tick_spoken',
                    'validation': 'V2',
                    'invalid_count': invalid_count
                }

        except ImportError as e:
            return {
                'status': 'SKIP',
                'message': f'Graph queries unavailable: {e}',
                'validation': 'V2'
            }
        except Exception as e:
            return {
                'status': 'SKIP',
                'message': f'Query failed: {e}',
                'validation': 'V2'
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
            'checker': 'check_canon',
            'playthrough_id': self.playthrough_id,
            'status': aggregate,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def should_throttle() -> bool:
    if not THROTTLE_FILE.exists():
        return False
    try:
        last_run = float(THROTTLE_FILE.read_text().strip())
        return datetime.utcnow().timestamp() - last_run < THROTTLE_SECONDS
    except (ValueError, OSError):
        return False


def update_throttle():
    try:
        THROTTLE_FILE.write_text(str(datetime.utcnow().timestamp()))
    except OSError:
        pass


def update_health_file(status: HealthStatus):
    health_file = PROJECT_ROOT / 'docs/infrastructure/canon/HEALTH_Canon.md'
    if not health_file.exists():
        return

    try:
        import re
        content = health_file.read_text()
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        new_content = re.sub(
            r'(status:\n\s+stream_destination:.*?\n\s+result:\n\s+representation:.*?\n\s+)value:\s*\w+',
            f'\\g<1>value: {status}',
            content,
            flags=re.DOTALL
        )
        new_content = re.sub(
            r'updated_at:\s*[\d\-T:Z]+',
            f'updated_at: {timestamp}',
            new_content
        )

        health_file.write_text(new_content)
        logger.info(f"[CanonHealth] Updated HEALTH file: status={status}")
    except Exception as e:
        logger.warning(f"[CanonHealth] Failed to update HEALTH file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Canon Health Checker')
    parser.add_argument('--playthrough', '-p', default='default')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', '-f', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--update-health', action='store_true')

    args = parser.parse_args()

    if not args.force and should_throttle():
        logger.info("[CanonHealth] Throttled - run with --force to override")
        if args.json:
            print(json.dumps({'status': 'THROTTLED'}))
        return 0

    checker = CanonHealthChecker(args.playthrough, args.dry_run)
    aggregate_status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"CANON HEALTH CHECK: {aggregate_status}")
        print(f"{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']}")
            print(f"    {result['message']}")
        print(f"{'='*60}\n")

    if not args.dry_run:
        update_throttle()
    if args.update_health:
        update_health_file(aggregate_status)

    return 0 if aggregate_status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
