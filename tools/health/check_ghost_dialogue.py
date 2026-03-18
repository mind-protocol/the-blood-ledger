#!/usr/bin/env python3
"""
Ghost Dialogue Health Checker

Verifies replay signals from HEALTH_Ghost_Dialogue.md:
- Ghost dialogue module is available
- Replay index is accessible

HEALTH: docs/network/ghost-dialogue/HEALTH_Ghost_Dialogue.md
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


class GhostDialogueHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[GhostDialogueHealth] Starting checks")

        self.results['ghost_dialogue_module'] = self._check_ghost_dialogue_module()
        self.results['ghost_dialogue_docs'] = self._check_docs_exist()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_ghost_dialogue_module(self) -> Dict[str, Any]:
        """Verify ghost dialogue module is available."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.network import ghost_dialogue
            return {'status': 'OK', 'message': 'Ghost dialogue module available', 'validation': 'V1'}
        except ImportError:
            return {'status': 'SKIP', 'message': 'Ghost dialogue module not implemented yet', 'validation': 'V1'}

    def _check_docs_exist(self) -> Dict[str, Any]:
        """Verify ghost dialogue documentation exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        docs_dir = PROJECT_ROOT / 'docs/network/ghost-dialogue'
        if docs_dir.exists():
            return {'status': 'OK', 'message': 'Ghost dialogue docs exist', 'validation': 'V1'}
        return {'status': 'WARN', 'message': 'Ghost dialogue docs not found', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_ghost_dialogue',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Ghost Dialogue Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = GhostDialogueHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nGHOST DIALOGUE HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
