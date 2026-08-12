import streamlit as st

from services.api_client import api_client

st.title("Facturacion")
resp = api_client.listar_facturas()
if resp["ok"]:
    data = resp["data"] or {}
    st.dataframe(data.get("items", []), use_container_width=True)
else:
    st.error(resp["message"])
