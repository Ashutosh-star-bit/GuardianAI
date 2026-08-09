# GuardianAI Testing Strategy & Test Automation Guide

**Document Version:** 1.0.0  
**Target Architecture:** Backend (Pytest) & Frontend (Vitest + React Testing Library)  
**Coverage Target:** Minimum 85% Code Line Coverage across core API routes and components  

---

## 1. Backend Pytest Infrastructure (`backend/tests/`)

### 1.1 In-Memory SQLite Isolation (`tests/conftest.py`)
To ensure total test isolation and sub-second execution speeds, Pytest overrides the primary database session dependency with an **In-Memory SQLite instance** (`sqlite:///:memory:`):
- Every test function runs inside an isolated database schema created via `Base.metadata.create_all()`.
- After execution, tables are dropped cleanly via `Base.metadata.drop_all()`.

### 1.2 Pytest Execution & Coverage Commands

```bash
# Run all backend unit and integration tests
cd backend
pytest

# Run tests with HTML coverage report generation
pytest --cov=app --cov-report=html:coverage_html
```

---

## 2. Frontend Vitest Infrastructure (`frontend/src/__tests__/`)

### 2.1 JSDOM & React Testing Library (`vitest.config.ts`)
Vitest is configured with `environment: 'jsdom'`, `@testing-library/react`, and `@testing-library/jest-dom` for component testing.

### 2.2 Frontend Execution Commands

```bash
# Run frontend Vitest test suite
cd frontend
npm run test
```

---

## 3. Mock Strategy for External Services

1. **AI Inference Provider Mocking:** External Gemini / Groq API calls are mocked using Pytest fixtures (`mock_ai_response`) or `unittest.mock.patch` to prevent network calls or API token usage during automated CI/CD runs.
2. **Web Worker PII Mocking:** Client-side Web Worker messages are tested via synthetic `MessageEvent` objects.
