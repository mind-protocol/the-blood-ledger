#!/bin/bash
# Blood Ledger - Run both frontend and backend with logging

LOG_DIR="data/logs"
mkdir -p "$LOG_DIR"

echo "Starting frontend on :3000..."
cd frontend
npm run dev 2>&1 | tee "../$LOG_DIR/frontend.log" &
FRONTEND_PID=$!

echo ""
echo "Services running:"
echo "  Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "Logs:"
echo "  $LOG_DIR/frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both
trap "kill $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
