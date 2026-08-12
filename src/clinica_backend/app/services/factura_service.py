# app/services/factura_service.py
"""
Service Layer - Logica de Negocio para Factura
"""

from app.extensions import db
from app.models.factura import Factura
from app.models.consulta import Consulta
from app.models.consulta_servicio import ConsultaServicio
from app.models.descuento import Descuento
from app.models.consumo_producto import ConsumoProducto
from sqlalchemy.exc import IntegrityError


class FacturaService:
    @staticmethod
    def crear_factura_desde_consulta(id_consulta, id_descuento=None):
        consulta = Consulta.query.get(id_consulta)
        if not consulta:
            raise ValueError("Consulta no encontrada")

        if consulta.factura:
            raise ValueError("La consulta ya tiene una factura asociada")

        total_bruto = 0

        for cs in consulta.servicios:
            total_bruto += float(cs.precio_servicio or 0)
            for consumo in cs.consumos:
                total_bruto += float(consumo.importe_venta or 0)

        monto_descuento = 0
        if id_descuento:
            descuento = Descuento.query.get(id_descuento)
            if descuento:
                if descuento.tipo_descuento == "PORCENTAJE":
                    monto_descuento = total_bruto * (float(descuento.valor) / 100)
                else:
                    monto_descuento = float(descuento.valor)

        total_neto = total_bruto - monto_descuento

        factura = Factura(
            id_consulta=id_consulta,
            total_bruto=total_bruto,
            id_descuento=id_descuento,
            monto_descuento=monto_descuento,
            total_neto=total_neto,
            total_historico=consulta.total_historico or total_neto,
        )

        try:
            db.session.add(factura)
            db.session.commit()
            return factura
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_factura(id_factura):
        return Factura.query.get(id_factura)

    @staticmethod
    def obtener_factura_por_consulta(id_consulta):
        return Factura.query.filter_by(id_consulta=id_consulta).first()

    @staticmethod
    def listar_facturas(
        page=1, per_page=20, paciente_id=None, fecha_inicio=None, fecha_fin=None
    ):
        query = Factura.query.join(Consulta)

        if paciente_id:
            query = query.filter(Consulta.id_paciente == paciente_id)

        if fecha_inicio:
            query = query.filter(Factura.fecha_emision >= fecha_inicio)

        if fecha_fin:
            query = query.filter(Factura.fecha_emision <= fecha_fin)

        query = query.order_by(Factura.fecha_emision.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def actualizar_factura(id_factura, data):
        factura = Factura.query.get(id_factura)
        if not factura:
            raise ValueError("Factura no encontrada")

        if "id_descuento" in data:
            factura.id_descuento = data["id_descuento"]

        total_bruto = float(factura.total_bruto)
        monto_descuento = 0

        if factura.id_descuento:
            descuento = Descuento.query.get(factura.id_descuento)
            if descuento:
                if descuento.tipo_descuento == "PORCENTAJE":
                    monto_descuento = total_bruto * (float(descuento.valor) / 100)
                else:
                    monto_descuento = float(descuento.valor)

        factura.monto_descuento = monto_descuento
        factura.total_neto = total_bruto - monto_descuento

        try:
            db.session.commit()
            return factura
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def eliminar_factura(id_factura):
        factura = Factura.query.get(id_factura)
        if not factura:
            raise ValueError("Factura no encontrada")

        if factura.pagos.count() > 0:
            raise ValueError("No se puede eliminar una factura con pagos asociados")

        try:
            db.session.delete(factura)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_facturas_pendientes():
        facturas = Factura.query.all()
        result = []
        for f in facturas:
            if not f.esta_pagada:
                result.append(f)
        return result
