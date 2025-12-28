import re
import os
import requests
import tempfile
from typing import Dict, Optional

from multiagent_system.graph import build_graph

from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text

# ----------------------------
# Configuration
# ----------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "amazon/nova-lite-v1"

SUMMARY_WORD_LIMITS = {
    "Short": "250-300 words",
    "Long": "600-800 words"
}

ANSWER_WORD_LIMITS = {
    "Short": "150-200 words",
    "Long": "300-500 words"
}

# ----------------------------
# URL Content Extraction
# ----------------------------

def fetch_url_content(url: str) -> str:
    """
    Fetches text content from a research paper URL.
    Supports both PDF and HTML pages.
    """
    url = url.strip()

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()

    # ---- PDF ----
    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        text = extract_text(tmp_path)
        return text.strip()

    # ---- HTML ----
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())


# ----------------------------
# Prompt Builders
# ----------------------------

def research_summary_prompt(topic: str, summary_length: str) -> str:
    return f"""
You are a research assistant.

Write a {summary_length.lower()} academic research summary
({SUMMARY_WORD_LIMITS[summary_length]}) on the topic below.

STRUCTURE REQUIREMENTS:
- Well-structured academic sections
- Multiple paragraphs allowed
- No bullet points
- Formal academic tone

CONTENT REQUIREMENTS:
- Synthesize findings from multiple research papers
- Do NOT fabricate claims or statistics

REFERENCES (MANDATORY):
- Include a final section titled "References"
- Each reference must include a clickable URL
- If unavailable, state "References not available"

Research Topic:
{topic}
"""


def grounded_answer_prompt(context: str, question: str, summary_length: str) -> str:
    return f"""
Answer the question strictly using ONLY the research summary below.

REQUIREMENTS:
- ONE paragraph only
- Length: {ANSWER_WORD_LIMITS[summary_length]}
- Academic tone
- No headings or bullet points
- No external knowledge

If the answer is not present, say:
"Not explicitly mentioned in the provided research summary."

Research Summary:
{context}

Question:
{question}
"""


def system_methodology_prompt() -> str:
    return """
Explain, in one concise paragraph, the methodology used by this system
to generate research summaries.

Do not use bullet points or headings.
Maintain a professional academic tone.
"""


# ----------------------------
# Intent Detection Helpers
# ----------------------------

def is_url(text: str) -> bool:
    return bool(re.match(r"https?://", text.strip()))


def looks_like_research_topic(text: str) -> bool:
    t = text.lower().strip()

    keywords = [
        "impact", "effect", "analysis", "study", "survey",
        "review", "method", "approach", "framework", "summarize"
    ]

    if len(t.split()) <= 2 and t.isalpha():
        return True

    return any(k in t for k in keywords)


def is_system_methodology_question(text: str) -> bool:
    t = text.lower()
    system_refs = ["you", "your", "this summary", "this response"]
    process_terms = [
        "summary", "summarized", "generate",
        "method", "methodology", "process"
    ]
    return any(r in t for r in system_refs) and any(p in t for p in process_terms)


# ----------------------------
# LLM Utility
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
    Routes user input using session-aware logic.
    Each session corresponds to one chat.
    """

    summary_length = session.get("summary_length", "Short")

    # ----------------------------
    # General Assistant
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
    # System / methodology question
    # ----------------------------
    if is_system_methodology_question(user_input):
        return call_llm(system_methodology_prompt())

    # ----------------------------
    # Follow-up question (grounded)
    # ----------------------------
    if session.get("research_context"):
        prompt = grounded_answer_prompt(
            session["research_context"],
            user_input,
            summary_length
        )
        return call_llm(prompt)

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
    # URL-based summarization
    # ----------------------------
    if is_url(user_input):
        try:
            paper_text = fetch_url_content(user_input)

            if not paper_text or len(paper_text.split()) < 500:
                return (
                    "⚠️ Unable to extract sufficient academic content from the URL. "
                    "Please upload the PDF version for accurate summarization."
                )

            prompt = f"""
Summarize the following research paper in a well-structured,
clear, and concise academic manner.

MANDATORY REQUIREMENTS:
- Include a final section titled "References"
- List only references present in the content
- Do NOT invent citations
- Formal academic tone

Summary length: {summary_length}

Paper content:
{paper_text}
"""
            summary = call_llm(prompt)
            session["research_context"] = summary
            session["source_type"] = "url"
            return summary

        except Exception as e:
            return f"❌ Failed to process the URL: {str(e)}"

    # ----------------------------
    # Research topic summarization
    # ----------------------------
    if looks_like_research_topic(user_input):
        prompt = research_summary_prompt(user_input, summary_length)
        summary = call_llm(prompt)
        session["research_context"] = summary
        session["source_type"] = "topic"
        return summary

    # ----------------------------
    # Fallback
    # ----------------------------
    prompt = f"""
Answer the following question clearly and concisely in one paragraph.

Question:
{user_input}
"""
    return call_llm(prompt, temperature=0.1)
