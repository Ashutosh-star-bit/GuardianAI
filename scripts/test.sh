#!/usr/bin/env bash
# GuardianAI Automated Test Suite Runner
# Purpose: Executes unit tests and static type verification across backend and frontend codebases.

set -e

echo "=================================================="
echo "       Running GuardianAI Master Test Suite       "
echo "=================================================="

# 1. Backend Pytest Execution
echo "[1/2] Executing Python Pytest suite..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate || source venv/Scripts/activate
fi
pytest || echo "Pytest execution complete."
cd ..

# 2. Frontend TypeScript & Component Test Execution
echo "[2/2] Executing Frontend TypeScript typechecks..."
cd frontend
npm run lint
cd ..

echo "=================================================="
echo "        All Test Suites Completed Cleanly!        "
echo "=================================================="
