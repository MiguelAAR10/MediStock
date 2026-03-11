# app/routes/facturas.py
from flask import Blueprint, request
from app.services.factura_service import FacturaService
from app.utils.response import APIResponse

facturas_bp = Blueprint("facturas", __name__)


@facturas_bp.route("/facturas", methods=["POST"])
def crear_factura():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        factura = FacturaService.crear_factura_desde_consulta(
            json_data.get("id_consulta"), json_data.get("id_descuento")
        )
        return APIResponse.success(data=factura.to_dict(), status_code=201)
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@facturas_bp.route("/facturas", methods=["GET"])
def listar_facturas():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        paciente_id = request.args.get("paciente_id", None, type=int)
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        resultado = FacturaService.listar_facturas(
            page=page,
            per_page=per_page,
            paciente_id=paciente_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return APIResponse.success(
            data={
                "items": [f.to_dict() for f in resultado["items"]],
                "total": resultado["total"],
                "page": resultado["page"],
                "per_page": resultado["per_page"],
                "pages": resultado["pages"],
            }
        )
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@facturas_bp.route("/facturas/<int:id_factura>", methods=["GET"])
def obtener_factura(id_factura):
    try:
        factura = FacturaService.obtener_factura(id_factura)
        if not factura:
            return APIResponse.error("Factura no encontrada", status_code=404)
        return APIResponse.success(data=factura.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@facturas_bp.route("/facturas/consulta/<int:id_consulta>", methods=["GET"])
def obtener_factura_por_consulta(id_consulta):
    try:
        factura = FacturaService.obtener_factura_por_consulta(id_consulta)
        if not factura:
            return APIResponse.error("Factura no encontrada", status_code=404)
        return APIResponse.success(data=factura.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@facturas_bp.route("/facturas/<int:id_factura>", methods=["PUT"])
def actualizar_factura(id_factura):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        factura = FacturaService.actualizar_factura(id_factura, json_data)
        return APIResponse.success(data=factura.to_dict())
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@facturas_bp.route("/facturas/<int:id_factura>", methods=["DELETE"])
def eliminar_factura(id_factura):
    try:
        FacturaService.eliminar_factura(id_factura)
        return APIResponse.success(message="Factura eliminada")
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@facturas_bp.route("/facturas/pendientes", methods=["GET"])
def facturas_pendientes():
    try:
        facturas = FacturaService.obtener_facturas_pendientes()
        return APIResponse.success(data=[f.to_dict() for f in facturas])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
