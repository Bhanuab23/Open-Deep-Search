from typing import Dict, List
from dotenv import load_dotenv
import os
import requests

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "amazon/nova-lite-v1"


def planner_agent(state: Dict) -> Dict:
    """
    Planner Agent:
    - Takes a research topic
    - Generates structured sub-questions
    - Defines expected output format
    """

    topic = state["topic"]

    prompt = f"""
You are a research planner.

Given the research topic below, generate:
1. Exactly 3 detailed research sub-questions
2. A short description of the expected final output format

Topic:
{topic}

Respond strictly in JSON format with keys:
- sub_questions (list of strings)
- output_format (string)
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Multi-Agent Research System"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()

    if "choices" not in data:
        raise RuntimeError(
         f"OpenRouter error in planner agent: {data}"
        )

    import re
    import json

    raw_text = data["choices"][0]["message"]["content"]

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)

    if not match:
        raise RuntimeError(
            f"Planner did not return valid JSON. Raw output:\n{raw_text}"
        )

    plan_json = match.group()

    json.loads(plan_json)

    return {
        **state,
        "plan": plan_json
    }

