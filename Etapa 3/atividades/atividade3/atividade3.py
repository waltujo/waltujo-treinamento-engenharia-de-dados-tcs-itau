import json
import pandas as pd

def carregar_usuarios_json(file_path: str) -> pd.DataFrame:
    """Crie uma função que leia o arquivo usuarios.json e converta os dados para um DataFrame"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data["usuarios"])

def filtrar_idade(df: pd.DataFrame) -> pd.DataFrame:
    """Crie uma função que filtre os usuários com idade maior que 18 anos"""
    return df[df["idade"] > 18]

def ordernar_usuarios(df: pd.DataFrame) -> pd.DataFrame:
    """Crie uma função que ordene os usuários por idade"""
    return df.sort_values(by='idade')

def gerar_relatorio(df: pd.DataFrame) -> pd.DataFrame:
    """Crie uma função que retorne um relatório final em formato de lista de dicionários com os dados processados"""
    return df.to_dict(orient='records')

if __name__ == "__main__":
    df = carregar_usuarios_json(r'C:\dados-tcs-itau\Etapa 3\dados\usuarios.json')
    df = filtrar_idade(df)
    df = ordernar_usuarios(df)
    relatorio = gerar_relatorio(df)
    print(relatorio)