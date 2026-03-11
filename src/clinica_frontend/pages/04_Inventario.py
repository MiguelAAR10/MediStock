import streamlit as st

from services.api_client import api_client

st.title("Inventario")
search = st.text_input("Buscar producto")
resp = api_client.listar_productos(search=search)
if resp["ok"]:
    data = resp["data"] or {}
    st.dataframe(data.get("items", []), use_container_width=True)
else:
    st.error(resp["message"])
