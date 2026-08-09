"""
GuardianAI Cross-Platform Development Launcher Script
Purpose: Launches FastAPI backend and Vite frontend servers concurrently in development mode, automatically detecting virtual environment Python executable.
"""

import subprocess
import sys
import os
import time

def get_backend_python(backend_dir: str) -> str:
    """Finds virtual environment Python executable if present, otherwise returns sys.executable."""
    if sys.platform == "win32":
        venv_python = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    if os.path.isfile(venv_python):
        print(f"Using virtual environment Python: {venv_python}")
        return venv_python

    print(f"Virtual environment not found in backend/venv. Using system Python: {sys.executable}")
    return sys.executable

def run_dev():
    print("==================================================")
    print("      Launching GuardianAI Development Stack      ")
    print("==================================================")

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    python_bin = get_backend_python(backend_dir)

    # Start FastAPI Backend
    print("[1/2] Launching FastAPI Backend on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [python_bin, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
        cwd=backend_dir
    )

    time.sleep(1.5)

    # Start Vite Frontend
    print("[2/2] Launching React Vite Frontend on http://localhost:5173 ...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir
    )

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping GuardianAI development servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    run_dev()
