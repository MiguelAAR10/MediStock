# app/routes/productos.py
from flask import Blueprint, request
from app.services.inventario_service import InventarioService
from app.utils.response import APIResponse

productos_bp = Blueprint("productos", __name__)


@productos_bp.route("/productos", methods=["POST"])
def crear_producto():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        producto = InventarioService.crear_producto(json_data)
        return APIResponse.success(data=producto.to_dict(), status_code=201)
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@productos_bp.route("/productos", methods=["GET"])
def listar_productos():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        id_marca = request.args.get("id_marca", None, type=int)
        search = request.args.get("search", None)

        resultado = InventarioService.listar_productos(
            page=page, per_page=per_page, id_marca=id_marca, search=search
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


@productos_bp.route("/productos/<int:id_producto>", methods=["GET"])
def obtener_producto(id_producto):
    try:
        producto = InventarioService.obtener_producto(id_producto)
        if not producto:
            return APIResponse.error("Producto no encontrado", status_code=404)
        return APIResponse.success(data=producto.to_dict())
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@productos_bp.route("/productos/<int:id_producto>", methods=["PUT"])
def actualizar_producto(id_producto):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        producto = InventarioService.actualizar_producto(id_producto, json_data)
        return APIResponse.success(data=producto.to_dict())
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@productos_bp.route("/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):
    try:
        InventarioService.eliminar_producto(id_producto)
        return APIResponse.success(message="Producto eliminado")
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@productos_bp.route("/productos/<int:id_producto>/stock", methods=["PUT"])
def ajustar_stock(id_producto):
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        producto = InventarioService.ajustar_stock(
            id_producto, json_data.get("cantidad"), json_data.get("operacion", "sum")
        )
        return APIResponse.success(data=producto.to_dict())
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@productos_bp.route("/productos/bajo-stock", methods=["GET"])
def productos_bajo_stock():
    try:
        minimo = request.args.get("minimo", 10, type=int)
        productos = InventarioService.obtener_productos_bajo_stock(minimo)
        return APIResponse.success(data=[p.to_dict() for p in productos])
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@productos_bp.route("/consumos", methods=["POST"])
def registrar_consumo():
    json_data = request.get_json()
    if not json_data:
        return APIResponse.error("No se enviaron datos", status_code=400)

    try:
        consumo = InventarioService.registrar_consumo(
            json_data.get("id_consulta_servicio"),
            json_data.get("id_producto"),
            json_data.get("cantidad"),
        )
        return APIResponse.success(data=consumo.to_dict(), status_code=201)
    except ValueError as e:
        return APIResponse.error(str(e), status_code=400)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
