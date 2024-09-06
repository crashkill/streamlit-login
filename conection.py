import msal
import os
from dotenv import load_dotenv
import supabase  # Supondo que o módulo supabase esteja instalado
import streamlit as st

class Conection:
    def __init__(self):
        # Carregar variáveis de ambiente do arquivo .env
        load_dotenv()

    def authenticate_msal(self):
        """Autenticação usando MSAL"""
        CLIENT_ID = os.getenv("CLIENT_ID")
        TENANT_ID = os.getenv("TENANT_ID")
        AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
        SCOPE = ["User.Read"]

        # Instância do MSAL
        app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

        try:
            # Inicia o fluxo de autenticação interativa
            result = app.acquire_token_interactive(scopes=SCOPE)
            if "access_token" in result:
                return True, result["expires_in"], result["access_token"]
            else:
                st.error(f"Erro ao autenticar MSAL: {result.get('error_description')}")
                return False, None, None
        except Exception as e:
            st.error(f"Erro ao autenticar MSAL: {e}")
            return False, None, None

    def authenticate_supabase(self, email, password):
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

        try:
            # Chamada para autenticar com e-mail e senha
            response = supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })

            # Verifica se a autenticação foi bem-sucedida (se o usuário existe)
            if response.user:
                access_token = response.session.access_token if response.session else None
                return True, None, access_token
            else:
                st.error("Credenciais inválidas no Supabase")
                return False, None, None
        except Exception as e:
            st.error(f"Erro ao autenticar Supabase: {e}")
            return False, None, None