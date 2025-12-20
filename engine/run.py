#!/usr/bin/env python3
"""
Blood Ledger — Run Script

Start the backend server locally.

Usage:
    python run.py
    python run.py --host 0.0.0.0 --port 8000
"""

import os
import sys
import argparse
import logging

# Add parent directory to path so 'from engine.' imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run Blood Ledger backend')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    parser.add_argument('--graph', default='blood_ledger', help='Graph name')
    parser.add_argument('--db-host', default='localhost', help='FalkorDB host')
    parser.add_argument('--db-port', type=int, default=6379, help='FalkorDB port')
    args = parser.parse_args()

    # Set environment variables
    os.environ['GRAPH_NAME'] = args.graph
    os.environ['FALKORDB_HOST'] = args.db_host
    os.environ['FALKORDB_PORT'] = str(args.db_port)

    logger.info(f"Starting Blood Ledger backend on {args.host}:{args.port}")
    logger.info(f"FalkorDB: {args.db_host}:{args.db_port}, Graph: {args.graph}")

    import uvicorn

    # Use fully-qualified module path so uvicorn never imports an unrelated
    # third-party `api` package when run outside the engine/ directory.
    uvicorn.run(
        "engine.infrastructure.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
