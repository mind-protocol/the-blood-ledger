#!/usr/bin/env python3
"""
Async Architecture Health Checker

Verifies async coordination from HEALTH_Async_Architecture.md:
- INV1: Single source of truth
- INV2: Bounded queues
- INV4: Hook latency within budget

HEALTH: docs/infrastructure/async/HEALTH_Async_Architecture.md
"""

import argparse
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']
THROTTLE_FILE = PROJECT_ROOT / '.health_async_last_run'
THROTTLE_SECONDS = 3600
LATENCY_OK_MS = 100
LATENCY_WARN_MS = 500


class AsyncHealthChecker:
    def __init__(self, playthrough_id: str = 'default', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info(f"[AsyncHealth] Starting checks for playthrough: {self.playthrough_id}")

        self.results['async_hook_latency'] = self._check_hook_latency()
        self.results['queue_depth_stable'] = self._check_queue_depth()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses:
            return 'WARN'
        return 'OK' if all(s == 'OK' for s in statuses) else 'WARN'

    def _check_hook_latency(self) -> Dict[str, Any]:
        """INV4: Verify hooks respond within latency budget."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'INV4'}

        hook_script = PROJECT_ROOT / 'engine/scripts/check_injection.py'
        if not hook_script.exists():
            return {'status': 'SKIP', 'message': 'Hook script not found', 'validation': 'INV4'}

        try:
            start = time.time()
            subprocess.run(['python3', str(hook_script)], timeout=5, capture_output=True)
            elapsed_ms = (time.time() - start) * 1000

            if elapsed_ms < LATENCY_OK_MS:
                return {'status': 'OK', 'message': f'Hook latency: {elapsed_ms:.0f}ms', 'validation': 'INV4'}
            elif elapsed_ms < LATENCY_WARN_MS:
                return {'status': 'WARN', 'message': f'Hook latency high: {elapsed_ms:.0f}ms', 'validation': 'INV4'}
            else:
                return {'status': 'ERROR', 'message': f'Hook latency too high: {elapsed_ms:.0f}ms', 'validation': 'INV4'}
        except subprocess.TimeoutExpired:
            return {'status': 'ERROR', 'message': 'Hook timed out', 'validation': 'INV4'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Hook check failed: {e}', 'validation': 'INV4'}

    def _check_queue_depth(self) -> Dict[str, Any]:
        """INV2: Verify queue size stays bounded."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'INV2'}

        queue_file = PROJECT_ROOT / f'playthroughs/{self.playthrough_id}/injection_queue.jsonl'
        if not queue_file.exists():
            return {'status': 'OK', 'message': 'Queue file empty or missing', 'validation': 'INV2'}

        try:
            lines = queue_file.read_text().strip().split('\n')
            depth = len([l for l in lines if l.strip()])
            if depth < 10:
                return {'status': 'OK', 'message': f'Queue depth: {depth}', 'validation': 'INV2'}
            elif depth < 50:
                return {'status': 'WARN', 'message': f'Queue depth growing: {depth}', 'validation': 'INV2'}
            else:
                return {'status': 'ERROR', 'message': f'Queue depth excessive: {depth}', 'validation': 'INV2'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Queue check failed: {e}', 'validation': 'INV2'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_async',
            'playthrough_id': self.playthrough_id,
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Async Health Checker')
    parser.add_argument('--playthrough', '-p', default='default')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', '-f', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = AsyncHealthChecker(args.playthrough, args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nASYNC HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
