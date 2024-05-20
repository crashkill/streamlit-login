import os
from dotenv import load_dotenv
from supabase import create_client

class SupabaseAuth:
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        # Recupera as variáveis de ambiente
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        # Inicializa o cliente Supabase
        self.client = create_client(self.supabase_url, self.supabase_key)

    def authenticate_user(self, email, password):
        # Realiza a autenticação do usuário com o e-mail e senha fornecidos
        try:
            auth = self.client.auth.sign_in_with_password({ "email": email, "password": password })
            return auth
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None
