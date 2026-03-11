import re
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import text

from app.extensions import db


class DataCurationService:
    @staticmethod
    def _normalize_text(value: Any) -> str | None:
        if value is None:
            return None
        text_value = str(value).strip()
        if not text_value:
            return None
        text_value = re.sub(r"\s+", " ", text_value)
        return text_value

    @staticmethod
    def _normalize_dni(value: Any) -> str | None:
        if value is None:
            return None
        digits = re.sub(r"\D", "", str(value))
        if len(digits) == 8:
            return digits
        return None

    @staticmethod
    def _normalize_phone(value: Any) -> str | None:
        if value is None:
            return None
        phone = re.sub(r"[^\d+]", "", str(value))
        return phone if phone else None

    @staticmethod
    def curate_paciente_payload(
        payload: Dict[str, Any],
        require_nombre: bool = True,
        require_dni: bool = True,
    ) -> Dict[str, Any]:
        issues: list[str] = []
        curated: Dict[str, Any] = {}

        raw_nombre = payload.get("nombre_completo", payload.get("nombreCompleto"))
        raw_dni = payload.get("dni")
        raw_sexo = payload.get("sexo")
        raw_telefono = payload.get("telefono")

        nombre = DataCurationService._normalize_text(raw_nombre)
        dni = DataCurationService._normalize_dni(raw_dni)
        sexo = DataCurationService._normalize_text(raw_sexo)
        telefono = DataCurationService._normalize_phone(raw_telefono)

        if nombre is None and require_nombre:
            issues.append("nombre_completo faltante o invalido")
        elif nombre is not None:
            curated["nombre_completo"] = nombre.title()

        if dni is None and require_dni:
            issues.append("dni invalido: debe contener 8 digitos")
        elif dni is not None:
            curated["dni"] = dni

        if sexo:
            sexo_map = {"MASCULINO": "M", "FEMENINO": "F", "OTRO": "O"}
            sexo_up = sexo.upper()
            sexo_norm = sexo_map.get(sexo_up, sexo_up)
            if sexo_norm not in {"M", "F", "O"}:
                issues.append("sexo invalido: usar M/F/O")
            else:
                curated["sexo"] = sexo_norm

        if telefono:
            curated["telefono"] = telefono

        for field in [
            "id_distrito",
            "nacimiento_year",
            "nacimiento_month",
            "nacimiento_day",
            "paciente_problematico",
        ]:
            if field in payload:
                curated[field] = payload[field]

        return {"curated": curated, "issues": issues}

    @staticmethod
    def curate_consulta_payload(
        payload: Dict[str, Any],
        require_paciente: bool = True,
        require_fecha: bool = True,
    ) -> Dict[str, Any]:
        issues: list[str] = []
        curated: Dict[str, Any] = {}

        id_paciente = payload.get("id_paciente")
        fecha_consulta = payload.get("fecha_consulta")
        notas = payload.get("notas_generales", "")
        total_historico = payload.get("total_historico", 0)

        if not id_paciente and require_paciente:
            issues.append("id_paciente es requerido")
        elif id_paciente is not None:
            curated["id_paciente"] = int(id_paciente)

        if fecha_consulta:
            try:
                if isinstance(fecha_consulta, str):
                    datetime.strptime(fecha_consulta, "%Y-%m-%d")
                curated["fecha_consulta"] = fecha_consulta
            except Exception:
                issues.append("fecha_consulta invalida, formato esperado YYYY-MM-DD")
        elif require_fecha:
            issues.append("fecha_consulta es requerida")

        if "notas_generales" in payload:
            curated["notas_generales"] = (
                DataCurationService._normalize_text(notas) or ""
            )

        if "total_historico" in payload:
            try:
                curated["total_historico"] = float(total_historico)
            except Exception:
                issues.append("total_historico invalido")

        return {"curated": curated, "issues": issues}

    @staticmethod
    def data_quality_snapshot() -> Dict[str, Any]:
        stmt = text(
            """
            SELECT
                COUNT(*) AS total_pacientes,
                COUNT(*) FILTER (WHERE dni IS NULL OR LENGTH(REGEXP_REPLACE(dni, '\\D', '', 'g')) <> 8) AS pacientes_dni_invalido,
                COUNT(*) FILTER (WHERE telefono IS NULL OR TRIM(telefono) = '') AS pacientes_sin_telefono,
                COUNT(*) FILTER (WHERE id_distrito IS NULL) AS pacientes_sin_distrito
            FROM pacientes;
            """
        )
        row = db.session.execute(stmt).mappings().first()
        return dict(row) if row else {}
