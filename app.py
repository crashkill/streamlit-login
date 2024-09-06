import streamlit as st
from navigation import make_sidebar
from conection import Conection
import datetime

def main():
    st.set_page_config(
        page_title="Sistema Financeiro - Globalhitss",
        page_icon=":chart_with_downwards_trend:"
    )

    make_sidebar()
    
    # Instância da classe conection
    conection = Conection()

    # Variável para selecionar o método de autenticação
    metodo_auth = st.selectbox("Escolha o método de autenticação", ["MSAL", "Supabase"])

    # Campos de e-mail e senha (usado apenas no Supabase)
    email = st.text_input("E-mail", placeholder="Digite seu e-mail corporativo")
    password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

    if st.button("Conectar", type="primary"):
        if metodo_auth == "MSAL":
            # Autenticação usando MSAL
            authenticated, expiration_time, access_token = conection.authenticate_msal()
        elif metodo_auth == "Supabase":
            if email and password:
                # Autenticação usando Supabase
                authenticated, expiration_time, access_token = conection.authenticate_supabase(email, password)
            else:
                st.error("Por favor, preencha o e-mail e senha.")
                return
        
        if authenticated:
            st.session_state.logged_in = True
            if expiration_time:
                st.session_state.login_expiration = datetime.datetime.now() + datetime.timedelta(seconds=expiration_time)
            st.session_state.access_token = access_token
            st.success("Logado com sucesso!")
            st.switch_page("pages/1 🕵️ Forecast Corporativo.py")
        else:
            st.error("Erro ao autenticar. Por favor, tente novamente.")

    # Verificação de sessão
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        if 'login_expiration' in st.session_state and datetime.datetime.now() > st.session_state.login_expiration:
            st.error("Sessão expirada. Por favor, faça o login novamente.")
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
