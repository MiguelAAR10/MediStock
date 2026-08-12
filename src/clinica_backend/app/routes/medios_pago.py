# app/routes/medios_pago.py
from flask import Blueprint, request
from app.models.medio_pago import MedioPago
from app.extensions import db
from app.utils.response import APIResponse

medios_pago_bp = Blueprint("medios_pago", __name__)


@medios_pago_bp.route("/medios-pago", methods=["POST"])
def crear_medio_pago():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        medio = MedioPago(**json_data)
        db.session.add(medio)
        db.session.commit()
        return APIResponse.success(data=medio.to_dict(), status_code=201)
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@medios_pago_bp.route("/medios-pago", methods=["GET"])
def listar_medios_pago():
    try:
        medios = MedioPago.query.order_by(MedioPago.nombre_m_pago).all()
        return APIResponse.success(data=[m.to_dict() for m in medios])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@medios_pago_bp.route("/medios-pago/<int:id_m_pago>", methods=["GET"])
def obtener_medio_pago(id_m_pago):
    try:
        medio = MedioPago.query.get(id_m_pago)
        if not medio:
            return APIResponse.error("Medio de pago no encontrado", status_code=404)
        return APIResponse.success(data=medio.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@medios_pago_bp.route("/medios-pago/<int:id_m_pago>", methods=["PUT"])
def actualizar_medio_pago(id_m_pago):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        medio = MedioPago.query.get(id_m_pago)
        if not medio:
            return APIResponse.error("Medio de pago no encontrado", status_code=404)

        for key, value in json_data.items():
            setattr(medio, key, value)

        db.session.commit()
        return APIResponse.success(data=medio.to_dict())
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@medios_pago_bp.route("/medios-pago/<int:id_m_pago>", methods=["DELETE"])
def eliminar_medio_pago(id_m_pago):
    try:
        medio = MedioPago.query.get(id_m_pago)
        if not medio:
            return APIResponse.error("Medio de pago no encontrado", status_code=404)

        db.session.delete(medio)
        db.session.commit()
        return APIResponse.success(message="Medio de pago eliminado")
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)
