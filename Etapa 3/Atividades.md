### **Atividade 0: Testes Unitários para a Função Fibonacci**

#### **Descrição:**
Desenvolva uma função que retorne o N-ésimo número da sequência de Fibonacci. Em seguida, crie testes unitários para garantir que a função esteja correta.

#### **Objetivos:**
- Praticar a criação de testes unitários.
- Escrever código modularizado e com boa cobertura de testes.

#### **Instruções:**
1. Implemente a função que calcula o N-ésimo número da sequência de Fibonacci.
2. Crie testes unitários que verifiquem:
   - Casos básicos (por exemplo, N = 0, 1, 2).
   - Comportamento em casos de entrada inválida, se aplicável.

---

### **Atividade 1: Processamento de Dados de Vendas com Pandas**

#### **Descrição:**
Utilize DataFrames para processar um conjunto de dados de vendas. O código deve ser organizado em funções bem definidas, e cada função precisa ser validada por meio de testes unitários.

#### **Objetivos:**
- Modularizar o código em funções reutilizáveis.
- Manipular dados utilizando DataFrames do Pandas.
- Garantir a qualidade do código por meio de testes unitários.

#### **Dados Utilizados (Conteúdo do arquivo CSV):**

Salve o conteúdo abaixo em um arquivo chamado `vendas.csv`:

```
produto,quantidade,preco_unitario
Produto A,10,50.0
Produto B,5,150.0
Produto C,8,80.0
Produto D,12,30.0
```

#### **Tarefas:**
1. **Carregar Dados:** Crie uma função que leia o arquivo `vendas.csv` e retorne um DataFrame.
2. **Calcular Valor Total:** Crie uma função que adicione uma nova coluna `valor_total` ao DataFrame, calculada como `quantidade * preco_unitario`.
3. **Filtrar Vendas:** Crie uma função que filtre os registros onde o `valor_total` seja superior a R$500.
4. **Salvar Resultado:** Crie uma função que salve o DataFrame filtrado em um novo arquivo CSV.

#### **Testes Unitários:**
- Verifique se a função de carregamento retorna um Dataframe com as colunas esperadas.
- Teste se a coluna `valor_total` é calculada corretamente.
- Confirme que a filtragem retorne apenas os registros com valor total acima de R$500.
- Valide se o arquivo CSV resultante é gerado corretamente.

---

### **Atividade 2: Processamento de Dados de Notas com Pandas**

#### **Descrição:**
Utilize DataFrames do Pandas para calcular a média de notas de alunos. Organize o código em funções bem definidas e crie testes unitários para cada uma delas.

#### **Objetivos:**
- Modularizar o código.
- Realizar cálculos utilizando DataFrames.
- Garantir a qualidade do código com testes unitários.

#### **Dados Utilizados (Conteúdo do arquivo CSV):**

Salve o conteúdo abaixo em um arquivo chamado `alunos.csv`:

```
aluno,nota1,nota2,nota3
Ana,8.0,7.0,9.0
Bruno,6.0,5.5,6.5
Carlos,7.5,8.0,7.0
Daniela,9.0,9.5,8.5
```

#### **Tarefas:**
1. **Calcular Média:** Crie uma função que calcule a média das notas para cada aluno.
2. **Identificar Aprovados:** Crie uma função que identifique os alunos com média maior ou igual a 7.
3. **Gerar Relatório:** Crie uma função que retorne um relatório com o nome do aluno, a média calculada e o status (`Aprovado` quando a nota for maior que 6, senão `Reprovado`).

#### **Testes Unitários:**
- Teste o cálculo correto da média para os alunos.
- Verifique se os alunos aprovados são identificados corretamente.
- Valide a estrutura e o conteúdo do relatório gerado.

---

### **Atividade 3: Integração Simulada com API e Processamento com Pandas**

#### **Descrição:**
Simule a integração com uma API utilizando dados fornecidos em um arquivo (ou diretamente como conteúdo hard coded) para obter informações de usuários. Converta os dados para um DataFrame do Pandas, processe as informações e gere um relatório. O código deve ser organizado em funções modulares e conter testes unitários.

#### **Objetivos:**
- Praticar a integração e manipulação de dados de uma fonte externa simulada.
- Organizar o código em funções.
- Validar a funcionalidade com testes unitários.

#### **Dados Utilizados (Conteúdo do arquivo JSON):**

Utilize o conteúdo abaixo para simular a resposta da API, salvando-o em um arquivo chamado `usuarios.json`:

```json
{
  "usuarios": [
    {"id": 1, "nome": "Alice", "idade": 22},
    {"id": 2, "nome": "Bruno", "idade": 17},
    {"id": 3, "nome": "Carla", "idade": 25},
    {"id": 4, "nome": "Daniel", "idade": 16}
  ]
}
```

#### **Tarefas:**
1. **Converter para DataFrame:** Crie uma função que leia o arquivo `usuarios.json` e converta os dados para um DataFrame.
2. **Filtrar Usuários:** Crie uma função que filtre os usuários com idade maior que 18 anos.
3. **Ordenar Usuários:** Crie uma função que ordene os usuários por idade.
4. **Gerar Relatório:** Crie uma função que retorne um relatório final em formato de lista de dicionários com os dados processados.

#### **Testes Unitários:**
- Verifique se a conversão para DataFrame está correta.
- Teste se o filtro seleciona apenas os usuários com idade acima de 18 anos.
- Confirme a ordenação correta dos usuários.
- Valide a geração do relatório final.

---

### **Atividade 4: Agregação de Dados e Carga em Arquivos Parquet**

#### **Descrição:**
Nesta atividade, vocês irão trabalhar com agregações de dados e, em seguida, salvar o resultado das agregações em um arquivo no formato Parquet. Assim como nas outras atividades, o código deverá ser organizado em funções modulares e cada função deve ser acompanhada de testes unitários.

#### **Objetivos:**
- Praticar a realização de agregações (como soma e média) em DataFrames.
- Aprender a salvar e carregar arquivos Parquet utilizando o Pandas.
- Garantir a integridade do código por meio de testes unitários.

#### **Dados Utilizados (Conteúdo do arquivo CSV):**

Salve o conteúdo abaixo em um arquivo chamado `dados_agregacao.csv`:

```
id,categoria,valor
1,A,100
2,B,200
3,A,150
4,B,250
5,A,200
6,C,300
```

#### **Tarefas:**

1. **Carregar Dados:**
   - Crie uma função que leia o arquivo `dados_agregacao.csv` e retorne um DataFrame.

2. **Realizar Agregações:**
   - Crie uma função que, a partir do DataFrame carregado, realize as seguintes agregações:
     - Agrupar os dados pela coluna `categoria`.
     - Calcular a soma dos valores (`valor`) para cada grupo.
     - Calcular a média dos valores para cada grupo.
   - O resultado deve ser um DataFrame com as colunas: `categoria`, `soma_valor` e `media_valor`.

3. **Salvar Dados em Parquet:**
   - Crie uma função que salve o DataFrame resultante das agregações em um arquivo Parquet chamado `dados_agregados.parquet`.

4. **Carregar e Validar:**
   - Crie uma função que leia o arquivo Parquet `dados_agregados.parquet` e retorne o DataFrame para validação.

#### **Testes Unitários:**
- Verifique se a função de carregamento do CSV retorna o DataFrame correto.
- Teste se a função de agregação retorna os valores corretos para cada categoria.
- Confirme que o arquivo Parquet é gerado e pode ser lido corretamente, mantendo a integridade dos dados agregados.
