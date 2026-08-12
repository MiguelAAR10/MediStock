# app/routes/pagos.py
from flask import Blueprint, request
from app.services.pago_service import PagoService
from app.utils.response import APIResponse

pagos_bp = Blueprint("pagos", __name__)


@pagos_bp.route("/pagos", methods=["POST"])
def crear_pago():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        pago = PagoService.registrar_pago(json_data)
        return APIResponse.success(data=pago.to_dict(), status_code=201)
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@pagos_bp.route("/pagos", methods=["GET"])
def listar_pagos():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        id_factura = request.args.get("id_factura", None, type=int)
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        resultado = PagoService.listar_pagos(
            page=page,
            per_page=per_page,
            id_factura=id_factura,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return APIResponse.success(
            data={
                "items": [p.to_dict() for p in resultado["items"]],
                "total": resultado["total"],
                "page": resultado["page"],
                "per_page": resultado["per_page"],
                "pages": resultado["pages"],
            }
        )
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@pagos_bp.route("/pagos/<int:id_pago>", methods=["GET"])
def obtener_pago(id_pago):
    try:
        pago = PagoService.obtener_pago(id_pago)
        if not pago:
            return APIResponse.error("Pago no encontrado", status_code=404)
        return APIResponse.success(data=pago.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@pagos_bp.route("/pagos/factura/<int:id_factura>", methods=["GET"])
def obtener_pagos_factura(id_factura):
    try:
        pagos = PagoService.obtener_pagos_factura(id_factura)
        return APIResponse.success(data=[p.to_dict() for p in pagos])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@pagos_bp.route("/pagos/<int:id_pago>", methods=["DELETE"])
def eliminar_pago(id_pago):
    try:
        PagoService.eliminar_pago(id_pago)
        return APIResponse.success(message="Pago eliminado")
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
