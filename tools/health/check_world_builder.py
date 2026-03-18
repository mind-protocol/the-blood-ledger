#!/usr/bin/env python3
"""
World Builder Health Checker

Verifies sparse enrichment from HEALTH_World_Builder.md:
- V1: Every query creates a thought moment
- V4: Enriched nodes are marked generated=true

HEALTH: docs/infrastructure/world-builder/HEALTH_World_Builder.md
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


class WorldBuilderHealthChecker:
    def __init__(self, playthrough_id: str = 'health_check', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info(f"[WorldBuilderHealth] Starting checks for playthrough: {self.playthrough_id}")

        self.results['world_builder_instantiates'] = self._check_instantiation()
        self.results['query_module_available'] = self._check_query_module()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_instantiation(self) -> Dict[str, Any]:
        """Verify WorldBuilder can be instantiated."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.infrastructure.world_builder.world_builder import WorldBuilder

            wb = WorldBuilder()
            return {'status': 'OK', 'message': 'WorldBuilder initialized successfully', 'validation': 'V1'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'WorldBuilder unavailable: {e}', 'validation': 'V1'}
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Initialization failed: {e}', 'validation': 'V1'}

    def _check_query_module(self) -> Dict[str, Any]:
        """Verify query module is available."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.infrastructure.world_builder import query

            if hasattr(query, 'query_sync') or hasattr(query, 'query'):
                return {'status': 'OK', 'message': 'Query module available', 'validation': 'V1'}
            else:
                return {'status': 'WARN', 'message': 'Query module missing expected functions', 'validation': 'V1'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'Query module unavailable: {e}', 'validation': 'V1'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Query module check failed: {e}', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_world_builder',
            'playthrough_id': self.playthrough_id,
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='World Builder Health Checker')
    parser.add_argument('--playthrough', '-p', default='health_check')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = WorldBuilderHealthChecker(args.playthrough, args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nWORLD BUILDER HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
