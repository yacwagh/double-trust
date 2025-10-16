from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentBase(BaseModel):
    """Base agent model"""
    role: str
    system_prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = None


class AgentResponse(AgentBase):
    """Model for agent response"""
    id: str
    file_path: Optional[str] = None
    framework: Optional[str] = None
    risk: Optional[str] = None
    risk_reason: Optional[str] = None
    created_at: str


class AgentListResponse(BaseModel):
    """Model for agent list response"""
    agents: List[AgentResponse]
    total: int


class AgentToolsResponse(BaseModel):
    """Model for agent tools response"""
    agent_id: str
    tools: List[Dict[str, Any]]


# Tool permissions removed by product decision.


class AgentStatistics(BaseModel):
    """Model for agent statistics"""
    total_agents: int
    discovered_agents: int
    agents_by_role: Dict[str, int]
