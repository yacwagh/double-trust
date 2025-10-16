from __future__ import annotations

DUPLICATE_DETECTION_PROMPT = """
Compare these two agent system prompts and determine similarity.

Prompt 1: {prompt1}

Prompt 2: {prompt2}

Analyze the prompts for:
- Semantic similarity in purpose and function
- Overlapping instructions and behaviors
- Similar role definitions
- Identical or very similar content

Respond with JSON in this format:
{{
    "similarity_score": 0.85,
    "is_duplicate": true,
    "explanation": "Detailed explanation of the similarity analysis",
    "differences": [
        "Key difference 1",
        "Key difference 2"
    ]
}}

Similarity score should be between 0.0 (completely different) and 1.0 (identical).
Consider it a duplicate if similarity_score >= 0.9.
""".strip()
