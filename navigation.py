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
            st.page_link("pages/1 🔒 Planilhas Financeiras.py", label="Planilhas Financeiras", icon="🔒")
            st.page_link("pages/2 🕵️ Forecast Corporativo.py", label="Forecast Corporativo", icon="🕵️")

            st.write("")
            st.write("")

            if st.button("Sair"):
                logout()

        elif get_current_page_name() != "home":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("home.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("home.py")
