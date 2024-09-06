import streamlit as st
from navigation import make_sidebar
import msal
import os
import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Sistema Financeiro - Globalhitss",
    page_icon=":chart_with_downwards_trend:"
)

# Configurações de MSAL
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]

# Instância do MSAL
app = msal.PublicClientApplication(
    CLIENT_ID,
    authority=AUTHORITY
)

def authenticate_user_interactive():
    try:
        # Inicia o fluxo de autenticação interativa
        result = app.acquire_token_interactive(
            scopes=SCOPE
        )
        if "access_token" in result:
            return True, result["expires_in"], result["access_token"]
        else:
            st.error(f"Erro ao autenticar: {result.get('error_description')}")
            return False, None, None
    except Exception as e:
        st.error(f"Erro ao autenticar: {e}")
        return False, None, None

# Exibir a barra lateral de navegação
make_sidebar()

st.title("Sistema Financeiro - Globalhitss")

# Campos de e-mail e senha (apenas para exibição)
email = st.text_input("E-mail", placeholder="Digite seu e-mail corporativo")
password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

if st.button("Conectar", type="primary"):
    if email and password:
        # Chama a autenticação interativa (não usa e-mail e senha diretamente)
        authenticated, expiration_time, access_token = authenticate_user_interactive()
        if authenticated:
            st.session_state.logged_in = True
            st.session_state.login_expiration = datetime.datetime.now() + datetime.timedelta(seconds=expiration_time)
            st.session_state.access_token = access_token  # Armazena o token de acesso na sessão
            st.success("Logado com sucesso!")
            st.experimental_rerun()  # Atualize a página para refletir o estado logado
        else:
            st.error("Erro ao autenticar. Por favor, tente novamente.")
    else:
        st.error("Por favor, preencha o e-mail e senha.")

# Verificar se o usuário ainda está logado
if 'logged_in' in st.session_state and st.session_state.logged_in:
    if datetime.datetime.now() > st.session_state.login_expiration:
        st.error("Sessão expirada. Por favor, faça o login novamente.")
        st.session_state.logged_in = False
        st.experimental_rerun()  # Atualize a página para refletir o estado deslogado
