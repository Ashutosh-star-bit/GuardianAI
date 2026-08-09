# GuardianAI Docker Architecture & Containerization Specification

**Document Version:** 1.0.0  
**Target Architecture:** Multi-Container Production Topology (Frontend, Backend, PostgreSQL+pgvector, Redis)  

---

## 1. Overview

GuardianAI provides **Multi-Stage Dockerfiles** and **Environment-Isolated Docker Compose Specs**:
- **Development Topology (`docker-compose.yml`):** Vite dev server with Hot-Module Replacement (HMR), FastAPI hot-reloading uvicorn, bind-mounted source directories, and SQLite / PostgreSQL.
- **Production Topology (`docker-compose.prod.yml`):** Multi-stage built React SPA served via Nginx Alpine, non-root Python 3.12 FastAPI backend running multi-worker Uvicorn, PostgreSQL 16 + pgvector, and Redis 7 caching.

---

## 2. Container Network & Volume Topology

```
                   [ Internet Client Browser ]
                                │
                                ▼ (Port 80 / 443)
              ┌───────────────────────────────────┐
              │   Nginx Frontend Container        │
              │   (Static React SPA + Reverse Proxy)
              └─────────────────┬─────────────────┘
                                │
                                │ (Internal Bridge Network: guardianai_network)
                                ▼ (Port 8000)
              ┌───────────────────────────────────┐
              │   FastAPI Backend Container       │
              │   (Non-root user 'appuser')       │
              └────────┬──────────────────┬───────┘
                       │                  │
         ┌─────────────┴──────┐    ┌──────┴──────────────┐
         │ PostgreSQL 16      │    │ Redis 7 Cache       │
         │ + PgVector Container│    │ Container           │
         └────────────────────┘    └─────────────────────┘
```

---

## 3. Storage Volumes & Persistence Matrix

| Volume Name | Target Path inside Container | Purpose & Retention Policy |
| :--- | :--- | :--- |
| `db_data` | `/var/lib/postgresql/data` | Persistent PostgreSQL database tables & PgVector vector embeddings. |
| `redis_data` | `/data` | Redis snapshot persistence (`dump.rdb`) for rate limiting counters. |
| `backend_uploads` | `/app/backend/uploads` | Transient uploaded raw `.eml` email files and QR image files. |
| `backend_logs` | `/app/backend/logs` | Structured JSON log files (`access.log`, `error.log`, `security.log`). |

---

## 4. Multi-Stage Dockerfile Strategy

### 4.1 Frontend Multi-Stage Build (`Dockerfile.frontend`)
- **Stage 1 (`base`):** Installs npm dependencies.
- **Stage 2 (`development`):** Starts Vite dev server listening on port `5173`.
- **Stage 3 (`builder`):** Compiles minified static production bundle into `/dist`.
- **Stage 4 (`production`):** Copies static bundle to `nginx:1.25-alpine` image with custom security headers and SPA fallback.

### 4.2 Backend Multi-Stage Build (`Dockerfile.backend`)
- **Stage 1 (`base`):** Installs Python 3.12 requirements and system build dependencies.
- **Stage 2 (`development`):** Runs Uvicorn with `--reload`.
- **Stage 3 (`production`):** Hardens image by creating non-root user `appuser:appgroup`, creating log directories, adding `HEALTHCHECK`, and launching 4 Uvicorn workers.

---

## 5. Security & Container Best Practices

1. **Non-Root Execution:** Production backend container drops `root` privileges and executes strictly under `appuser` (UID 1001).
2. **Layer Caching:** Dependencies (`requirements.txt` and `package.json`) are copied and installed *before* copying application code to maximize Docker layer cache hits.
3. **Health Checks:** Native `HEALTHCHECK` directives inspect `GET /api/v1/health` every 30 seconds.
4. **Context Exclusion:** `.dockerignore` excludes node_modules, virtualenvs, local databases, and temporary logs.
