import streamlit as st
from time import sleep
from navigation import make_sidebar
from supabase_auth import SupabaseAuth
import datetime

st.set_page_config(
    page_title="Sistema Financeiro - Globalhitss",
    page_icon=":chart_with_downwards_trend:"
)
authenticator = SupabaseAuth()

make_sidebar()

st.title("Sistema Financeiro - Globalhitss")

email = st.text_input("E-mail", placeholder="Digite seu e-mail corporativo")
password = st.text_input("Senha", type="password", placeholder="Digite uma senha")

if st.button("Logar", type="primary"):
    if email and password:
        authenticated = authenticator.authenticate_user(email, password)
        if authenticated:
            st.session_state.logged_in = True
            #st.session_state.login_expiration = expiration_time
            st.success("Logado com sucesso")
            sleep(0.5)
            st.switch_page("pages/1 🕵️ Forecast Corporativo.py")
        else:
            st.error("Credenciais inválidas. Por favor, reveja o e-mail e senha")
    else:
        st.error("Por favor, preencha o e-mail e senha")

# Verificar se o usuário ainda está logado
if 'logged_in' in st.session_state and st.session_state.logged_in:
    if datetime.datetime.now() > st.session_state.login_expiration:
        st.error("Sessão expirada. Por favor, faça o login novamente.")
        st.session_state.logged_in = False
