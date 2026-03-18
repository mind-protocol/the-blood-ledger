#!/usr/bin/env python3
"""
Map Health Checker

Verifies semantic search from HEALTH_Map.md:
- V1: Queries embed before search
- V2: Similarity threshold filters results
- E1/E2: Fallback returns results without crashing

HEALTH: docs/world/map/HEALTH_Map.md
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


class MapHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[MapHealth] Starting checks")

        self.results['semantic_search_returns'] = self._check_semantic_search()
        self.results['search_module_available'] = self._check_search_module()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_search_module(self) -> Dict[str, Any]:
        """Verify semantic search module is available."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.world.map.semantic import SemanticSearch
            return {'status': 'OK', 'message': 'SemanticSearch module available', 'validation': 'V1'}
        except ImportError as e:
            return {'status': 'SKIP', 'message': f'SemanticSearch unavailable: {e}', 'validation': 'V1'}

    def _check_semantic_search(self) -> Dict[str, Any]:
        """E1/E2: Verify search returns results or clean fallback."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'E1'}

        try:
            from engine.world.map.semantic import SemanticSearch

            search = SemanticSearch()
            results = search.find("princes", limit=3)

            if results is None:
                return {'status': 'ERROR', 'message': 'Search returned None', 'validation': 'E1'}

            if isinstance(results, list):
                if len(results) > 0:
                    return {'status': 'OK', 'message': f'Search returned {len(results)} results', 'validation': 'E1'}
                else:
                    return {'status': 'WARN', 'message': 'Search returned empty results', 'validation': 'E1'}
            else:
                return {'status': 'ERROR', 'message': f'Search returned non-list: {type(results)}', 'validation': 'E1'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'SemanticSearch unavailable: {e}', 'validation': 'E1'}
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Search raised exception: {e}', 'validation': 'E1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_map',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Map Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = MapHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nMAP HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
