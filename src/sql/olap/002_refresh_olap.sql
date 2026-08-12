CREATE OR REPLACE FUNCTION olap.refresh_olap_full()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO olap.dim_fecha (fecha_key, fecha, anio, mes, dia, trimestre, semana, dia_semana)
    SELECT DISTINCT
        TO_CHAR(c.fecha_consulta, 'YYYYMMDD')::INTEGER AS fecha_key,
        c.fecha_consulta,
        EXTRACT(YEAR FROM c.fecha_consulta)::INTEGER,
        EXTRACT(MONTH FROM c.fecha_consulta)::INTEGER,
        EXTRACT(DAY FROM c.fecha_consulta)::INTEGER,
        EXTRACT(QUARTER FROM c.fecha_consulta)::INTEGER,
        EXTRACT(WEEK FROM c.fecha_consulta)::INTEGER,
        TO_CHAR(c.fecha_consulta, 'Day')
    FROM consultas c
    ON CONFLICT (fecha_key) DO NOTHING;

    INSERT INTO olap.dim_paciente (id_paciente_oltp, dni, nombre_completo, sexo, distrito, paciente_problematico)
    SELECT
        p.id_paciente,
        p.dni,
        p.nombre_completo,
        p.sexo,
        d.nombre_distrito,
        p.paciente_problematico
    FROM pacientes p
    LEFT JOIN distritos d ON d.id_distrito = p.id_distrito
    ON CONFLICT (id_paciente_oltp)
    DO UPDATE SET
        dni = EXCLUDED.dni,
        nombre_completo = EXCLUDED.nombre_completo,
        sexo = EXCLUDED.sexo,
        distrito = EXCLUDED.distrito,
        paciente_problematico = EXCLUDED.paciente_problematico;

    INSERT INTO olap.dim_servicio (id_servicio_oltp, nombre_servicio)
    SELECT s.id_servicio, s.nombre_servicio
    FROM servicios_catalogo s
    ON CONFLICT (id_servicio_oltp)
    DO UPDATE SET nombre_servicio = EXCLUDED.nombre_servicio;

    INSERT INTO olap.dim_producto (id_producto_oltp, nombre_producto, marca, unidad_de_medida)
    SELECT
        p.id_producto,
        p.nombre_producto,
        m.nombre_marca,
        p.unidad_de_medida
    FROM productos_catalogo p
    LEFT JOIN marcas_catalogo m ON m.id_marca = p.id_marca
    ON CONFLICT (id_producto_oltp)
    DO UPDATE SET
        nombre_producto = EXCLUDED.nombre_producto,
        marca = EXCLUDED.marca,
        unidad_de_medida = EXCLUDED.unidad_de_medida;

    INSERT INTO olap.dim_medio_pago (id_medio_pago_oltp, nombre_medio_pago)
    SELECT mp.id_m_pago, mp.nombre_m_pago
    FROM medios_de_pago mp
    ON CONFLICT (id_medio_pago_oltp)
    DO UPDATE SET nombre_medio_pago = EXCLUDED.nombre_medio_pago;

    TRUNCATE TABLE olap.fact_ventas, olap.fact_servicios, olap.fact_consumo_productos RESTART IDENTITY;

    INSERT INTO olap.fact_ventas (
        fecha_key,
        paciente_key,
        factura_id_oltp,
        total_bruto,
        monto_descuento,
        total_neto,
        total_pagado,
        saldo_pendiente
    )
    SELECT
        TO_CHAR(c.fecha_consulta, 'YYYYMMDD')::INTEGER AS fecha_key,
        dp.paciente_key,
        f.id_factura,
        f.total_bruto,
        COALESCE(f.monto_descuento, 0),
        f.total_neto,
        COALESCE(SUM(pg.monto_pagado), 0) AS total_pagado,
        f.total_neto - COALESCE(SUM(pg.monto_pagado), 0) AS saldo_pendiente
    FROM facturas f
    JOIN consultas c ON c.id_consulta = f.id_consulta
    JOIN olap.dim_paciente dp ON dp.id_paciente_oltp = c.id_paciente
    LEFT JOIN pagos pg ON pg.id_factura = f.id_factura
    GROUP BY
        c.fecha_consulta,
        dp.paciente_key,
        f.id_factura,
        f.total_bruto,
        f.monto_descuento,
        f.total_neto;

    INSERT INTO olap.fact_servicios (
        fecha_key,
        paciente_key,
        servicio_key,
        consulta_servicio_id_oltp,
        precio_servicio
    )
    SELECT
        TO_CHAR(c.fecha_consulta, 'YYYYMMDD')::INTEGER AS fecha_key,
        dp.paciente_key,
        ds.servicio_key,
        cs.id_consulta_servicio,
        COALESCE(cs.precio_servicio, 0)
    FROM consultas_servicios cs
    JOIN consultas c ON c.id_consulta = cs.id_consulta
    JOIN olap.dim_paciente dp ON dp.id_paciente_oltp = c.id_paciente
    JOIN olap.dim_servicio ds ON ds.id_servicio_oltp = cs.id_servicio;

    INSERT INTO olap.fact_consumo_productos (
        fecha_key,
        paciente_key,
        producto_key,
        consumo_id_oltp,
        cantidad_consumida,
        precio_producto,
        importe_venta
    )
    SELECT
        TO_CHAR(c.fecha_consulta, 'YYYYMMDD')::INTEGER AS fecha_key,
        dp.paciente_key,
        dpr.producto_key,
        cp.id_consumo,
        COALESCE(cp.cantidad_consumida, 0),
        COALESCE(cp.precio_producto, 0),
        COALESCE(cp.importe_venta, 0)
    FROM consumo_productos cp
    JOIN consultas_servicios cs ON cs.id_consulta_servicio = cp.id_consulta_servicio
    JOIN consultas c ON c.id_consulta = cs.id_consulta
    JOIN olap.dim_paciente dp ON dp.id_paciente_oltp = c.id_paciente
    JOIN olap.dim_producto dpr ON dpr.id_producto_oltp = cp.id_producto;
END;
$$;
