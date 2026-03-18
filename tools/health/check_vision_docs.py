#!/usr/bin/env python3
"""
Vision Docs Health Checker

Verifies documentation integrity from HEALTH_Vision_Doc_Integrity.md:
- Vision chain files exist
- CHAIN blocks are present in vision docs

HEALTH: docs/design/HEALTH_Vision_Doc_Integrity.md
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

PROJECT_ROOT = Path(__file__).parent.parent.parent
DESIGN_DIR = PROJECT_ROOT / 'docs/design'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class VisionDocsHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[VisionDocsHealth] Starting checks")

        self.results['vision_docs_exist'] = self._check_vision_docs_exist()
        self.results['chain_blocks_present'] = self._check_chain_blocks()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_vision_docs_exist(self) -> Dict[str, Any]:
        """Verify vision documentation exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not DESIGN_DIR.exists():
            return {'status': 'WARN', 'message': 'docs/design directory not found', 'validation': 'V1'}

        md_files = list(DESIGN_DIR.glob('*.md'))
        if not md_files:
            return {'status': 'WARN', 'message': 'No markdown files in docs/design', 'validation': 'V1'}

        return {
            'status': 'OK',
            'message': f'{len(md_files)} vision docs found',
            'validation': 'V1',
            'count': len(md_files)
        }

    def _check_chain_blocks(self) -> Dict[str, Any]:
        """Verify CHAIN blocks are present in vision docs."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not DESIGN_DIR.exists():
            return {'status': 'SKIP', 'message': 'Design directory not found', 'validation': 'V1'}

        patterns_files = list(DESIGN_DIR.glob('PATTERNS_*.md'))
        files_with_chain = 0
        files_without_chain = []

        for pf in patterns_files:
            try:
                content = pf.read_text()
                if '## CHAIN' in content or '```\nPATTERNS:' in content:
                    files_with_chain += 1
                else:
                    files_without_chain.append(pf.name)
            except Exception:
                pass

        if not patterns_files:
            return {'status': 'OK', 'message': 'No PATTERNS files to check', 'validation': 'V1'}

        if files_without_chain:
            return {
                'status': 'WARN',
                'message': f'{len(files_without_chain)} files missing CHAIN block',
                'validation': 'V1',
                'missing': files_without_chain[:5]
            }

        return {'status': 'OK', 'message': f'{files_with_chain} files have CHAIN blocks', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_vision_docs',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Vision Docs Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = VisionDocsHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nVISION DOCS HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
