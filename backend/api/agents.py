from __future__ import annotations

from typing import List
from fastapi import APIRouter, HTTPException, status

from ..models.agents import (
    AgentResponse, AgentListResponse, 
    AgentToolsResponse, AgentStatistics
)
from ..services.agent_service import AgentService

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("/", response_model=AgentListResponse)
async def list_agents():
    """List all agents"""
    agents = AgentService.get_all_agents()
    return AgentListResponse(agents=agents, total=len(agents))


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent details"""
    agent = AgentService.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    return agent


@router.get("/{agent_id}/tools", response_model=AgentToolsResponse)
async def get_agent_tools(agent_id: str):
    """Get agent's tool permissions"""
    # Check if agent exists
    agent = AgentService.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    tools = AgentService.get_agent_tools(agent_id)
    return AgentToolsResponse(agent_id=agent_id, tools=tools)


# Permissions removed by product decision


@router.get("/statistics/overview", response_model=AgentStatistics)
async def get_agent_statistics():
    """Get agent statistics"""
    return AgentService.get_agent_statistics()
