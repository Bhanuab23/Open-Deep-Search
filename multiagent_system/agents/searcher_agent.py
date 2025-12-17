from typing import Dict
from dotenv import load_dotenv
import os
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily = TavilyClient(api_key=TAVILY_API_KEY)


def searcher_agent(state: Dict) -> Dict:
    """
    Searcher Agent:
    - Takes sub-questions from planner output
    - Uses Tavily to fetch information
    - Returns structured search results
    """

    plan = state["plan"]

    
    import json
    plan_data = json.loads(plan)

    sub_questions = plan_data["sub_questions"]

    search_results = {}

    for question in sub_questions:
        response = tavily.search(
            query=question,
            search_depth="basic",
            max_results=3
        )

        if response.get("results"):
            combined_answer = " ".join(
                result["content"] for result in response["results"]
            )
        else:
            combined_answer = "No relevant results found."

        search_results[question] = combined_answer

    return {
        **state,
        "search_results": search_results
    }
