# app/routes/distritos.py
from flask import Blueprint, request
from app.models.distrito import Distrito
from app.extensions import db
from app.utils.response import APIResponse

distritos_bp = Blueprint("distritos", __name__)


@distritos_bp.route("/distritos", methods=["POST"])
def crear_distrito():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        distrito = Distrito(**json_data)
        db.session.add(distrito)
        db.session.commit()
        return APIResponse.success(data=distrito.to_dict(), status_code=201)
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@distritos_bp.route("/distritos", methods=["GET"])
def listar_distritos():
    try:
        distritos = Distrito.query.order_by(Distrito.nombre_distrito).all()
        return APIResponse.success(data=[d.to_dict() for d in distritos])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@distritos_bp.route("/distritos/<int:id_distrito>", methods=["GET"])
def obtener_distrito(id_distrito):
    try:
        distrito = Distrito.query.get(id_distrito)
        if not distrito:
            return APIResponse.error("Distrito no encontrado", status_code=404)
        return APIResponse.success(data=distrito.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@distritos_bp.route("/distritos/<int:id_distrito>", methods=["PUT"])
def actualizar_distrito(id_distrito):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        distrito = Distrito.query.get(id_distrito)
        if not distrito:
            return APIResponse.error("Distrito no encontrado", status_code=404)

        for key, value in json_data.items():
            setattr(distrito, key, value)

        db.session.commit()
        return APIResponse.success(data=distrito.to_dict())
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@distritos_bp.route("/distritos/<int:id_distrito>", methods=["DELETE"])
def eliminar_distrito(id_distrito):
    try:
        distrito = Distrito.query.get(id_distrito)
        if not distrito:
            return APIResponse.error("Distrito no encontrado", status_code=404)

        db.session.delete(distrito)
        db.session.commit()
        return APIResponse.success(message="Distrito eliminado")
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)
