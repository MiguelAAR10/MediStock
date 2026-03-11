from app.extensions import db
from app.models.base import BaseModel


class Descuento(BaseModel):
    __tablename__ = "descuentos"

    id_descuento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_descuento = db.Column(db.String(50), unique=True, nullable=False)
    tipo_descuento = db.Column(db.String(10), nullable=False)
    valor = db.Column(db.Numeric(5, 2), nullable=False)

    facturas = db.relationship("Factura", back_populates="descuento", lazy="dynamic")

    def __repr__(self):
        return f"<Descuento {self.codigo_descuento}>"
