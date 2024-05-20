from navigation import make_sidebar
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Financeiro - Operações SP & CP",
                   page_icon=":bar_chart:",
                   layout="wide")

make_sidebar()

st.write(
    """
# 🕵️ Forecast Corporativo
"""
)

# Definição de Filtros
st.markdown("###")

arquivo_forecast = pd.read_excel("assets/BaseFCT.xlsx")

arquivo_forecast