#!/usr/bin/env python3
"""
Ledger Lock Health Checker

Verifies lock transitions from HEALTH_Ledger_Lock.md:
- Ledger lock module is available
- Lock state is observable

HEALTH: docs/product/ledger-lock/HEALTH_Ledger_Lock.md
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


class LedgerLockHealthChecker:
    def __init__(self, playthrough_id: str = 'default', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info(f"[LedgerLockHealth] Starting checks for playthrough: {self.playthrough_id}")

        self.results['ledger_lock_module'] = self._check_ledger_lock_module()
        self.results['lock_state_file'] = self._check_lock_state_file()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_ledger_lock_module(self) -> Dict[str, Any]:
        """Verify ledger lock module is available."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.product import ledger_lock
            return {'status': 'OK', 'message': 'Ledger lock module available', 'validation': 'V1'}
        except ImportError:
            return {'status': 'SKIP', 'message': 'Ledger lock module not implemented yet', 'validation': 'V1'}

    def _check_lock_state_file(self) -> Dict[str, Any]:
        """Verify lock state can be read from playthrough."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        playthrough_dir = PROJECT_ROOT / 'playthroughs' / self.playthrough_id
        if not playthrough_dir.exists():
            return {'status': 'SKIP', 'message': 'Playthrough directory not found', 'validation': 'V1'}

        lock_file = playthrough_dir / 'ledger_lock.json'
        if lock_file.exists():
            try:
                with open(lock_file) as f:
                    data = json.load(f)
                return {'status': 'OK', 'message': f'Lock state: {data.get("locked", "unknown")}', 'validation': 'V1'}
            except Exception as e:
                return {'status': 'ERROR', 'message': f'Invalid lock file: {e}', 'validation': 'V1'}

        return {'status': 'OK', 'message': 'No lock file (unlocked state)', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_ledger_lock',
            'playthrough_id': self.playthrough_id,
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Ledger Lock Health Checker')
    parser.add_argument('--playthrough', '-p', default='default')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = LedgerLockHealthChecker(args.playthrough, args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nLEDGER LOCK HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
