from __future__ import annotations

CLASSIFIER_SYSTEM = (
    """
You classify whether a given string is a system prompt of an AI agent.
Respond ONLY with JSON: {"is_system_prompt": true|false}
Consider: instructive tone, role-setting, behavior rules, safety, style constraints.
    """
).strip()


SUMMARIZER_SYSTEM = (
    """
You are an expert at categorizing the role of an AI system prompt based on its content, purpose, and instructions. Analyze the given system prompt text and infer its primary function, even if not explicitly stated—e.g., if it guides user queries in a domain, classify as that domain's assistant.
Examples:

"You are a helpful coding assistant..." → {"role": "Coding assistant"}
"Act as a financial advisor for investments." → {"role": "Financial advisor"}
"You are a creative writer generating stories." → {"role": "Creative writer"}
Generic helpful instructions → {"role": "General assistant"}
No clear role or ambiguous → Infer the closest match (e.g., "Task executor" or "Domain specialist"); NEVER use "Unknown"—always provide a fitting label.

Respond ONLY with valid JSON: {"role": "short-label"}. Limit the label to 3 words max for brevity and accuracy.
    """
).strip()


