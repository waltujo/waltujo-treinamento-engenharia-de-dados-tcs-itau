import pytest
from atividade2 import *

def test_carregar_dados():
    """Carregar dados do arquivo CSV"""
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\alunos.csv')
    
    assert not df.empty

def test_calcula_media_notas():
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\alunos.csv')
    df = calcula_media_notas(df)
    
    assert "media" in df.columns, "A coluna 'media' deveria existir no DataFrame"
    
def test_identificar_aprovados():
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\alunos.csv')
    df = calcula_media_notas(df)
    df = identificar_aprovados(df)
    
    assert "aprovado" in df.columns, "A coluna 'aprovado' deveria existir no DataFrame"
    
    
def test_gerar_relatoio():
    df = carregar_dados(r'C:\dados-tcs-itau\Etapa 3\dados\alunos.csv')
    df = calcula_media_notas(df)
    df = identificar_aprovados(df)
    relatorio = gerar_relatoio(df)
    
    assert "status" in relatorio.columns, "A coluna 'status' deveria existir no DataFrame"
    
    