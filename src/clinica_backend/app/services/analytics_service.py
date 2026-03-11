# app/services/analytics_service.py
"""
Service Layer - Logica de Negocio para Analytics (ML)
Este servicio proporciona los datos necesarios para los modelos de ML:
- Forecasting de ventas
- Clustering de clientes
- Segmentación PCA
"""

from app.extensions import db
from app.models.consulta import Consulta
from app.models.factura import Factura
from app.models.pago import Pago
from app.models.paciente import Paciente
from app.models.marca import Marca
from app.models.producto import Producto
from app.models.servicio_catalogo import ServicioCatalogo
from app.models.consulta_servicio import ConsultaServicio
from app.models.consumo_producto import ConsumoProducto
from sqlalchemy import func, extract
from datetime import datetime, timedelta


class AnalyticsService:
    @staticmethod
    def get_ventas_diarias(fecha_inicio=None, fecha_fin=None):
        query = db.session.query(
            func.date(Consulta.fecha_consulta).label("fecha"),
            func.count(Consulta.id_consulta).label("num_consultas"),
            func.sum(Factura.total_neto).label("ventas"),
        ).join(Factura, Consulta.id_consulta == Factura.id_consulta)

        if fecha_inicio:
            query = query.filter(Consulta.fecha_consulta >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Consulta.fecha_consulta <= fecha_fin)

        resultados = query.group_by("fecha").order_by("fecha").all()

        return [
            {
                "fecha": str(r.fecha),
                "num_consultas": r.num_consultas,
                "ventas": float(r.ventas or 0),
            }
            for r in resultados
        ]

    @staticmethod
    def get_ventas_mensuales(año=None):
        query = db.session.query(
            extract("year", Consulta.fecha_consulta).label("año"),
            extract("month", Consulta.fecha_consulta).label("mes"),
            func.count(Consulta.id_consulta).label("num_consultas"),
            func.sum(Factura.total_neto).label("ventas"),
        ).join(Factura, Consulta.id_consulta == Factura.id_consulta)

        if año:
            query = query.filter(extract("year", Consulta.fecha_consulta) == año)

        resultados = query.group_by("año", "mes").order_by("año", "mes").all()

        return [
            {
                "año": int(r.año),
                "mes": int(r.mes),
                "num_consultas": r.num_consultas,
                "ventas": float(r.ventas or 0),
            }
            for r in resultados
        ]

    @staticmethod
    def get_kpis():
        total_pacientes = Paciente.query.count()
        total_consultas = Consulta.query.count()
        total_facturas = Factura.query.count()

        ingresos_totales = db.session.query(func.sum(Factura.total_neto)).scalar() or 0
        promedio_venta = db.session.query(func.avg(Factura.total_neto)).scalar() or 0

        facturas_pendientes = 0
        for f in Factura.query.all():
            if not f.esta_pagada:
                facturas_pendientes += 1

        return {
            "total_pacientes": total_pacientes,
            "total_consultas": total_consultas,
            "total_facturas": total_facturas,
            "ingresos_totales": float(ingresos_totales),
            "promedio_venta": float(promedio_venta),
            "facturas_pendientes": facturas_pendientes,
        }

    @staticmethod
    def get_clientes_para_clustering():
        clientes = Paciente.query.all()
        resultados = []

        for cliente in clientes:
            num_consultas = cliente.consultas.count()

            ingresos = (
                db.session.query(func.sum(Factura.total_neto))
                .join(Consulta)
                .filter(Consulta.id_paciente == cliente.id_paciente)
                .scalar()
                or 0
            )

            ultimo_servicio = None
            if cliente.consultas.count() > 0:
                ultima = cliente.consultas.order_by(
                    Consulta.fecha_consulta.desc()
                ).first()
                ultimo_servicio = ultima.fecha_consulta

            resultados.append(
                {
                    "id_paciente": cliente.id_paciente,
                    "nombre": cliente.nombre_completo,
                    "dni": cliente.dni,
                    "sexo": cliente.sexo,
                    "telefono": cliente.telefono,
                    "num_consultas": num_consultas,
                    "ingresos_totales": float(ingresos),
                    "ultima_consulta": ultimo_servicio.strftime("%Y-%m-%d")
                    if ultimo_servicio
                    else None,
                    "edad": cliente.edad,
                }
            )

        return resultados

    @staticmethod
    def get_productos_vendidos(fecha_inicio=None, fecha_fin=None):
        query = (
            db.session.query(
                Producto.id_producto,
                Producto.nombre_producto,
                Marca.nombre_marca,
                func.sum(ConsumoProducto.cantidad_consumida).label("cantidad_vendida"),
                func.sum(ConsumoProducto.importe_venta).label("ventas"),
            )
            .join(ConsumoProducto)
            .join(
                ConsultaServicio,
                ConsultaServicio.id_consulta_servicio
                == ConsumoProducto.id_consulta_servicio,
            )
            .join(Consulta)
            .join(Marca)
        )

        if fecha_inicio:
            query = query.filter(Consulta.fecha_consulta >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Consulta.fecha_consulta <= fecha_fin)

        resultados = (
            query.group_by(
                Producto.id_producto, Producto.nombre_producto, Marca.nombre_marca
            )
            .order_by(func.sum(ConsumoProducto.cantidad_consumida).desc())
            .all()
        )

        return [
            {
                "id_producto": r.id_producto,
                "nombre_producto": r.nombre_producto,
                "marca": r.nombre_marca,
                "cantidad_vendida": int(r.cantidad_vendida or 0),
                "ventas": float(r.ventas or 0),
            }
            for r in resultados
        ]

    @staticmethod
    def get_servicios_populares(fecha_inicio=None, fecha_fin=None):
        query = (
            db.session.query(
                ServicioCatalogo.id_servicio,
                ServicioCatalogo.nombre_servicio,
                func.count(ConsultaServicio.id_consulta_servicio).label(
                    "veces_solicitado"
                ),
                func.sum(ConsultaServicio.precio_servicio).label("ingresos"),
            )
            .join(ConsultaServicio)
            .join(Consulta)
        )

        if fecha_inicio:
            query = query.filter(Consulta.fecha_consulta >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Consulta.fecha_consulta <= fecha_fin)

        resultados = (
            query.group_by(
                ServicioCatalogo.id_servicio, ServicioCatalogo.nombre_servicio
            )
            .order_by(func.count(ConsultaServicio.id_consulta_servicio).desc())
            .all()
        )

        return [
            {
                "id_servicio": r.id_servicio,
                "nombre_servicio": r.nombre_servicio,
                "veces_solicitado": r.veces_solicitado,
                "ingresos": float(r.ingresos or 0),
            }
            for r in resultados
        ]

    @staticmethod
    def get_tendencias(periodo_dias=30):
        fecha_fin = datetime.now().date()
        fecha_inicio = fecha_fin - timedelta(days=periodo_dias)

        ventas = AnalyticsService.get_ventas_diarias(fecha_inicio, fecha_fin)

        total_ventas_periodo = sum(v["ventas"] for v in ventas)

        fecha_anterior_inicio = fecha_inicio - timedelta(days=periodo_dias)
        fecha_anterior_fin = fecha_inicio

        ventas_anterior = AnalyticsService.get_ventas_diarias(
            fecha_anterior_inicio, fecha_anterior_fin
        )
        total_ventas_anterior = sum(v["ventas"] for v in ventas_anterior)

        cambio_porcentaje = 0
        if total_ventas_anterior > 0:
            cambio_porcentaje = (
                (total_ventas_periodo - total_ventas_anterior) / total_ventas_anterior
            ) * 100

        return {
            "periodo": f"Últimos {periodo_dias} días",
            "ventas_periodo": total_ventas_periodo,
            "ventas_periodo_anterior": total_ventas_anterior,
            "cambio_porcentaje": round(cambio_porcentaje, 2),
            "ventas_diarias": ventas,
        }

    @staticmethod
    def get_ingresos_por_medio_pago(fecha_inicio=None, fecha_fin=None):
        from app.models.medio_pago import MedioPago

        query = db.session.query(
            MedioPago.nombre_m_pago, func.sum(Pago.monto_pagado).label("total")
        ).join(Pago, Pago.id_medio_de_pago == MedioPago.id_m_pago)

        if fecha_inicio:
            query = query.filter(Pago.fecha_pago >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Pago.fecha_pago <= fecha_fin)

        resultados = query.group_by(MedioPago.nombre_m_pago).all()

        return [
            {"medio_pago": r.nombre_m_pago, "total": float(r.total or 0)}
            for r in resultados
        ]

    @staticmethod
    def get_segmentos():
        clientes = AnalyticsService.get_clientes_para_clustering()

        segmentos = {"VIP": [], "Frecuentes": [], "Ocasionales": [], "Inactivos": []}

        for cliente in clientes:
            if cliente["num_consultas"] >= 5 and cliente["ingresos_totales"] >= 5000:
                segmentos["VIP"].append(cliente)
            elif cliente["num_consultas"] >= 3:
                segmentos["Frecuentes"].append(cliente)
            elif cliente["num_consultas"] >= 1:
                segmentos["Ocasionales"].append(cliente)
            else:
                segmentos["Inactivos"].append(cliente)

        return {
            "VIP": {"count": len(segmentos["VIP"]), "clientes": segmentos["VIP"]},
            "Frecuentes": {
                "count": len(segmentos["Frecuentes"]),
                "clientes": segmentos["Frecuentes"],
            },
            "Ocasionales": {
                "count": len(segmentos["Ocasionales"]),
                "clientes": segmentos["Ocasionales"],
            },
            "Inactivos": {
                "count": len(segmentos["Inactivos"]),
                "clientes": segmentos["Inactivos"],
            },
        }
