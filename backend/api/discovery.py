from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..models.discovery import (
    GitHubDiscoveryRequest, 
    DiscoveryResponse, DiscoveryStatusResponse
)
from ..services.discovery_service import DiscoveryService

router = APIRouter(prefix="/api/discovery", tags=["discovery"])


@router.post("/agents", response_model=DiscoveryResponse)
async def discover_agents_from_github(request: GitHubDiscoveryRequest):
    """Trigger agent discovery from GitHub repository"""
    try:
        agents = DiscoveryService.discover_agents_from_github(str(request.github_repo_url))
        return DiscoveryResponse(
            success=True,
            message=f"Successfully discovered {len(agents)} agents",
            data={"agents": agents}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Discovery failed: {str(e)}"
        )



@router.get("/status", response_model=DiscoveryStatusResponse)
async def get_discovery_status():
    """Get current discovery status"""
    status_data = DiscoveryService.get_discovery_status()
    return DiscoveryStatusResponse(**status_data)
