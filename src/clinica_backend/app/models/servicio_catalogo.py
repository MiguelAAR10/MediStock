from app.extensions import db
from app.models.base import BaseModel


class ServicioCatalogo(BaseModel):
    __tablename__ = "servicios_catalogo"

    id_servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_servicio = db.Column(db.String(250), unique=True, nullable=False)
    precio_servicio = db.Column(db.Numeric(10, 2))

    consultas_servicios = db.relationship(
        "ConsultaServicio", back_populates="servicio", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Servicio {self.nombre_servicio}>"
