import os
import requests
from tavily import TavilyClient

OPENROUTER_API_KEY = "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"
TAVILY_API_KEY = "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"

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def openrouter_chat(prompt, model="meta-llama/llama-3.3-70b-instruct:free", temperature=0.3):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_subquestions(topic):
    prompt = f"Generate exactly 3 concise research sub-questions about: {topic}"
    text = openrouter_chat(prompt)
    return [q.strip("- ").strip() for q in text.split("\n") if q.strip()]

def search_answers(questions):
    answers = []
    for q in questions:
        result = tavily.search(query=q, search_depth="basic")
        answers.append(result["results"][0]["content"] if result["results"] else "No results found")
    return answers

def summarize(topic, questions, answers):
    combined = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)])
    prompt = f"Topic: {topic}\n\nWrite one concise summary paragraph based on the information below:\n{combined}"
    return openrouter_chat(prompt)

if __name__ == "__main__":
    topic = input("Enter research topic: ")

    subquestions = generate_subquestions(topic)
    print("\nGenerated Sub-Questions:")
    for q in subquestions:
        print("-", q)

    answers = search_answers(subquestions)

    final_summary = summarize(topic, subquestions, answers)
    print("\nFinal Summary:\n")
    print(final_summary)
