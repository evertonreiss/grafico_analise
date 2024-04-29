import pandas as pd
import plotly.graph_objs as go

def exibir_grafico(arquivo, campo_interesse, ano_inicio=None, ano_fim=None):
    try:
        # Verifica a extensão do arquivo para determinar o tipo
        if arquivo.endswith('.parquet'):
            # Carrega o arquivo Parquet
            df = pd.read_parquet(arquivo)
        elif arquivo.endswith('.csv'):
            # Carrega o arquivo CSV diretamente com o pandas
            df = pd.read_csv(arquivo, index_col=0, parse_dates=True)
        else:
            print("Tipo de arquivo não suportado.")
            return

        # Ordena os dados pela coluna de data
        df.sort_index(inplace=True)

        # Define os anos de início e fim se não forem fornecidos
        ano_inicio = ano_inicio if ano_inicio else df.index.min().year
        ano_fim = ano_fim if ano_fim else df.index.max().year

        # Filtra o DataFrame para incluir apenas os anos dentro do intervalo especificado
        filtro = (df.index.year >= ano_inicio) & (df.index.year <= ano_fim)
        df_filtrado = df[filtro]

        # Agrupa os dados por ano
        grupo_por_ano = df_filtrado.groupby(df_filtrado.index.year)

        # Cria uma lista de linhas para cada ano
        linhas = []
        for ano, dados_ano in grupo_por_ano:
            linha = go.Scatter(x=dados_ano.index.strftime('%b'),
                               y=dados_ano[campo_interesse],
                               mode='lines',
                               name=str(ano))
            linhas.append(linha)

        # Define o layout do gráfico
        layout = go.Layout(title=f'Campo selecionado: {campo_interesse}',
                           xaxis=dict(title='Mês'),
                           yaxis=dict(title='Valor'),
                           hovermode='closest') #'x', 'y', 'closest', False, 'x unified', 'y unified'

        # Cria a figura do gráfico
        fig = go.Figure(data=linhas, layout=layout)

        # Exibe o gráfico
        fig.show()

    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except KeyError:
        print(f"Campo '{campo_interesse}' não encontrado no DataFrame.")

exibir_grafico('base.parquet', 'EA_SECO')
