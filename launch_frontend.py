#!/usr/bin/env python3
"""
Launch script for DoubleTrust Frontend
Starts the React development server
"""

import sys
import os
import subprocess
import signal
from pathlib import Path

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
    """Launch the DoubleTrust frontend server"""
    
    print("🚀 Starting DoubleTrust Frontend...")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    frontend_path = project_root / "frontend"
    
    # Kill any existing process on port 3000
    print("🔍 Checking for existing processes on port 3000...")
    kill_process_on_port(3000)
    
    # Check if frontend directory exists
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        sys.exit(1)
    
    # Check if node_modules exists
    node_modules_path = frontend_path / "node_modules"
    if not node_modules_path.exists():
        print("❌ Node modules not found!")
        print("Please run: cd frontend && npm install")
        sys.exit(1)
    
    # Check if package.json exists
    package_json_path = frontend_path / "package.json"
    if not package_json_path.exists():
        print("❌ package.json not found!")
        sys.exit(1)
    
    print("📍 Frontend will be available at: http://localhost:3000")
    print("📍 Make sure the backend is running at: http://localhost:8000")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Store the subprocess reference for cleanup
    process = None
    
    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Shutting down frontend server...")
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("✅ Frontend server stopped")
        print("🔓 Port 3000 is now free")
        sys.exit(0)
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Run the frontend using npm start
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_path)
        
        # Wait for the process to complete
        process.wait()
        
    except FileNotFoundError:
        print("❌ npm not found! Please install Node.js")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        if process:
            process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
