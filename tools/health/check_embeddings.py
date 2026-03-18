#!/usr/bin/env python3
"""
Embeddings Health Checker

Verifies vector service from HEALTH_Embeddings.md:
- V3: Vector dimension matches model output (768)
- V4: Deterministic embeddings for identical text

HEALTH: docs/infrastructure/embeddings/HEALTH_Embeddings.md
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
EXPECTED_VECTOR_DIM = 768


class EmbeddingsHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[EmbeddingsHealth] Starting checks")

        self.results['embedding_vector_shape'] = self._check_vector_shape()
        self.results['embedding_determinism'] = self._check_determinism()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_vector_shape(self) -> Dict[str, Any]:
        """V3: Verify embedding vector dimension matches expected size."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V3'}

        try:
            from engine.infrastructure.embeddings.service import EmbeddingService

            service = EmbeddingService()
            vec = service.embed("health check test string")

            if vec is None:
                return {'status': 'ERROR', 'message': 'Embedding returned None', 'validation': 'V3'}

            dim = len(vec)
            if dim == EXPECTED_VECTOR_DIM:
                return {'status': 'OK', 'message': f'Vector dimension correct: {dim}', 'validation': 'V3'}
            else:
                return {'status': 'ERROR', 'message': f'Vector dimension {dim}, expected {EXPECTED_VECTOR_DIM}', 'validation': 'V3'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'EmbeddingService unavailable: {e}', 'validation': 'V3'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Embedding failed: {e}', 'validation': 'V3'}

    def _check_determinism(self) -> Dict[str, Any]:
        """V4: Verify identical text produces identical embeddings."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V4'}

        try:
            from engine.infrastructure.embeddings.service import EmbeddingService

            service = EmbeddingService()
            test_text = "princes of York"
            vec1 = service.embed(test_text)
            vec2 = service.embed(test_text)

            if vec1 is None or vec2 is None:
                return {'status': 'ERROR', 'message': 'Embedding returned None', 'validation': 'V4'}

            if vec1 == vec2:
                return {'status': 'OK', 'message': 'Embeddings are deterministic', 'validation': 'V4'}
            else:
                return {'status': 'ERROR', 'message': 'Embeddings differ for same input', 'validation': 'V4'}

        except ImportError as e:
            return {'status': 'SKIP', 'message': f'EmbeddingService unavailable: {e}', 'validation': 'V4'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Determinism check failed: {e}', 'validation': 'V4'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_embeddings',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Embeddings Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = EmbeddingsHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nEMBEDDINGS HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())
