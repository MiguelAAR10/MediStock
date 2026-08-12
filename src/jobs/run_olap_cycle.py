import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "src" / "clinica_backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

load_dotenv(BACKEND_DIR / ".env")

from app import create_app
from app.agents import AgentOrchestrator
from app.services.olap_service import OLAPService


def run_cycle() -> None:
    app = create_app(os.getenv("FLASK_ENV", "default"))

    with app.app_context():
        refresh_result = OLAPService.refresh_olap()
        print(
            f"[{datetime.utcnow().isoformat()}] Refresh OLAP: {refresh_result['message']}"
        )

        orchestrator = AgentOrchestrator()
        prompts = [
            "Analiza ventas, forecasting y segmentos para generar insight ejecutivo.",
            "Evalua calidad de datos y propone acciones de curacion antes de OLTP.",
        ]

        for prompt in prompts:
            result = orchestrator.handle(prompt, session_id="cron-olap")
            severity = "info"

            if result.agent == "curation":
                quality = result.payload.get("quality_snapshot", {})
                if quality.get("pacientes_dni_invalido", 0) > 0:
                    severity = "warning"

            OLAPService.insert_insight(
                source_agent=result.agent,
                title=f"Insight automatico: {result.agent}",
                body=result.response,
                payload=result.payload,
                severity=severity,
            )
            print(f"[{datetime.utcnow().isoformat()}] Insight guardado: {result.agent}")


if __name__ == "__main__":
    run_cycle()
