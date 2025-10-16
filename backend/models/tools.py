from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ToolResponse(BaseModel):
    """Model for tool response"""
    id: int
    name: str
    description: str
    parameters: Dict[str, Any]
    server_url: str
    permission: Optional[str] = None


class ToolListResponse(BaseModel):
    """Model for tool list response"""
    tools: List[ToolResponse]
    total: int


class ToolExecuteRequest(BaseModel):
    """Model for tool execution request"""
    agent_id: str
    parameters: Dict[str, Any]


class ToolExecuteResponse(BaseModel):
    """Model for tool execution response"""
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    tool_name: str
    server_url: str


class ToolSelectionRequest(BaseModel):
    """Model for tool selection request"""
    user_prompt: str


class ToolSelectionResponse(BaseModel):
    """Model for tool selection response"""
    selected_tool: Optional[ToolResponse] = None
    reason: str


class ToolStatistics(BaseModel):
    """Model for tool statistics"""
    total_tools: int
    total_servers: int
    tools_by_server: Dict[str, int]
