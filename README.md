# 🏛️ Proyecto ETL: Clínica Prime

**Versión 1.0.0**

## 🎯 1. Resumen Ejecutivo 

Este proyecto implementa un pipeline de ETL (Extract, Transform, Load) robusto y modular, construido en Python con la librería Pandas. Su misión es ingerir, limpiar, transformar y consolidar los registros históricos de pacientes y consultas de la Clínica Prime, que actualmente residen en un archivo Excel multi-hoja con una estructura inconsistente y datos de baja calidad. El destino final de los datos limpios es una base de datos PostgreSQL relacional, sentando las bases para futuras iniciativas de Business Intelligence y análisis de negocio.

---

## 🗺️ 2. Arquitectura del Pipeline

El pipeline sigue una arquitectura ETL (Extract-Transform-Load) modular, donde la lógica de limpieza y transformación se encapsula en un taller de herramientas reutilizables (`limpieza_utils.py`) y es orquestada desde un notebook principal (`main.ipynb`).

```mermaid
graph TD;
    A[📄 Excel Crudo Múltiples Hojas] -->|1. Extracción| B 🐼 DataFrame Maestro en Pandas;
    B -->|2. Transformación en Cascada| C{⚙️ Pipeline de Limpieza};
    C -->|Lógica A| D[🔧 Estandarización de Esquema];
    C -->|Lógica B| E[🔧 Cirugía de Tipos de Datos];
    C -->|Lógica C| F[🔧 Reconstrucción de Identidades];
    C -->|Lógica D| G[🔧 Extracción de Características Notas];
    G --> H[📊 DataFrame Limpio y Consolidado];
    H -->|3. Carga| I🐘 Base de Datos PostgreSQL;
```

---

## 🛠️ 3. Stack Tecnológico

*   **Lenguaje Principal:** Python 3.10+
*   **Análisis y Manipulación de Datos:** Pandas
*   **Conectividad de Base de Datos:** SQLAlchemy, Psycopg2
*   **Base de Datos de Destino:** PostgreSQL
*   **Entorno de Desarrollo:** Jupyter Notebooks, Visual Studio Code

---

## 📂 4. Estructura del Proyecto

Un taller bien organizado es la clave para un proyecto mantenible.

```
/clinica-prime-etl-pipeline
│
├── data/
│   └── 📄 (Archivos de datos brutos y sensibles - IGNORADO POR GIT)
│
├── notebooks/
│   └── 📓 main.ipynb         # Puesto de Mando: Orquesta el pipeline completo.
│
├── src/
│   └── 🐍 limpieza_utils.py  # La Armería: Contiene todas las funciones de limpieza.
│
├── output/
│   └── 📈 (Resultados, CSVs limpios, gráficos - IGNORADO POR GIT)
│
├── .gitignore               # El Manto de Invisibilidad
└── README.md                # El Alma del Proyecto (este archivo)
```

---

## 🚀 5. Instrucciones de Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone git@github.com:TuUsuario/clinica-prime-etl-pipeline.git
    cd clinica-prime-etl-pipeline
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar las dependencias:**
    ```bash
    pip install pandas numpy sqlalchemy psycopg2-binary openpyxl
    ```
4.  **Configurar los Datos:** Colocar el archivo `clientes_work.xlsx` dentro de la carpeta `data/`.
5.  **Ejecutar el Pipeline:** Abrir `notebooks/main.ipynb` y ejecutar las celdas en orden.

---

## 🧠 6. Lógica de Negocio y Decisiones de Limpieza Clave

*   **Reconstrucción de Identidad:** Se implementó un sistema de "mapa de la verdad" para rellenar DNI y nombres de pacientes faltantes, maximizando la retención de datos.
*   **Inferencia de Contexto en 'Deuda':** Se utiliza una expresión regular con `negative lookbehind` (o una estrategia de dos pasos) para diferenciar entre la creación de una deuda y el pago de una deuda existente.
*   **Extracción de Características de 'Notas':** Se aplican `regex` para extraer datos estructurados (Unidades, Jeringas, etc.) de la columna de texto libre `notas`.

---

## 🏗️ 7. Arquitectura OLTP + OLAP + Agentes

### OLAP en PostgreSQL

Se añadió un esquema analítico en PostgreSQL bajo `olap`:

- `src/sql/olap/001_create_olap_schema.sql`: dimensiones, hechos e `ai_insights`.
- `src/sql/olap/002_refresh_olap.sql`: función `olap.refresh_olap_full()` para refresco completo.

Tablas clave:

- Dimensiones: `dim_fecha`, `dim_paciente`, `dim_servicio`, `dim_producto`, `dim_medio_pago`.
- Hechos: `fact_ventas`, `fact_servicios`, `fact_consumo_productos`.
- Insights automáticos: `ai_insights`.

### Agentes multi-nodo (LangGraph)

Nodos activos en backend:

- `analytics`: KPIs, tendencias y segmentación.
- `process`: operación e inventario.
- `reception`: consultas de atención.
- `curation`: calidad y limpieza de datos antes de OLTP.

Archivos principales:

- `src/clinica_backend/app/agents/graph.py`
- `src/clinica_backend/app/agents/nodes.py`
- `src/clinica_backend/app/agents/memory.py`
- `src/clinica_backend/app/routes/agentes.py`

### Curación previa a OLTP

La API ahora pasa por un servicio de curación para altas/actualizaciones:

- `src/clinica_backend/app/services/data_curation_service.py`
- `src/clinica_backend/app/routes/curation.py`

Endpoints:

- `POST /api/v1/curation/paciente-preview`
- `POST /api/v1/curation/consulta-preview`
- `GET /api/v1/curation/quality`

### Automatización con cron

Se incluye ciclo automático de refresco OLAP + captura de insights:

- Script: `src/jobs/run_olap_cycle.py`
- Cron template: `ops/cron/clinica_prime.cron`

También disponible endpoint manual:

- `POST /api/v1/olap/run-cycle`
