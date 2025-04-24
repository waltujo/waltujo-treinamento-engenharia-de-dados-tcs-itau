import pandas as pd

def carregar_dados_csv(file_path: str) -> pd.DataFrame:
    """Crie uma função que leia o arquivo dados_agregacao.csv e retorne um DataFrame."""
    return pd.read_csv(file_path)

def realizar_agregacao(df: pd.DataFrame) -> pd.DataFrame:
    """agrupar por categoria, calcular soma dos valores para cada grupo e calcular a média dos valores para cada grupo."""
    df_agregado = df.groupby("categoria").agg(
        soma_valor=("valor", "sum"),
        media_valor=("valor", "mean")
    ).reset_index()
    return df_agregado

def salvar_dados_parquet(df: pd.DataFrame, file_path: str):
    """Salvar dados do DataFrame em Parquet"""
    df.to_parquet(file_path, index=False)
    
def carregar_dados_parquet(file_path: str) -> pd.DataFrame:
    """Carregar dados Parquet e retornar DataFrame"""
    return pd.read_parquet(file_path)

if __name__ == "__main__":
    df = carregar_dados_csv(r"C:\dados-tcs-itau\Etapa 3\dados\dados_agregacao.csv")
    print(df)
    df_agregado = realizar_agregacao(df)
    print(df_agregado)
    salvar_dados_parquet(df_agregado, r"C:\dados-tcs-itau\Etapa 3\dados\dados_agregados.parquet")
    df_parquet = carregar_dados_parquet(r"C:\dados-tcs-itau\Etapa 3\dados\dados_agregados.parquet")
    print(df_parquet)
    

                         