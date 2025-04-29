from pyspark.sql import SparkSession
import pyspark.sql.functions as F

def main():
    spark = SparkSession.builder \
        .appName("MySQL to DataFrame") \
        .enableHiveSupport() \
        .config("hive.exec.dynamic.partition.mode", "nonstrict") \
        .config("hive.exec.dynamic.partition", "true") \
        .getOrCreate()

    contas_df = spark.table("walter_araujo_database_sor.contas")
    categorias_df = spark.table("walter_araujo_database_sor.categorias")
    transacoes_df = spark.table("walter_araujo_database_sor.transacoes")
    interest_rate_df = spark.table("walter_araujo_database_sor.interest_rate")

    df_final = (
    transacoes_df
    .join(contas_df, transacoes_df.conta_id == contas_df.id, "left")
    .join(categorias_df, transacoes_df.categoria_id == categorias_df.id, "left")
    .crossJoin(interest_rate_df)
    .select(
        F.expr("uuid()").alias("identificador_unico"),
        transacoes_df["id"].alias("transacao_id"),
        transacoes_df["conta_id"],
        transacoes_df["categoria_id"],
        F.to_timestamp(transacoes_df["data"], "yyyy-MM-dd").alias("transacao_data"),
        F.year(F.to_date(transacoes_df["data"], "yyyy-MM-dd")).alias("transacao_ano"),
        F.month(F.to_date(transacoes_df["data"], "yyyy-MM-dd")).alias("transacao_mes"),
        F.dayofmonth(F.to_date(transacoes_df["data"], "yyyy-MM-dd")).alias("transacao_dia"),
        transacoes_df["descricao"].alias("transacao_descricao"),
        transacoes_df["valor"].alias("transacao_valor"),
        transacoes_df["data_criacao"].alias("transacao_data_criacao"),
        contas_df["nome"].alias("conta_nome"),
        contas_df["descricao"].alias("conta_descricao"),
        categorias_df["nome"].alias("categoria_nome"),
        categorias_df["tipo"].alias("categoria_tipo"),
        interest_rate_df["data_referencia"].alias("taxa_juros_referencia"),
        interest_rate_df["porcentagem"].alias("taxa_juros_porcentagem"),
        F.current_date().cast("string").alias("data_ingestao")
    )
)

    df_final.write.insertInto("walter_araujo_database_sot.sot_financeira", overwrite=True)

if __name__ == "__main__":
    from traceback import format_exc
    try:
        main()
    except:
        print(format_exc())
        exit(1)