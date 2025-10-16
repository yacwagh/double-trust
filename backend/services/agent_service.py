from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

from ..database import db


class AgentService:
    """Service for agent management"""
    
    @staticmethod
    def check_duplicate_agent(system_prompt: str) -> Optional[str]:
        """Check for duplicate agent by system prompt hash"""
        agent_id = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
        existing_agent = db.get_agent(agent_id)
        return existing_agent["id"] if existing_agent else None
    
    @staticmethod
    def get_agent_tools(agent_id: str) -> List[Dict[str, Any]]:
        """Get tool permissions for an agent"""
        return db.get_agent_tools(agent_id)
    
    @staticmethod
    def update_tool_permission(agent_id: str, tool_id: int, permission: str) -> None:
        """Deprecated: tool permissions removed"""
        raise ValueError("Tool permissions are disabled")
    
    @staticmethod
    def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        return db.get_agent(agent_id)
    
    @staticmethod
    def get_all_agents() -> List[Dict[str, Any]]:
        """Get all agents"""
        return db.get_all_agents()
    
    @staticmethod
    def get_agent_by_system_prompt(system_prompt: str) -> Optional[Dict[str, Any]]:
        """Get agent by system prompt hash"""
        agent_id = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
        return db.get_agent(agent_id)
    
    @staticmethod
    def get_agent_statistics() -> Dict[str, Any]:
        """Get agent statistics"""
        agents = db.get_all_agents()
        
        stats = {
            "total_agents": len(agents),
            "discovered_agents": len([a for a in agents]),
            "agents_by_role": {}
        }
        
        # Count agents by role
        for agent in agents:
            role = agent["role"]
            if role not in stats["agents_by_role"]:
                stats["agents_by_role"][role] = 0
            stats["agents_by_role"][role] += 1
        
        return stats
