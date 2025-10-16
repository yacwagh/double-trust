from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

from ..database import db
from .github_service import GitHubService
from .discovery.discovery import discover_agents
from llm_service.llm import get_json_llm_response, MissingApiKeyError
from llm_service.prompts.tool_detection import TOOL_DETECTION_PROMPT
from llm_service.prompts.agent_risk import AGENT_RISK_PROMPT


class DiscoveryService:
    """Service for discovering agents"""
    
    @staticmethod
    def discover_agents_from_github(github_repo_url: str) -> List[Dict[str, Any]]:
        """Discover agents from GitHub repository"""
        temp_dir = None
        try:
            # Clone the repository
            temp_dir = GitHubService.clone_repository(github_repo_url)
            
            # Use existing discovery function
            discovery_result = discover_agents(temp_dir)
            agents = discovery_result.get("agents", [])
            
            # Save discovered agents to database
            saved_agents = []
            for agent in agents:
                agent_data = {
                    "id": agent["id"],
                    "file_path": agent["file"],
                    "role": agent["role"],
                    "system_prompt": agent["system_prompt"],
                    "model": None,
                    "temperature": None,
                    "framework": agent.get("framework"),
                    "risk": None,
                    "risk_reason": None,
                }
                
                # Check if agent already exists
                existing_agent = db.get_agent(agent["id"])
                if not existing_agent:
                    db.create_agent(agent_data)
                    saved_agents.append(agent_data)
                else:
                    saved_agents.append(existing_agent)

                # Persist any pre-extracted tools (from LangChain visitor)
                pre_tools = agent.get("__lc_tools__")
                if pre_tools:
                    for tname in pre_tools:
                        try:
                            # Avoid duplicates by checking first
                            if not db.has_agent_tool(agent_data["id"], tname):
                                db.create_agent_tool({
                                    "agent_id": agent_data["id"],
                                    "name": tname,
                                    "description": None,
                                    "parameters": {}
                                })
                        except Exception:
                            pass

                # If custom agent: detect tools from prompt via LLM
                if agent_data.get("framework") == "Custom":
                    try:
                        prompt = TOOL_DETECTION_PROMPT + "\n\n" + agent_data["system_prompt"]
                        tools_json = get_json_llm_response(prompt, "")
                        for t in tools_json.get("tools", []) or []:
                            try:
                                tname = t.get("name")
                                if tname and not db.has_agent_tool(agent_data["id"], tname):
                                    db.create_agent_tool({
                                        "agent_id": agent_data["id"],
                                        "name": tname,
                                        "description": t.get("description"),
                                        "parameters": t.get("parameters") or {}
                                    })
                            except Exception:
                                pass
                    except MissingApiKeyError:
                        pass
                    except Exception:
                        pass

                # Compute agent risk via LLM using role and tool names
                try:
                    tools = db.get_agent_tools(agent_data["id"]) or []
                    tool_names = [t.get("name") for t in tools]
                    prompt = AGENT_RISK_PROMPT.format(role=agent_data["role"], tools=tool_names)
                    risk_json = get_json_llm_response(prompt, "")
                    risk = (risk_json.get("risk") or "").lower()
                    if risk in ("low", "medium", "high"):
                        # Update agent row with risk
                        db.execute_update(
                            "UPDATE agents SET risk = ?, risk_reason = ? WHERE id = ?",
                            (risk, risk_json.get("reason"), agent_data["id"]) 
                        )
                except MissingApiKeyError:
                    pass
                except Exception as e:
                    pass
            
            return saved_agents
            
        finally:
            # Clean up temporary directory
            if temp_dir:
                GitHubService.cleanup_temp_directory(temp_dir)
    
    @staticmethod
    def save_discovered_agent(agent_data: Dict[str, Any]) -> str:
        """Save discovered agent to database"""
        return db.create_agent(agent_data)
    
    @staticmethod
    def get_discovery_status() -> Dict[str, Any]:
        """Get current discovery status"""
        agents = db.get_all_agents()
        
        return {
            "total_agents": len(agents),
            "discovered_agents": len([a for a in agents])
        }
