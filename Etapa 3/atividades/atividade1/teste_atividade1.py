import pytest
import pandas as pd
from atividade1 import *

def test_carregar_dados():
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\vendas.csv')
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ['produto', 'quantidade', 'preco_unitario']
    

def test_calcular_valor_total():
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\vendas.csv')
    df = calcular_valor_total(df)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'valor_total' in df.columns
    assert all(df['valor_total'] == df['quantidade'] * df['preco_unitario'])
    
def test_filtrar_vendas():
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\vendas.csv')
    df = calcular_valor_total(df)
    df_filtrado = filtrar_vendas(df)
    
    assert isinstance(df_filtrado, pd.DataFrame)
    assert not df_filtrado.empty
    assert all(df_filtrado['valor_total'] > 500)
     
def test_salvar_resultado(tmp_path):
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\vendas.csv')
    df = calcular_valor_total(df)
    df_filtrado = filtrar_vendas(df)
    
    arquivo_saida = tmp_path / "resultado.csv"
    
    salvar_resultado(df_filtrado, arquivo_saida)
    
    df_lido = pd.read_csv(arquivo_saida)
    
    assert isinstance(df_lido, pd.DataFrame)
    assert arquivo_saida.exists()
    assert list(df_lido.columns) == ['produto', 'quantidade', 'preco_unitario', 'valor_total']
    assert all(df_lido['valor_total'] > 500)
     