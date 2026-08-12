import pandas as pd
import streamlit as st
import plotly.express as px

from services.ml_client import ml_client

st.title("Analytics IA")
tab1, tab2 = st.tabs(["Forecasting", "Segmentacion"])

with tab1:
    ventas = ml_client.get_forecasting_data()
    if ventas["ok"] and ventas["data"]:
        df = pd.DataFrame(ventas["data"])
        fig = px.line(df, x="fecha", y="ventas", markers=True, title="Serie de ventas")
        st.plotly_chart(fig, use_container_width=True)

        if len(df) >= 7:
            avg_7 = df.tail(7)["ventas"].mean()
            st.metric("Promedio 7 dias", f"S/ {avg_7:,.2f}")
    else:
        st.info("Sin datos para forecasting")

with tab2:
    segmentos = ml_client.get_segmentos()
    if segmentos["ok"] and segmentos["data"]:
        data = segmentos["data"]
        resumen = [{"segmento": k, "clientes": v.get("count", 0)} for k, v in data.items()]
        df_seg = pd.DataFrame(resumen)
        fig = px.bar(df_seg, x="segmento", y="clientes", title="Clientes por segmento")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_seg, use_container_width=True)
    else:
        st.info("Sin datos de segmentacion")
