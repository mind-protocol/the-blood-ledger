#!/usr/bin/env python3
"""
Schema Archive Health Checker

Verifies archive integrity from HEALTH_Schema_Archive_Verification.md:
- Archive documentation exists
- Schema files are accessible

HEALTH: docs/schema/archive/HEALTH_Schema_Archive_Verification.md
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

PROJECT_ROOT = Path(__file__).parent.parent.parent
SCHEMA_DIR = PROJECT_ROOT / 'docs/schema'
ARCHIVE_DIR = PROJECT_ROOT / 'docs/schema/archive'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class SchemaArchiveHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[SchemaArchiveHealth] Starting checks")

        self.results['schema_docs_exist'] = self._check_schema_docs()
        self.results['archive_docs_exist'] = self._check_archive_docs()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_schema_docs(self) -> Dict[str, Any]:
        """Verify schema documentation exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not SCHEMA_DIR.exists():
            return {'status': 'WARN', 'message': 'docs/schema directory not found', 'validation': 'V1'}

        md_files = list(SCHEMA_DIR.glob('*.md'))
        return {
            'status': 'OK' if md_files else 'WARN',
            'message': f'{len(md_files)} schema docs found' if md_files else 'No schema docs',
            'validation': 'V1',
            'count': len(md_files)
        }

    def _check_archive_docs(self) -> Dict[str, Any]:
        """Verify archive documentation exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not ARCHIVE_DIR.exists():
            return {'status': 'WARN', 'message': 'docs/schema/archive directory not found', 'validation': 'V1'}

        md_files = list(ARCHIVE_DIR.glob('*.md'))
        sync_files = [f for f in md_files if f.name.startswith('SYNC_')]

        return {
            'status': 'OK' if sync_files else 'WARN',
            'message': f'{len(sync_files)} archive SYNC files found' if sync_files else 'No archive SYNC files',
            'validation': 'V1',
            'count': len(sync_files)
        }

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_schema_archive',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Schema Archive Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = SchemaArchiveHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nSCHEMA ARCHIVE HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
