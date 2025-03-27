import pytest
import os
from atividade4 import *

CSV_FILE_PATH = r"C:\dados-tcs-itau\Etapa 3\dados\dados_agregacao.csv"
PARQUET_FILE_PATH = r"C:\dados-tcs-itau\Etapa 3\dados\dados_agregados.parquet"

def test_carregar_dados_csv():
    df = carregar_dados_csv(CSV_FILE_PATH)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "O DataFrame carregado está vazio"
    assert set(df.columns) == {"id", "categoria", "valor"}, "As colunas do DataFrame não correspondem aos esperados"
    
def test_realizar_agregacao():
    df = carregar_dados_csv(CSV_FILE_PATH)
    df_agregado = realizar_agregacao(df)
    
    dados_esperados = {
        "categoria": ["A", "B", "C"],
        "soma_valor": [450, 450, 300],
        "media_valor": [150.0, 225.0, 300.0]
    }
    
    df_esperado = pd.DataFrame(dados_esperados)
    
    assert isinstance(df_agregado, pd.DataFrame)
    assert not df_agregado.empty, "O DataFrame agregado está vazio"
    pd.testing.assert_frame_equal(df_agregado, df_esperado, check_dtype=False)
    
def test_salvar_dados_parquet():
    df = carregar_dados_csv(CSV_FILE_PATH)
    df_agregado = realizar_agregacao(df)
    
    salvar_dados_parquet(df_agregado, PARQUET_FILE_PATH)
    
    assert os.path.exists(PARQUET_FILE_PATH), "O arquivo Parquet não foi criado"

def test_carregar_dados():
    df = carregar_dados_csv(CSV_FILE_PATH)
    df_agregado = realizar_agregacao(df)
    
    df_carregado = carregar_dados_parquet(PARQUET_FILE_PATH)
    
    pd.testing.assert_frame_equal(df_agregado, df_carregado, check_dtype=False)
    

    

    