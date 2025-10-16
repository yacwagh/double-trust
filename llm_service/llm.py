from __future__ import annotations

import os
from typing import Any, Dict, List


class MissingApiKeyError(Exception):
    pass


def llm_json(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    import httpx
    import json as _json

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        # Aid debugging when env isn't loaded
        raise MissingApiKeyError("Missing OPENROUTER_API_KEY for LLM usage (env not set)")
    url = "https://openrouter.ai/api/v1/chat/completions"
    model = os.getenv("OPENROUTER_MODEL", "openrouter/auto")
    referer = os.getenv("OPENROUTER_REFERER", "http://localhost:8000")
    app_title = os.getenv("OPENROUTER_APP_TITLE", "DoubleTrust")
    sys_msg = {
        "role": "system",
        "content": "You must output only a single JSON object, no prose.",
    }
    payload = {"model": model, "messages": [sys_msg, *messages], "temperature": 0}
    with httpx.Client(timeout=30) as client:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            # OpenRouter recommends these headers for server environments
            "HTTP-Referer": referer,
            "X-Title": app_title,
        }
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        return _json.loads(content)

from openai import OpenAI
import os
import json
import re

def get_llm_response(content: str, system_prompt: str = "") -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise MissingApiKeyError("Missing OPENROUTER_API_KEY for LLM usage (env not set)")
    
    # Set the API key as an environment variable for the OpenAI client
    os.environ["OPENAI_API_KEY"] = api_key
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
    )

    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": content
    })

    # OpenRouter recommends including referer/title via standard headers; the OpenAI SDK
    # used through OpenRouter doesn't expose header injection here, so prefer llm_json for JSON.
    completion = client.chat.completions.create(model="openai/gpt-4.1-nano", messages=messages, temperature=0.1)
    return completion.choices[0].message.content

def get_json_llm_response(content: str, system_prompt: str) -> dict:
    """
    Extracts JSON from an LLM response using the httpx-based function.
    
    Args:
        content: The user prompt to send to the LLM
        system_prompt: Optional system prompt to guide the LLM
        
    Returns:
        A dictionary parsed from the JSON in the LLM response
    """
    
    # Use the httpx-based function instead of the OpenAI client
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": content
    })
    
    try:
        response = llm_json(messages)
        return response
    except MissingApiKeyError:
        # Surface a consistent exception so callers can detect missing key
        raise
    except Exception as e:
        # If httpx fails, fall back to the OpenAI client
        response = get_llm_response(content, system_prompt)
        
        # Try to extract JSON using regex pattern matching
        json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        match = re.search(json_pattern, response)
        
        if match:
            # Extract the JSON content from the code block
            json_str = match.group(1)
        else:
            # If no code block is found, try to use the entire response
            json_str = response
        
        try:
            # Parse the JSON string into a Python dictionary
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If parsing fails, return an empty dictionary
            return {}