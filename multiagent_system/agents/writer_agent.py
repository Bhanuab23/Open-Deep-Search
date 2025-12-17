from typing import Dict
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "meta-llama/llama-3.3-70b-instruct:free"


def writer_agent(state: Dict) -> Dict:
    """
    Writer Agent:
    - Synthesizes planner instructions and search results
    - Produces a structured final summary
    """

    plan = json.loads(state["plan"])
    search_results = state["search_results"]

    prompt = f"""
You are a research writer.

Planner instructions:
- Sub-questions: {plan["sub_questions"]}
- Expected output format: {plan["output_format"]}

Research findings:
{json.dumps(search_results, indent=2)}

Write a well-structured, clear, and concise final research summary.
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
            f"OpenRouter error in writer agent: {data}"
        )

    final_summary = data["choices"][0]["message"]["content"]

    return {
        **state,
        "final_summary": final_summary
    }
