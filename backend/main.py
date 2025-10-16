from __future__ import annotations

from fastapi import FastAPI
import os
from pathlib import Path

# Ensure environment variables from .env are loaded when starting via uvicorn/python
try:
    from dotenv import load_dotenv  # type: ignore
    # Load from project root explicitly to avoid CWD issues
    project_root = Path(__file__).resolve().parents[1]
    root_env = project_root / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=str(root_env))
    else:
        load_dotenv()
except Exception:
    # .env loading is best-effort; continue if python-dotenv isn't installed
    pass
from fastapi.middleware.cors import CORSMiddleware

from .api import agents, tools, discovery

app = FastAPI(
    title="DoubleTrust API",
    description="Agent and Tools Governance Platform MVP",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router)
app.include_router(tools.router)
app.include_router(discovery.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DoubleTrust API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
