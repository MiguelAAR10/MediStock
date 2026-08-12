from typing import Any, Dict, List

from sqlalchemy import text

from app.extensions import db


class OLAPService:
    @staticmethod
    def refresh_olap() -> Dict[str, Any]:
        db.session.execute(text("SELECT olap.refresh_olap_full();"))
        db.session.commit()
        return {"status": "ok", "message": "OLAP refresh completado"}

    @staticmethod
    def insert_insight(
        source_agent: str,
        title: str,
        body: str,
        payload: Dict[str, Any] | None = None,
        severity: str = "info",
    ) -> Dict[str, Any]:
        stmt = text(
            """
            INSERT INTO olap.ai_insights (source_agent, insight_title, insight_body, payload, severity)
            VALUES (:source_agent, :title, :body, CAST(:payload AS JSONB), :severity)
            RETURNING insight_id, generated_at, source_agent, insight_title, insight_body, payload, severity;
            """
        )

        payload_json = "{}"
        if payload is not None:
            import json

            payload_json = json.dumps(payload)

        row = (
            db.session.execute(
                stmt,
                {
                    "source_agent": source_agent,
                    "title": title,
                    "body": body,
                    "payload": payload_json,
                    "severity": severity,
                },
            )
            .mappings()
            .first()
        )
        db.session.commit()
        return dict(row) if row else {}

    @staticmethod
    def latest_insights(limit: int = 20) -> List[Dict[str, Any]]:
        stmt = text(
            """
            SELECT insight_id, generated_at, source_agent, insight_title, insight_body, payload, severity
            FROM olap.ai_insights
            ORDER BY generated_at DESC
            LIMIT :limit;
            """
        )
        rows = db.session.execute(stmt, {"limit": limit}).mappings().all()
        return [dict(r) for r in rows]

    @staticmethod
    def olap_kpis() -> Dict[str, Any]:
        stmt = text(
            """
            SELECT
                COALESCE(SUM(total_neto), 0) AS total_ventas,
                COALESCE(SUM(total_pagado), 0) AS total_pagado,
                COALESCE(SUM(saldo_pendiente), 0) AS saldo_pendiente,
                COUNT(*) AS total_facturas
            FROM olap.fact_ventas;
            """
        )
        row = db.session.execute(stmt).mappings().first()
        return dict(row) if row else {}
