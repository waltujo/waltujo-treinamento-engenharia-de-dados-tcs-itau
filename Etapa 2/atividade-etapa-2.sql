-- Lista os nomes e cidades de todos os clientes da tabela Clientes.
SELECT nome, cidade FROM Clientes;

-- Lista todos os pedidos cujo valor é maior que R$100.
SELECT * FROM Pedidos WHERE valor > 100;

-- Lista todos os pedidos ordenados pelo valor em ordem decrescente (do maior para o menor).
SELECT * FROM Pedidos ORDER BY valor DESC;

-- Lista os três primeiros produtos cadastrados na tabela Produtos.
SELECT * FROM Produtos LIMIT 3;

-- Lista o total de valor gasto por cada cliente em pedidos.
-- Faz um JOIN entre Clientes e Pedidos, agrupando os resultados por cliente e somando os valores dos pedidos.
SELECT Clientes.nome, SUM(Pedidos.valor) AS total_gasto
FROM Clientes
JOIN Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
GROUP BY Clientes.id_cliente;

-- Encontra o cliente que mais gastou, ordenando os clientes pelo total gasto em ordem decrescente e limitando o resultado a um único cliente.
SELECT Clientes.nome, SUM(Pedidos.valor) AS total_gasto
FROM Clientes
JOIN Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
GROUP BY Clientes.id_cliente
ORDER BY total_gasto DESC
LIMIT 1;

-- Calcula o total de vendas por produto usando uma CTE (Common Table Expression).
WITH total_vendas_produto AS (
    SELECT 
        Produtos.nome_produto,
        SUM(ItensPedido.quantidade * Produtos.preco) AS total_vendido
    FROM ItensPedido
    JOIN Produtos ON ItensPedido.id_produto = Produtos.id_produto
    GROUP BY Produtos.nome_produto
)
-- Recupera os resultados da CTE.
SELECT * FROM total_vendas_produto;

-- Lista todos os produtos comprados por cada cliente.
-- Faz JOIN entre Clientes, Pedidos, ItensPedido e Produtos, ordenando o resultado pelo nome do cliente.
SELECT 
    Clientes.nome AS cliente, 
    Produtos.nome_produto, 
    ItensPedido.quantidade
FROM Clientes
JOIN Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
JOIN ItensPedido ON Pedidos.id_pedido = ItensPedido.id_pedido
JOIN Produtos ON ItensPedido.id_produto = Produtos.id_produto
ORDER BY cliente;

-- Ranquear clientes pelo valor total gasto, com a melhor posição para o maior valor.
-- Usa uma CTE para calcular o total gasto por cliente e depois gera um ranking usando ROW_NUMBER().
WITH rank_clientes AS (
    SELECT 
        Clientes.nome, 
        SUM(Pedidos.valor) AS total_gasto
    FROM Clientes
    JOIN Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
    GROUP BY Clientes.id_cliente
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY total_gasto DESC) AS rank,
    nome, 
    total_gasto
FROM rank_clientes;            

-- Número de pedidos por cliente, considerando apenas aqueles que fizeram mais de um pedido.
-- Usa GROUP BY para contar os pedidos por cliente e HAVING para filtrar aqueles com mais de 1 pedido.
SELECT 
    Clientes.nome AS nome_cliente, 
    COUNT(Pedidos.id_pedido) AS quantidade_pedidos
FROM Clientes
JOIN Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
GROUP BY Clientes.id_cliente
HAVING quantidade_pedidos > 1;

-- Calcula a quantidade de dias entre pedidos consecutivos de cada cliente.
-- Usa LAG() para obter a data do pedido anterior e JULIANDAY() para calcular a diferença em dias.
SELECT 
    Clientes.nome AS nome_cliente,
    Pedidos.id_pedido,
    Pedidos.data_pedido,
    COALESCE(
        JULIANDAY(Pedidos.data_pedido) - JULIANDAY(
            LAG(Pedidos.data_pedido) OVER (PARTITION BY Clientes.id_cliente ORDER BY Pedidos.data_pedido)
        ),
        0
    ) AS dias_desde_ultimo_pedido
FROM Clientes
JOIN Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
ORDER BY nome_cliente, Pedidos.data_pedido;

-- Relatório completo contendo diversas informações sobre os pedidos dos clientes.
-- Inclui a diferença de dias entre pedidos e o cálculo do valor dos pedidos sem desconto.
WITH PedidoDetalhado AS (
    SELECT 
        Pedidos.id_pedido,
        Pedidos.id_cliente,
        Pedidos.data_pedido,
        Pedidos.valor AS valor_com_desconto,
        SUM(Produtos.preco * ItensPedido.quantidade) AS preco_sem_desconto
    FROM Pedidos
    JOIN ItensPedido ON Pedidos.id_pedido = ItensPedido.id_pedido
    JOIN Produtos ON ItensPedido.id_produto = Produtos.id_produto
    GROUP BY Pedidos.id_pedido
),
RelatorioCompleto AS (
    SELECT 
        Clientes.id_cliente,
        Clientes.nome AS nome_cliente,
        Clientes.cidade AS cidade_cliente,
        PedidoDetalhado.id_pedido,
        PedidoDetalhado.data_pedido,
        PedidoDetalhado.valor_com_desconto,
        PedidoDetalhado.preco_sem_desconto,
        COALESCE(
            JULIANDAY(PedidoDetalhado.data_pedido) - JULIANDAY(
                LAG(PedidoDetalhado.data_pedido) OVER (PARTITION BY Clientes.id_cliente ORDER BY PedidoDetalhado.data_pedido)
            ), 
            0
        ) AS dias_desde_ultimo_pedido
    FROM Clientes
    JOIN PedidoDetalhado ON Clientes.id_cliente = PedidoDetalhado.id_cliente
)
-- Retorna o relatório completo ordenado por nome do cliente e data do pedido.
SELECT * FROM RelatorioCompleto
ORDER BY nome_cliente, data_pedido;
