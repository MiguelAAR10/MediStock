from typing import Any, Dict

from langgraph.graph import END, StateGraph

from .nodes import (
    analytics_node,
    curation_node,
    process_node,
    reception_node,
    router_node,
)
from .state import AgentState


def _route_selector(state: Dict[str, Any]) -> str:
    route = state.get("route", "reception")
    if route not in {"analytics", "curation", "process", "reception"}:
        return "reception"
    return route


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("router", router_node)
    workflow.add_node("analytics", analytics_node)
    workflow.add_node("curation", curation_node)
    workflow.add_node("process", process_node)
    workflow.add_node("reception", reception_node)

    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        _route_selector,
        {
            "analytics": "analytics",
            "curation": "curation",
            "process": "process",
            "reception": "reception",
        },
    )

    workflow.add_edge("analytics", END)
    workflow.add_edge("curation", END)
    workflow.add_edge("process", END)
    workflow.add_edge("reception", END)

    return workflow.compile()
