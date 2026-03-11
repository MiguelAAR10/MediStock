from app.extensions import db
from app.models.base import BaseModel


class Consulta(BaseModel):
    __tablename__ = "consultas"

    id_consulta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(
        db.Integer, db.ForeignKey("pacientes.id_paciente"), nullable=False
    )
    fecha_consulta = db.Column(db.Date, nullable=False)
    notas_generales = db.Column(db.Text)
    total_historico = db.Column(db.Numeric(10, 2), default=0)

    paciente = db.relationship("Paciente", back_populates="consultas")
    servicios = db.relationship(
        "ConsultaServicio",
        back_populates="consulta",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    factura = db.relationship("Factura", back_populates="consulta", uselist=False)

    def __repr__(self):
        return f"<Consulta {self.id_consulta} - Paciente {self.id_paciente}>"

    @property
    def fecha_consulta_formatted(self):
        if self.fecha_consulta:
            return self.fecha_consulta.strftime("%Y-%m-%d")
        return None

    def to_dictCompleto(self):
        data = self.to_dict()
        data["paciente"] = (
            {
                "id_paciente": self.paciente.id_paciente,
                "nombre_completo": self.paciente.nombre_completo,
                "dni": self.paciente.dni,
            }
            if self.paciente
            else None
        )
        data["fecha_consulta_formatted"] = self.fecha_consulta_formatted
        data["servicios_count"] = self.servicios.count() if self.servicios else 0
        data["has_factura"] = self.factura is not None
        return data
