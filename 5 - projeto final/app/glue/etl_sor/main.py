from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F

DB_CONFIG = {
    "host": "mysql-financial-db.c3imkkke2ssh.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "F(VD]Qe8r!BOCg72",
    "database": "financial_db"
}

def create_spark_session() -> SparkSession:
    return (
        SparkSession
        .builder
        .appName("MySQL to DataFrame")  # type: ignore
        .config("hive.exec.dynamic.partition.mode", "nonstrict")
        .config("hive.exec.dynamic.partition", "true")
        .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.32")
        .master("local[*]")
        .getOrCreate()
    )

def read_mysql_table(spark: SparkSession, table_name: str, db_config: dict) -> DataFrame:
    return (
        spark
        .read
        .format("jdbc")
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("url", f"jdbc:mysql://{db_config['host']}/{db_config['database']}?useSSL=false")
        .option("ssl", "false")
        .option("user", db_config["user"])
        .option("password", db_config["password"])
        .option("dbtable", table_name)
        .load()
    )

def processar_tabela(spark: SparkSession, tabela: str):
    df = read_mysql_table(spark, tabela, DB_CONFIG)
    df = df.withColumn("data_ingestao", F.current_timestamp())
    
    df.write.insertInto(f"walter_araujo_database_sor.{tabela}", overwrite=True)

def main():
    spark = create_spark_session()

    tabelas = ["contas", "categorias", "transacoes"]

    for tabela in tabelas:
        processar_tabela(spark, tabela)

if __name__ == "__main__":
    from traceback import format_exc
    try:
        main()
    except:
        print(format_exc())
        exit(1)
