# GuardianAI Developer Experience (DX) & Command Reference

**Document Version:** 1.0.0  
**Target Audience:** GuardianAI Engineering Team & Contributors  

---

## 1. Developer Tooling Architecture

GuardianAI provides **3 Ergonomic Execution Interfaces**:
1. **Makefile Interface (`make <target>`):** Universal CLI entrypoint for local development, testing, linting, formatting, containerization, and workspace cleanup.
2. **Python Launcher (`python scripts/dev.py`):** Cross-platform, dual-process runner that boots FastAPI (port 8000) and Vite (port 5173) concurrently.
3. **NPM Package Shortcuts (`npm run <script>`):** Root and frontend package.json script wrappers for JavaScript ecosystem compatibility.

---

## 2. Master Command Reference Table

### 2.1 Local Environment & Server Controls

| Command Target | Executing File / Tool | Purpose & Explanation |
| :--- | :--- | :--- |
| `make install` | `pip install` + `npm install` | Installs all Python 3.12 requirements and Node 20 npm packages in one command. |
| `make dev` | `python scripts/dev.py` | Launches FastAPI backend (port `8000`) and Vite React frontend (port `5173`) concurrently. |
| `make dev-backend` | `uvicorn main:app --reload` | Launches standalone FastAPI uvicorn backend with hot-reload enabled. |
| `make dev-frontend` | `cd frontend && npm run dev` | Launches standalone React Vite development server with HMR. |
| `bash scripts/setup.sh`| Shell setup script | One-command bootstrap copying `.env.example`, creating `venv`, and installing dependencies. |

### 2.2 Testing, Linting & Formatting

| Command Target | Tooling | Purpose & Explanation |
| :--- | :--- | :--- |
| `make test` | `pytest` + `npm run test` | Runs the full test suite across Python backend unit tests and frontend component tests. |
| `make lint` | `flake8` + `tsc --noEmit` | Runs Flake8 style verification on Python code and TypeScript static type checks on React code. |
| `make format` | `black` | Auto-formats all Python backend code (`backend/app`, `backend/main.py`) to PEP-8 standards. |
| `bash scripts/format.sh`| Shell formatting script| Runs Black auto-formatter followed by Flake8 style audit. |

### 2.3 Containerization & Docker Commands

| Command Target | Executing Command | Purpose & Explanation |
| :--- | :--- | :--- |
| `make docker-up` | `docker-compose up -d --build` | Builds and launches multi-container Docker stack (backend, frontend, database) in background. |
| `make docker-down` | `docker-compose down` | Stops and removes running Docker containers and networks. |
| `npm run docker:logs` | `docker-compose logs -f` | Streams real-time container log outputs across all services. |

### 2.4 Production Build & Workspace Cleanup

| Command Target | Executing Command | Purpose & Explanation |
| :--- | :--- | :--- |
| `make build` | `tsc && vite build` | Typechecks TypeScript source code and compiles minified production web bundle into `frontend/dist/`. |
| `make clean` | `find` & `rm -rf` | Cleans temporary Python `__pycache__`, `.pytest_cache`, `.vite` cache, and local build artifacts. |

---

## 3. Developer Workflow Summary

```
[ Clone Repo ] ──> [ make install ] ──> [ make dev ]
                                             │
                                             ├──> Frontend: http://localhost:5173
                                             └──> Backend:  http://localhost:8000/docs
                                             │
 [ make format ] <── [ make lint ] <── [ make test ]
```
