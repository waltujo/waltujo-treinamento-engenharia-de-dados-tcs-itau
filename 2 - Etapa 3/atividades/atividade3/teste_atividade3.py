import pytest
from atividade3 import *

def test_carregar_usuarios_json():
    df = carregar_usuarios_json(r'C:\dados-tcs-itau\Etapa 3\dados\usuarios.json')
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ['id', 'nome', 'idade']
    
def test_filtrar_idade():
    df = carregar_usuarios_json(r'C:\dados-tcs-itau\Etapa 3\dados\usuarios.json')
    df_filtrado = filtrar_idade(df)
    
    assert isinstance(df_filtrado, pd.DataFrame)
    assert not df_filtrado.empty
    assert all(df_filtrado['idade'] > 18)
    
def test_ordenar_usuarios():
    df = carregar_usuarios_json(r'C:\dados-tcs-itau\Etapa 3\dados\usuarios.json')
    
    df_ordenado = ordernar_usuarios(df)
    
    assert isinstance(df_ordenado, pd.DataFrame)
    assert not df_ordenado.empty
    assert df_ordenado['idade'].is_monotonic_increasing
    
def test_gerar_relatorio():
    df = carregar_usuarios_json(r'C:\dados-tcs-itau\Etapa 3\dados\usuarios.json')
    
    relatorio = gerar_relatorio(df)
    
    assert isinstance(relatorio, list)
    assert all(isinstance(item, dict) for item in relatorio)
    assert all('id' in item and 'nome' in item and 'idade' in item for item in relatorio)
    