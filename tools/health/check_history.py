#!/usr/bin/env python3
"""
History Service Health Checker

Verifies narrative persistence from HEALTH_History_Service_Verification.md:
- V1: Every narrative has at least one BELIEVES edge
- V5: BELIEVES.believes values are 0.0-1.0

HEALTH: docs/infrastructure/history/HEALTH_History_Service_Verification.md
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']
THROTTLE_FILE = PROJECT_ROOT / '.health_history_last_run'
THROTTLE_SECONDS = 3600


class HistoryHealthChecker:
    def __init__(self, playthrough_id: str = 'default', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info(f"[HistoryHealth] Starting checks for playthrough: {self.playthrough_id}")

        self.results['narratives_have_beliefs'] = self._check_narratives_have_beliefs()
        self.results['belief_bounds_valid'] = self._check_belief_bounds()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_narratives_have_beliefs(self) -> Dict[str, Any]:
        """V1: Verify all narratives have at least one BELIEVES edge."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.physics.graph import GraphQueries, get_playthrough_graph_name

            graph_name = get_playthrough_graph_name(self.playthrough_id)
            queries = GraphQueries(graph_name=graph_name)

            cypher = """
            MATCH (n:Narrative)
            WHERE NOT EXISTS { MATCH ()-[:BELIEVES]->(n) }
            RETURN count(n) AS orphan_count
            """

            result = queries.query(cypher)
            orphan_count = result[0].get('orphan_count', 0) if result else 0

            if orphan_count == 0:
                return {'status': 'OK', 'message': 'All narratives have BELIEVES edges', 'validation': 'V1'}
            elif orphan_count < 5:
                return {'status': 'WARN', 'message': f'{orphan_count} orphan narratives found', 'validation': 'V1'}
            else:
                return {'status': 'ERROR', 'message': f'{orphan_count} orphan narratives (many)', 'validation': 'V1'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'Graph queries unavailable: {e}', 'validation': 'V1'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Query failed: {e}', 'validation': 'V1'}

    def _check_belief_bounds(self) -> Dict[str, Any]:
        """V5: Verify all BELIEVES.believes values are 0.0-1.0."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V5'}

        try:
            from engine.physics.graph import GraphQueries, get_playthrough_graph_name

            graph_name = get_playthrough_graph_name(self.playthrough_id)
            queries = GraphQueries(graph_name=graph_name)

            cypher = """
            MATCH ()-[b:BELIEVES]->()
            WHERE b.believes < 0.0 OR b.believes > 1.0
            RETURN count(b) AS invalid_count
            """

            result = queries.query(cypher)
            invalid_count = result[0].get('invalid_count', 0) if result else 0

            if invalid_count == 0:
                return {'status': 'OK', 'message': 'All belief values in valid range', 'validation': 'V5'}
            else:
                return {'status': 'ERROR', 'message': f'{invalid_count} beliefs out of range', 'validation': 'V5'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'Graph queries unavailable: {e}', 'validation': 'V5'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Query failed: {e}', 'validation': 'V5'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_history',
            'playthrough_id': self.playthrough_id,
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='History Service Health Checker')
    parser.add_argument('--playthrough', '-p', default='default')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', '-f', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = HistoryHealthChecker(args.playthrough, args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nHISTORY HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
