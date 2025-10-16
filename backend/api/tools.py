from __future__ import annotations

import json
from typing import Dict, List
from fastapi import APIRouter, HTTPException, status

from ..models.tools import (
    ToolListResponse, ToolExecuteRequest, ToolExecuteResponse,
    ToolSelectionRequest, ToolSelectionResponse, ToolStatistics, ToolResponse
)
from ..services.tool_service import ToolService

router = APIRouter(prefix="/api/tools", tags=["tools"])


@router.get("/", response_model=ToolListResponse)
async def list_tools():
    """List all tools"""
    # Return empty list since tools are not implemented yet
    return ToolListResponse(tools=[], total=0)




