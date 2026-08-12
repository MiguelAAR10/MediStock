# app/__init__.py
from flask import Flask
from app.config import config

# Importamos desde extensiones (NO CREAR AQUÍ)
from app.extensions import db, migrate, ma, cors


def create_app(config_name="default"):
    app = Flask(__name__)

    # 1. Configuración
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 2. Inicializar Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)

    # 3. Registrar Rutas
    try:
        from app.routes.health import health_bp

        app.register_blueprint(health_bp, url_prefix="/api")

        from app.routes.pacientes import pacientes_bp

        app.register_blueprint(pacientes_bp, url_prefix="/api/v1")

        from app.routes.consultas import consultas_bp

        app.register_blueprint(consultas_bp, url_prefix="/api/v1")

        from app.routes.facturas import facturas_bp

        app.register_blueprint(facturas_bp, url_prefix="/api/v1")

        from app.routes.pagos import pagos_bp

        app.register_blueprint(pagos_bp, url_prefix="/api/v1")

        from app.routes.productos import productos_bp

        app.register_blueprint(productos_bp, url_prefix="/api/v1")

        from app.routes.servicios import servicios_bp

        app.register_blueprint(servicios_bp, url_prefix="/api/v1")

        from app.routes.marcas import marcas_bp

        app.register_blueprint(marcas_bp, url_prefix="/api/v1")

        from app.routes.distritos import distritos_bp

        app.register_blueprint(distritos_bp, url_prefix="/api/v1")

        from app.routes.medios_pago import medios_pago_bp

        app.register_blueprint(medios_pago_bp, url_prefix="/api/v1")

        from app.routes.descuentos import descuentos_bp

        app.register_blueprint(descuentos_bp, url_prefix="/api/v1")

        from app.routes.analytics import analytics_bp

        app.register_blueprint(analytics_bp, url_prefix="/api/v1")

        from app.routes.agentes import agentes_bp

        app.register_blueprint(agentes_bp, url_prefix="/api/v1")

        from app.routes.olap import olap_bp

        app.register_blueprint(olap_bp, url_prefix="/api/v1")

        from app.routes.curation import curation_bp

        app.register_blueprint(curation_bp, url_prefix="/api/v1")

    except Exception as e:
        print(f"⚠️ Error cargando rutas: {e}")

    # ¡¡¡ AQUÍ NO DEBE HABER NADA MÁS !!!
    # NADA DE app.schemas = ...
    # NADA DE import schemas...

    return app
