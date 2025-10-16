from __future__ import annotations

AGENT_ANALYSIS_PROMPT = """
Analyze agent capabilities and suggest optimal tool assignments.

Agent role: {role}
Agent system prompt: {system_prompt}
Available tools: {tools}

Based on the agent's role and system prompt, analyze which tools would be most beneficial for this agent. Consider:
- The agent's primary function and domain expertise
- The tools' capabilities and how they align with the agent's purpose
- Potential synergies between the agent's capabilities and tool functions

Respond with JSON in this format:
{{
    "recommended_tools": [
        {{
            "tool_name": "tool_name",
            "reason": "Why this tool is recommended for this agent",
            "priority": "high|medium|low"
        }}
    ],
    "analysis": "Overall analysis of the agent's tool needs and capabilities"
}}
""".strip()
