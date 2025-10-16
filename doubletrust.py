#!/usr/bin/env python3
"""
Unified launcher for DoubleTrust (backend + frontend)
 - Clears database
 - Loads environment from .env
 - Kills conflicting processes on ports 8000 (backend) and 3000 (frontend)
 - Starts FastAPI backend with uvicorn
 - Starts React frontend with npm start
 - Handles graceful shutdown of both
"""

from __future__ import annotations

import os
import sys
import signal
import subprocess
from pathlib import Path


def kill_process_on_port(port: int) -> None:
    """Kill any process running on the specified port."""
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                if pid:
                    subprocess.run(["kill", "-9", pid], check=False)
                    print(f"🔪 Killed process {pid} on port {port}")
    except Exception:
        # lsof might not be available; ignore failures
        pass


def clear_database(project_root: Path) -> None:
    """Clear all data from the database on startup."""
    try:
        import sqlite3
        db_path = project_root / "backend" / "doubletrust.db"
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            # Clear tables we own; backend migration will recreate/adjust as needed
            cursor.execute("DELETE FROM agents")
            conn.commit()
            conn.close()
            print("🗑️  Database cleared - starting fresh")
        else:
            print("ℹ️  No existing database found - will create new one")
    except Exception as e:
        print(f"⚠️  Warning: Could not clear database: {e}")


def ensure_env_loaded(project_root: Path) -> None:
    """Load environment variables from .env at project root if available."""
    try:
        from dotenv import load_dotenv  # type: ignore
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=str(env_path))
        else:
            load_dotenv()
    except Exception:
        # Best effort only
        pass


def main() -> None:
    print("🚀 Starting DoubleTrust (Backend + Frontend)...")
    print("=" * 50)

    project_root = Path(__file__).parent.absolute()
    backend_cwd = project_root
    frontend_path = project_root / "frontend"

    # Kill ports first to avoid conflicts
    print("🔍 Checking for existing processes on ports 8000 and 3000...")
    kill_process_on_port(8000)
    kill_process_on_port(3000)

    # Check backend environment (venv)
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv venv")
        print("Then: source venv/bin/activate")
        print("Then: pip install -r requirements.txt")
        sys.exit(1)

    # Clear DB
    clear_database(project_root)

    # Load env
    ensure_env_loaded(project_root)

    # Check frontend
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        sys.exit(1)
    node_modules_path = frontend_path / "node_modules"
    if not node_modules_path.exists():
        print("❌ Node modules not found!")
        print("Please run: cd frontend && npm install")
        sys.exit(1)
    if not (frontend_path / "package.json").exists():
        print("❌ package.json not found in frontend/")
        sys.exit(1)

    print("📍 Backend: http://localhost:8000 (docs: /docs)")
    print("📍 Frontend: http://localhost:3000")
    print()
    print("Press Ctrl+C to stop both servers")
    print("=" * 50)

    backend_proc: subprocess.Popen[str] | None = None
    frontend_proc: subprocess.Popen[str] | None = None

    def shutdown() -> None:
        print("\n🛑 Shutting down DoubleTrust...")
        for name, proc in (("frontend", frontend_proc), ("backend", backend_proc)):
            if proc and proc.poll() is None:
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                except Exception:
                    pass
                print(f"✅ {name.capitalize()} stopped")
        print("🔓 Ports 8000 and 3000 are now free")

    def signal_handler(sig, frame):  # type: ignore[no-redef]
        shutdown()
        sys.exit(0)

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Start backend (uvicorn)
        backend_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            cwd=backend_cwd,
        )

        # Start frontend (npm start)
        frontend_proc = subprocess.Popen(["npm", "start"], cwd=frontend_path)

        # Wait on both; if either exits, stop the other
        while True:
            backend_code = backend_proc.poll() if backend_proc else 0
            frontend_code = frontend_proc.poll() if frontend_proc else 0
            if backend_code is not None:
                print(f"❌ Backend exited with code {backend_code}")
                break
            if frontend_code is not None:
                print(f"❌ Frontend exited with code {frontend_code}")
                break
            # Avoid busy loop
            try:
                backend_proc.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                pass
    except FileNotFoundError as e:
        print(f"❌ Required executable not found: {e}")
    except Exception as e:
        print(f"❌ Error starting DoubleTrust: {e}")
    finally:
        shutdown()


if __name__ == "__main__":
    main()


