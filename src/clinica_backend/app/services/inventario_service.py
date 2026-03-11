# app/services/inventario_service.py
"""
Service Layer - Logica de Negocio para Inventario
"""

from app.extensions import db
from app.models.producto import Producto
from app.models.marca import Marca
from app.models.consumo_producto import ConsumoProducto
from app.models.consulta_servicio import ConsultaServicio


class InventarioService:
    @staticmethod
    def crear_producto(data):
        if data.get("id_marca"):
            marca = Marca.query.get(data["id_marca"])
            if not marca:
                raise ValueError("Marca no encontrada")

        producto = Producto(**data)

        try:
            db.session.add(producto)
            db.session.commit()
            return producto
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_producto(id_producto):
        return Producto.query.get(id_producto)

    @staticmethod
    def listar_productos(page=1, per_page=20, id_marca=None, search=None):
        query = Producto.query

        if id_marca:
            query = query.filter_by(id_marca=id_marca)

        if search:
            query = query.filter(Producto.nombre_producto.ilike(f"%{search}%"))

        query = query.order_by(Producto.nombre_producto.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def actualizar_producto(id_producto, data):
        producto = Producto.query.get(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")

        for key, value in data.items():
            setattr(producto, key, value)

        try:
            db.session.commit()
            return producto
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def eliminar_producto(id_producto):
        producto = Producto.query.get(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")

        if producto.consumos.count() > 0:
            raise ValueError("No se puede eliminar un producto con consumos asociados")

        try:
            db.session.delete(producto)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def ajustar_stock(id_producto, cantidad, operacion="sum"):
        producto = Producto.query.get(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")

        stock_actual = float(producto.stock_actual or 0)

        if operacion == "sum":
            producto.stock_actual = stock_actual + cantidad
        elif operacion == "subtract":
            producto.stock_actual = stock_actual - cantidad
            if producto.stock_actual < 0:
                raise ValueError("Stock no puede ser negativo")
        else:
            raise ValueError("Operación no válida")

        try:
            db.session.commit()
            return producto
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_productos_bajo_stock(minimo=10):
        return Producto.query.filter(Producto.stock_actual <= minimo).all()

    @staticmethod
    def registrar_consumo(id_consulta_servicio, id_producto, cantidad):
        consulta_servicio = ConsultaServicio.query.get(id_consulta_servicio)
        if not consulta_servicio:
            raise ValueError("Consulta servicio no encontrada")

        producto = Producto.query.get(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")

        stock_actual = float(producto.stock_actual or 0)
        if stock_actual < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {stock_actual}")

        importe_venta = float(producto.precio_venta) * cantidad

        consumo = ConsumoProducto(
            id_consulta_servicio=id_consulta_servicio,
            id_producto=id_producto,
            cantidad_consumida=cantidad,
            precio_producto=producto.precio_venta,
            importe_venta=importe_venta,
        )

        producto.stock_actual = stock_actual - cantidad

        try:
            db.session.add(consumo)
            db.session.commit()
            return consumo
        except Exception as e:
            db.session.rollback()
            raise e
