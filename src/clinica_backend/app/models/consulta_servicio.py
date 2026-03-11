from app.extensions import db
from app.models.base import BaseModel


class ConsultaServicio(BaseModel):
    __tablename__ = "consultas_servicios"

    id_consulta_servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(
        db.Integer, db.ForeignKey("consultas.id_consulta"), nullable=False
    )
    id_servicio = db.Column(
        db.Integer, db.ForeignKey("servicios_catalogo.id_servicio"), nullable=False
    )
    precio_servicio = db.Column(db.Numeric(10, 2))

    consulta = db.relationship("Consulta", back_populates="servicios")
    servicio = db.relationship("ServicioCatalogo", back_populates="consultas_servicios")
    consumos = db.relationship(
        "ConsumoProducto",
        back_populates="consulta_servicio",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<ConsultaServicio {self.id_consulta_servicio}>"

    @property
    def total_productos(self):
        total = 0
        for consumo in self.consumos:
            total += float(consumo.importe_venta or 0)
        return total

    @property
    def total(self):
        precio = float(self.precio_servicio or 0)
        return precio + self.total_productos

    def to_dictCompleto(self):
        data = self.to_dict()
        data["servicio"] = (
            {
                "id_servicio": self.servicio.id_servicio,
                "nombre_servicio": self.servicio.nombre_servicio,
                "precio_servicio": float(self.servicio.precio_servicio or 0),
            }
            if self.servicio
            else None
        )
        data["consumos"] = [c.to_dict() for c in self.consumos]
        data["total_productos"] = self.total_productos
        data["total"] = self.total
        return data
