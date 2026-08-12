import streamlit as st

from services.api_client import api_client

st.title("Pacientes")

with st.expander("Registrar paciente"):
    with st.form("crear_paciente"):
        nombre = st.text_input("Nombre completo")
        dni = st.text_input("DNI")
        sexo = st.selectbox("Sexo", ["", "F", "M"])
        telefono = st.text_input("Telefono")
        submit = st.form_submit_button("Guardar")

    if submit:
        payload = {
            "nombreCompleto": nombre,
            "dni": dni,
            "sexo": sexo if sexo else None,
            "telefono": telefono if telefono else None,
        }
        payload = {k: v for k, v in payload.items() if v is not None and v != ""}
        resp = api_client.crear_paciente(payload)
        if resp["ok"]:
            st.success("Paciente creado")
        else:
            st.error(resp["message"])

search = st.text_input("Buscar por nombre o DNI")
resp = api_client.listar_pacientes(search=search)
if not resp["ok"]:
    st.error(resp["message"])
    st.stop()

data = resp["data"] or {}
items = data.get("items", [])
st.caption(f"Total: {data.get('pagination', {}).get('total', 0)}")
st.dataframe(items, use_container_width=True)
