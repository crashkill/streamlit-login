import pandas as pd
import streamlit as st

class XlsxToDataFrame:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def read_xlsx_to_dataframe(self):
        try:
            df = pd.read_excel(self.file_name)
            return df
        except FileNotFoundError:
            st.error(f"Arquivo '{self.file_name}' não encontrado.")
            return None
        except Exception as e:
            st.error(f"Ocorreu um erro ao ler o arquivo '{self.file_name}': {e}")
            return None
    
    def sum_column_by_group_and_filter(self, df, sum_column, group_column, filter_column, filter_value):
        try:
            # Filtrando o DataFrame
            filtered_df = df[df[filter_column] == filter_value]
            
            # Somando as vendas agrupando por produto
            sum_by_group = filtered_df.groupby(group_column)[sum_column].sum()
            
            return filtered_df
        #, sum_by_group
        except Exception as e:
            st.error(f"Ocorreu um erro ao somar os valores: {e}")
            return None