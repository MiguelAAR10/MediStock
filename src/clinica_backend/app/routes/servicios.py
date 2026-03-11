# app/routes/servicios.py
from flask import Blueprint, request
from app.models.servicio_catalogo import ServicioCatalogo
from app.extensions import db
from app.utils.response import APIResponse

servicios_bp = Blueprint("servicios", __name__)


@servicios_bp.route("/servicios", methods=["POST"])
def crear_servicio():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        servicio = ServicioCatalogo(**json_data)
        db.session.add(servicio)
        db.session.commit()
        return APIResponse.success(data=servicio.to_dict(), status_code=201)
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@servicios_bp.route("/servicios", methods=["GET"])
def listar_servicios():
    try:
        servicios = ServicioCatalogo.query.order_by(
            ServicioCatalogo.nombre_servicio
        ).all()
        return APIResponse.success(data=[s.to_dict() for s in servicios])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@servicios_bp.route("/servicios/<int:id_servicio>", methods=["GET"])
def obtener_servicio(id_servicio):
    try:
        servicio = ServicioCatalogo.query.get(id_servicio)
        if not servicio:
            return APIResponse.error("Servicio no encontrado", status_code=404)
        return APIResponse.success(data=servicio.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@servicios_bp.route("/servicios/<int:id_servicio>", methods=["PUT"])
def actualizar_servicio(id_servicio):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        servicio = ServicioCatalogo.query.get(id_servicio)
        if not servicio:
            return APIResponse.error("Servicio no encontrado", status_code=404)

        for key, value in json_data.items():
            setattr(servicio, key, value)

        db.session.commit()
        return APIResponse.success(data=servicio.to_dict())
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@servicios_bp.route("/servicios/<int:id_servicio>", methods=["DELETE"])
def eliminar_servicio(id_servicio):
    try:
        servicio = ServicioCatalogo.query.get(id_servicio)
        if not servicio:
            return APIResponse.error("Servicio no encontrado", status_code=404)

        db.session.delete(servicio)
        db.session.commit()
        return APIResponse.success(message="Servicio eliminado")
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)
