import requests
from typing import Any, Dict, Optional

from config import Settings


class APIClient:
    def __init__(self) -> None:
        self.base_url = Settings.API_BASE_URL.rstrip("/")
        self.timeout = Settings.REQUEST_TIMEOUT

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            resp = requests.request(
                method=method, url=url, params=params, json=json, timeout=self.timeout
            )
            payload = resp.json()
            if not resp.ok:
                message = payload.get("error", {}).get(
                    "message", f"HTTP {resp.status_code}"
                )
                return {"ok": False, "message": message, "data": None}
            return {
                "ok": True,
                "message": payload.get("message", "OK"),
                "data": payload.get("data"),
            }
        except requests.RequestException as exc:
            return {"ok": False, "message": str(exc), "data": None}
        except ValueError:
            return {
                "ok": False,
                "message": "Respuesta no JSON del servidor",
                "data": None,
            }

    def health(self) -> Dict[str, Any]:
        health_base = self.base_url.replace("/api/v1", "/api")
        url = f"{health_base}/health"
        try:
            resp = requests.get(url, timeout=self.timeout)
            payload = resp.json()
            if not resp.ok:
                message = payload.get("error", {}).get(
                    "message", f"HTTP {resp.status_code}"
                )
                return {"ok": False, "message": message, "data": None}
            return {
                "ok": True,
                "message": payload.get("message", "OK"),
                "data": payload.get("data"),
            }
        except requests.RequestException as exc:
            return {"ok": False, "message": str(exc), "data": None}
        except ValueError:
            return {
                "ok": False,
                "message": "Respuesta no JSON del servidor",
                "data": None,
            }

    def get_kpis(self) -> Dict[str, Any]:
        return self._request("GET", "/analytics/kpis")

    def get_ventas_diarias(
        self, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
        params = {k: v for k, v in params.items() if v}
        return self._request("GET", "/analytics/ventas-diarias", params=params)

    def get_clientes_analytics(self) -> Dict[str, Any]:
        return self._request("GET", "/analytics/clientes")

    def get_segmentos(self) -> Dict[str, Any]:
        return self._request("GET", "/analytics/segmentos")

    def listar_pacientes(
        self, page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"page": page, "per_page": per_page, "search": search}
        params = {k: v for k, v in params.items() if v is not None and v != ""}
        return self._request("GET", "/pacientes", params=params)

    def crear_paciente(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pacientes", json=payload)

    def listar_consultas(
        self, page: int = 1, per_page: int = 20, paciente_id: Optional[int] = None
    ) -> Dict[str, Any]:
        params = {"page": page, "per_page": per_page, "paciente_id": paciente_id}
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "/consultas", params=params)

    def crear_consulta(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/consultas", json=payload)

    def listar_productos(
        self, page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"page": page, "per_page": per_page, "search": search}
        params = {k: v for k, v in params.items() if v is not None and v != ""}
        return self._request("GET", "/productos", params=params)

    def listar_facturas(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        return self._request(
            "GET", "/facturas", params={"page": page, "per_page": per_page}
        )

    def agentes_chat(self, message: str, session_id: str) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/agentes/chat",
            json={"message": message, "session_id": session_id},
        )


api_client = APIClient()
