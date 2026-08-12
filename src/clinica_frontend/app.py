import streamlit as st

from config import Settings
from services.api_client import api_client


st.set_page_config(
    page_title=Settings.PAGE_TITLE,
    page_icon=Settings.PAGE_ICON,
    layout=Settings.LAYOUT,
)

st.title("Clinica Prime AI")
st.caption("Plataforma operativa y analitica para ventas, pacientes e inventario")

col1, col2 = st.columns(2)
with col1:
    health = api_client.health()
    if health["ok"]:
        st.success("Backend conectado")
    else:
        st.error(f"Backend no disponible: {health['message']}")

with col2:
    kpis = api_client.get_kpis()
    if kpis["ok"] and kpis["data"]:
        st.metric("Pacientes totales", int(kpis["data"].get("total_pacientes", 0)))
    else:
        st.metric("Pacientes totales", 0)

st.markdown("""
### Modulos disponibles
- Dashboard y KPIs de negocio
- Gestion de pacientes
- Consultas clinicas
- Inventario y productos
- Facturacion y pagos
- Analytics IA (forecasting y segmentos)
- Agentes IA (orquestacion LangGraph)
""")
