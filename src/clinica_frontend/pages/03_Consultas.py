import streamlit as st

from services.api_client import api_client

st.title("Consultas")

with st.expander("Registrar consulta"):
    with st.form("crear_consulta"):
        id_paciente = st.number_input("ID paciente", min_value=1, step=1)
        fecha = st.date_input("Fecha consulta")
        notas = st.text_area("Notas")
        total_historico = st.number_input("Total historico", min_value=0.0, step=10.0)
        submit = st.form_submit_button("Guardar")

    if submit:
        payload = {
            "id_paciente": int(id_paciente),
            "fecha_consulta": str(fecha),
            "notas_generales": notas,
            "total_historico": total_historico,
        }
        resp = api_client.crear_consulta(payload)
        if resp["ok"]:
            st.success("Consulta registrada")
        else:
            st.error(resp["message"])

resp = api_client.listar_consultas()
if resp["ok"]:
    data = resp["data"] or {}
    st.dataframe(data.get("items", []), use_container_width=True)
else:
    st.error(resp["message"])
