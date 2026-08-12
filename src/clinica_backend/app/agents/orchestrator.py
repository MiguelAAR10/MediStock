from dataclasses import dataclass
import time
from typing import Any, Dict

from .memory import session_memory


@dataclass
class AgentResult:
    agent: str
    response: str
    payload: Dict[str, Any]


class AgentOrchestrator:
    MAX_MESSAGE_CHARS = 1500

    def __init__(self) -> None:
        self._graph = None
        try:
            from .graph import build_graph

            self._graph = build_graph()
        except Exception:
            self._graph = None

    def route(self, message: str) -> str:
        text = (message or "").lower()
        if any(
            k in text
            for k in ["venta", "forecast", "predic", "segment", "analit", "kpi"]
        ):
            return "analytics"
        if any(
            k in text
            for k in ["curar", "curacion", "calidad", "limpieza", "depurar", "data"]
        ):
            return "curation"
        if any(
            k in text for k in ["stock", "inventario", "factura", "pago", "consulta"]
        ):
            return "process"
        return "reception"

    def handle(self, message: str, session_id: str = "default") -> AgentResult:
        clean_message = (message or "").strip()
        if len(clean_message) > self.MAX_MESSAGE_CHARS:
            clean_message = clean_message[: self.MAX_MESSAGE_CHARS]

        start = time.perf_counter()
        history = session_memory.get_history(session_id)

        if self._graph is not None:
            result = self._graph.invoke(
                {
                    "message": clean_message,
                    "session_id": session_id,
                    "history": history,
                }
            )
            agent_result = AgentResult(
                agent=result.get("route", "reception"),
                response=result.get("response", "Sin respuesta del agente"),
                payload={
                    **result.get("payload", {}),
                    "meta": {
                        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                        "history_turns": len(history),
                    },
                },
            )
            session_memory.append_user(session_id, clean_message)
            session_memory.append_assistant(session_id, agent_result.response)
            return agent_result

        agent = self.route(clean_message)

        if agent == "analytics":
            agent_result = AgentResult(
                agent=agent,
                response="Agente Analytics: modo fallback activo.",
                payload={
                    "meta": {
                        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                        "history_turns": len(history),
                    }
                },
            )
            session_memory.append_user(session_id, clean_message)
            session_memory.append_assistant(session_id, agent_result.response)
            return agent_result

        if agent == "process":
            agent_result = AgentResult(
                agent=agent,
                response=(
                    "Agente Process: puedo ejecutar flujos operativos como "
                    "facturacion, control de stock y seguimiento de pagos."
                ),
                payload={
                    "meta": {
                        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                        "history_turns": len(history),
                    }
                },
            )
            session_memory.append_user(session_id, clean_message)
            session_memory.append_assistant(session_id, agent_result.response)
            return agent_result

        if agent == "curation":
            agent_result = AgentResult(
                agent=agent,
                response="Agente Curation: puedo validar calidad de datos antes de OLTP.",
                payload={
                    "meta": {
                        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                        "history_turns": len(history),
                    }
                },
            )
            session_memory.append_user(session_id, clean_message)
            session_memory.append_assistant(session_id, agent_result.response)
            return agent_result

        agent_result = AgentResult(
            agent=agent,
            response=(
                "Agente Reception: puedo ayudarte con atencion, estado de pacientes y "
                "consultas generales de la clinica."
            ),
            payload={
                "meta": {
                    "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                    "history_turns": len(history),
                }
            },
        )
        session_memory.append_user(session_id, clean_message)
        session_memory.append_assistant(session_id, agent_result.response)
        return agent_result
