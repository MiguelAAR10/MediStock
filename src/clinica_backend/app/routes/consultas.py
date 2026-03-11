# app/routes/consultas.py
from flask import Blueprint, request
from marshmallow import ValidationError
from app.services.consulta_service import ConsultaService
from app.services.data_curation_service import DataCurationService
from app.schemas.paciente_schema import PacienteSchema
from app.utils.response import APIResponse

consultas_bp = Blueprint("consultas", __name__)
consulta_schema = PacienteSchema()


@consultas_bp.route("/consultas", methods=["POST"])
def crear_consulta():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        curation_result = DataCurationService.curate_consulta_payload(
            json_data,
            require_paciente=True,
            require_fecha=True,
        )
        if curation_result["issues"]:
            return APIResponse.error(
                "Error de curacion de datos",
                status_code=400,
                details=curation_result["issues"],
            )

        consulta = ConsultaService.crear_consulta(curation_result["curated"])
        return APIResponse.success(data=consulta.to_dict(), status_code=201)
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas", methods=["GET"])
def listar_consultas():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        paciente_id = request.args.get("paciente_id", None, type=int)
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        resultado = ConsultaService.listar_consultas(
            page=page,
            per_page=per_page,
            paciente_id=paciente_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return APIResponse.success(
            data={
                "items": [c.to_dict() for c in resultado["items"]],
                "total": resultado["total"],
                "page": resultado["page"],
                "per_page": resultado["per_page"],
                "pages": resultado["pages"],
            }
        )
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas/<int:id_consulta>", methods=["GET"])
def obtener_consulta(id_consulta):
    try:
        consulta = ConsultaService.obtener_consulta(id_consulta)
        if not consulta:
            return APIResponse.error("Consulta no encontrada", status_code=404)
        return APIResponse.success(data=consulta.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas/<int:id_consulta>", methods=["PUT"])
def actualizar_consulta(id_consulta):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        curation_result = DataCurationService.curate_consulta_payload(
            json_data,
            require_paciente=False,
            require_fecha=False,
        )
        curated = curation_result["curated"]
        if curation_result["issues"] and not curated:
            return APIResponse.error(
                "Error de curacion de datos",
                status_code=400,
                details=curation_result["issues"],
            )

        consulta = ConsultaService.actualizar_consulta(id_consulta, curated)
        return APIResponse.success(data=consulta.to_dict())
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas/<int:id_consulta>", methods=["DELETE"])
def eliminar_consulta(id_consulta):
    try:
        ConsultaService.eliminar_consulta(id_consulta)
        return APIResponse.success(message="Consulta eliminada")
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas/<int:id_consulta>/servicios", methods=["POST"])
def agregar_servicio(id_consulta):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        cs = ConsultaService.agregar_servicio_consulta(
            id_consulta, json_data.get("id_servicio"), json_data.get("precio_servicio")
        )
        return APIResponse.success(data=cs.to_dict(), status_code=201)
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas/<int:id_consulta>/servicios", methods=["GET"])
def listar_servicios_consulta(id_consulta):
    try:
        servicios = ConsultaService.obtener_servicios_consulta(id_consulta)
        return APIResponse.success(data=[s.to_dict() for s in servicios])
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@consultas_bp.route("/consultas/paciente/<int:id_paciente>/historial", methods=["GET"])
def historial_paciente(id_paciente):
    try:
        limit = request.args.get("limit", 10, type=int)
        consultas = ConsultaService.obtener_historial_paciente(id_paciente, limit)
        return APIResponse.success(data=[c.to_dict() for c in consultas])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
