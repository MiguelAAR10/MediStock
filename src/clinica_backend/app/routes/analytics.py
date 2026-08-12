# app/routes/analytics.py
from flask import Blueprint, request
from app.services.analytics_service import AnalyticsService
from app.utils.response import APIResponse

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics/ventas-diarias", methods=["GET"])
def get_ventas_diarias():
    try:
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        ventas = AnalyticsService.get_ventas_diarias(fecha_inicio, fecha_fin)
        return APIResponse.success(data=ventas)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/ventas-mensuales", methods=["GET"])
def get_ventas_mensuales():
    try:
        año = request.args.get("año", None, type=int)

        ventas = AnalyticsService.get_ventas_mensuales(año)
        return APIResponse.success(data=ventas)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/kpis", methods=["GET"])
def get_kpis():
    try:
        kpis = AnalyticsService.get_kpis()
        return APIResponse.success(data=kpis)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/clientes", methods=["GET"])
def get_clientes():
    try:
        clientes = AnalyticsService.get_clientes_para_clustering()
        return APIResponse.success(data=clientes)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/productos", methods=["GET"])
def get_productos():
    try:
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        productos = AnalyticsService.get_productos_vendidos(fecha_inicio, fecha_fin)
        return APIResponse.success(data=productos)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/servicios-populares", methods=["GET"])
def get_servicios_populares():
    try:
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        servicios = AnalyticsService.get_servicios_populares(fecha_inicio, fecha_fin)
        return APIResponse.success(data=servicios)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/tendencias", methods=["GET"])
def get_tendencias():
    try:
        periodo_dias = request.args.get("periodo_dias", 30, type=int)

        tendencias = AnalyticsService.get_tendencias(periodo_dias)
        return APIResponse.success(data=tendencias)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/segmentos", methods=["GET"])
def get_segmentos():
    try:
        segmentos = AnalyticsService.get_segmentos()
        return APIResponse.success(data=segmentos)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)


@analytics_bp.route("/analytics/ingresos-medio-pago", methods=["GET"])
def get_ingresos_medio_pago():
    try:
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        ingresos = AnalyticsService.get_ingresos_por_medio_pago(fecha_inicio, fecha_fin)
        return APIResponse.success(data=ingresos)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
