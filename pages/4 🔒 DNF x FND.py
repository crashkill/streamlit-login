import streamlit as st
from navigation import make_sidebar
import pandas as pd
import numpy as np
import locale

st.set_page_config(page_title="Dashboard Financeiro - Operações SP & CP",
                   page_icon=":bar_chart:",
                   layout="wide")

arquivo_DRE = "assets/DRE.xlsx"

make_sidebar()

st.write(
    """
# 🔓 Planilhas Financeiras
"""
)
@st.cache_data
def importExcel(filename, sheet_name):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    return df

# Definição de Filtros
st.markdown("###")

# Filro de Projeto usando Multiselect

df = importExcel(arquivo_DRE, "Dados")

# Conversão de dados

# Filtrando o relatorio 
df = df.loc[df["Relatorio"] == "Realizado"]

df["Periodo"] = pd.to_datetime(df["Periodo"], format="mixed")

df['Mes_Ano'] = df['Periodo'].dt.strftime('%B-%Y')

# Extrair o ano da coluna 'Periodo'
df['Ano'] = df['Periodo'].dt.year

# Adicionar uma coluna com o nome do mês
df['Mes'] = df['Periodo'].dt.strftime('%B')

# Adicionar uma coluna com o nome do mês em português
meses_ingles_portugues = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

df['Mes'] = df['Periodo'].dt.strftime('%B').map(meses_ingles_portugues)

# Ordenar os dados pelo nome do mês em português
meses_ordenados = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
df['Mes'] = pd.Categorical(df['Mes'], categories=meses_ordenados, ordered=True)
df = df.sort_values(by='Mes')

# filtro_projeto = ''

# filtro_projeto = filtro_projeto.applymap(lambda x: f'R$ {locale.format_string("%.0f", x, grouping=True)}' if not pd.isna(x) else '')
# # Filtrando a série
# if filtro_projeto == '':
#     pivotado = df.pivot_table(index=['CodigoProjeto', 'Natureza'], columns=['Ano', 'Mes'], values='Lancamento', aggfunc='sum', observed=False)
# else:
#     filtro_projeto = pivotado.loc[('NSPCLA1230',), :]

pivotado = df.pivot_table(index=['CodigoProjeto', 'Natureza'], columns=['Ano', 'Mes'], values='Lancamento', aggfunc='sum', observed=False)

# Lista de códigos de projeto
lista_codigos_projeto = []

# Filtro pelos projetos da lista, ou todos se a lista estiver vazia
if lista_codigos_projeto and all(p in pivotado.index.get_level_values(0) for p in lista_codigos_projeto):
    filtro_projeto = pivotado.loc[lista_codigos_projeto]
else:
    filtro_projeto = pivotado

# Converter os valores para Reais (R$) formatados
filtro_projeto = filtro_projeto.map(lambda x: f'R$ {locale.format_string("%.0f", x, grouping=True)}' if not pd.isna(x) else '')


# Pivotar o DataFrame

filtro_projeto

# df_projeto = df['CodigoProjeto'].value_counts().index
# df_projeto

# edited_df = st.data_editor(importExcel('assets/DRE.xlsx', 'Dados'), hide_index=True, disabled=True)
