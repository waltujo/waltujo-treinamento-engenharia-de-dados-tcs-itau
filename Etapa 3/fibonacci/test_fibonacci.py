import pytest
from fibonacci import Fibonacci  # Importa a classe do outro arquivo

def test_casos_basicos():
    assert Fibonacci.calculate(0) == 0
    assert Fibonacci.calculate(1) == 1
    assert Fibonacci.calculate(2) == 1
    assert Fibonacci.calculate(3) == 2
    assert Fibonacci.calculate(4) == 3
    assert Fibonacci.calculate(5) == 5
    assert Fibonacci.calculate(10) == 55

def test_entrada_invalida():
    with pytest.raises(ValueError):
        Fibonacci.calculate(-1)
        
    with pytest.raises(ValueError):
        Fibonacci.calculate(3.5)
        
    with pytest.raises(ValueError):
        Fibonacci.calculate("texto")
        
    with pytest.raises(ValueError):
        Fibonacci.calculate(None)

# Para rodar os testes, use o comando:
# pytest test_fibonacci.py -v
