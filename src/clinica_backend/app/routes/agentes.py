from flask import Blueprint, request

from app.agents import AgentOrchestrator
from app.utils.response import APIResponse


agentes_bp = Blueprint("agentes", __name__)
orchestrator = AgentOrchestrator()


@agentes_bp.route("/agentes/chat", methods=["POST"])
def agentes_chat():
    json_data = request.get_json() or {}
    message = json_data.get("message", "")
    session_id = json_data.get("session_id", "default")

    if not message:
        return APIResponse.error("Campo 'message' requerido", status_code=400)

    result = orchestrator.handle(message, session_id=session_id)
    return APIResponse.success(
        data={
            "session_id": session_id,
            "agent": result.agent,
            "response": result.response,
            "payload": result.payload,
        }
    )
