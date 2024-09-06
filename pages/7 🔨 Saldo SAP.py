import streamlit as st
import pandas as pd
#from sap_connection import SAPConnection
from navigation import make_sidebar

# Configurações da página
st.set_page_config(page_title="Dashboard Financeiro - Operações SP & CP",
                   page_icon=":bar_chart:",
                   layout="wide")

# Definição do caminho para o arquivo Excel
arquivo_DRE = "assets/DRE.xlsx"

# Criação da barra lateral usando a função make_sidebar
make_sidebar()

# Título da página
st.write(
    """
# 🔨 Saldos SAP
"""
)

# Seção para teste de conexão SAP
st.header("Teste de Conexão SAP")

# Informações da conexão SAP
server = "brux1500"
username = "93186667"
password = "Y#YueN5kPSyV"

# Criação da instância da classe SAPConnection
sap_conn = SAPConnection(server, username, password)
sap_conn.connect()

# Parâmetros para a função RFC
parameters = {
    'PARAM1': 'value1',
    'PARAM2': 'value2'
}

# Execução da função RFC e exibição do resultado
result = sap_conn.execute('RFC_FUNCTION_NAME', parameters)
if result:
    st.write(result)  # Exibe o resultado no Streamlit

# Desconexão do servidor SAP
sap_conn.disconnect()

# Seção para exibir dados do arquivo Excel
st.header("Dados do DRE")

# Leitura dos dados do arquivo Excel usando pandas
try:
    df = pd.read_excel(arquivo_DRE)
    st.write(df)  # Exibe os dados no Streamlit
except FileNotFoundError:
    st.error(f"Arquivo {arquivo_DRE} não encontrado.")
except Exception as e:
    st.error(f"Ocorreu um erro ao ler o arquivo: {e}")
