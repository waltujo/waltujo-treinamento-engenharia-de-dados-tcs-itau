import pandas as pd

def carregar_dados(arquivo: str) -> pd.DataFrame:
    """Carrega os dados de um arquivo CSV em um DataFrame."""
    return pd.read_csv(arquivo)

def calcula_media_notas(df: pd.DataFrame) -> pd.DataFrame:
    """Crie uma função que calcule a média das notas para cada aluno"""
    df["media"] = df.iloc[:, 1:].mean(axis=1)
    return df

def identificar_aprovados(df: pd.DataFrame, nota_corte: float = 7.0) -> pd.DataFrame:
    """Crie uma função que identifique os alunos com média maior ou igual a 7"""
    df["aprovado"] = df["media"] >= nota_corte
    return df

def gerar_relatoio(df: pd.DataFrame) -> pd.DataFrame:
    """ Crie uma função que retorne um relatório com o nome do aluno, a média calculada e o status (Aprovado quando a nota for maior que 6, senão Reprovado)"""
    df["status"] = df["media"].apply(lambda x: "Aprovado" if x >= 6 else "Reprovado")
    return df[["aluno", "media", "status"]]

if __name__ == "__main__":
    df = carregar_dados('../dados/alunos.csv')
    df = calcula_media_notas(df)
    df = identificar_aprovados(df)
    relatorio = gerar_relatoio(df)
    print(relatorio)