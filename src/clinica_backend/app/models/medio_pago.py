from app.extensions import db
from app.models.base import BaseModel


class MedioPago(BaseModel):
    __tablename__ = "medios_de_pago"

    id_m_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_m_pago = db.Column(db.String(50), unique=True, nullable=False)

    pagos = db.relationship("Pago", back_populates="medio_pago", lazy="dynamic")

    def __repr__(self):
        return f"<MedioPago {self.nombre_m_pago}>"
