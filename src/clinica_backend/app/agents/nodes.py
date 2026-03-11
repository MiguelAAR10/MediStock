import os
import re
from typing import Any, Dict

from app.models.paciente import Paciente
from app.services.analytics_service import AnalyticsService
from app.services.data_curation_service import DataCurationService
from app.services.inventario_service import InventarioService


def _heuristic_route(message: str) -> str:
    text = (message or "").lower()
    if any(
        k in text
        for k in [
            "venta",
            "forecast",
            "predic",
            "segment",
            "analit",
            "kpi",
            "tendencia",
        ]
    ):
        return "analytics"
    if any(
        k in text
        for k in ["curar", "curacion", "calidad", "limpieza", "depurar", "data quality"]
    ):
        return "curation"
    if any(
        k in text
        for k in ["stock", "inventario", "factura", "pago", "consulta", "operacion"]
    ):
        return "process"
    return "reception"


def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
    message = state.get("message", "")
    history = state.get("history", [])

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"route": _heuristic_route(message), "route_source": "heuristic"}

    try:
        from pydantic import BaseModel
        from typing import Literal
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        class RouteDecision(BaseModel):
            route: Literal["analytics", "process", "reception", "curation"]

        model_name = os.getenv("AGENT_ROUTER_MODEL", "gpt-4o-mini")
        llm = ChatOpenAI(model=model_name, temperature=0)
        router = llm.with_structured_output(RouteDecision)
        history_text = "\n".join(
            [
                f"{item.get('role', 'user')}: {item.get('content', '')}"
                for item in history[-6:]
            ]
        )

        decision = router.invoke(
            [
                SystemMessage(
                    content=(
                        "Eres un enrutador de agentes de una clinica. "
                        "Devuelve solo analytics, process, reception o curation. "
                        "analytics: preguntas de ventas, pronostico, segmentos, KPIs. "
                        "curation: calidad y limpieza de datos antes de OLTP. "
                        "process: stock, facturacion, pagos, operaciones. "
                        "reception: atencion general y pacientes."
                    )
                ),
                HumanMessage(
                    content=(
                        f"Historial reciente:\n{history_text}\n\n"
                        f"Mensaje actual:\n{message}"
                    )
                ),
            ]
        )
        return {"route": decision.route, "route_source": "llm"}
    except Exception:
        return {
            "route": _heuristic_route(message),
            "route_source": "heuristic_fallback",
        }


def analytics_node(state: Dict[str, Any]) -> Dict[str, Any]:
    kpis = AnalyticsService.get_kpis()
    tendencias = AnalyticsService.get_tendencias(periodo_dias=30)
    segmentos = AnalyticsService.get_segmentos()

    response = (
        "Agente Analytics: "
        f"ingresos S/ {kpis.get('ingresos_totales', 0):,.2f}, "
        f"consultas {kpis.get('total_consultas', 0)}, "
        f"cambio 30d {tendencias.get('cambio_porcentaje', 0)}%."
    )

    payload = {
        "route_source": state.get("route_source", "unknown"),
        "kpis": kpis,
        "tendencias_30d": {
            "ventas_periodo": tendencias.get("ventas_periodo", 0),
            "ventas_periodo_anterior": tendencias.get("ventas_periodo_anterior", 0),
            "cambio_porcentaje": tendencias.get("cambio_porcentaje", 0),
        },
        "segmentos_resumen": {k: v.get("count", 0) for k, v in segmentos.items()},
    }
    return {"response": response, "payload": payload}


def process_node(state: Dict[str, Any]) -> Dict[str, Any]:
    low_stock = InventarioService.obtener_productos_bajo_stock(minimo=10)
    payload = {
        "route_source": state.get("route_source", "unknown"),
        "productos_bajo_stock": [
            {
                "id_producto": p.id_producto,
                "nombre_producto": p.nombre_producto,
                "stock_actual": float(p.stock_actual or 0),
            }
            for p in low_stock
        ],
    }

    response = (
        "Agente Process: operacion lista. "
        f"Productos con stock bajo: {len(payload['productos_bajo_stock'])}."
    )
    return {"response": response, "payload": payload}


def curation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    quality = DataCurationService.data_quality_snapshot()
    recommendations = []

    if quality.get("pacientes_dni_invalido", 0) > 0:
        recommendations.append("Normalizar DNI a 8 digitos antes de insertar en OLTP.")
    if quality.get("pacientes_sin_telefono", 0) > 0:
        recommendations.append(
            "Completar telefonos para activar campañas de retencion."
        )
    if quality.get("pacientes_sin_distrito", 0) > 0:
        recommendations.append(
            "Completar distrito para mejorar segmentacion geografica."
        )

    response = (
        "Agente Curation: calidad evaluada. "
        f"DNI invalido: {quality.get('pacientes_dni_invalido', 0)}, "
        f"sin telefono: {quality.get('pacientes_sin_telefono', 0)}."
    )

    return {
        "response": response,
        "payload": {
            "route_source": state.get("route_source", "unknown"),
            "quality_snapshot": quality,
            "recommendations": recommendations,
        },
    }


def reception_node(state: Dict[str, Any]) -> Dict[str, Any]:
    message = state.get("message", "")
    dni_match = re.search(r"\b\d{8}\b", message)

    if dni_match:
        dni = dni_match.group(0)
        paciente = Paciente.buscar_por_dni(dni)
        if paciente:
            response = (
                "Agente Reception: paciente encontrado. "
                f"Nombre: {paciente.nombre_completo}, telefono: {paciente.telefono or 'N/A'}."
            )
            payload = {
                "route_source": state.get("route_source", "unknown"),
                "paciente": {
                    "id_paciente": paciente.id_paciente,
                    "dni": paciente.dni,
                    "nombre_completo": paciente.nombre_completo,
                    "telefono": paciente.telefono,
                },
            }
            return {"response": response, "payload": payload}

    return {
        "response": (
            "Agente Reception: puedo ayudarte con estado de pacientes, "
            "consultas y orientacion general de servicios."
        ),
        "payload": {"route_source": state.get("route_source", "unknown")},
    }
