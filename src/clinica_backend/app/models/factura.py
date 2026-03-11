from app.extensions import db
from app.models.base import BaseModel
from datetime import datetime
import pytz


class Factura(BaseModel):
    __tablename__ = "facturas"

    id_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(
        db.Integer, db.ForeignKey("consultas.id_consulta"), nullable=False, unique=True
    )
    fecha_emision = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(pytz.timezone("America/Lima")),
    )
    total_bruto = db.Column(db.Numeric(12, 2), nullable=False)
    id_descuento = db.Column(db.Integer, db.ForeignKey("descuentos.id_descuento"))
    monto_descuento = db.Column(db.Numeric(12, 2), default=0)
    total_neto = db.Column(db.Numeric(12, 2), nullable=False)
    total_historico = db.Column(db.Numeric(12, 2), nullable=False)

    consulta = db.relationship("Consulta", back_populates="factura")
    descuento = db.relationship("Descuento", back_populates="facturas")
    pagos = db.relationship(
        "Pago", back_populates="factura", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Factura {self.id_factura}>"

    @property
    def saldo_pendiente(self):
        total_pagado = sum(float(p.monto_pagado or 0) for p in self.pagos)
        return float(self.total_neto) - total_pagado

    @property
    def esta_pagada(self):
        return self.saldo_pendiente <= 0

    @property
    def pagos_count(self):
        return self.pagos.count()

    def to_dictCompleto(self):
        data = self.to_dict()
        data["paciente"] = (
            {
                "id_paciente": self.consulta.paciente.id_paciente,
                "nombre_completo": self.consulta.paciente.nombre_completo,
                "dni": self.consulta.paciente.dni,
            }
            if self.consulta and self.consulta.paciente
            else None
        )
        data["fecha_consulta"] = (
            self.consulta.fecha_consulta.strftime("%Y-%m-%d") if self.consulta else None
        )
        data["fecha_emision"] = (
            self.fecha_emision.strftime("%Y-%m-%d %H:%M")
            if self.fecha_emision
            else None
        )
        data["saldo_pendiente"] = self.saldo_pendiente
        data["esta_pagada"] = self.esta_pagada
        data["pagos_count"] = self.pagos_count
        data["descuento_info"] = (
            {
                "codigo": self.descuento.codigo_descuento,
                "monto": float(self.monto_descuento or 0),
            }
            if self.descuento
            else None
        )
        return data
