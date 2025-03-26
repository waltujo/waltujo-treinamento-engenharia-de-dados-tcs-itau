import pandas as pd

def carregar_dados(arquivo: str) -> pd.DataFrame:
    """Crie uma função que leia o arquivo vendas.csv e retorne um DataFrame"""
    return pd.read_csv(arquivo)

def calcular_valor_total(datafremae: pd.DataFrame) -> pd.DataFrame:
    """Crie uma função que adicione uma nova coluna valor_total ao DataFrame, calculada como quantidade * preco_unitario"""
    datafremae['valor_total'] = datafremae['quantidade'] * datafremae['preco_unitario']
    return datafremae

def filtrar_vendas(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Crie uma função que filtre os registros onde o valor_total seja superior a R$500"""
    return dataframe[dataframe['valor_total'] > 500]

def salvar_resultado(dataframe: pd.DataFrame, arquivo_saida: str) -> None:
    """Crie uma função que salve o DataFrame filtrado em um novo arquivo CSV"""
    dataframe.to_csv(arquivo_saida, index=False)
    
if __name__ == "__main__":
    df = carregar_dados('../dados/vendas.csv')
    df = calcular_valor_total(df)
    df_filtrado = filtrar_vendas(df)
    salvar_resultado(df_filtrado, '../dados/resultado.csv')
    print(df_filtrado)