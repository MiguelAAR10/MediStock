import pandas as pd
import streamlit as st
import plotly.express as px

from services.api_client import api_client

st.title("Dashboard")

kpis_resp = api_client.get_kpis()
if not kpis_resp["ok"]:
    st.error(kpis_resp["message"])
    st.stop()

kpis = kpis_resp["data"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Pacientes", int(kpis.get("total_pacientes", 0)))
c2.metric("Consultas", int(kpis.get("total_consultas", 0)))
c3.metric("Facturas", int(kpis.get("total_facturas", 0)))
c4.metric("Ingresos", f"S/ {kpis.get('ingresos_totales', 0):,.2f}")

st.subheader("Ventas diarias")
ventas_resp = api_client.get_ventas_diarias()
if ventas_resp["ok"] and ventas_resp["data"]:
    df = pd.DataFrame(ventas_resp["data"])
    fig = px.line(df, x="fecha", y="ventas", markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay datos de ventas diarios disponibles.")
