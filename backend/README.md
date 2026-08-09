# GuardianAI FastAPI Backend Engine

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-purple.svg)](https://docs.pydantic.dev/)

GuardianAI Backend is a **Privacy-First Explainable AI (XAI) Anti-Scam Platform Engine** built using Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, and Uvicorn.

---

## 1. Clean Architecture Folder Structure

The project strictly follows **Clean Architecture** principles, decoupling API routes, business logic schemas, data models, and infrastructure.

```
backend/
├── alembic/                # Alembic Database Migration Scripts & History
│   ├── env.py              # Migration Runtime Environment Config
│   └── versions/           # Versioned Migration Revisions
├── app/
│   ├── api/                # Presentation Layer (API Controllers & Routes)
│   │   └── v1/             # REST API Version 1 Endpoints
│   │       ├── auth.py     # Login, Registration & JWT Auth Routes
│   │       ├── scans.py    # XAI Threat Inspection Scan Routes
│   │       ├── users.py    # User Profile Management Routes
│   │       └── router.py   # Master V1 API Router Collector
│   ├── core/               # Cross-Cutting Infrastructure Layer
│   │   ├── config.py       # Pydantic Settings & Environment Variables
│   │   ├── exceptions.py   # Domain Exceptions & RFC 7807 Problem Details
│   │   ├── handlers.py     # Global FastAPI Exception Handlers
│   │   ├── logging.py      # Structured Loguru / Standard Logging Configuration
│   │   └── security.py     # Password Hashing & JWT Token Generation
│   ├── db/                 # Persistence Layer (Database Engine & ORM)
│   │   ├── base.py         # Declarative Base Model & Timestamp Mixins
│   │   └── session.py      # SQLAlchemy 2.0 Engine & Sessionmaker
│   ├── middleware/         # HTTP Middleware Stack
│   │   ├── process_time.py # X-Process-Time Header Middleware
│   │   ├── request_id.py   # X-Request-ID Correlation Middleware
│   │   └── security_headers.py # OWASP Security Headers Middleware
│   ├── models/             # Domain ORM Models (SQLAlchemy 2.0 Mapped)
│   │   ├── user.py         # User & Account Entity Model
│   │   └── scan.py         # Inspection Threat Scan Entity Model
│   └── schemas/            # Application DTOs (Pydantic v2 Validation)
│       ├── auth.py         # Auth Payloads (Login, Token, Register)
│       └── scan.py         # Scan Payloads & Explainable AI Response Schemas
├── main.py                 # Application Entry Point & FastAPI Initialization
├── alembic.ini             # Database Migration Configuration
├── pyproject.toml          # Modern Packaging & Tooling Specification
├── requirements.txt        # Frozen Dependency Lockfile
└── README.md               # Backend Architecture Documentation
```

---

## 2. Prerequisites & Installation

### Requirements
- **Python 3.12** or higher
- **Virtualenv** (`venv`)

### Setup Instructions

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create Python 3.12 virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Configuration & Environment Variables

Copy `.env.example` to create your local `.env` configuration:

```bash
cp .env.example .env
```

Key environment variables in `.env`:
```env
PROJECT_NAME="GuardianAI"
ENVIRONMENT="development"
DEBUG=true
API_V1_STR="/api/v1"

# Database Configuration (SQLite for local dev, PostgreSQL for prod)
DATABASE_URL="sqlite:///./guardianai.db"

# JWT Security
SECRET_KEY="super-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 4. Running Database Migrations (Alembic)

```bash
# Run database migrations to apply latest schema
alembic upgrade head

# Generate a new migration revision after modifying ORM models
alembic revision --autogenerate -m "Add new feature column"
```

---

## 5. Running the Backend Development Server

 launch both FastAPI and React simultaneously from project root:
```bash
python scripts/dev.py
```

Or run the backend standalone via Uvicorn:
```bash
# From backend directory with venv activated
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Interactive API documentation will be available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc UI:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/api/v1/openapi.json`

---

## 6. Running Automated Tests

```bash
# Execute test suite via pytest
pytest

# Execute test suite with coverage report
pytest --cov=app --cov-report=term-missing
```

---

## 7. Clean Architecture Design Principles

1. **Separation of Concerns:** API endpoints only parse HTTP requests and delegate logic to domain services or database models.
2. **DTO Validation:** All payload serialization and strict validation are handled by Pydantic v2 schemas (`app/schemas/`).
3. **ORM Decoupling:** Database models (`app/models/`) use SQLAlchemy 2.0 `Mapped` annotations.
4. **RFC 7807 Error Resiliency:** All HTTP exceptions return structured JSON problem detail responses containing request correlation IDs.
