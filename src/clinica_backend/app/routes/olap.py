from flask import Blueprint, request

from app.agents import AgentOrchestrator
from app.services.olap_service import OLAPService
from app.utils.response import APIResponse


olap_bp = Blueprint("olap", __name__)


@olap_bp.route("/olap/refresh", methods=["POST"])
def olap_refresh():
    try:
        result = OLAPService.refresh_olap()
        return APIResponse.success(data=result, message="Refresh OLAP ejecutado")
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@olap_bp.route("/olap/insights", methods=["POST"])
def create_insight():
    json_data = request.get_json() or {}
    source_agent = json_data.get("source_agent", "analytics")
    title = json_data.get("title")
    body = json_data.get("body")
    payload = json_data.get("payload", {})
    severity = json_data.get("severity", "info")

    if not title or not body:
        return APIResponse.error(
            "Campos 'title' y 'body' son requeridos", status_code=400
        )

    try:
        insight = OLAPService.insert_insight(
            source_agent=source_agent,
            title=title,
            body=body,
            payload=payload,
            severity=severity,
        )
        return APIResponse.success(data=insight, status_code=201)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@olap_bp.route("/olap/insights", methods=["GET"])
def get_insights():
    limit = request.args.get("limit", 20, type=int)
    try:
        items = OLAPService.latest_insights(limit=limit)
        return APIResponse.success(data=items)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@olap_bp.route("/olap/kpis", methods=["GET"])
def get_olap_kpis():
    try:
        data = OLAPService.olap_kpis()
        return APIResponse.success(data=data)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@olap_bp.route("/olap/run-cycle", methods=["POST"])
def run_olap_cycle():
    try:
        refresh = OLAPService.refresh_olap()
        orchestrator = AgentOrchestrator()

        prompts = [
            "Analiza ventas y genera insight ejecutivo",
            "Evalua curacion de datos y calidad para OLTP",
        ]

        saved = []
        for prompt in prompts:
            result = orchestrator.handle(prompt, session_id="manual-olap-cycle")
            saved.append(
                OLAPService.insert_insight(
                    source_agent=result.agent,
                    title=f"Insight manual: {result.agent}",
                    body=result.response,
                    payload=result.payload,
                )
            )

        return APIResponse.success(
            data={"refresh": refresh, "insights_saved": saved},
            message="Ciclo OLAP + insights completado",
        )
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
