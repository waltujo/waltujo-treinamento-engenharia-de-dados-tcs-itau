# O que é um DataFrame?
Um DataFrame é como uma "super tabela" que ajuda a organizar e manipular dados de forma eficiente em Python. Ele é uma das estruturas de dados fundamentais na análise e engenharia de dados, tornando as tarefas mais intuitivas e produtivas.

- Cada linha representa um registro.
- Cada coluna representa um atributo.

Essa estrutura facilita a manipulação de dados: ao filtrar, agrupar, ordenar ou transformar um DataFrame, você está manipulando os dados de todas as linhas ao mesmo tempo. É muito mais rápido, fácil e eficiente do que fazer isso manualmente utilizando algum tipo de laço ou algoritmo complexo.

Por exemplo, imagine que você precisa agrupar os dados de uma tabela por região e calcular a média de vendas em cada uma. Usando Python puro, você teria que percorrer cada linha, verificar a região e calcular a média manualmente. Com um DataFrame, você pode fazer isso em poucas linhas de código, de forma muito mais simples e legível.

Exemplo no Python puro:
```python
# Dados fictícios
dados = [
    {"regiao": "Norte", "vendas": 100},
    {"regiao": "Sul", "vendas": 200},
    {"regiao": "Norte", "vendas": 150},
    {"regiao": "Sul", "vendas": 250},
]

# Dicionário para armazenar as médias
medias = {}

# Cálculo das médias
for linha in dados:
    regiao = linha["regiao"]
    vendas = linha["vendas"]
    
    if regiao not in medias:
        medias[regiao] = {"total": 0, "qtd": 0}
    
    medias[regiao]["total"] += vendas
    medias[regiao]["qtd"] += 1

for regiao, valores in medias.items():
    media = valores["total"] / valores["qtd"]
    print(f"Média de vendas na região {regiao}: {media}")
```

Exemplo com Pandas:
```python
import pandas as pd

# Dados fictícios
dados = {
    "regiao": ["Norte", "Sul", "Norte", "Sul"],
    "vendas": [100, 200, 150, 250]
}

# Criação do DataFrame
df = pd.DataFrame(dados)

# Cálculo das médias
medias = df.groupby("regiao")["vendas"].mean()
print(medias)
```
---

# Overview de operações com DataFrames

### 1. Criação de DataFrame

```python
import pandas as pd

# Criando um DataFrame a partir de um dicionário em memória
dados = {
    'id': [1, 2, 3],
    'nome': ['João', 'Maria', 'Carlos'],
    'cidade': ['São Paulo', 'Curitiba', 'Belo Horizonte']
}

df = pd.DataFrame(dados)
print("DataFrame criado:")
print(df)
```

---

### 2. Leitura de Arquivos

#### a) Leitura de CSV

Supondo que você tenha um arquivo chamado `exemplo.csv` com o conteúdo:
```
id,nome,cidade
1,João,São Paulo
2,Maria,Curitiba
3,Carlos,Belo Horizonte
```

```python
# Lendo o arquivo CSV para um DataFrame
df_csv = pd.read_csv('exemplo.csv')
print("DataFrame lido de CSV:")
print(df_csv)
```

#### b) Leitura de JSON

Supondo que você tenha um arquivo chamado `exemplo.json` com o seguinte conteúdo:
```json
{
  "usuarios": [
    {"id": 1, "nome": "João", "cidade": "São Paulo"},
    {"id": 2, "nome": "Maria", "cidade": "Curitiba"}
  ]
}
```

```python
# Lendo o arquivo JSON para um DataFrame
df_json = pd.read_json('exemplo.json')
# Se o JSON estiver aninhado, pode ser necessário converter:
df_json = pd.json_normalize(df_json['usuarios'])
print("DataFrame lido de JSON:")
print(df_json)
```

---

### 3. Manipulação de Colunas e Cálculos

#### a) Criação/Adição de Coluna

```python
# DataFrame com dados de vendas
dados_vendas = {
    'produto': ['Produto A', 'Produto B'],
    'quantidade': [10, 5],
    'preco_unitario': [50.0, 150.0]
}
df_vendas = pd.DataFrame(dados_vendas)

# Adicionando a coluna 'valor_total'
df_vendas['valor_total'] = df_vendas['quantidade'] * df_vendas['preco_unitario']
print("DataFrame com coluna 'valor_total':")
print(df_vendas)
```

---

### 4. Filtragem de Dados

```python
# Filtrar vendas com valor_total acima de 500
df_filtrado = df_vendas[df_vendas['valor_total'] > 500]
print("Vendas com valor_total > 500:")
print(df_filtrado)
```

---

### 5. Ordenação

```python
# Ordenar o DataFrame por 'valor_total' de forma crescente
df_ordenado = df_vendas.sort_values(by='valor_total')
print("DataFrame ordenado por 'valor_total':")
print(df_ordenado)
```

---

### 6. Agregações e Agrupamentos

```python
# Dados para agregação
dados_agregacao = {
    'categoria': ['A', 'B', 'A', 'B', 'A'],
    'valor': [100, 200, 150, 250, 200]
}
df_agregacao = pd.DataFrame(dados_agregacao)

# Agrupar por 'categoria' e calcular soma e média
agrupado = df_agregacao.groupby('categoria')['valor'].agg(soma_valor='sum', media_valor='mean').reset_index()
print("Dados agregados por categoria:")
print(agrupado)
```

---

### 7. Exportação de Dados

#### a) Salvar em CSV

```python
# Salvando o DataFrame filtrado em um arquivo CSV
df_filtrado.to_csv('vendas_filtradas.csv', index=False)
print("Arquivo 'vendas_filtradas.csv' salvo.")
```

#### b) Salvar em Parquet

> **Observação:** Para salvar em Parquet, é necessário ter instalado o pacote `pyarrow` ou `fastparquet`.

```python
# Salvando o DataFrame agregado em um arquivo Parquet
agrupado.to_parquet('dados_agregados.parquet', index=False)
print("Arquivo 'dados_agregados.parquet' salvo.")
```

---

### 8. Conversão para Outros Formatos

#### a) Converter para Lista de Dicionários

```python
# Converter o DataFrame para uma lista de dicionários
lista_registros = df.to_dict(orient='records')
print("DataFrame convertido para lista de dicionários:")
print(lista_registros)
```
