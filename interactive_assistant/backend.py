import re
import os
import requests
from typing import Dict, Optional

from multiagent_system.graph import build_graph

SUMMARY_WORD_LIMITS = {
    "Short": "250-300 words",
    "Long": "600-800 words"
}

ANSWER_WORD_LIMITS = {
    "Short": "150-200 words",
    "Long": "300-500 words"
}

def research_summary_prompt(topic: str, summary_length: str) -> str:
    return f"""
You are a research assistant.

Write a {summary_length.lower()} academic research summary
({SUMMARY_WORD_LIMITS[summary_length]}) on the topic below.

STRUCTURE REQUIREMENTS:
- Summarize the research in a well-structured,
  clear, and concise academic manner.
- Each section may contain multiple paragraphs
- DO NOT restrict the summary to a single paragraph
- NO bullet points
- NO casual explanations

CONTENT REQUIREMENTS:
- Synthesize findings from multiple research papers
- Maintain formal academic tone throughout
- Do NOT fabricate statistics or claims

REFERENCES (MANDATORY):
- Include a final section titled "References"
- Each reference MUST include a clickable URL
- Use well-known academic or institutional sources only
- If reliable references are unavailable, explicitly state:
  "References not available"

Research Topic:
{topic}
"""



# ----------------------------
# Config
# ----------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "amazon/nova-lite-v1"


# ----------------------------
# Intent Detection Helpers
# ----------------------------

def is_url(text: str) -> bool:
    return bool(re.match(r"https?://", text.strip()))


def looks_like_research_topic(text: str) -> bool:
    t = text.lower().strip()

    keywords = [
        "impact", "effect", "analysis", "study", "survey",
        "review", "method", "approach", "framework"
    ]

    # Single-word or short academic topics (e.g., NLP, AI, Blockchain)
    if len(t.split()) <= 2 and t.isalpha():
        return True

    return any(k in t for k in keywords)



def is_system_methodology_question(text: str) -> bool:
    t = text.lower()
    system_refs = ["you", "your", "this summary", "this response"]
    process_terms = [
        "summarize", "summary", "generate", "generated",
        "approach", "method", "methodology", "process"
    ]
    return any(r in t for r in system_refs) and any(p in t for p in process_terms)


# ----------------------------
# LLM Utilities
# ----------------------------

def call_llm(prompt: str, temperature: float = 0.2) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def grounded_answer(context: str, question: str, summary_length: str) -> str:
    prompt = f"""
Answer the question strictly using ONLY the research summary below.

REQUIREMENTS:
- ONE paragraph only
- Length: {ANSWER_WORD_LIMITS[summary_length]}
- Academic tone
- No headings, bullet points, or lists
- Do NOT introduce external knowledge
- If the answer is not present, say:
"Not explicitly mentioned in the provided research summary."

Research Summary:
{context}

Question:
{question}
"""
    return call_llm(prompt)


def system_methodology_answer(summary_length: str) -> str:
    prompt = f"""
Explain, in one concise paragraph, the methodology used by this system
to generate research summaries.

Do not use bullet points or headings.
Maintain a professional academic tone.
"""
    return call_llm(prompt)

# ----------------------------
# Core Router
# ----------------------------

def route_user_input(
    user_input: str,
    session: Dict,
    pdf_text: Optional[str] = None,
    mode: str = "Research Assistant"
) -> str:
    """
    Routes user input based on strict precedence rules.
    """

    summary_length = session.get("summary_length", "Short")

    # ----------------------------
    # General Assistant (NO research pipeline)
    # ----------------------------
    if mode == "General Assistant":
        prompt = f"""
    Answer the following question in ONE paragraph.

    Length: {ANSWER_WORD_LIMITS[summary_length]}
    Tone: Clear and factual
    No headings, no bullet points, no citations.

    Question:
    {user_input}
    """
        return call_llm(prompt, temperature=0.1)


    # ----------------------------
    # System / methodology questions (highest priority)
    # ----------------------------
    if is_system_methodology_question(user_input):
        return system_methodology_answer(summary_length)

    if session.get("research_context"):
        return grounded_answer(
            session["research_context"],
            user_input,
            summary_length
        )    

    # ----------------------------
    # PDF-based summarization
    # ----------------------------
    if pdf_text:
        prompt = f"""
Summarize the following research paper in a well-structured,
clear, and concise academic manner.

MANDATORY REQUIREMENTS:
- Include a final section titled "References"
- List only references present in the content
- If no references are available, state "References not available"
- Do NOT invent citations

Summary length: {summary_length}

Paper content:
{pdf_text}
"""
        summary = call_llm(prompt)
        session["research_context"] = summary
        session["source_type"] = "pdf"
        return summary

    # ----------------------------
    # URL-based handling
    # ----------------------------
    if is_url(user_input):
        return (
            "📄 A research paper URL was detected. "
            "Please upload the PDF version for accurate summarization."
        )

    # ----------------------------
    # Research Topic Summarization (HIGHEST PRIORITY TASK)
    # ----------------------------
    if looks_like_research_topic(user_input):
        prompt = research_summary_prompt(
            user_input,
            summary_length
        )
        summary = call_llm(prompt)
        session["research_context"] = summary
        session["source_type"] = "topic"
        return summary


    # ----------------------------
    # Fallback (should rarely happen)
    # ----------------------------
    prompt = f"""
Answer the following question clearly and concisely in one paragraph.

Question:
{user_input}
"""
    return call_llm(prompt, temperature=0.1)
