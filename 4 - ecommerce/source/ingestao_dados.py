from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window
import pandas as pd

DB_FILEPATH = r'C:\dados-tcs-itau\4 - ecommerce\data\ecommerce.db'

# Cria uma sessão do PySpark
spark: SparkSession = (
    SparkSession
    .builder
    .enableHiveSupport() # type: ignore
    .config('spark.jars.packages', 'org.xerial:sqlite-jdbc:3.34.0') # type: ignore
    .master('local[*]')
    .getOrCreate()
)

#Função auxiliar para ler tabelas do SQLite
def ler_tabela(nome: str) -> pd.DataFrame:
    return (
        spark.read
    .format('jdbc')
    .option('url', f'jdbc:sqlite:{DB_FILEPATH}')
    .option('driver', 'org.sqlite.JDBC')
    .option('dbtable', nome) # Lê a tabela inteira
    #.option('query', 'SELECT * FROM user') # Retorna o resultado da consulta SQL
    .load()
    )

#Lê as tabelas do banco
usuarios = ler_tabela("user")
pedidos = ler_tabela("'order'")
itens = ler_tabela("order_item")
produtos = ler_tabela("product")

#Filtra pedidos com status válidos e traduz status
pedidos_filtrados = pedidos.filter(
    F.col("status").isin("approved", "shipped", "delivered")
).withColumn(
    "status_traduzido",
    F.when(F.col("status") == "approved", "APROVADO")
    .when(F.col("status") == "shipped", "ENVIADO")
    .when(F.col("status") == "delivered", "ENTREGUE")
)

pedidos_filtrados.show()

#Unir tabelas e selecionar colunas necessárias
df_final = pedidos_filtrados.join(usuarios, pedidos_filtrados.user_id == usuarios.id, "left") \
    .join(itens, pedidos_filtrados.id == itens.order_id, "left") \
    .join(produtos, itens.product_id == produtos.id, "left") \
    .select(
        usuarios["name"].alias("nome_usuario"),
        usuarios["email"].alias("email_usuario"),
        pedidos_filtrados["id"].alias("id_pedido"),
        pedidos_filtrados["order_date"].alias("data_pedido"),
        produtos["name"].alias("nome_produto"),
        itens["quantity"].alias("quantidade_comprada"),
        itens["unit_price"].alias("preco_unitario"),
        produtos["category"].alias("categoria_produto"),
        pedidos_filtrados["total_value"].alias("total_gasto")
    )
    
df_final.show()

#Criar ranking com base no total gasto por usuário
window_spec = Window.partitionBy("nome_usuario").orderBy(F.col("total_gasto").desc())
df_final = df_final.withColumn("ranking_usuario", F.rank().over(window_spec))

#Exibir os primeiros registros
df_final.show()

df_final.write.mode("overwrite").parquet("C:/dados-tcs-itau/4 - ecommerce/data/resultados/ranking_usuarios.parquet")

spark.stop()