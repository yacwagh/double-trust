from __future__ import annotations

from typing import Dict, List, Any
import logging

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from llm_service.llm import llm_json
from llm_service.prompts.discovery_prompts import SUMMARIZER_SYSTEM


logger = logging.getLogger(__name__)


def summarize_prompt_role(text: str) -> str:
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SUMMARIZER_SYSTEM},
        {"role": "user", "content": text},
    ]
    logger.debug("Summarizing role for prompt of length %d", len(text))
    data: Dict[str, Any] = llm_json(messages)
    role = str(data.get("role", "Unknown")).strip()
    logger.debug("Role summarization result: %s", role)
    return role or "Unknown"


