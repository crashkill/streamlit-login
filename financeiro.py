import pandas as pd
from Helper import import_excel

class Financeiro:
    def __init__(self, arquivo, sheet_name):
        self.df = import_excel(arquivo, sheet_name)
        self.df_realizado = self.df.loc[self.df["Relatorio"] == "Realizado"]
        self.df_realizado["Lancamento"] = pd.to_numeric(self.df_realizado["Lancamento"], errors='coerce')

    def get_valor(self, projeto="Todos", periodo="Todos", natureza="RECEITA"):
        df_filtrado = self.filtrar_dados(projeto, periodo)
        df_valor = df_filtrado.loc[df_filtrado["Natureza"] == natureza]
        return df_valor["Lancamento"].sum()

    def filtrar_dados(self, projeto="Todos", periodo="Todos"):
        df_filtrado = self.df_realizado.copy()
        if projeto != "Todos":
            df_filtrado = df_filtrado.loc[df_filtrado["Projeto"] == projeto]
        if periodo != "Todos":
            df_filtrado = df_filtrado.loc[df_filtrado["Periodo"] == periodo]
        return df_filtrado

    def get_projetos(self):
        return ["Todos"] + list(self.df_realizado["Projeto"].unique())

    def get_periodos(self, projeto="Todos"):
        if projeto == "Todos":
            return ["Todos"] + sorted(self.df_realizado["Periodo"].unique(), reverse=True)
        else:
            return ["Todos"] + sorted(self.df_realizado[self.df_realizado["Projeto"] == projeto]["Periodo"].unique(), reverse=True)
        
    def get_date_input_data(self, projeto="Todos"):
        if projeto == "Todos":
            date_list = sorted(pd.to_datetime(self.df_realizado["Periodo"].unique()), reverse=True)
        else:
            date_list = sorted(pd.to_datetime(self.df_realizado[self.df_realizado["Projeto"] == projeto]["Periodo"].unique()), reverse=True)
        return date_list
