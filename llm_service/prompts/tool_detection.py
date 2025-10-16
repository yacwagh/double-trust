from __future__ import annotations

TOOL_DETECTION_PROMPT = (
    """
You are given an agent system prompt. Identify any external tools, APIs, services, or resources
explicitly mentioned that the agent expects to use. Be conservative: only include tools that are clearly named
or obviously implied by specific phrases (e.g., "GitHub", "filesystem", "browser", "calendar"). If none, return an empty list.

Return JSON with this shape:
{
  "tools": [
    {"name": "...", "description": "...", "parameters": {}}
  ]
}

Prompt:
"""
).strip()


