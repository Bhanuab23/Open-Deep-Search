from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

from multiagent_system.agents.planner_agent import planner_agent
from multiagent_system.agents.searcher_agent import searcher_agent
from multiagent_system.agents.writer_agent import writer_agent


class ResearchState(TypedDict):
    topic: str
    plan: str
    search_results: Dict[str, str]
    final_summary: str


def build_graph():
    """
    Builds the LangGraph execution pipeline:
    User Input → Planner → Searcher → Writer → Final Output
    """

    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_agent)
    graph.add_node("searcher", searcher_agent)
    graph.add_node("writer", writer_agent)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
