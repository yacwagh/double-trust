#!/usr/bin/env python3
"""
Launch script for DoubleTrust Backend
Starts the FastAPI server with proper configuration
"""

import sys
import os
import subprocess
import signal
import time
from pathlib import Path

def clear_database():
    """Clear all data from the database on startup"""
    try:
        import sqlite3
        db_path = Path(__file__).parent / "doubletrust.db"
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Clear all tables
            cursor.execute("DELETE FROM agents")
            
            conn.commit()
            conn.close()
            print("🗑️  Database cleared - starting fresh")
        else:
            print("ℹ️  No existing database found - will create new one")
    except Exception as e:
        print(f"⚠️  Warning: Could not clear database: {e}")

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    try:
        # Find process using the port
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"], 
            capture_output=True, 
            text=True
        )
        
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(["kill", "-9", pid], check=False)
                    print(f"🔪 Killed process {pid} on port {port}")
    except Exception as e:
        # lsof might not be available on all systems
        pass

def main():
    """Launch the DoubleTrust backend server"""
    
    print("🚀 Starting DoubleTrust Backend...")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Kill any existing process on port 8000
    print("🔍 Checking for existing processes on port 8000...")
    kill_process_on_port(8000)
    
    # Check if virtual environment exists
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv venv")
        print("Then: source venv/bin/activate")
        print("Then: pip install -r requirements.txt")
        sys.exit(1)
    
    # Clear database on startup
    clear_database()
    
    # Ensure environment variables are loaded from .env file if present
    from dotenv import load_dotenv
    load_dotenv()
    
    print("📍 Backend will be available at: http://localhost:8000")
    print("📍 API documentation at: http://localhost:8000/docs")
    print("📍 Health check at: http://localhost:8000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Store the subprocess reference for cleanup
    process = None
    
    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Shutting down backend server...")
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("✅ Backend server stopped")
        print("🔓 Port 8000 is now free")
        sys.exit(0)
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Run the backend using uvicorn
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=project_root)
        
        # Wait for the process to complete
        process.wait()
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        if process:
            process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
