import streamlit as st

from services.api_client import api_client

st.title("Agentes IA")
st.caption("Interfaz inicial para orquestacion LangGraph")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_payload" not in st.session_state:
    st.session_state.last_payload = None

if "agent_session_id" not in st.session_state:
    st.session_state.agent_session_id = "streamlit-default"

st.session_state.agent_session_id = st.text_input(
    "Session ID",
    value=st.session_state.agent_session_id,
    help="Identificador para conservar contexto entre mensajes.",
)

prompt = st.chat_input("Escribe una instruccion para el sistema multi-agente")
if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    result = api_client.agentes_chat(
        prompt,
        session_id=st.session_state.agent_session_id,
    )
    if result["ok"] and result["data"]:
        agent = result["data"].get("agent", "unknown")
        response = result["data"].get("response", "Sin respuesta")
        st.session_state.last_payload = result["data"].get("payload", {})
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": f"[{agent}] {response}",
            }
        )
    else:
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": f"Error: {result['message']}",
            }
        )

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        st.write(item["content"])

if st.session_state.last_payload:
    st.subheader("Payload tecnico")
    st.json(st.session_state.last_payload)
