from app.extensions import db
from app.models.base import BaseModel
from datetime import datetime
import pytz


class Pago(BaseModel):
    __tablename__ = "pagos"

    id_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura = db.Column(
        db.Integer, db.ForeignKey("facturas.id_factura"), nullable=False
    )
    fecha_pago = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(pytz.timezone("America/Lima")),
    )
    id_medio_de_pago = db.Column(
        db.Integer, db.ForeignKey("medios_de_pago.id_m_pago"), nullable=False
    )
    monto_pagado = db.Column(db.Numeric(12, 2), nullable=False)

    factura = db.relationship("Factura", back_populates="pagos")
    medio_pago = db.relationship("MedioPago", back_populates="pagos")

    def __repr__(self):
        return f"<Pago {self.id_pago} - Factura {self.id_factura}>"

    def to_dictCompleto(self):
        data = self.to_dict()
        data["medio_pago"] = (
            {
                "id_m_pago": self.medio_pago.id_m_pago,
                "nombre_m_pago": self.medio_pago.nombre_m_pago,
            }
            if self.medio_pago
            else None
        )
        data["fecha_pago"] = (
            self.fecha_pago.strftime("%Y-%m-%d %H:%M") if self.fecha_pago else None
        )
        return data
