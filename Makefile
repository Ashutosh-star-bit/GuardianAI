# ==============================================================================
# GuardianAI Master Project Automation Makefile
# Purpose: One-command ergonomics for local development, testing, linting, formatting, and containerization.
# Usage: Run `make <target>` (e.g. `make dev`, `make test`, `make lint`, `make format`)
# ==============================================================================

.PHONY: help install dev dev-backend dev-frontend test test-backend test-frontend lint lint-backend lint-frontend format format-backend build build-frontend docker-up docker-down docker-build clean

# Default target
help:
	@echo "========================================================================"
	@echo "                   GuardianAI Developer CLI Commands                    "
	@echo "========================================================================"
	@echo "  make install         Install all backend Python & frontend npm dependencies"
	@echo "  make dev             Run backend and frontend dev servers concurrently"
	@echo "  make dev-backend     Run FastAPI backend server on http://localhost:8000"
	@echo "  make dev-frontend    Run Vite frontend server on http://localhost:5173"
	@echo "  make test            Run all backend Pytest and frontend unit tests"
	@echo "  make lint            Run Flake8 linting and ESLint code checks"
	@echo "  make format          Auto-format backend code (Black) and frontend code"
	@echo "  make build           Build production frontend bundle and typecheck"
	@echo "  make docker-up       Start Docker Compose multi-container stack"
	@echo "  make docker-down     Stop Docker Compose containers"
	@echo "  make clean           Clean build artifacts, __pycache__, and temp logs"
	@echo "========================================================================"

# 1. Dependency Installation
install:
	@echo "[1/2] Installing backend Python dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "[2/2] Installing frontend npm dependencies..."
	cd frontend && npm install

# 2. Local Development Servers
dev:
	python scripts/dev.py

dev-backend:
	cd backend && uvicorn main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# 3. Testing
test: test-backend test-frontend

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm run test

# 4. Code Linting & Static Analysis
lint: lint-backend lint-frontend

lint-backend:
	cd backend && flake8 app main.py

lint-frontend:
	cd frontend && npm run lint

# 5. Code Formatting
format: format-backend

format-backend:
	cd backend && black app main.py

# 6. Production Builds
build: build-frontend

build-frontend:
	cd frontend && npm run build

# 7. Docker Orchestration
docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

docker-build:
	docker-compose build

# 8. Workspace Cleaning
clean:
	@echo "Cleaning Python bytecode, test caches, and build outputs..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf frontend/dist frontend/node_modules/.vite
	@echo "Workspace cleaned successfully!"
