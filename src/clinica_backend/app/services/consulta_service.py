# app/services/consulta_service.py
"""
Service Layer - Logica de Negocio para Consulta
"""

from app.extensions import db
from app.models.consulta import Consulta
from app.models.paciente import Paciente
from app.models.consulta_servicio import ConsultaServicio
from app.models.servicio_catalogo import ServicioCatalogo
from sqlalchemy.exc import IntegrityError


class ConsultaService:
    @staticmethod
    def crear_consulta(data):
        id_paciente = data.get("id_paciente")
        paciente = Paciente.query.get(id_paciente)
        if not paciente:
            raise ValueError(f"Paciente con id {id_paciente} no encontrado")

        consulta = Consulta(
            id_paciente=id_paciente,
            fecha_consulta=data.get("fecha_consulta"),
            notas_generales=data.get("notas_generales"),
            total_historico=data.get("total_historico", 0),
        )

        try:
            db.session.add(consulta)
            db.session.commit()
            return consulta
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_consulta(id_consulta):
        return Consulta.query.get(id_consulta)

    @staticmethod
    def listar_consultas(
        page=1, per_page=20, paciente_id=None, fecha_inicio=None, fecha_fin=None
    ):
        query = Consulta.query

        if paciente_id:
            query = query.filter_by(id_paciente=paciente_id)

        if fecha_inicio:
            query = query.filter(Consulta.fecha_consulta >= fecha_inicio)

        if fecha_fin:
            query = query.filter(Consulta.fecha_consulta <= fecha_fin)

        query = query.order_by(Consulta.fecha_consulta.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def agregar_servicio_consulta(id_consulta, id_servicio, precio_servicio):
        consulta = Consulta.query.get(id_consulta)
        if not consulta:
            raise ValueError("Consulta no encontrada")

        servicio = ServicioCatalogo.query.get(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        consulta_servicio = ConsultaServicio(
            id_consulta=id_consulta,
            id_servicio=id_servicio,
            precio_servicio=precio_servicio or servicio.precio_servicio,
        )

        try:
            db.session.add(consulta_servicio)
            db.session.commit()
            return consulta_servicio
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_servicios_consulta(id_consulta):
        consulta = Consulta.query.get(id_consulta)
        if not consulta:
            raise ValueError("Consulta no encontrada")

        return consulta.servicios.all()

    @staticmethod
    def actualizar_consulta(id_consulta, data):
        consulta = Consulta.query.get(id_consulta)
        if not consulta:
            raise ValueError("Consulta no encontrada")

        if "fecha_consulta" in data:
            consulta.fecha_consulta = data["fecha_consulta"]
        if "notas_generales" in data:
            consulta.notas_generales = data["notas_generales"]
        if "total_historico" in data:
            consulta.total_historico = data["total_historico"]

        try:
            db.session.commit()
            return consulta
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def eliminar_consulta(id_consulta):
        consulta = Consulta.query.get(id_consulta)
        if not consulta:
            raise ValueError("Consulta no encontrada")

        try:
            db.session.delete(consulta)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_historial_paciente(id_paciente, limit=10):
        return (
            Consulta.query.filter_by(id_paciente=id_paciente)
            .order_by(Consulta.fecha_consulta.desc())
            .limit(limit)
            .all()
        )
