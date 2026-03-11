from typing import Any, Dict, TypedDict


class AgentState(TypedDict, total=False):
    message: str
    session_id: str
    history: list
    route: str
    route_source: str
    response: str
    payload: Dict[str, Any]
