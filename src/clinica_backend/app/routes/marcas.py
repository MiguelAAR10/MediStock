# app/routes/marcas.py
from flask import Blueprint, request
from app.models.marca import Marca
from app.extensions import db
from app.utils.response import APIResponse

marcas_bp = Blueprint("marcas", __name__)


@marcas_bp.route("/marcas", methods=["POST"])
def crear_marca():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        marca = Marca(**json_data)
        db.session.add(marca)
        db.session.commit()
        return APIResponse.success(data=marca.to_dict(), status_code=201)
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@marcas_bp.route("/marcas", methods=["GET"])
def listar_marcas():
    try:
        marcas = Marca.query.order_by(Marca.nombre_marca).all()
        return APIResponse.success(data=[m.to_dict() for m in marcas])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@marcas_bp.route("/marcas/<int:id_marca>", methods=["GET"])
def obtener_marca(id_marca):
    try:
        marca = Marca.query.get(id_marca)
        if not marca:
            return APIResponse.error("Marca no encontrada", status_code=404)
        return APIResponse.success(data=marca.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@marcas_bp.route("/marcas/<int:id_marca>", methods=["PUT"])
def actualizar_marca(id_marca):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        marca = Marca.query.get(id_marca)
        if not marca:
            return APIResponse.error("Marca no encontrada", status_code=404)

        for key, value in json_data.items():
            setattr(marca, key, value)

        db.session.commit()
        return APIResponse.success(data=marca.to_dict())
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)


@marcas_bp.route("/marcas/<int:id_marca>", methods=["DELETE"])
def eliminar_marca(id_marca):
    try:
        marca = Marca.query.get(id_marca)
        if not marca:
            return APIResponse.error("Marca no encontrada", status_code=404)

        db.session.delete(marca)
        db.session.commit()
        return APIResponse.success(message="Marca eliminada")
    except Exception as e:
        db.session.rollback()
        return APIResponse.error(str(e), status_code=500)
