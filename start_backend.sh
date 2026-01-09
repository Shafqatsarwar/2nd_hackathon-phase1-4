#!/bin/bash
# Kill existing uvicorn if any
pkill -f uvicorn
echo "Starting Backend..." > backend_launch.log
nohup uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload --env-file src/backend/.env.backend >> backend_launch.log 2>&1 &
echo "Backend started with PID $!" >> backend_launch.log
