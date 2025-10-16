from __future__ import annotations

import argparse
import json
from typing import Dict, Any
import logging
import hashlib

from .extractor import extract_system_prompts, extract_langchain_agents
from .role_assigner import summarize_prompt_role
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from llm_service.llm import MissingApiKeyError


logger = logging.getLogger(__name__)


def discover_agents(directory: str) -> Dict[str, Any]:
    logger.info("Starting discovery in: %s", directory)
    items = extract_system_prompts(directory)
    # Also detect LangChain-based agents (create_react_agent)
    lc = extract_langchain_agents(directory)
    agents = []
    seen: set[str] = set()
    for file_path, s in items:
        key = s[:2000]
        if key in seen:
            continue
        seen.add(key)
        try:
            if s.strip():
                try:
                    role = summarize_prompt_role(s)
                except MissingApiKeyError:
                    # Fallback to simple role detection when API key is not available
                    role = "AI Assistant"
                except Exception as e:
                    role = "AI Assistant"
            else:
                role = "Unknown"
            
            agent_id = hashlib.sha256(s.encode("utf-8")).hexdigest()
            agents.append({
                "id": agent_id,
                "file": file_path,
                "role": role,
                "system_prompt": s,
                "framework": "Custom"
            })
            logger.info("Found system prompt in %s → id=%s role=%s", file_path, agent_id[:8], role)
        except Exception as e:
            logger.warning("Error processing string from %s: %s", file_path, e)
            continue
    # Add LangChain agents
    for file_path, data in lc:
        prompt = data.get("prompt") or ""
        key = (prompt or file_path)[:2000]
        if key in seen:
            continue
        seen.add(key)
        try:
            if prompt.strip():
                try:
                    role = summarize_prompt_role(prompt)
                except MissingApiKeyError:
                    role = "AI Assistant"
                except Exception as e:
                    role = "AI Assistant"
            else:
                role = "Unknown"
            agent_id = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            agent_entry = {
                "id": agent_id,
                "file": file_path,
                "role": role,
                "system_prompt": prompt,
                "framework": "Langchain"
            }
            # Pass through any extracted tool names (strings only)
            tools = data.get("tools") or []
            if isinstance(tools, list) and any(isinstance(t, str) for t in tools):
                agent_entry["__lc_tools__"] = [t for t in tools if isinstance(t, str)]
            agents.append(agent_entry)
            logger.info("Found LangChain agent in %s → id=%s role=%s", file_path, agent_id[:8], role)
        except Exception as e:
            logger.warning("Error processing LC agent in %s: %s", file_path, e)
            continue

    logger.info("Discovery complete. %d agents found", len(agents))
    return {"agents": agents}

# Alias for backward compatibility
d = discover_agents


def cli() -> None:
    parser = argparse.ArgumentParser(description="Discover agents by scanning system prompts")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        result = discover_agents(args.directory)
        print(json.dumps(result, indent=2))
    except MissingApiKeyError:
        # Non-zero exit via exception propagation avoided; print nothing besides logs
        raise SystemExit(1)


if __name__ == "__main__":
    cli()


