
import pandas as pd

def Trata_Dataframe(df):
        # Filtrar os dados para o ano de 2024 e para Relatorio = Forecast
        df_2024 = df[(df['Ano'] == 2024) & (df['Relatorio'] == 'Forecast')]

        # Pivot table para agrupar dados por CodigoProjeto e Periodo
        pivot_df = df_2024.pivot_table(index=['CodigoProjeto', 'Periodo', 'Mes'], 
                                    columns='Natureza', 
                                    values='Lançamento', 
                                    aggfunc='sum').reset_index()

        # Substituir NaN por 0 para cálculos
        pivot_df = pivot_df.fillna(0)

        # Calcular a margem bruta
        pivot_df['Margem Bruta'] = pivot_df['Receita'] + pivot_df['Custo Total']

        # Calcular a porcentagem entre Margem Bruta e Receita
        pivot_df['Margem %'] = pivot_df.apply(lambda row: row['Margem Bruta'] / row['Receita'] if row['Receita'] != 0 else 0, axis=1)

        # Reformatar os dados para exibição em linhas
        pivot_df_melted = pivot_df.melt(id_vars=['CodigoProjeto', 'Periodo', 'Mes'], 
                                        value_vars=['Receita', 'Custo Total', 'Margem Bruta', 'Margem %'],
                                        var_name='Tipo', value_name='Valor')

        # Ordenar os tipos de dados
        tipo_order = pd.CategoricalDtype(categories=['Receita', 'Custo Total', 'Margem Bruta', 'Margem %'], ordered=True)
        pivot_df_melted['Tipo'] = pivot_df_melted['Tipo'].astype(tipo_order)

        # Mapeamento dos números dos meses para nomes no formato "Jan/24"
        meses_map = {
            1: 'Jan/24', 2: 'Fev/24', 3: 'Mar/24', 4: 'Abr/24', 5: 'Mai/24', 6: 'Jun/24',
            7: 'Jul/24', 8: 'Ago/24', 9: 'Set/24', 10: 'Out/24', 11: 'Nov/24', 12: 'Dez/24'
        }
        pivot_df_melted['Periodo'] = pivot_df_melted['Mes'].map(meses_map)

        # Lista para armazenar DataFrames de cada projeto
        project_dfs = []

        # Iterar sobre cada projeto
        for project in pivot_df_melted['CodigoProjeto'].unique():
            project_df = pivot_df_melted[pivot_df_melted['CodigoProjeto'] == project]

            # Pivot table final para exibir meses como colunas
            final_df = project_df.pivot_table(index=['CodigoProjeto', 'Tipo'], 
                                            columns='Periodo', 
                                            values='Valor', 
                                            aggfunc='sum')

            # Ordenar as colunas de acordo com os meses do ano no formato "Jan/24"
            meses_order = ['Jan/24', 'Fev/24', 'Mar/24', 'Abr/24', 'Mai/24', 'Jun/24',
                        'Jul/24', 'Ago/24', 'Set/24', 'Out/24', 'Nov/24', 'Dez/24']
            final_df = final_df.reindex(columns=meses_order)

            # Adicionar coluna de Total
            final_df['Total'] = final_df.sum(axis=1)

            # Renomear as colunas para os meses
            final_df.columns.name = None  # Remover o nome das colunas multi-index
            final_df.reset_index(inplace=True)

            # Adicionar coluna Editável: True para 'Receita' e 'Custo Total', False para os outros
            final_df['Editável'] = final_df['Tipo'].isin(['Receita', 'Custo Total'])

            # Ordenar as linhas
            final_df = final_df.sort_values(by=['CodigoProjeto', 'Tipo'])

            # Adicionar o DataFrame do projeto à lista
            project_dfs.append(final_df)

            # Adicionar separador visual
            separator = pd.DataFrame({'CodigoProjeto': [""], 'Tipo': [""], **{col: [""] for col in final_df.columns[2:]}})
            project_dfs.append(separator)

        # Concatenar todos os DataFrames de projetos
        final_df_all = pd.concat(project_dfs, ignore_index=True)

        return final_df_all