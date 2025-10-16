from __future__ import annotations

from typing import Any, Dict, List
import json

from ..database import db
from .agent_service import AgentService


class ToolService:
    """Service for tool management and execution"""
    
    @staticmethod
    def select_tool_for_agent(agent_id: str, user_prompt: str) -> Dict[str, Any]:
        """Select appropriate tool for agent based on user prompt"""
        # Get agent details
        agent = AgentService.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Get available tools for this agent
        tools = AgentService.get_agent_tools(agent_id)
        
        # Filter to only allowed tools
        allowed_tools = [t for t in tools if t.get("permission") == "allowed"]
        
        if not allowed_tools:
            return {
                "selected_tool": None,
                "reason": "No tools available for this agent"
            }
        
        # Use LLM to select the best tool
        from llm_service.llm import get_json_llm_response
        from llm_service.prompts.tool_selection import TOOL_SELECTION_PROMPT
        
        tools_description = []
        for tool in allowed_tools:
            tools_description.append({
                "name": tool["name"],
                "description": tool["description"],
                "parameters": json.loads(tool["parameters"]) if tool["parameters"] else {}
            })
        
        prompt = TOOL_SELECTION_PROMPT.format(
            user_prompt=user_prompt,
            tools=json.dumps(tools_description, indent=2)
        )
        
        try:
            response = get_json_llm_response(prompt, "")
            selected_tool_name = response.get("tool_name")
            
            # Find the selected tool
            selected_tool = None
            for tool in allowed_tools:
                if tool["name"] == selected_tool_name:
                    selected_tool = tool
                    break
            
            return {
                "selected_tool": selected_tool,
                "reason": response.get("reason", "Tool selected by LLM")
            }
            
        except Exception as e:
            # Fallback to first available tool
            return {
                "selected_tool": allowed_tools[0],
                "reason": f"LLM selection failed, using first available tool: {str(e)}"
            }
    
    
