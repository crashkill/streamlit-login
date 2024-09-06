import streamlit as st
from navigation import make_sidebar
from financeiro import Financeiro

def main():
    st.set_page_config(page_title="Dashboard Financeiro - Operações SP & CP",
                       page_icon=":bar_chart:",
                       layout="wide")

    make_sidebar()

    st.write(
        """
        # 💻 Faturamento de Projetos
        """
    )
    st.markdown("#####")

    arquivo_DRE = "assets/DRE.xlsx"
    sheet_name = "Dados"

    financeiro = Financeiro(arquivo_DRE, sheet_name)

    # Definição dos filtros da página
    projetos = financeiro.get_projetos()
    periodos = financeiro.get_periodos()

        # Filtros para Projeto e Período
    st.markdown("### Filtros")
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        filtro_projeto = st.selectbox('Projetos', options=projetos, index=0, key="filtro_projeto")
    with coluna2:
        filtro_data = st.selectbox('Periodo', options=periodos, index=0, key="filtro_periodo")
    # Obtendo os dados para o st.date_input
    # periodos = financeiro.get_date_input_data(filtro_projeto)
    # with coluna2:
    #     if periodos:
    #         filtro_data = st.date_input("Periodo", value=periodos[0], min_value=min(periodos), max_value=max(periodos), key="filtro_periodo", format="MM-DD-YYYY")
    #     else:
    #         filtro_data = None


    # filtro_data
    # Filtrando os dados com base nos filtros selecionados
    df_filtrado = financeiro.filtrar_dados(filtro_projeto, filtro_data)

    # Calculando as métricas com base nos dados filtrados
    soma_receita = financeiro.get_valor(filtro_projeto, filtro_data)
    soma_custo = financeiro.get_valor(filtro_projeto, filtro_data, "CUSTO")
    lucro = soma_receita - soma_custo
    percentual = (soma_custo / soma_receita) * 100


    # Exibindo as métricas filtradas antes dos filtros
    st.markdown("### Métricas Filtradas")
    coluna_metrica1, coluna_metrica2, coluna_metrica3, coluna_metrica4 = st.columns(4)
    coluna_metrica1.metric("RECEITA FILTRADA", f"R$ {soma_receita:,.2f}")
    coluna_metrica2.metric("CUSTO FILTRADO", f"R$ {soma_custo:,.2f}")
    coluna_metrica3.metric("LUCRO FILTRADO", f"R$ {lucro:,.2f}")
    coluna_metrica4.metric("PERCENTUAL",  F"{percentual:.2f}%")

    st.markdown("---")

    # Exibindo o DataFrame filtrado
    st.markdown("### DataFrame Filtrado")
    st.dataframe(df_filtrado)

if __name__ == "__main__":
    main()
