from __future__ import annotations

TOOL_SELECTION_PROMPT = """
Given the user prompt and available tools, select the most appropriate tool.

User prompt: {user_prompt}

Available tools: {tools}

Analyze the user's intent and select the tool that best matches their request. Consider:
- The tool's description and capabilities
- The parameters the tool accepts
- How well the tool addresses the user's specific request

Respond with JSON in this format:
{{
    "tool_name": "selected_tool_name",
    "reason": "Brief explanation of why this tool was selected"
}}

If no tool is suitable, respond with:
{{
    "tool_name": null,
    "reason": "No suitable tool found for this request"
}}
""".strip()
