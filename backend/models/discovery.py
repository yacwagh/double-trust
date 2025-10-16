from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, HttpUrl


class GitHubDiscoveryRequest(BaseModel):
    """Model for GitHub discovery request"""
    github_repo_url: HttpUrl


class DiscoveryResponse(BaseModel):
    """Model for discovery response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class DiscoveryStatusResponse(BaseModel):
    """Model for discovery status response"""
    total_agents: int
    discovered_agents: int
