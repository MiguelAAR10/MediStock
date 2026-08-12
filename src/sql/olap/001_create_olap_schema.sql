CREATE SCHEMA IF NOT EXISTS olap;

CREATE TABLE IF NOT EXISTS olap.dim_fecha (
    fecha_key INTEGER PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    semana INTEGER NOT NULL,
    dia_semana VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS olap.dim_paciente (
    paciente_key BIGSERIAL PRIMARY KEY,
    id_paciente_oltp BIGINT UNIQUE NOT NULL,
    dni VARCHAR(20),
    nombre_completo VARCHAR(255),
    sexo VARCHAR(10),
    distrito VARCHAR(80),
    paciente_problematico BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS olap.dim_servicio (
    servicio_key BIGSERIAL PRIMARY KEY,
    id_servicio_oltp BIGINT UNIQUE NOT NULL,
    nombre_servicio VARCHAR(250) NOT NULL
);

CREATE TABLE IF NOT EXISTS olap.dim_producto (
    producto_key BIGSERIAL PRIMARY KEY,
    id_producto_oltp BIGINT UNIQUE NOT NULL,
    nombre_producto VARCHAR(150) NOT NULL,
    marca VARCHAR(150),
    unidad_de_medida VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS olap.dim_medio_pago (
    medio_pago_key BIGSERIAL PRIMARY KEY,
    id_medio_pago_oltp BIGINT UNIQUE NOT NULL,
    nombre_medio_pago VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS olap.fact_ventas (
    fact_venta_key BIGSERIAL PRIMARY KEY,
    fecha_key INTEGER NOT NULL REFERENCES olap.dim_fecha(fecha_key),
    paciente_key BIGINT NOT NULL REFERENCES olap.dim_paciente(paciente_key),
    factura_id_oltp BIGINT NOT NULL,
    total_bruto NUMERIC(12, 2) NOT NULL,
    monto_descuento NUMERIC(12, 2) NOT NULL DEFAULT 0,
    total_neto NUMERIC(12, 2) NOT NULL,
    total_pagado NUMERIC(12, 2) NOT NULL DEFAULT 0,
    saldo_pendiente NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_fact_ventas_fecha_key ON olap.fact_ventas(fecha_key);
CREATE INDEX IF NOT EXISTS ix_fact_ventas_paciente_key ON olap.fact_ventas(paciente_key);

CREATE TABLE IF NOT EXISTS olap.fact_servicios (
    fact_servicio_key BIGSERIAL PRIMARY KEY,
    fecha_key INTEGER NOT NULL REFERENCES olap.dim_fecha(fecha_key),
    paciente_key BIGINT NOT NULL REFERENCES olap.dim_paciente(paciente_key),
    servicio_key BIGINT NOT NULL REFERENCES olap.dim_servicio(servicio_key),
    consulta_servicio_id_oltp BIGINT NOT NULL,
    precio_servicio NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS olap.fact_consumo_productos (
    fact_consumo_key BIGSERIAL PRIMARY KEY,
    fecha_key INTEGER NOT NULL REFERENCES olap.dim_fecha(fecha_key),
    paciente_key BIGINT NOT NULL REFERENCES olap.dim_paciente(paciente_key),
    producto_key BIGINT NOT NULL REFERENCES olap.dim_producto(producto_key),
    consumo_id_oltp BIGINT NOT NULL,
    cantidad_consumida NUMERIC(12, 2) NOT NULL,
    precio_producto NUMERIC(12, 2) NOT NULL,
    importe_venta NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS olap.ai_insights (
    insight_id BIGSERIAL PRIMARY KEY,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_agent VARCHAR(40) NOT NULL,
    insight_title VARCHAR(255) NOT NULL,
    insight_body TEXT NOT NULL,
    payload JSONB,
    severity VARCHAR(20) NOT NULL DEFAULT 'info'
);

CREATE INDEX IF NOT EXISTS ix_ai_insights_generated_at ON olap.ai_insights(generated_at DESC);
