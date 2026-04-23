from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import intent_node, rag_node, lead_node, extract_details, greeting_node


def route(state):
    if state["intent"] == "greeting":
        return "greeting"

    if state["intent"] in ["pricing", "personal_info"]:
        return "rag"

    if state["intent"] in ["high_intent", "info_sharing"]:
        return "extract"

    return "rag"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent", intent_node)
    graph.add_node("greeting", greeting_node)
    graph.add_node("rag", rag_node)
    graph.add_node("extract", extract_details)
    graph.add_node("lead", lead_node)

    graph.set_entry_point("intent")

    graph.add_conditional_edges("intent", route, {
        "greeting": "greeting",
        "rag": "rag",
        "extract": "extract"
    })

    graph.add_edge("extract", "lead")
    graph.add_edge("greeting", END)
    graph.add_edge("rag", END)
    graph.add_edge("lead", END)

    return graph.compile()