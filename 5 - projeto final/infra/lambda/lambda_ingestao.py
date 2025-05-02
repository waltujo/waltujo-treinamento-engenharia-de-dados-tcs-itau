import awswrangler as wr
import pandas as pd
from datetime import datetime
import logging

# Configura o logger para a Lambda
logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_FILE_PATH = "s3://recepcao-taxa-de-juros/interest_rate.csv"
S3_PARQUET_PATH = "s3://walter-araujo-bucket-exemplo/interest_rate/"
DATABASE_NAME = "walter_araujo_database_sor"
TABLE_NAME = "interest_rate"

def lambda_handler(event, context):
    try:
        # Log de início
        logger.info("Iniciando a leitura do arquivo CSV do S3.")
        
        # Lê o arquivo CSV do S3
        df = wr.s3.read_csv(path=S3_FILE_PATH, dtype=str)
        logger.info(f"{len(df)} registros lidos do arquivo CSV.")
        
        # Adiciona a coluna de ingestão
        df["data_ingestao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("Coluna 'data_ingestao' adicionada.")
        
        # Salva os dados como Parquet no S3
        logger.info("Iniciando a gravação dos dados em formato Parquet.")
        wr.s3.to_parquet(
            df=df,
            path=S3_PARQUET_PATH,
            dataset=True,
            mode="overwrite",
            database=DATABASE_NAME,
            table=TABLE_NAME,
            dtype={col: "string" for col in df.columns}
        )
        logger.info("Dados gravados com sucesso em formato Parquet.")
        
        # Resposta de sucesso
        return {
            'statusCode': 200,
            'body': 'Processamento concluído com sucesso.'
        }
    
    except Exception as e:
        logger.error(f"Erro durante o processamento: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': f"Erro: {str(e)}"
        }
