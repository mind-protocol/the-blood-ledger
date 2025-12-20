#!/bin/bash
# Blood Ledger - Run both frontend and backend with logging

LOG_DIR="data/logs"
mkdir -p "$LOG_DIR"

# Kill any existing processes
pkill -f "uvicorn engine.infrastructure.api.app" 2>/dev/null
pkill -f "next dev" 2>/dev/null
sleep 1

echo "Starting backend on :8000..."
cd "$(dirname "$0")"
python3 -m uvicorn engine.infrastructure.api.app:app --host 0.0.0.0 --port 8000 --reload 2>&1 | tee "$LOG_DIR/backend-console.log" &
BACKEND_PID=$!

sleep 2

echo "Starting frontend on :3000..."
cd frontend
npm run dev 2>&1 | tee "../$LOG_DIR/frontend.log" &
FRONTEND_PID=$!

echo ""
echo "Services running:"
echo "  Backend:  http://localhost:8000 (PID: $BACKEND_PID)"
echo "  Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "Logs:"
echo "  $LOG_DIR/backend.log (structured)"
echo "  $LOG_DIR/backend-console.log (console)"
echo "  $LOG_DIR/frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
