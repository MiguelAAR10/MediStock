# src/app/models/__init__.py
"""
Este archivo convierte la carpeta 'models' en un Paquete Python.
Se usa como Fachada (Facade Pattern) para exponer los modelos
de dominio (Paciente, Distrito) y la clase base (BaseModel)
a toda la aplicación.
"""

# Importa tu clase Base que contiene los métodos de persistencia
# desde el archivo 'base.py' en el mismo directorio.
from .base import BaseModel

# Importa el Modelo Distrito desde el archivo 'distrito.py'
from .distrito import Distrito

# Importa el Modelo Paciente desde el archivo 'paciente.py'
from .paciente import Paciente

# Importa el Modelo Marca desde el archivo 'marca.py'
from .marca import Marca

# Importa el Modelo Producto desde el archivo 'producto.py'
from .producto import Producto

# Importa el Modelo ServicioCatalogo desde el archivo 'servicio_catalogo.py'
from .servicio_catalogo import ServicioCatalogo

# Importa el Modelo MedioPago desde el archivo 'medio_pago.py'
from .medio_pago import MedioPago

# Importa el Modelo Descuento desde el archivo 'descuento.py'
from .descuento import Descuento

# Importa el Modelo Consulta desde el archivo 'consulta.py'
from .consulta import Consulta

# Importa el Modelo ConsultaServicio desde el archivo 'consulta_servicio.py'
from .consulta_servicio import ConsultaServicio

# Importa el Modelo ConsumoProducto desde el archivo 'consumo_producto.py'
from .consumo_producto import ConsumoProducto

# Importa el Modelo Factura desde el archivo 'factura.py'
from .factura import Factura

# Importa el Modelo Pago desde el archivo 'pago.py'
from .pago import Pago

# Ahora, el resto de la aplicación puede hacer la importación limpia:
# from app.models import Paciente, Distrito, BaseModel, Marca, Producto, etc.
