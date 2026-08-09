#!/usr/bin/env bash
# GuardianAI Code Auto-Formatter Script
# Purpose: Formats backend Python code with Black and verifies formatting standards.

set -e

echo "=================================================="
echo "       Formatting GuardianAI Workspace Code       "
echo "=================================================="

# 1. Format Python Backend Code with Black
echo "[1/2] Auto-formatting Python code with Black..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate || source venv/Scripts/activate
fi
black app main.py
cd ..

# 2. Linting Python Backend Code with Flake8
echo "[2/2] Checking style rules with Flake8..."
cd backend
flake8 app main.py || true
cd ..

echo "=================================================="
echo "          Code Formatting Completed!              "
echo "=================================================="
