-- Listar os nomes e cidades de todos os clientes em uma só consulta

SELECT nome, cidade FROM Clientes 

-- Listar os pedidos com valor acima de R$100

SELECT * FROM Pedidos WHERE valor > 100

-- Listar os pedidos ordenados pelo valor (decrescente)
SELECT * FROM Pedidos ORDER BY valor;

-- Listar os 3 primeiros produtos cadastrados
SELECT * FROM Produtos ORDER BY id_produto LIMIT 3

-- Listar o total de valor gasto por cada cliente em pedidos.
SELECT 
	c.id_cliente,
	c.nome, 
	SUM(p.valor)
FROM
	Clientes c
	INNER JOIN Pedidos p 
		ON c.id_cliente = p.id_cliente
GROUP BY 
	c.id_cliente,
	c.nome
;
	
-- Encontrar o cliente com o maior valor gasto

SELECT 
	c.id_cliente,
	c.nome,
	SUM(p.valor) valor_gasto
FROM 
	Clientes c 
	INNER JOIN Pedidos p 
		ON c.id_cliente = p.id_cliente
GROUP BY 
	c.id_cliente,
	c.nome
ORDER BY valor_gasto DESC
LIMIT 1;


-- Utilizar CTE para calcular o total de vendas por produto
WITH VendasPorProduto AS (
	SELECT 
		ip.id_produto,
		SUM(ip.quantidade) total_vendido
	FROM ItensPedido ip
	GROUP BY ip.id_produto
)
SELECT 
	p.id_produto, 
	p.nome_produto, 
	vp.total_vendido, 
	(vp.total_vendido * p.preco) valor_total_vendas
FROM 
	Produtos p 
	INNER JOIN VendasPorProduto vp 
		ON p.id_produto = vp.id_produto


-- Listar todos os produtos comprados por cada cliente
SELECT 
	c.id_cliente, 
	c.nome,
	p.id_produto,
	p.nome_produto
FROM 
	Clientes c 
	INNER JOIN Pedidos pd 
		ON c.id_cliente = pd.id_cliente
	INNER JOIN ItensPedido ip 
		ON pd.id_pedido = ip.id_pedido
	INNER JOIN Produtos p
		ON p.id_produto = ip.id_produto

-- Ranquear clientes pelo valor total gasto começando pelo rank 1 para o maior valor.
SELECT 
	c.id_cliente,
	c.nome,
	SUM(p.valor) total_gasto,
	RANK() OVER (ORDER BY SUM(p.valor) DESC) ranking
FROM 
	Clientes c 
	INNER JOIN Pedidos p 
		ON c.id_cliente = p.id_cliente
GROUP BY 
	c.id_cliente, c.nome
	
	
-- Número de pedidos por cliente, considerando apenas aqueles com mais de 1 pedido
SELECT 
	c.id_cliente,
	c.nome,
	COUNT(p.id_pedido) quantidade_pedidos
FROM 
	Clientes c 
	INNER JOIN Pedidos p 
		ON c.id_cliente = p.id_cliente
GROUP BY 
	c.id_cliente,
	c.nome
HAVING 
	COUNT(p.id_pedido) > 1


-- Calcular para cada cliente a quantidade de dias entre um pedido e o pedido imediatamente anterior
WITH t AS (
	SELECT 
		c.id_cliente,
		c.nome,
		p.id_pedido,
		p.data_pedido,
		LAG(p.data_pedido) OVER (PARTITION BY c.id_cliente ORDER BY p.data_pedido) as data_pedido_anterior
	FROM 
		Clientes c 
		INNER JOIN Pedidos p 
			ON c.id_cliente = p.id_cliente
)
SELECT 
	*,
	(JULIANDAY(data_pedido) - JULIANDAY(data_pedido_anterior)) dias_entre_pedidos
FROM t


-- Crie uma consulta que retorne um relatórios contedo as seguintes colunas (obs: use o padrão que preferir para nomear as colunas):

WITH ValorSemDesconto AS (
	SELECT 
		ip.id_pedido,
		SUM(p.preco * ip.quantidade) preco_sem_desconto
	FROM 
		ItensPedido ip 
		INNER JOIN Produtos p 
			ON ip.id_produto = p.id_produto
	GROUP BY 
		ip.id_pedido
)
SELECT 
	c.id_cliente 			ID_CLIENTE,
	c.nome 					NOME_CLIENTE,
	c.cidade				CIDADE_CLIENTE,
	p.id_pedido				ID_PEDIDO,
	p.data_pedido			DATA_PEDIDO,
	p.valor					VALOR_PEDIDO,
	vsd.preco_sem_desconto 	VALOR_PEDIDO_SEM_DESCONTO,
	(vsd.preco_sem_desconto - p.valor) DESCONTO,
	JULIANDAY(p.data_pedido) - JULIANDAY(
		LAG(p.data_pedido) 
		OVER (PARTITION BY c.id_cliente ORDER BY p.data_pedido )
	) DIAS_DESDE_PEDIDO_ANTERIOR
FROM 
	Clientes c 
	INNER JOIN Pedidos p 
		ON c.id_cliente = p.id_cliente
	LEFT JOIN ValorSemDesconto vsd 
		ON p.id_pedido = vsd.id_pedido
	