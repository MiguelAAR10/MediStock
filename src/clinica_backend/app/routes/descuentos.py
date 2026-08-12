# app/routes/descuentos.py
from flask import Blueprint, request
from app.models.descuento import Descuento
from app.extensions import db
from app.utils.response import APIResponse

descuentos_bp = Blueprint("descuentos", __name__)


@descuentos_bp.route("/descuentos", methods=["POST"])
def crear_descuento():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        descuento = Descuento(**json_data)
        db.session.add(descuento)
        db.session.commit()
        return APIResponse.success(data=descuento.to_dict(), status_code=201)
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@descuentos_bp.route("/descuentos", methods=["GET"])
def listar_descuentos():
    try:
        descuentos = Descuento.query.order_by(Descuento.codigo_descuento).all()
        return APIResponse.success(data=[d.to_dict() for d in descuentos])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@descuentos_bp.route("/descuentos/<int:id_descuento>", methods=["GET"])
def obtener_descuento(id_descuento):
    try:
        descuento = Descuento.query.get(id_descuento)
        if not descuento:
            return APIResponse.error("Descuento no encontrado", status_code=404)
        return APIResponse.success(data=descuento.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@descuentos_bp.route("/descuentos/<int:id_descuento>", methods=["PUT"])
def actualizar_descuento(id_descuento):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        descuento = Descuento.query.get(id_descuento)
        if not descuento:
            return APIResponse.error("Descuento no encontrado", status_code=404)

        for key, value in json_data.items():
            setattr(descuento, key, value)

        db.session.commit()
        return APIResponse.success(data=descuento.to_dict())
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@descuentos_bp.route("/descuentos/<int:id_descuento>", methods=["DELETE"])
def eliminar_descuento(id_descuento):
    try:
        descuento = Descuento.query.get(id_descuento)
        if not descuento:
            return APIResponse.error("Descuento no encontrado", status_code=404)

        db.session.delete(descuento)
        db.session.commit()
        return APIResponse.success(message="Descuento eliminado")
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)
