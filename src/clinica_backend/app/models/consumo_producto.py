from app.extensions import db
from app.models.base import BaseModel


class ConsumoProducto(BaseModel):
    __tablename__ = "consumo_productos"

    id_consumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta_servicio = db.Column(
        db.Integer,
        db.ForeignKey("consultas_servicios.id_consulta_servicio"),
        nullable=False,
    )
    id_producto = db.Column(
        db.Integer, db.ForeignKey("productos_catalogo.id_producto"), nullable=False
    )
    cantidad_consumida = db.Column(db.Integer, default=1, nullable=False)
    precio_producto = db.Column(db.Numeric(10, 2), nullable=False)
    importe_venta = db.Column(db.Numeric(10, 2))

    consulta_servicio = db.relationship("ConsultaServicio", back_populates="consumos")
    producto = db.relationship("Producto", back_populates="consumos")

    def __repr__(self):
        return f"<ConsumoProducto {self.id_consumo}>"

    def to_dictCompleto(self):
        data = self.to_dict()
        data["producto"] = (
            {
                "id_producto": self.producto.id_producto,
                "nombre_producto": self.producto.nombre_producto,
                "marca": self.producto.marca.nombre_marca
                if self.producto.marca
                else None,
            }
            if self.producto
            else None
        )
        return data
