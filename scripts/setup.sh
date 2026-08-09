#!/usr/bin/env bash
# GuardianAI Local Environment Setup Script
# Purpose: One-command automated setup script installing backend Python dependencies and frontend npm packages.

set -e

echo "=================================================="
echo "      GuardianAI Local Development Setup"
echo "=================================================="

# 1. Environment Configuration Setup
if [ ! -f .env ]; then
    echo "[1/3] Creating .env file from .env.example..."
    cp .env.example .env
else
    echo "[1/3] Existing .env file found. Skipping."
fi

# 2. Backend Virtual Environment Setup
echo "[2/3] Setting up Python virtual environment and installing backend requirements..."
cd backend
python3 -m venv venv
source venv/bin/activate || source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 3. Frontend npm Dependencies Setup
echo "[3/3] Installing frontend npm dependencies..."
cd frontend
npm install
cd ..

echo "=================================================="
echo " Setup Complete!"
echo " Start Backend:  cd backend && uvicorn main:app --reload"
echo " Start Frontend: cd frontend && npm run dev"
echo "=================================================="
