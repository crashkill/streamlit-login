import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("💎 Operações São Paulo")
        st.write("")
        
        if st.session_state.get("logged_in", False):
            st.page_link("pages/1 🕵️ Forecast Corporativo.py", label="Forecast Corporativo", icon="🕵️")
            st.page_link("pages/2 🔒 Planilhas Financeiras.py", label="Planilhas Financeiras", icon="🔒")
            st.page_link("pages/3 💻 Faturamento de Projetos.py", label="Faturamento de Projetos", icon="💻")
            st.page_link("pages/4 🔒 DNF x FND.py", label="DNF x FND", icon="🔒")
            st.page_link("pages/5 🔒 Lista de Profissionais.py", label="Lista de Profissionais", icon="🔒")
            st.page_link("pages/6 🔒 Controle de Férias.py", label="Controle de Férias", icon="🔒")
            st.page_link("pages/7 🔨 Saldo SAP.py", label="Saldo SAP", icon="🔨")

            st.write("")
            st.write("")

            if st.button("Sair"):
                logout()

        elif get_current_page_name() != "app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("app.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("app.py")
