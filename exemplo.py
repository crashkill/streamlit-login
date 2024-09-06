import pandas as pd
import streamlit as st

# Carregar a planilha Excel
file_path = 'assets/forecast.xlsx'
df = pd.read_excel(file_path)

# Configurar a interface Streamlit
st.title("Edição da Planilha Excel")

# Exibir a planilha no Streamlit e permitir edição dos campos "Receita" e "Custo Total"
edited_df = st.data_editor(
    df,
    use_container_width=True,
    column_config={
        "Receita": {"editable": True},
        "Custo Total": {"editable": True},
    }
)

# Atualizar os campos "Receita Bruta" e "Receita %"
if "Receita" in edited_df.columns and "Custo Total" in edited_df.columns:
    edited_df["Receita Bruta"] = edited_df["Receita"] - edited_df["Custo Total"]
    edited_df["Receita %"] = (edited_df["Receita Bruta"] / edited_df["Receita"]) * 100

# Exibir a tabela atualizada
st.write("Tabela atualizada:")
st.dataframe(edited_df)

# Salvar as alterações de volta no arquivo Excel, se necessário
save_changes = st.button("Salvar alterações")
if save_changes:
    edited_df.to_excel(file_path, index=False)
    st.write("Alterações salvas com sucesso!")
