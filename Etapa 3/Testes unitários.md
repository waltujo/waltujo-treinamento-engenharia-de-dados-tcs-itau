### **O que são Testes Unitários?**

**Testes unitários** são uma técnica de teste de software que verifica se unidades individuais de código (como funções, métodos ou classes) funcionam corretamente. Cada unidade é testada isoladamente para garantir que produz o resultado esperado, dado um conjunto específico de entradas.

---

### **Por que usar Testes Unitários?**

1. **Confiabilidade:** Certificam que o código funciona como esperado.
2. **Manutenção:** Ajudam a identificar problemas rapidamente ao modificar o código.
3. **Documentação:** Servem como uma forma prática de documentar como o código deve se comportar.
4. **Agilidade:** Facilitam a identificação e correção de bugs.

---

### **Características dos Testes Unitários**

- **Isolamento:** Cada teste verifica apenas uma unidade de código.
- **Reprodutibilidade:** Os testes devem ser executados repetidamente, produzindo os mesmos resultados.
- **Automação:** Usualmente, os testes são automatizados com ferramentas como `pytest`.

---

### **O que é pytest?**

**pytest** é uma biblioteca poderosa para criar e executar testes unitários em Python. Ele é fácil de usar, mas também oferece recursos avançados, como:

1. **Detecção automática de testes:** Não é necessário configurar manualmente os testes, desde que sigam a convenção de nomenclatura (`test_nome_do_teste`).
2. **Assert simplificado:** Usa o próprio `assert` do Python para verificar condições, em vez de métodos específicos.
3. **Suporte para fixtures:** Permite configurar dados ou estados antes de executar os testes.
4. **Plugins:** Possui uma grande quantidade de extensões para diversas necessidades.

---

### **Criando Testes Unitários com pytest**

#### **1. Configuração Básica**

Certifique-se de instalar o pytest:
```bash
pip install pytest
```

#### **2. Estrutura de um Teste Unitário**

Vamos criar uma função e um teste para ela:

**Código-fonte:**  
```python
# arquivo: calculadora.py
def soma(a, b):
    return a + b
```

**Teste Unitário:**  
Crie um arquivo chamado `test_calculadora.py`:
```python
# arquivo: test_calculadora.py
from calculadora import soma

def test_soma():
    assert soma(2, 3) == 5  # Testa a soma de 2 e 3
    assert soma(-1, 1) == 0  # Testa a soma de -1 e 1
    assert soma(0, 0) == 0   # Testa a soma de 0 e 0
```

#### **3. Executando os Testes**

Execute o pytest no terminal:
```bash
pytest
```

**Saída esperada:**
```
================ test session starts =================
collected 1 item

test_calculadora.py .                              [100%]

================ 1 passed in 0.01s ==================
```

---

### **Recursos Avançados do pytest**

#### **1. Uso de Fixtures**
Fixtures são usadas para configurar dados ou estados antes de executar os testes.

**Exemplo:**
```python
import pytest

@pytest.fixture
def numeros():
    return 2, 3

def test_soma_com_fixture(numeros):
    a, b = numeros
    assert a + b == 5
```

#### **2. Testes Parametrizados**
Permite executar o mesmo teste com múltiplos conjuntos de entradas.

**Exemplo:**
```python
import pytest

@pytest.mark.parametrize("a, b, esperado", [
    (2, 3, 5),    # Teste 1
    (-1, 1, 0),   # Teste 2
    (0, 0, 0)     # Teste 3
])
def test_soma_parametrizado(a, b, esperado):
    assert a + b == esperado
```

#### **3. Testando Erros**
Verifica se a função levanta uma exceção quando algo dá errado.

**Exemplo:**
```python
import pytest

def dividir(a, b):
    if b == 0:
        raise ValueError("Divisão por zero não é permitida")
    return a / b

def test_divisao_por_zero():
    with pytest.raises(ValueError, match="Divisão por zero não é permitida"):
        dividir(10, 0)
```

---

### **Estratégias para Escrever Bons Testes Unitários**

1. **Nomeclatura Clara:** Use nomes de testes que descrevam o comportamento esperado.
2. **Casos Limite:** Inclua testes para cenários incomuns (ex.: valores nulos ou negativos).
3. **Isolamento Completo:** Certifique-se de que os testes não dependem uns dos outros.
4. **Feedback Rápido:** Escreva testes pequenos e fáceis de executar.
5. **Cobertura de Código:** Garanta que todas as partes do código são testadas.

---

### **Resumo**

- **Testes Unitários:** Verificam partes individuais do código para garantir que funcionam como esperado.
- **pytest:** Uma ferramenta prática, eficiente e extensível para automação de testes em Python.
- **Benefícios:** Melhor qualidade do código, maior confiabilidade e menor risco de regressões.