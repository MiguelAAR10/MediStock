# app/services/pago_service.py
"""
Service Layer - Logica de Negocio para Pago
"""

from app.extensions import db
from app.models.pago import Pago
from app.models.factura import Factura
from app.models.medio_pago import MedioPago


class PagoService:
    @staticmethod
    def registrar_pago(data):
        id_factura = data.get("id_factura")
        factura = Factura.query.get(id_factura)
        if not factura:
            raise ValueError("Factura no encontrada")

        id_medio = data.get("id_medio_de_pago")
        medio = MedioPago.query.get(id_medio)
        if not medio:
            raise ValueError("Medio de pago no encontrado")

        monto = data.get("monto_pagado")

        pago = Pago(
            id_factura=id_factura, id_medio_de_pago=id_medio, monto_pagado=monto
        )

        try:
            db.session.add(pago)
            db.session.commit()
            return pago
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_pago(id_pago):
        return Pago.query.get(id_pago)

    @staticmethod
    def listar_pagos(
        page=1, per_page=20, id_factura=None, fecha_inicio=None, fecha_fin=None
    ):
        query = Pago.query

        if id_factura:
            query = query.filter_by(id_factura=id_factura)

        if fecha_inicio:
            query = query.filter(Pago.fecha_pago >= fecha_inicio)

        if fecha_fin:
            query = query.filter(Pago.fecha_pago <= fecha_fin)

        query = query.order_by(Pago.fecha_pago.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def obtener_pagos_factura(id_factura):
        return Pago.query.filter_by(id_factura=id_factura).all()

    @staticmethod
    def eliminar_pago(id_pago):
        pago = Pago.query.get(id_pago)
        if not pago:
            raise ValueError("Pago no encontrado")

        try:
            db.session.delete(pago)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
